"""Generate and maintain page-mappings.json config."""

import argparse
import json
import os
import re
from pathlib import Path


def scan_html_pages(html_dir: str) -> list[dict]:
    """Scan /html/ directory for HTML pages and extract section selectors."""
    pages = []
    html_path = Path(html_dir)

    for html_file in sorted(html_path.glob("*.html")):
        content = html_file.read_text(encoding="utf-8")
        page_name = html_file.stem.replace("-", " ").title()
        if page_name == "Index":
            page_name = "Homepage"

        section_classes = re.findall(
            r'<(?:section|div|header|footer|main)\s+[^>]*class="([^"]+)"',
            content,
        )

        sections = []
        for cls_str in section_classes:
            classes = cls_str.split()
            primary = next(
                (c for c in classes if not c.startswith("color-") and c != "container" and not c.startswith("grid-")),
                None,
            )
            if primary:
                sections.append({
                    "name": primary.replace("-", " ").title(),
                    "mockupSelector": f".{primary}",
                    "themeSelector": f".{primary}",
                    "themeFile": "",
                    "elements": [],
                })

        seen = set()
        unique_sections = []
        for s in sections:
            if s["mockupSelector"] not in seen:
                seen.add(s["mockupSelector"])
                unique_sections.append(s)

        theme_routes = {
            "index": "/",
            "product": "/products/body-candle",
            "shop": "/collections/all",
            "cart": "/cart",
            "contact": "/pages/contact",
            "our-story": "/pages/our-story",
            "your-story": "/pages/your-story",
            "body-candles": "/collections/body-candles",
            "scar-collection": "/collections/scar-collection",
            "sculpted-collection": "/collections/sculpted-collection",
            "gifts": "/collections/gifts",
            "checkout": "/checkout",
        }

        pages.append({
            "name": page_name,
            "mockup": html_file.name,
            "theme": theme_routes.get(html_file.stem, f"/pages/{html_file.stem}"),
            "sections": unique_sections,
        })

    return pages


def scan_theme_sections(theme_dir: str) -> dict[str, str]:
    """Scan /theme/sections/ and return mapping of CSS class -> filename."""
    sections_dir = Path(theme_dir) / "sections"
    class_to_file = {}

    for liquid_file in sorted(sections_dir.glob("*.liquid")):
        content = liquid_file.read_text(encoding="utf-8")
        classes = re.findall(r'class="([^"]*)"', content[:2000])
        for cls_str in classes:
            for cls in cls_str.split():
                if not cls.startswith("color-") and not cls.startswith("{"):
                    class_to_file[cls] = liquid_file.name

    return class_to_file


def generate_config(html_dir: str, theme_dir: str) -> dict:
    """Generate initial page-mappings.json config."""
    pages = scan_html_pages(html_dir)
    theme_classes = scan_theme_sections(theme_dir)

    for page in pages:
        for section in page["sections"]:
            css_class = section["mockupSelector"].lstrip(".")
            if css_class in theme_classes:
                section["themeFile"] = f"sections/{theme_classes[css_class]}"

    return {
        "defaults": {
            "themeBaseUrl": "http://127.0.0.1:9292",
            "htmlBaseUrl": "http://127.0.0.1:8080",
            "htmlBaseDir": html_dir,
            "tolerance": 2,
            "storePassword": "",
            "viewports": {
                "core": [1920, 1440, 768, 480],
                "full": [1920, 1440, 1024, 768, 480, 390],
            },
        },
        "pages": pages,
    }


def diff_config(config_path: str, html_dir: str, theme_dir: str):
    """Compare existing config against current mockup state."""
    with open(config_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    current_pages = scan_html_pages(html_dir)
    existing_pages = {p["mockup"]: p for p in existing.get("pages", [])}
    current_page_files = {p["mockup"] for p in current_pages}
    existing_page_files = set(existing_pages.keys())

    has_drift = False

    new_pages = current_page_files - existing_page_files
    if new_pages:
        has_drift = True
        print("\n  NEW pages (not in config):")
        for p in sorted(new_pages):
            print(f"    - {p}")

    removed_pages = existing_page_files - current_page_files
    if removed_pages:
        has_drift = True
        print("\n  REMOVED pages (in config but not in /html/):")
        for p in sorted(removed_pages):
            print(f"    - {p}")

    for current_page in current_pages:
        mockup_file = current_page["mockup"]
        if mockup_file not in existing_pages:
            continue

        existing_page = existing_pages[mockup_file]
        current_selectors = {s["mockupSelector"] for s in current_page["sections"]}
        existing_selectors = {s["mockupSelector"] for s in existing_page.get("sections", [])}

        new_secs = current_selectors - existing_selectors
        if new_secs:
            has_drift = True
            print(f"\n  NEW sections in {mockup_file}:")
            for s in sorted(new_secs):
                print(f"    - {s}")

        removed_secs = existing_selectors - current_selectors
        if removed_secs:
            has_drift = True
            print(f"\n  STALE sections in {mockup_file} (selector no longer in HTML):")
            for s in sorted(removed_secs):
                print(f"    - {s}")

    if not has_drift:
        print("\n  No config drift detected.")
    else:
        print(f"\n  Update config at: {config_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate or diff page-mappings.json")
    parser.add_argument("--diff", action="store_true", help="Compare existing config against current mockup")
    parser.add_argument("--html-dir", default="html", help="Path to HTML mockup directory")
    parser.add_argument("--theme-dir", default="theme", help="Path to Shopify theme directory")
    parser.add_argument("--output", default=None, help="Output path for generated config")

    args = parser.parse_args()

    config_path = Path(__file__).parent.parent / "config" / "page-mappings.json"

    if args.diff:
        if not config_path.exists():
            print(f"  No existing config at {config_path}. Run without --diff first.")
            return
        diff_config(str(config_path), args.html_dir, args.theme_dir)
        return

    config = generate_config(args.html_dir, args.theme_dir)
    output = args.output or str(config_path)
    os.makedirs(os.path.dirname(output), exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"\n  Config generated: {output}")
    print(f"  Pages: {len(config['pages'])}")
    total_sections = sum(len(p['sections']) for p in config['pages'])
    print(f"  Sections: {total_sections}")
    print(f"\n  Review and hand-edit the config:")
    print(f"    - themeSelector values (may differ from mockup class names)")
    print(f"    - themeFile paths")
    print(f"    - Add element-level mappings to 'elements' arrays")


if __name__ == "__main__":
    main()
