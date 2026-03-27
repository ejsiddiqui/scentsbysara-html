"""Screenshot Match — CLI orchestrator."""

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
from compare import compare_screenshots, detect_uncertainties
from report import generate_report, save_report

import anthropic
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


def ask_clarifications(uncertainties: list[str]) -> str:
    """Present uncertain statements to the user and collect answers."""
    if not uncertainties:
        return ""
    print("\n  [?] Claude was uncertain about the following. Please clarify:")
    answers = []
    for i, sentence in enumerate(uncertainties, 1):
        print(f"  {i}. {sentence}")
        answer = input(f"     Your answer: ").strip()
        if answer:
            answers.append(f"Q: {sentence}\nA: {answer}")
    return "\n".join(answers)


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
    print("  [OK] Config valid. No browser or API calls made.")


def audit_page(
    page_config: dict,
    defaults: dict,
    browser,
    client: anthropic.Anthropic,
    repo_root: Path,
    output_dir: str,
    interactive: bool,
    store_password: str | None,
) -> str | None:
    """Audit a single page. Returns path to saved report."""
    page_name = page_config["name"]
    figma_image = page_config.get("figmaImage", "")
    theme_url_path = page_config.get("themeUrl", "/")
    viewport = page_config.get("viewport")
    hints = defaults.get("hints", {})
    theme_base_url = defaults.get("themeBaseUrl", "http://127.0.0.1:9292")
    figma_dir = defaults.get("figmaDir", "figma-exports")

    print(f"\n  Auditing: {page_name}")

    # Resolve viewport interactively if missing
    if not viewport:
        if interactive:
            viewport = ask_viewport(page_name)
        else:
            print(f"  [!] No viewport set for '{page_name}' and --no-interactive is on. Skipping.")
            return None

    # Resolve Figma image path
    figma_path = repo_root / figma_dir / figma_image
    if not figma_path.exists():
        print(f"  [X] Figma image not found: {figma_path}")
        print(f"  Drop the PNG into {repo_root / figma_dir}/ and re-run.")
        return None

    # Screenshot output paths
    screenshot_dir = os.path.join(output_dir, "screenshots")
    slug = page_name.lower().replace(" ", "-")
    theme_screenshot = os.path.join(screenshot_dir, f"screenshot-match-{slug}-{viewport}-theme.png")
    figma_screenshot_copy = os.path.join(screenshot_dir, f"screenshot-match-{slug}-{viewport}-figma.png")

    # Capture theme screenshot
    print(f"    Capturing theme @ {viewport}px ... ", end="", flush=True)
    theme_url = f"{theme_base_url}{theme_url_path}"
    capture_theme_screenshot(browser, theme_url, viewport, theme_screenshot, password=store_password)
    print("done")

    # Copy Figma PNG to screenshots folder for report reference
    os.makedirs(screenshot_dir, exist_ok=True)
    shutil.copy2(str(figma_path), figma_screenshot_copy)

    # Compare (first pass)
    print("    Comparing with Claude Vision ... ", end="", flush=True)
    issues, raw = compare_screenshots(str(figma_path), theme_screenshot, hints, client)
    print(f"{len(issues)} issues found")

    # Clarifying questions if AI was uncertain (max one re-run)
    if interactive:
        uncertainties = detect_uncertainties(raw)
        if uncertainties:
            extra_context = ask_clarifications(uncertainties)
            if extra_context:
                print("    Re-running comparison with your answers ... ", end="", flush=True)
                issues, raw = compare_screenshots(
                    str(figma_path), theme_screenshot, hints, client, extra_context=extra_context
                )
                print(f"{len(issues)} issues found")

    # Determine if parse failed (no issues but raw response is non-empty and has no tables)
    parse_error = len(issues) == 0 and bool(raw) and "|" not in raw

    # Generate and save report
    report_content = generate_report(
        page_name=page_name,
        figma_path=str(figma_path),
        theme_url=theme_url,
        viewport=viewport,
        issues=issues,
        raw_response=raw if parse_error else None,
        parse_error=parse_error,
        figma_screenshot_path=figma_screenshot_copy,
        theme_screenshot_path=theme_screenshot,
    )
    report_path = save_report(report_content, page_name, output_dir)

    critical = sum(1 for i in issues if i.severity == "Critical")
    notable = sum(1 for i in issues if i.severity == "Notable")
    marginal = sum(1 for i in issues if i.severity == "Marginal")
    print(f"    Report: {report_path}  [C:{critical} N:{notable} M:{marginal}]")
    return report_path


def main():
    parser = argparse.ArgumentParser(
        description="Screenshot Match: compare Figma PNGs against live Shopify theme"
    )
    parser.add_argument("--page", default=None, help="Audit specific page (name from config)")
    parser.add_argument("--url", default=None, help="Override Shopify dev server URL")
    parser.add_argument("--password", default=None, help="Shopify store password")
    parser.add_argument("--no-interactive", action="store_true", help="Skip clarifying questions")
    parser.add_argument("--output", default="docs/qa-reports", help="Report output directory")
    parser.add_argument("--dry-run", action="store_true", help="Validate config, no browser/API")
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

    # Check ANTHROPIC_API_KEY
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  [X] ANTHROPIC_API_KEY environment variable is not set.")
        print("  Run: export ANTHROPIC_API_KEY=sk-...")
        sys.exit(1)

    # Resolve repo root (config is at .agents/skills/screenshot-match/config/)
    repo_root = config_path.parents[4]

    theme_url = defaults.get("themeBaseUrl", "http://127.0.0.1:9292")
    wait_for_server(theme_url)

    client = anthropic.Anthropic(api_key=api_key)

    pages = config.get("pages", [])
    report_paths = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for page_config in pages:
                if args.page and page_config["name"].lower() != args.page.lower():
                    continue
                report_path = audit_page(
                    page_config=page_config,
                    defaults=defaults,
                    browser=browser,
                    client=client,
                    repo_root=repo_root,
                    output_dir=args.output,
                    interactive=interactive,
                    store_password=store_password,
                )
                if report_path:
                    report_paths.append(report_path)
        finally:
            browser.close()

    print(f"\n  [OK] Done. {len(report_paths)} report(s) generated.")
    for rp in report_paths:
        print(f"    - {rp}")


if __name__ == "__main__":
    main()
