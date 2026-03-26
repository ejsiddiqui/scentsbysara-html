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

# Add parent dir so imports work when run as script
sys.path.insert(0, str(Path(__file__).parent))

from serve_html import MockupServer
from extract_styles import (
    all_property_names,
    create_browser_context,
    extract_section_styles,
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
        time.sleep(interval)

    print(f"\n  [X] Could not reach {url} after {max_retries} attempts. Exiting.")
    sys.exit(1)


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
                print(f"      - {el['name']}: mockup={el.get('mockup', '?')} → theme={el.get('theme', '?')}")
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
    """Audit a single page. Returns path to saved report, or None if no issues."""
    page_name = page_config["name"]
    mockup_file = page_config["mockup"]
    theme_path = page_config["theme"]
    sections = page_config.get("sections", [])

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

    for section in sections:
        if section_filter and section["name"].lower() != section_filter.lower():
            continue

        sec_name = section["name"]
        elements = section.get("elements", [])
        print(f"    Section: {sec_name} ({len(elements)} elements)")

        for vp_width in viewports:
            print(f"      Viewport: {vp_width}px ... ", end="", flush=True)

            # --- Mockup ---
            mockup_ctx = create_browser_context(browser, vp_width)
            mockup_page = mockup_ctx.new_page()
            mockup_url = f"{mockup_base_url}/{mockup_file}"
            navigate_to_page(mockup_page, mockup_url)

            mockup_elements = [{"name": e["name"], "mockup": e["mockup"]} for e in elements]
            mockup_results = extract_section_styles(
                mockup_page, section["mockupSelector"], mockup_elements, properties
            )

            # Screenshot (mockup)
            slug = sec_name.lower().replace(" ", "-")
            take_section_screenshot(
                mockup_page,
                section["mockupSelector"],
                os.path.join(screenshot_dir, f"{page_name.lower()}-{slug}-{vp_width}-mockup.png"),
            )
            mockup_ctx.close()

            # --- Theme ---
            theme_ctx = create_browser_context(browser, vp_width)
            theme_page = theme_ctx.new_page()
            theme_url = f"{theme_base_url}{theme_path}"
            navigate_to_page(theme_page, theme_url, password=store_password)

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
            theme_ctx.close()

            # --- Diff ---
            diffs = diff_sections(mockup_results, theme_results, tolerance, vp_width)
            # Tag each diff with section name for report grouping
            for d in diffs:
                d.section_name = sec_name
            all_diffs.extend(diffs)

            critical = sum(1 for d in diffs if d.severity == "Critical")
            notable = sum(1 for d in diffs if d.severity == "Notable")
            marginal = sum(1 for d in diffs if d.severity == "Marginal")
            unknown = sum(1 for d in diffs if d.severity == "Unknown")
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
    html_port = int(defaults.get("htmlBaseUrl", "http://127.0.0.1:8080").split(":")[-1])
    mockup_server = MockupServer(html_base_dir, html_port)

    try:
        mockup_server.start()
    except RuntimeError as e:
        print(f"  ✗ {e}")
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
