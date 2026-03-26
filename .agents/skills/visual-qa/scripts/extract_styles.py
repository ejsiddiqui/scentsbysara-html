"""Extract computed styles from HTML elements using Playwright."""

from pathlib import Path
from playwright.sync_api import Page, Browser, BrowserContext


def load_properties() -> dict[str, list[str]]:
    """Parse properties.md and return dict of category -> property names."""
    props_file = Path(__file__).parent.parent / "references" / "properties.md"
    if not props_file.exists():
        raise FileNotFoundError(
            f"Properties file not found: {props_file}. "
            "Ensure references/properties.md exists in the visual-qa skill directory."
        )
    categories = {}
    current_category = None
    for line in props_file.read_text().splitlines():
        line = line.strip()
        if line.startswith("## ") and not line.startswith("# Audited"):
            current_category = line[3:].strip()
            categories[current_category] = []
        elif line.startswith("- ") and current_category:
            categories[current_category].append(line[2:].strip())
    return categories


def all_property_names() -> list[str]:
    """Return flat deduplicated list of all CSS property names."""
    seen = set()
    result = []
    for props in load_properties().values():
        for p in props:
            if p not in seen:
                seen.add(p)
                result.append(p)
    return result


EXTRACT_STYLES_JS = """
(args) => {
    const { selector, properties } = args;
    const el = document.querySelector(selector);
    if (!el) return { found: false, selector, styles: {}, tag: null, rect: null };

    const computed = window.getComputedStyle(el);
    const styles = {};
    for (const prop of properties) {
        styles[prop] = computed.getPropertyValue(prop);
    }

    const rect = el.getBoundingClientRect();
    return {
        found: true,
        selector,
        tag: el.tagName.toLowerCase(),
        rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
        styles
    };
}
"""

EXTRACT_SVG_JS = """
(selector) => {
    const el = document.querySelector(selector);
    if (!el) return null;
    const svg = el.tagName === 'svg' ? el : el.querySelector('svg');
    if (!svg) return null;
    return {
        viewBox: svg.getAttribute('viewBox'),
        innerHTML: svg.innerHTML.trim(),
        pathData: Array.from(svg.querySelectorAll('path')).map(p => p.getAttribute('d'))
    };
}
"""

EXTRACT_IMAGE_JS = """
(selector) => {
    const el = document.querySelector(selector);
    if (!el) return null;
    const img = el.tagName === 'IMG' ? el : el.querySelector('img');
    if (!img) return null;
    const rect = img.getBoundingClientRect();
    const computed = window.getComputedStyle(img);
    return {
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight,
        renderedWidth: rect.width,
        renderedHeight: rect.height,
        aspectRatio: rect.height > 0 ? rect.width / rect.height : null,
        objectFit: computed.getPropertyValue('object-fit'),
        objectPosition: computed.getPropertyValue('object-position'),
        borderRadius: computed.getPropertyValue('border-radius')
    };
}
"""


def wait_for_page_ready(page: Page, timeout: int = 15000):
    """Wait for page to be fully loaded including fonts."""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except Exception:
        pass
    page.evaluate("() => document.fonts.ready")


def navigate_to_page(page: Page, url: str, password: str | None = None):
    """Navigate to a page, handling Shopify password gate if needed."""
    page.goto(url, wait_until="domcontentloaded", timeout=25000)
    if password and "/password" in page.url:
        pwd_input = page.locator("input[type='password']")
        if pwd_input.count() > 0:
            pwd_input.fill(password)
            page.locator("button[type='submit']").click()
            page.wait_for_load_state("domcontentloaded", timeout=15000)
    wait_for_page_ready(page)


def extract_element_styles(page: Page, selector: str, properties: list[str]) -> dict:
    """Extract computed styles for a single element."""
    return page.evaluate(EXTRACT_STYLES_JS, {"selector": selector, "properties": properties})


def extract_section_styles(
    page: Page,
    section_selector: str,
    elements: list[dict],
    properties: list[str],
) -> list[dict]:
    """Extract styles for a section container and its child elements.

    Args:
        page: Playwright page
        section_selector: CSS selector for the section container
        elements: List of dicts with "name" and either "mockup" or "theme" key
        properties: List of CSS property names to extract

    Returns:
        List of extraction results (section container first, then each element)
    """
    results = []

    container = extract_element_styles(page, section_selector, properties)
    container["name"] = "Section Container"
    results.append(container)

    if container["found"]:
        try:
            page.evaluate(
                "(s) => { const el = document.querySelector(s); if (el) el.scrollIntoView({block: 'center'}); }",
                section_selector
            )
            page.wait_for_timeout(300)
        except Exception:
            pass

    for el in elements:
        selector = el.get("mockup") or el.get("theme")
        result = extract_element_styles(page, selector, properties)
        result["name"] = el.get("name", selector)
        results.append(result)

    return results


def extract_image_info(page: Page, selector: str) -> dict | None:
    """Extract image-specific properties."""
    return page.evaluate(EXTRACT_IMAGE_JS, selector)


def extract_svg_info(page: Page, selector: str) -> dict | None:
    """Extract SVG-specific attributes."""
    return page.evaluate(EXTRACT_SVG_JS, selector)


def take_section_screenshot(page: Page, section_selector: str, output_path: str) -> bool:
    """Take a screenshot of a specific section. Returns True if successful."""
    el = page.locator(section_selector)
    if el.count() == 0:
        return False
    el.first.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    el.first.screenshot(path=output_path)
    return True


def create_browser_context(
    browser: Browser, viewport_width: int, viewport_height: int = 900
) -> BrowserContext:
    """Create a new browser context with the specified viewport."""
    return browser.new_context(
        viewport={"width": viewport_width, "height": viewport_height}
    )
