"""Screenshot Match — CLI orchestrator.

Captures screenshots of the Figma PNG and live theme, then outputs their
paths so Claude Code can read both images and perform the visual comparison.
"""

import argparse
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from capture_theme import capture_theme_screenshot
from playwright.sync_api import sync_playwright


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_server(url: str) -> bool:
    try:
        urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=5)
        return True
    except (urllib.error.URLError, OSError):
        return False


def wait_for_server(url: str, retries: int = 3, interval: int = 5) -> None:
    for attempt in range(retries):
        if check_server(url):
            return
        if attempt == 0:
            print(f"\n  [!] Cannot reach theme server at {url}")
            print("  Start it with: cd theme && shopify theme dev --store=scentsbysara-dev.myshopify.com")
        else:
            print(f"  Retrying... ({attempt + 1}/{retries})")
        if attempt < retries - 1:
            time.sleep(interval)
    print(f"\n  [X] Could not reach {url} after {retries} attempts. Exiting.")
    sys.exit(1)


def ask_viewport(page_name: str) -> int:
    while True:
        raw = input(f"  [?] Viewport width for '{page_name}' (e.g. 1440): ").strip()
        if raw.isdigit() and int(raw) > 0:
            return int(raw)
        print("  Please enter a positive integer.")


def run_dry_run(config: dict, page_filter: str | None) -> None:
    defaults = config.get("defaults", {})
    pages = config.get("pages", [])
    print("\n  DRY RUN — Config validation")
    print(f"  Theme URL: {defaults.get('themeBaseUrl', 'not set')}")
    print(f"  Figma dir: {defaults.get('figmaDir', 'figma-exports')}")
    hints = defaults.get("hints", {})
    print(f"  Font families: {hints.get('fontFamilies', [])}")
    print(f"  Brand colors: {hints.get('brandColors', [])}")
    print()
    for page in pages:
        if page_filter and page["name"].lower() != page_filter.lower():
            continue
        print(f"  Page: {page['name']}")
        print(f"    Figma image: {page.get('figmaImage', 'NOT SET')}")
        print(f"    Theme URL: {page.get('themeUrl', 'NOT SET')}")
        print(f"    Viewport: {page.get('viewport', 'NOT SET — will ask interactively')}")
        print()
    print("  [OK] Config valid. No browser calls made.")


def capture_page(
    page_config: dict,
    defaults: dict,
    browser,
    repo_root: Path,
    output_dir: str,
    interactive: bool,
    store_password: str | None,
) -> dict | None:
    """
    Capture Figma PNG copy and live theme screenshot for one page.
    Returns a dict with paths and design hints, or None if skipped.
    """
    page_name = page_config["name"]
    figma_image = page_config.get("figmaImage", "")
    theme_url_path = page_config.get("themeUrl", "/")
    viewport = page_config.get("viewport")
    hints = defaults.get("hints", {})
    theme_base_url = defaults.get("themeBaseUrl", "http://127.0.0.1:9292")
    figma_dir = defaults.get("figmaDir", "figma-exports")

    print(f"\n  Capturing: {page_name}")

    if not viewport:
        if interactive:
            viewport = ask_viewport(page_name)
        else:
            print(f"  [!] No viewport set for '{page_name}' and --no-interactive is on. Skipping.")
            return None

    figma_path = repo_root / figma_dir / figma_image
    if not figma_path.exists():
        print(f"  [X] Figma image not found: {figma_path}")
        print(f"  Drop the PNG into {repo_root / figma_dir}/ and re-run.")
        return None

    screenshot_dir = os.path.join(output_dir, "screenshots")
    slug = page_name.lower().replace(" ", "-")
    theme_screenshot = os.path.join(screenshot_dir, f"screenshot-match-{slug}-{viewport}-theme.png")
    figma_screenshot_copy = os.path.join(screenshot_dir, f"screenshot-match-{slug}-{viewport}-figma.png")

    print(f"    Capturing theme @ {viewport}px ... ", end="", flush=True)
    theme_url = f"{theme_base_url}{theme_url_path}"
    capture_theme_screenshot(browser, theme_url, viewport, theme_screenshot, password=store_password)
    print("done")

    os.makedirs(screenshot_dir, exist_ok=True)
    shutil.copy2(str(figma_path), figma_screenshot_copy)

    return {
        "page_name": page_name,
        "theme_url": theme_url,
        "viewport": viewport,
        "figma_path": figma_screenshot_copy,
        "theme_path": theme_screenshot,
        "hints": hints,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Screenshot Match: capture Figma + theme screenshots for visual comparison by Claude"
    )
    parser.add_argument("--page", default=None, help="Capture specific page (name from config)")
    parser.add_argument("--url", default=None, help="Override Shopify dev server URL")
    parser.add_argument("--password", default=None, help="Shopify store password")
    parser.add_argument("--no-interactive", action="store_true", help="Skip interactive viewport prompts")
    parser.add_argument("--output", default="docs/qa-reports", help="Report output directory")
    parser.add_argument("--dry-run", action="store_true", help="Validate config, no browser calls")
    args = parser.parse_args()

    config_path = Path(__file__).parent.parent / "config" / "page-mappings.json"
    if not config_path.exists():
        print(f"  [X] Config not found: {config_path}")
        sys.exit(1)

    config = load_config(str(config_path))
    defaults = config.get("defaults", {})

    if args.url:
        defaults["themeBaseUrl"] = args.url

    store_password = args.password or defaults.get("storePassword") or None
    interactive = not args.no_interactive

    if args.dry_run:
        run_dry_run(config, args.page)
        return

    repo_root = config_path.parents[4]
    theme_url = defaults.get("themeBaseUrl", "http://127.0.0.1:9292")
    wait_for_server(theme_url)

    pages = config.get("pages", [])
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for page_config in pages:
                if args.page and page_config["name"].lower() != args.page.lower():
                    continue
                result = capture_page(
                    page_config=page_config,
                    defaults=defaults,
                    browser=browser,
                    repo_root=repo_root,
                    output_dir=args.output,
                    interactive=interactive,
                    store_password=store_password,
                )
                if result:
                    results.append(result)
        finally:
            browser.close()

    print(f"\n  [OK] Screenshots captured for {len(results)} page(s).\n")
    for r in results:
        print(f"  ── {r['page_name']} ──")
        print(f"  Figma PNG:        {r['figma_path']}")
        print(f"  Theme screenshot: {r['theme_path']}")
        print(f"  Theme URL:        {r['theme_url']}")
        print(f"  Viewport:         {r['viewport']}px")
        if r["hints"].get("fontFamilies"):
            print(f"  Font families:    {', '.join(r['hints']['fontFamilies'])}")
        if r["hints"].get("brandColors"):
            print(f"  Brand colors:     {', '.join(r['hints']['brandColors'])}")
        if r["hints"].get("notes"):
            print(f"  Notes:            {r['hints']['notes']}")
        print()
    print("  Next: Read both images above and perform visual comparison.")


if __name__ == "__main__":
    main()
