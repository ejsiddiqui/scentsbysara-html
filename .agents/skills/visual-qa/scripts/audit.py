"""Visual QA audit tool — compares HTML mockups against live Shopify theme."""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# Add parent dir so imports work when run as script
sys.path.insert(0, str(Path(__file__).parent))

from serve_html import MockupServer
from extract_styles import (
    all_property_names,
    create_browser_context,
    extract_section_styles,
    extract_image_info,   # ADD THIS
    extract_svg_info,     # ADD THIS
    navigate_to_page,
    take_section_screenshot,
)
from diff_styles import diff_sections, StyleDiff
from report import generate_report, save_report

from playwright.sync_api import sync_playwright


def load_config(config_path: str) -> dict:
    """Load and validate page-mappings.json."""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_server_reachable(url: str) -> bool:
    """Check if a URL is reachable."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        urllib.request.urlopen(req, timeout=5)
        return True
    except urllib.error.HTTPError as exc:
        # Shopify preview/dev stores can return 401 before the password page is
        # handled in the browser flow. That still means the server is live.
        return exc.code in {200, 301, 302, 401, 403}
    except (urllib.error.URLError, OSError):
        return False


def wait_for_theme_server(url: str, max_retries: int = 3, interval: int = 5):
    """Check if theme server is reachable, prompt user if not."""
    for attempt in range(max_retries):
        if check_server_reachable(url):
            return True
        if attempt == 0:
            print(f"\n  [!] Cannot reach Shopify dev server at {url}")
            print(f"  Please start it with: cd theme && shopify theme dev --store=scentsbysara-dev.myshopify.com")
            print(f"  Waiting... (attempt {attempt + 1}/{max_retries})")
        else:
            print(f"  Retrying... (attempt {attempt + 1}/{max_retries})")
        if attempt < max_retries - 1:
            time.sleep(interval)

    print(f"\n  [X] Could not reach {url} after {max_retries} attempts. Exiting.")
    sys.exit(1)


def seed_cart(theme_ctx, theme_base_url: str, cart_seed: dict | None) -> bool:
    """Populate the preview cart when a page needs a filled-cart state."""
    if not cart_seed:
        return True

    request = theme_ctx.request
    variant_id = cart_seed["variantId"]
    quantity = cart_seed.get("quantity", 1)

    def is_rate_limited(response) -> bool:
        try:
            body = response.text()
        except Exception:
            body = ""
        return response.status == 429 or "too_many_requests" in body

    def fetch_cart_state():
        response = request.get(
            f"{theme_base_url}/cart.js",
            headers={"Accept": "application/json"},
        )
        if not response.ok:
            return None

        try:
            return response.json()
        except Exception:
            try:
                return json.loads(response.text())
            except Exception:
                return None

    def cart_matches_seed(cart_state: dict | None) -> bool:
        if not cart_state:
            return False

        for item in cart_state.get("items", []):
            if item.get("variant_id") == variant_id and item.get("quantity") == quantity:
                return True

        return False

    current_cart = fetch_cart_state()
    if cart_matches_seed(current_cart):
        return True

    clear_response = None
    add_response = None

    for attempt in range(3):
        if current_cart and current_cart.get("item_count", 0) > 0:
            clear_response = request.post(
                f"{theme_base_url}/cart/clear.js",
                headers={"Accept": "application/json"},
            )
            if is_rate_limited(clear_response):
                time.sleep(5 * (attempt + 1))
                current_cart = fetch_cart_state()
                continue

        add_response = request.post(
            f"{theme_base_url}/cart/add.js",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            data=json.dumps(
                {
                    "items": [
                        {
                            "id": variant_id,
                            "quantity": quantity,
                        }
                    ]
                }
            ),
        )

        current_cart = fetch_cart_state()
        if cart_matches_seed(current_cart):
            return True

        if is_rate_limited(add_response):
            time.sleep(5 * (attempt + 1))
            continue

        break

    clear_status = clear_response.status if clear_response else "n/a"
    add_status = add_response.status if add_response else "n/a"
    item_count = current_cart.get("item_count", 0) if current_cart else "n/a"
    print(
        "        [!] Cart seed failed:",
        f"clear={clear_status} add={add_status} item_count={item_count}",
    )
    return False


def seed_mockup_cart(mockup_ctx, cart_seed: dict | None):
    """Populate the HTML mockup cart so comparisons use the same filled-cart state."""
    if not cart_seed:
        return

    mockup_item = cart_seed.get("mockupItem") or {
        "id": "she-is-beauty",
        "name": "She Is Beauty",
        "price": 22.59,
        "quantity": cart_seed.get("quantity", 1),
        "image": "assets/images/product-1.png",
        "color": "IVORY",
        "size": "SLIM",
        "scent": "VANILLA",
        "url": "product.html",
    }

    mockup_payload = json.dumps([mockup_item])
    mockup_ctx.add_init_script(
        f"""
        window.localStorage.setItem('scentsbysara-cart-v1', {json.dumps(mockup_payload)});
        window.localStorage.setItem('sbs_currency', 'GBP');
        """,
    )


def wait_for_mockup_cart_render(mockup_page, cart_seed: dict | None):
    """Wait until the seeded mockup cart has rendered its JS-driven state."""
    if not cart_seed:
        return

    try:
        mockup_page.wait_for_function(
            """
            () => {
                const rows = document.querySelectorAll('#cart-items-table tr');
                const subtotal = document.getElementById('cart-subtotal');
                return rows.length > 0
                  && subtotal
                  && subtotal.textContent
                  && !['£0.00', '$0.00', 'AED 0.00'].includes(subtotal.textContent.trim());
            }
            """,
            timeout=5000,
        )
    except Exception:
        # The mockup cart is JS-rendered; give it a short grace period before
        # falling back to whatever state is available.
        mockup_page.wait_for_timeout(1200)


def wait_for_theme_cart_render(theme_page, cart_seed: dict | None):
    """Wait until the Shopify cart renders a filled state after seeding."""
    if not cart_seed:
        return

    try:
        theme_page.wait_for_function(
            """
            () => {
                if (document.body.innerText.includes('Too many attempts')) {
                    return false;
                }

                const subtotal = document.querySelector('.cart-total-subtotal');
                const hasNonZeroSubtotal = subtotal
                  && subtotal.textContent
                  && !['£0.00', '$0.00', 'AED 0.00'].includes(subtotal.textContent.trim());

                return Boolean(document.querySelector('.cart-table-wrap, .cart-mobile-list')) || hasNonZeroSubtotal;
            }
            """,
            timeout=5000,
        )
    except Exception:
        theme_page.wait_for_timeout(1200)


def theme_cart_is_seeded(theme_page, cart_seed: dict | None) -> bool:
    """Return True when the Shopify page reflects a seeded filled-cart state."""
    if not cart_seed:
        return True

    return bool(
        theme_page.evaluate(
            """
            () => {
                if (document.body.innerText.includes('Too many attempts')) {
                    return false;
                }

                if (document.querySelector('.cart-table-wrap, .cart-mobile-list')) {
                    return true;
                }

                const subtotal = document.querySelector('.cart-total-subtotal');
                return Boolean(
                    subtotal
                    && subtotal.textContent
                    && !['£0.00', '$0.00', 'AED 0.00'].includes(subtotal.textContent.trim())
                );
            }
            """
        )
    )


def navigate_mockup_page(mockup_page, mockup_url: str, cart_seed: dict | None):
    """Open a mockup page and wait for any seeded client-side cart state to render."""
    navigate_to_page(mockup_page, mockup_url)
    wait_for_mockup_cart_render(mockup_page, cart_seed)


def section_matches_viewport(section: dict, viewport_width: int) -> bool:
    """Return True when a section should be audited for the current viewport."""
    min_viewport = section.get("minViewport")
    max_viewport = section.get("maxViewport")
    if min_viewport is not None and viewport_width < min_viewport:
        return False
    if max_viewport is not None and viewport_width > max_viewport:
        return False
    return True


def run_dry_run(config: dict, page_filter: str | None, section_filter: str | None):
    """Validate config and list what would be audited."""
    defaults = config.get("defaults", {})
    pages = config.get("pages", [])

    print("\n  DRY RUN - Config validation")
    print(f"  Theme URL: {defaults.get('themeBaseUrl', 'not set')}")
    print(f"  HTML URL: {defaults.get('htmlBaseUrl', 'not set')}")
    print(f"  Tolerance: {defaults.get('tolerance', 2)}px")
    print(f"  Core viewports: {defaults.get('viewports', {}).get('core', [])}")
    print(f"  Full viewports: {defaults.get('viewports', {}).get('full', [])}")
    print()

    for page in pages:
        if page_filter and page["name"].lower() != page_filter.lower():
            continue
        print(f"  Page: {page['name']}")
        print(f"    Mockup: {page['mockup']}")
        print(f"    Theme: {page['theme']}")
        for sec in page.get("sections", []):
            if section_filter and sec["name"].lower() != section_filter.lower():
                continue
            el_count = len(sec.get("elements", []))
            print(f"    Section: {sec['name']} ({el_count} elements)")
            for el in sec.get("elements", []):
                print(f"      - {el['name']}: mockup={el.get('mockup', '?')} -> theme={el.get('theme', '?')}")
        print()

    print("  [OK] Config is valid. No browser launched.")


def audit_page(
    page_config: dict,
    defaults: dict,
    browser,
    mockup_base_url: str,
    viewports: list[int],
    tolerance: int,
    section_filter: str | None,
    image_diff: bool,
    svg_compare: bool,
    output_dir: str,
    store_password: str | None = None,
) -> str | None:
    """Audit a single page. Returns path to saved report."""
    page_name = page_config["name"]
    mockup_file = page_config["mockup"]
    theme_path = page_config["theme"]
    sections = page_config.get("sections", [])
    cart_seed = page_config.get("cartSeed")
    skip_theme_cart_seed = page_config.get("skipThemeCartSeed", False)

    if not sections:
        print(f"  [!] No sections configured for {page_name} — skipping")
        return None

    theme_base_url = defaults.get("themeBaseUrl", "http://127.0.0.1:9292")
    properties = all_property_names()

    all_diffs: list[StyleDiff] = []
    screenshot_dir = os.path.join(output_dir, "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    flags = []
    if image_diff:
        flags.append("--image-diff")
    if svg_compare:
        flags.append("--svg-compare")

    print(f"\n  Auditing: {page_name}")

    seeded_theme_storage = None
    if cart_seed and not skip_theme_cart_seed:
        with create_browser_context(browser, viewports[0]) as seed_theme_ctx:
            seed_page = seed_theme_ctx.new_page()
            theme_url = f"{theme_base_url}{theme_path}"
            navigate_to_page(seed_page, theme_url, password=store_password)

            if not seed_cart(seed_theme_ctx, theme_base_url, cart_seed):
                print(
                    f"  [!] Skipping {page_name}: unable to seed Shopify cart without rate limiting."
                )
                return None

            navigate_to_page(seed_page, theme_url, password=store_password)
            wait_for_theme_cart_render(seed_page, cart_seed)

            if not theme_cart_is_seeded(seed_page, cart_seed):
                print(
                    f"  [!] Skipping {page_name}: Shopify cart remained empty after seeding."
                )
                return None

            seeded_theme_storage = seed_theme_ctx.storage_state()

    for section in sections:
        if section_filter and section["name"].lower() != section_filter.lower():
            continue

        sec_name = section["name"]
        elements = section.get("elements", [])
        print(f"    Section: {sec_name} ({len(elements)} elements)")

        for vp_width in viewports:
            if not section_matches_viewport(section, vp_width):
                continue

            print(f"      Viewport: {vp_width}px ... ", end="", flush=True)

            slug = sec_name.lower().replace(" ", "-")

            # --- Mockup ---
            with create_browser_context(browser, vp_width) as mockup_ctx:
                seed_mockup_cart(mockup_ctx, cart_seed)
                mockup_page = mockup_ctx.new_page()
                mockup_url = f"{mockup_base_url}/{mockup_file}"
                navigate_mockup_page(mockup_page, mockup_url, cart_seed)

                mockup_elements = [{"name": e["name"], "mockup": e["mockup"]} for e in elements]
                mockup_results = extract_section_styles(
                    mockup_page, section["mockupSelector"], mockup_elements, properties
                )

                # Screenshot (mockup)
                take_section_screenshot(
                    mockup_page,
                    section["mockupSelector"],
                    os.path.join(screenshot_dir, f"{page_name.lower()}-{slug}-{vp_width}-mockup.png"),
                )

            # --- Theme ---
            with create_browser_context(
                browser, vp_width, storage_state=seeded_theme_storage
            ) as theme_ctx:
                theme_page = theme_ctx.new_page()
                theme_url = f"{theme_base_url}{theme_path}"
                navigate_to_page(theme_page, theme_url, password=store_password)
                if cart_seed and not skip_theme_cart_seed:
                    wait_for_theme_cart_render(theme_page, cart_seed)

                theme_elements = [{"name": e["name"], "theme": e["theme"]} for e in elements]
                theme_results = extract_section_styles(
                    theme_page, section["themeSelector"], theme_elements, properties
                )

                # Screenshot (theme)
                take_section_screenshot(
                    theme_page,
                    section["themeSelector"],
                    os.path.join(screenshot_dir, f"{page_name.lower()}-{slug}-{vp_width}-theme.png"),
                )

            # --- Diff ---
            diffs = diff_sections(mockup_results, theme_results, tolerance, vp_width)
            # Tag each diff with section name for report grouping
            for d in diffs:
                d.section_name = sec_name
            all_diffs.extend(diffs)

            # --- Image diff (optional) ---
            if image_diff:
                for el in elements:
                    mockup_sel = el.get("mockup", "")
                    theme_sel = el.get("theme", "")
                    if not mockup_sel or not theme_sel:
                        print(f"      [!] Skipping image diff for '{el.get('name', '?')}' — missing selector mapping")
                        continue

                    with create_browser_context(browser, vp_width) as mockup_ctx2:
                        seed_mockup_cart(mockup_ctx2, cart_seed)
                        mp = mockup_ctx2.new_page()
                        navigate_mockup_page(mp, f"{mockup_base_url}/{mockup_file}", cart_seed)
                        mockup_img = extract_image_info(mp, mockup_sel)

                    with create_browser_context(
                        browser, vp_width, storage_state=seeded_theme_storage
                    ) as theme_ctx2:
                        tp = theme_ctx2.new_page()
                        navigate_to_page(tp, f"{theme_base_url}{theme_path}", password=store_password)
                        if cart_seed and not skip_theme_cart_seed:
                            wait_for_theme_cart_render(tp, cart_seed)
                        theme_img = extract_image_info(tp, theme_sel)

                    if mockup_img and theme_img:
                        # Compare aspect ratios
                        if mockup_img.get("aspectRatio") and theme_img.get("aspectRatio"):
                            ar_diff = abs(mockup_img["aspectRatio"] - theme_img["aspectRatio"])
                            if ar_diff > 0.05:
                                all_diffs.append(StyleDiff(
                                    element_name=el["name"],
                                    element_selector=el.get("theme", ""),
                                    property="aspect-ratio",
                                    category="Images",
                                    expected=f"{mockup_img['aspectRatio']:.3f}",
                                    actual=f"{theme_img['aspectRatio']:.3f}",
                                    severity="Critical" if ar_diff > 0.1 else "Notable",
                                    viewport=vp_width,
                                    section_name=sec_name,
                                ))

                        # Compare rendered dimensions
                        for dim in ["renderedWidth", "renderedHeight"]:
                            if mockup_img.get(dim) is not None and theme_img.get(dim) is not None:
                                dim_diff = abs(mockup_img[dim] - theme_img[dim])
                                if dim_diff > tolerance:
                                    severity = "Critical" if dim_diff > tolerance * 2 else "Notable"
                                    all_diffs.append(StyleDiff(
                                        element_name=el["name"],
                                        element_selector=el.get("theme", ""),
                                        property=dim,
                                        category="Images",
                                        expected=f"{mockup_img[dim]:.0f}px",
                                        actual=f"{theme_img[dim]:.0f}px",
                                        severity=severity,
                                        viewport=vp_width,
                                        section_name=sec_name,
                                    ))

            # --- SVG compare (optional) ---
            if svg_compare:
                for el in elements:
                    mockup_sel = el.get("mockup", "")
                    theme_sel = el.get("theme", "")
                    if not mockup_sel or not theme_sel:
                        print(f"      [!] Skipping SVG compare for '{el.get('name', '?')}' — missing selector mapping")
                        continue

                    with create_browser_context(browser, vp_width) as mockup_ctx3:
                        seed_mockup_cart(mockup_ctx3, cart_seed)
                        mp = mockup_ctx3.new_page()
                        navigate_mockup_page(mp, f"{mockup_base_url}/{mockup_file}", cart_seed)
                        mockup_svg = extract_svg_info(mp, mockup_sel)

                    with create_browser_context(
                        browser, vp_width, storage_state=seeded_theme_storage
                    ) as theme_ctx3:
                        tp = theme_ctx3.new_page()
                        navigate_to_page(tp, f"{theme_base_url}{theme_path}", password=store_password)
                        if cart_seed and not skip_theme_cart_seed:
                            wait_for_theme_cart_render(tp, cart_seed)
                        theme_svg = extract_svg_info(tp, theme_sel)

                    if mockup_svg and theme_svg:
                        if mockup_svg.get("pathData") != theme_svg.get("pathData"):
                            all_diffs.append(StyleDiff(
                                element_name=el["name"],
                                element_selector=el.get("theme", ""),
                                property="svg-paths",
                                category="Icons & SVGs",
                                expected=f"{len(mockup_svg.get('pathData', []))} paths",
                                actual=f"{len(theme_svg.get('pathData', []))} paths (content differs)",
                                severity="Notable",
                                viewport=vp_width,
                                section_name=sec_name,
                            ))

            # Summary for this viewport (includes style + image + SVG diffs)
            vp_diffs = [d for d in all_diffs if d.viewport == vp_width and d.section_name == sec_name]
            critical = sum(1 for d in vp_diffs if d.severity == "Critical")
            notable = sum(1 for d in vp_diffs if d.severity == "Notable")
            marginal = sum(1 for d in vp_diffs if d.severity == "Marginal")
            unknown = sum(1 for d in vp_diffs if d.severity == "Unknown")
            print(f"C:{critical} N:{notable} M:{marginal} U:{unknown}")

    # Generate and save report
    report_content = generate_report(
        page_name, sections, all_diffs, viewports, tolerance, flags, screenshot_dir
    )
    report_path = save_report(report_content, page_name, output_dir)
    print(f"\n  Report saved: {report_path}")
    return report_path


def main():
    parser = argparse.ArgumentParser(
        description="Visual QA: compare HTML mockups against live Shopify theme"
    )
    parser.add_argument("--page", default=None, help="Audit specific page (name from config)")
    parser.add_argument("--section", default=None, help="Audit specific section (requires --page)")
    parser.add_argument("--url", default=None, help="Override Shopify dev server URL")
    parser.add_argument("--viewports", choices=["core", "full"], default="core", help="Viewport set")
    parser.add_argument("--tolerance", type=int, default=None, help="Pixel tolerance (default: from config or 2)")
    parser.add_argument("--image-diff", action="store_true", help="Enable visual screenshot diff for images")
    parser.add_argument("--svg-compare", action="store_true", help="Enable SVG content comparison")
    parser.add_argument("--output", default=None, help="Report output directory")
    parser.add_argument("--dry-run", action="store_true", help="Validate config, list sections, no browser")
    parser.add_argument("--password", default=None, help="Shopify store password for dev store")

    args = parser.parse_args()

    # Validate --section requires --page
    if args.section and not args.page:
        parser.error("--section requires --page")

    # Load config
    config_path = Path(__file__).parent.parent / "config" / "page-mappings.json"
    if not config_path.exists():
        print(f"  [X] Config not found: {config_path}")
        print(f"  Run scaffold_mappings.py to generate initial config.")
        sys.exit(1)

    config = load_config(str(config_path))

    if "pages" not in config:
        print("  [X] Config is missing required 'pages' key.")
        sys.exit(1)

    defaults = config.get("defaults", {})

    # Apply CLI overrides
    if args.url:
        defaults["themeBaseUrl"] = args.url
    tolerance = args.tolerance if args.tolerance is not None else defaults.get("tolerance", 2)
    output_dir = args.output or "docs/qa-reports"
    viewports = defaults.get("viewports", {}).get(args.viewports, [1920, 1440, 768, 480])
    store_password = args.password or defaults.get("storePassword") or None

    # Dry run
    if args.dry_run:
        run_dry_run(config, args.page, args.section)
        return

    # Check theme server
    theme_url = defaults.get("themeBaseUrl", "http://127.0.0.1:9292")
    wait_for_theme_server(theme_url)

    # Start mockup server
    html_base_dir = defaults.get("htmlBaseDir", "html")
    # Resolve html_base_dir relative to repo root (config is at .agents/skills/visual-qa/config/)
    repo_root = config_path.parents[4]
    resolved_html_dir = repo_root / html_base_dir
    if not resolved_html_dir.exists():
        print(f"  [X] HTML directory not found: {resolved_html_dir}")
        print(f"  Check htmlBaseDir in config/page-mappings.json")
        sys.exit(1)
    html_base_dir = str(resolved_html_dir)
    html_url_parsed = urlparse(defaults.get("htmlBaseUrl", "http://127.0.0.1:8080"))
    html_port = html_url_parsed.port or 8080
    mockup_server = MockupServer(html_base_dir, html_port)

    try:
        mockup_server.start()
    except RuntimeError as e:
        print(f"  [X] {e}")
        sys.exit(1)

    # Run audit
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            pages = config.get("pages", [])
            report_paths = []

            for page_config in pages:
                if args.page and page_config["name"].lower() != args.page.lower():
                    continue

                report_path = audit_page(
                    page_config=page_config,
                    defaults=defaults,
                    browser=browser,
                    mockup_base_url=mockup_server.base_url,
                    viewports=viewports,
                    tolerance=tolerance,
                    section_filter=args.section,
                    image_diff=args.image_diff,
                    svg_compare=args.svg_compare,
                    output_dir=output_dir,
                    store_password=store_password,
                )
                if report_path:
                    report_paths.append(report_path)

            browser.close()

            # Final summary
            print(f"\n  [OK] Audit complete. {len(report_paths)} report(s) generated.")
            for rp in report_paths:
                print(f"    - {rp}")

    finally:
        mockup_server.stop()


if __name__ == "__main__":
    main()
