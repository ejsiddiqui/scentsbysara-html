# Visual QA Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Playwright-based visual QA skill that compares HTML mockups against the live Shopify theme, extracting computed styles section-by-section and producing actionable Markdown reports.

**Architecture:** A Python CLI tool (`audit.py`) orchestrates the workflow: starts an HTTP server for HTML mockups, opens both mockup and theme pages in Playwright at multiple viewports, extracts computed styles via JS injection, diffs them with configurable tolerance, and generates a Markdown report. Configuration is driven by a JSON page-mapping file.

**Tech Stack:** Python 3.10+, Playwright (sync API), Pillow (optional, for `--image-diff`), http.server (stdlib)

**Spec:** `docs/superpowers/specs/2026-03-27-visual-qa-skill-design.md`

**Existing patterns to reuse from `scripts/qa_phase8.py`:**
- Password gate unlock (`unlock()` function)
- `goto()` with `wait_until="domcontentloaded"` + `networkidle` fallback
- Viewport sizing with `page.set_viewport_size()`
- Console error filtering (CSP/GTM/favicon allow-list)
- Context lifecycle management (new context per viewport, explicit cleanup)

---

## File Structure

```
.agents/skills/visual-qa/
├── SKILL.md                          — Skill instructions for AI agents
├── config/
│   └── page-mappings.json            — Page/section/element mapping config
├── scripts/
│   ├── audit.py                      — Main CLI entry point & orchestrator
│   ├── serve_html.py                 — Simple HTTP server for /html/ directory
│   ├── extract_styles.py             — Playwright JS injection & style extraction
│   ├── diff_styles.py                — Style comparison & severity classification
│   ├── report.py                     — Markdown report generator
│   ├── scaffold_mappings.py          — Config generator & --diff mode
│   └── requirements.txt              — Python dependencies
└── references/
    └── properties.md                 — Audited CSS properties by category
```

**Change from spec:** Split `extract_styles.py` into three focused modules:
- `extract_styles.py` — Only Playwright JS injection and raw style extraction
- `diff_styles.py` — Comparison logic, tolerance, severity classification
- `report.py` — Markdown report generation

This keeps each file focused and independently testable.

---

## Task 1: Skill skeleton & dependencies

**Files:**
- Create: `.agents/skills/visual-qa/SKILL.md`
- Create: `.agents/skills/visual-qa/scripts/requirements.txt`
- Create: `.agents/skills/visual-qa/references/properties.md`

- [ ] **Step 1: Create `requirements.txt`**

```
playwright>=1.40.0
Pillow>=10.0.0
```

- [ ] **Step 2: Create `references/properties.md`**

This file lists all CSS properties audited, grouped by category. The scripts import this as the source of truth for which properties to extract.

```markdown
# Audited CSS Properties

## Typography
- font-family
- font-size
- font-weight
- font-style
- line-height
- letter-spacing
- text-transform
- color
- text-align
- text-decoration

## Sizes & Spacing
- width
- height
- min-width
- max-width
- min-height
- max-height
- padding-top
- padding-right
- padding-bottom
- padding-left
- margin-top
- margin-right
- margin-bottom
- margin-left
- border-top-width
- border-right-width
- border-bottom-width
- border-left-width
- border-top-style
- border-right-style
- border-bottom-style
- border-left-style
- border-top-color
- border-right-color
- border-bottom-color
- border-left-color
- border-top-left-radius
- border-top-right-radius
- border-bottom-left-radius
- border-bottom-right-radius
- box-shadow

## Layout & Positioning
- display
- flex-direction
- justify-content
- align-items
- gap
- grid-template-columns
- grid-template-rows
- position
- top
- right
- bottom
- left

## Images
- width
- height
- object-fit
- object-position
- border-radius

## Icons & SVGs
- width
- height
- fill
- stroke
- color
- margin-top
- margin-right
- margin-bottom
- margin-left

## Backgrounds & Visual
- background-color
- background-image
- box-shadow
- opacity
```

- [ ] **Step 3: Create `SKILL.md`**

```markdown
---
name: visual-qa
description: Visual QA audit comparing HTML mockups against live Shopify theme. Use when asked to audit, QA, compare, or verify visual fidelity between mockup and theme. Compares computed CSS styles section-by-section at multiple viewports and generates actionable Markdown reports with severity levels (Critical/Notable/Marginal/Unknown).
---

# Visual QA Skill

Automate visual QA by comparing HTML mockups (`/html/`) against the live Shopify theme using Playwright.

## Prerequisites

Install dependencies (one-time):
```bash
pip install -r .agents/skills/visual-qa/scripts/requirements.txt
playwright install chromium
```

Ensure the Shopify dev server is running:
```bash
cd theme && shopify theme dev --store=scentsbysara-dev.myshopify.com
```

## Quick Start

```bash
# Audit entire site (core viewports: 1920, 1440, 768, 480)
python .agents/skills/visual-qa/scripts/audit.py

# Audit specific page
python .agents/skills/visual-qa/scripts/audit.py --page homepage

# Audit specific section
python .agents/skills/visual-qa/scripts/audit.py --page homepage --section "Hero Slideshow"

# Full viewports (adds 1024, 390)
python .agents/skills/visual-qa/scripts/audit.py --viewports full

# With image visual diff
python .agents/skills/visual-qa/scripts/audit.py --image-diff

# Validate config without running browser
python .agents/skills/visual-qa/scripts/audit.py --dry-run
```

## CLI Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--page <name>` | all | Audit specific page (name from config) |
| `--section <name>` | all | Audit specific section (requires `--page`) |
| `--url <url>` | `http://127.0.0.1:9292` | Shopify dev server URL |
| `--viewports full` | core | Use full viewport set |
| `--tolerance <px>` | 2 | Pixel tolerance threshold |
| `--image-diff` | off | Enable visual screenshot diff for images |
| `--svg-compare` | off | Enable SVG content/path comparison |
| `--output <path>` | `docs/qa-reports/` | Report output directory |
| `--dry-run` | off | Validate config and list sections |

## Configuration

Edit `config/page-mappings.json` to define page-to-section-to-element mappings. See spec for format.

To detect config drift after mockup changes:
```bash
python .agents/skills/visual-qa/scripts/scaffold_mappings.py --diff
```

## Workflow

1. Run audit → get report at `docs/qa-reports/visual-qa-<page>-<datetime>.md`
2. Implement fixes based on report (each issue lists element, property, expected/actual, severity, theme file)
3. Re-run audit → verify fixes
4. Repeat until no Critical or Notable issues remain
5. Marginal issues are acceptable (flagged, not blocking)

## Severity Levels

| Severity | Meaning |
|----------|---------|
| Critical | Large diff (>4px default), non-numeric mismatch, color diff >10, missing property |
| Notable | Medium diff (2-4px default), color diff >5 |
| Marginal | Within tolerance but non-zero |
| Unknown | Selector not found — stale config |

## Report Format

Reports are Markdown files grouped by: Page > Section > Category (Viewport). Each issue includes the element selector, property, expected value, actual value, and severity. Theme file path is included per section for easy navigation.
```

- [ ] **Step 4: Install dependencies**

Run: `pip install -r .agents/skills/visual-qa/scripts/requirements.txt && playwright install chromium`
Expected: Dependencies install successfully

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/visual-qa/SKILL.md .agents/skills/visual-qa/scripts/requirements.txt .agents/skills/visual-qa/references/properties.md
git commit -m "feat(visual-qa): add skill skeleton, dependencies, and property reference"
```

---

## Task 2: HTML mockup server (`serve_html.py`)

**Files:**
- Create: `.agents/skills/visual-qa/scripts/serve_html.py`

- [ ] **Step 1: Implement `serve_html.py`**

A simple HTTP server that serves the `/html/` directory. Must be startable/stoppable programmatically from `audit.py`.

```python
"""Simple HTTP server for serving HTML mockup files."""

import http.server
import threading
import socket
import os
from pathlib import Path


class MockupServer:
    """Serves the /html/ directory over HTTP for Playwright to access."""

    def __init__(self, html_dir: str, port: int = 8080):
        self.html_dir = os.path.abspath(html_dir)
        self.port = port
        self._server = None
        self._thread = None

    def start(self):
        """Start the server in a background thread. Fails fast if port is occupied."""
        # Check port availability
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", self.port))
            except OSError:
                raise RuntimeError(
                    f"Port {self.port} is already in use. "
                    f"Stop the process using it or configure a different port in page-mappings.json."
                )

        handler = http.server.SimpleHTTPRequestHandler
        self._server = http.server.HTTPServer(
            ("127.0.0.1", self.port),
            lambda *args, **kwargs: handler(*args, directory=self.html_dir, **kwargs),
        )
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        print(f"  Mockup server started at http://127.0.0.1:{self.port} (serving {self.html_dir})")

    def stop(self):
        """Shut down the server."""
        if self._server:
            self._server.shutdown()
            self._thread.join(timeout=5)
            self._server = None
            self._thread = None

    @property
    def base_url(self):
        return f"http://127.0.0.1:{self.port}"


if __name__ == "__main__":
    import sys
    html_dir = sys.argv[1] if len(sys.argv) > 1 else "html"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    server = MockupServer(html_dir, port)
    server.start()
    print(f"Serving {html_dir} at http://127.0.0.1:{port} — press Ctrl+C to stop")
    try:
        server._thread.join()
    except KeyboardInterrupt:
        server.stop()
```

- [ ] **Step 2: Test manually**

Run: `python .agents/skills/visual-qa/scripts/serve_html.py html 8080`
Then in another terminal: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/index.html`
Expected: `200`
Stop server with Ctrl+C.

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/visual-qa/scripts/serve_html.py
git commit -m "feat(visual-qa): add HTML mockup HTTP server"
```

---

## Task 3: Style extraction module (`extract_styles.py`)

**Files:**
- Create: `.agents/skills/visual-qa/scripts/extract_styles.py`

- [ ] **Step 1: Implement `extract_styles.py`**

This module handles Playwright browser interaction: navigating pages, waiting for fonts, scrolling to sections, and extracting computed styles via JS injection.

```python
"""Extract computed styles from HTML elements using Playwright."""

from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext


# Load property list from references/properties.md
def load_properties() -> dict[str, list[str]]:
    """Parse properties.md and return dict of category -> property names."""
    props_file = Path(__file__).parent.parent / "references" / "properties.md"
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


# JavaScript injected into the page to extract computed styles
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

# JavaScript to extract SVG-specific attributes
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

# JavaScript to extract image-specific info
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
        aspectRatio: rect.width / rect.height,
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
        pass  # Fallback: proceed after domcontentloaded
    # Wait for web fonts to finish loading
    page.evaluate("() => document.fonts.ready")


def navigate_to_page(page: Page, url: str, password: str | None = None):
    """Navigate to a page, handling Shopify password gate if needed."""
    page.goto(url, wait_until="domcontentloaded", timeout=25000)

    # Handle Shopify password page
    if password and "/password" in page.url:
        pwd_input = page.locator("input[type='password']")
        if pwd_input.count() > 0:
            pwd_input.fill(password)
            page.locator("button[type='submit']").click()
            page.wait_for_load_state("domcontentloaded", timeout=15000)

    wait_for_page_ready(page)


def extract_element_styles(
    page: Page, selector: str, properties: list[str]
) -> dict:
    """Extract computed styles for a single element.

    Returns dict with keys: found, selector, tag, rect, styles
    """
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
        elements: List of {"name": str, "mockup"|"theme": str} element mappings
        properties: List of CSS property names to extract

    Returns:
        List of extraction results (one per element, plus the section container)
    """
    results = []

    # Extract section container styles
    container = extract_element_styles(page, section_selector, properties)
    container["name"] = "Section Container"
    results.append(container)

    # Scroll section into view for accurate rendering
    if container["found"]:
        page.evaluate(
            f"document.querySelector('{section_selector}').scrollIntoView({{block: 'center'}})"
        )
        page.wait_for_timeout(300)  # Allow layout to settle after scroll

    # Extract each mapped element
    for el in elements:
        # Use whichever key is present (mockup or theme)
        selector = el.get("mockup") or el.get("theme")
        result = extract_element_styles(page, selector, properties)
        result["name"] = el.get("name", selector)
        results.append(result)

    return results


def extract_image_info(page: Page, selector: str) -> dict | None:
    """Extract image-specific properties (dimensions, object-fit, aspect ratio)."""
    return page.evaluate(EXTRACT_IMAGE_JS, selector)


def extract_svg_info(page: Page, selector: str) -> dict | None:
    """Extract SVG-specific attributes (viewBox, paths)."""
    return page.evaluate(EXTRACT_SVG_JS, selector)


def take_section_screenshot(
    page: Page, section_selector: str, output_path: str
) -> bool:
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
```

- [ ] **Step 2: Verify module loads**

Run: `python -c "from scripts.extract_styles import load_properties, all_property_names; print(len(all_property_names()), 'properties loaded')"`
(Run from `.agents/skills/visual-qa/` directory)
Expected: prints count of properties (should be ~45+)

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/visual-qa/scripts/extract_styles.py
git commit -m "feat(visual-qa): add Playwright style extraction module"
```

---

## Task 4: Style diffing module (`diff_styles.py`)

**Files:**
- Create: `.agents/skills/visual-qa/scripts/diff_styles.py`

- [ ] **Step 1: Implement `diff_styles.py`**

Handles comparison of extracted style values and severity classification.

```python
"""Compare extracted CSS styles and classify differences by severity."""

import re
from dataclasses import dataclass


@dataclass
class StyleDiff:
    """A single style difference between mockup and theme."""
    element_name: str
    element_selector: str
    property: str
    category: str
    expected: str
    actual: str
    severity: str  # "Critical", "Notable", "Marginal", "Unknown"
    viewport: int
    section_name: str = ""


# Properties where values are colors (parsed into RGB channels)
COLOR_PROPERTIES = {
    "color", "background-color",
    "border-top-color", "border-right-color", "border-bottom-color", "border-left-color",
    "fill", "stroke",
}

# Properties with numeric pixel values
NUMERIC_PROPERTIES = {
    "font-size", "font-weight", "line-height", "letter-spacing",
    "width", "height", "min-width", "max-width", "min-height", "max-height",
    "padding-top", "padding-right", "padding-bottom", "padding-left",
    "margin-top", "margin-right", "margin-bottom", "margin-left",
    "border-top-width", "border-right-width", "border-bottom-width", "border-left-width",
    "border-top-left-radius", "border-top-right-radius",
    "border-bottom-left-radius", "border-bottom-right-radius",
    "gap", "top", "right", "bottom", "left", "opacity",
}

# Properties that map to categories in the report
PROPERTY_CATEGORIES = {
    "Typography": {
        "font-family", "font-size", "font-weight", "font-style",
        "line-height", "letter-spacing", "text-transform",
        "color", "text-align", "text-decoration",
    },
    "Sizes & Spacing": {
        "width", "height", "min-width", "max-width", "min-height", "max-height",
        "padding-top", "padding-right", "padding-bottom", "padding-left",
        "margin-top", "margin-right", "margin-bottom", "margin-left",
        "border-top-width", "border-right-width", "border-bottom-width", "border-left-width",
        "border-top-style", "border-right-style", "border-bottom-style", "border-left-style",
        "border-top-color", "border-right-color", "border-bottom-color", "border-left-color",
        "border-top-left-radius", "border-top-right-radius",
        "border-bottom-left-radius", "border-bottom-right-radius",
        "box-shadow",
    },
    "Layout & Positioning": {
        "display", "flex-direction", "justify-content", "align-items", "gap",
        "grid-template-columns", "grid-template-rows",
        "position", "top", "right", "bottom", "left",
    },
    "Backgrounds & Visual": {
        "background-color", "background-image", "opacity",
    },
    "Images": {
        "object-fit", "object-position",
    },
    "Icons & SVGs": {
        "fill", "stroke",
    },
}


def _parse_rgb(value: str) -> tuple[int, int, int] | None:
    """Parse rgb(r, g, b) or rgba(r, g, b, a) string into (r, g, b) tuple."""
    match = re.match(r"rgba?\(\s*(\d+),\s*(\d+),\s*(\d+)", value)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    # Handle hex colors
    hex_match = re.match(r"#([0-9a-fA-F]{6})", value)
    if hex_match:
        h = hex_match.group(1)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return None


def _parse_numeric(value: str) -> float | None:
    """Parse a CSS value to a numeric pixel value."""
    match = re.match(r"(-?[\d.]+)", value)
    if match:
        return float(match.group(1))
    if value == "normal":
        return None  # Can't compare "normal" numerically
    return None


def _get_category(prop: str) -> str:
    """Get the report category for a CSS property."""
    for category, props in PROPERTY_CATEGORIES.items():
        if prop in props:
            return category
    return "Other"


def classify_color_diff(expected: str, actual: str, prop: str) -> tuple[str, float]:
    """Classify a color difference. Returns (severity, max_channel_diff)."""
    rgb_expected = _parse_rgb(expected)
    rgb_actual = _parse_rgb(actual)

    if rgb_expected is None or rgb_actual is None:
        # Can't parse as color — treat as non-numeric
        if expected != actual:
            return "Critical", 0
        return "", 0

    max_diff = max(
        abs(rgb_expected[0] - rgb_actual[0]),
        abs(rgb_expected[1] - rgb_actual[1]),
        abs(rgb_expected[2] - rgb_actual[2]),
    )

    if max_diff == 0:
        return "", 0
    elif max_diff > 10:
        return "Critical", max_diff
    elif max_diff > 5:
        return "Notable", max_diff
    else:
        return "Marginal", max_diff


def classify_numeric_diff(
    expected: str, actual: str, tolerance: float
) -> tuple[str, float]:
    """Classify a numeric difference. Returns (severity, diff_value)."""
    val_expected = _parse_numeric(expected)
    val_actual = _parse_numeric(actual)

    if val_expected is None or val_actual is None:
        # Can't parse as numeric — treat as non-numeric
        if expected != actual:
            return "Critical", 0
        return "", 0

    diff = abs(val_expected - val_actual)

    if diff == 0:
        return "", 0
    elif diff > tolerance * 2:
        return "Critical", diff
    elif diff > tolerance:
        return "Notable", diff
    else:
        return "Marginal", diff


def classify_nonnumeric_diff(expected: str, actual: str) -> str:
    """Classify a non-numeric property difference."""
    if expected == actual:
        return ""
    return "Critical"


def diff_element_styles(
    element_name: str,
    element_selector: str,
    mockup_styles: dict,
    theme_styles: dict,
    tolerance: float,
    viewport: int,
) -> list[StyleDiff]:
    """Compare styles for one element between mockup and theme.

    Returns list of StyleDiff for each property that differs.
    """
    diffs = []

    for prop, expected in mockup_styles.items():
        actual = theme_styles.get(prop, "")
        category = _get_category(prop)

        # Explicit check for missing property
        if actual == "" and expected != "":
            diffs.append(StyleDiff(
                element_name=element_name,
                element_selector=element_selector,
                property=prop,
                category=category,
                expected=expected,
                actual="(missing)",
                severity="Critical",
                viewport=viewport,
            ))
            continue

        if prop in COLOR_PROPERTIES:
            severity, _ = classify_color_diff(expected, actual, prop)
        elif prop in NUMERIC_PROPERTIES:
            severity, _ = classify_numeric_diff(expected, actual, tolerance)
        else:
            severity = classify_nonnumeric_diff(expected, actual)

        if severity:  # Only include differences
            diffs.append(StyleDiff(
                element_name=element_name,
                element_selector=element_selector,
                property=prop,
                category=category,
                expected=expected,
                actual=actual,
                severity=severity,
                viewport=viewport,
            ))

    return diffs


def diff_sections(
    mockup_results: list[dict],
    theme_results: list[dict],
    tolerance: float,
    viewport: int,
) -> list[StyleDiff]:
    """Compare extracted styles for all elements in a section.

    Args:
        mockup_results: Output from extract_section_styles() for mockup
        theme_results: Output from extract_section_styles() for theme
        tolerance: Pixel tolerance for numeric comparisons
        viewport: Viewport width for the report

    Returns:
        List of all StyleDiff items for this section/viewport combination
    """
    all_diffs = []

    for mockup_el, theme_el in zip(mockup_results, theme_results):
        # Handle Unknown — selector not found
        if not mockup_el["found"]:
            all_diffs.append(StyleDiff(
                element_name=mockup_el["name"],
                element_selector=mockup_el["selector"],
                property="selector",
                category="Unknown",
                expected="exists",
                actual="not found in mockup",
                severity="Unknown",
                viewport=viewport,
            ))
            continue
        if not theme_el["found"]:
            all_diffs.append(StyleDiff(
                element_name=theme_el["name"],
                element_selector=theme_el["selector"],
                property="selector",
                category="Unknown",
                expected="exists",
                actual="not found in theme",
                severity="Unknown",
                viewport=viewport,
            ))
            continue

        element_diffs = diff_element_styles(
            element_name=mockup_el["name"],
            element_selector=theme_el["selector"],  # Use theme selector in report
            mockup_styles=mockup_el["styles"],
            theme_styles=theme_el["styles"],
            tolerance=tolerance,
            viewport=viewport,
        )
        all_diffs.extend(element_diffs)

    return all_diffs
```

- [ ] **Step 2: Test severity classification**

Run: `python -c "
from scripts.diff_styles import classify_numeric_diff, classify_color_diff, classify_nonnumeric_diff
# Numeric
assert classify_numeric_diff('48px', '42px', 2) == ('Critical', 6.0)
assert classify_numeric_diff('48px', '45px', 2) == ('Notable', 3.0)
assert classify_numeric_diff('48px', '47px', 2) == ('Marginal', 1.0)
assert classify_numeric_diff('48px', '48px', 2) == ('', 0)
# Color
assert classify_color_diff('rgb(139, 115, 85)', 'rgb(139, 115, 85)', 'color') == ('', 0)
assert classify_color_diff('rgb(139, 115, 85)', 'rgb(138, 114, 84)', 'color') == ('Marginal', 1)
assert classify_color_diff('rgb(139, 115, 85)', 'rgb(130, 115, 85)', 'color') == ('Notable', 9)
assert classify_color_diff('rgb(139, 115, 85)', 'rgb(100, 115, 85)', 'color') == ('Critical', 39)
# Non-numeric
assert classify_nonnumeric_diff('flex', 'block') == 'Critical'
assert classify_nonnumeric_diff('flex', 'flex') == ''
print('All diff tests passed')
"`
Expected: `All diff tests passed`

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/visual-qa/scripts/diff_styles.py
git commit -m "feat(visual-qa): add style diffing and severity classification module"
```

---

## Task 5: Report generator (`report.py`)

**Files:**
- Create: `.agents/skills/visual-qa/scripts/report.py`

- [ ] **Step 1: Implement `report.py`**

Generates Markdown reports from StyleDiff lists.

```python
"""Generate Markdown QA reports from style diffs."""

import os
from datetime import datetime
from collections import defaultdict
from pathlib import Path

from diff_styles import StyleDiff


def generate_report(
    page_name: str,
    sections: list[dict],
    all_diffs: list[StyleDiff],
    viewports: list[int],
    tolerance: int,
    flags: list[str],
    screenshot_dir: str | None = None,
) -> str:
    """Generate a Markdown report for a single page.

    Args:
        page_name: Display name of the page
        sections: Section configs from page-mappings.json
        all_diffs: All StyleDiff items for this page
        viewports: List of viewport widths used
        tolerance: Tolerance value used
        flags: List of active flags (e.g., ["--image-diff"])
        screenshot_dir: Relative path to screenshots directory

    Returns:
        Markdown string
    """
    now = datetime.now()
    viewport_str = ", ".join(f"{v}px" for v in viewports)
    flags_str = " ".join(flags) if flags else "none"

    # Count severities
    counts = defaultdict(int)
    for d in all_diffs:
        counts[d.severity] += 1

    lines = []
    lines.append(f"# Visual QA Report: {page_name}")
    lines.append(f"**Date:** {now.strftime('%Y-%m-%d %H:%M')} | **Viewports:** {viewport_str}")
    lines.append(f"**Tolerance:** {tolerance}px | **Flags:** {flags_str}")
    lines.append("")

    # Summary
    lines.append("## Summary")
    summary_parts = []
    for sev in ["Critical", "Notable", "Marginal", "Unknown"]:
        if counts[sev] > 0:
            summary_parts.append(f"{sev}: {counts[sev]}")
    if summary_parts:
        lines.append("- " + " | ".join(summary_parts))
    else:
        lines.append("- No issues found!")
    lines.append("")

    # Unknown items (prominent)
    unknowns = [d for d in all_diffs if d.severity == "Unknown"]
    if unknowns:
        lines.append("### Unknown Selectors (config may be stale)")
        lines.append("")
        lines.append("| Element | Selector | Viewport | Details |")
        lines.append("|---------|----------|----------|---------|")
        for d in unknowns:
            lines.append(f"| {d.element_name} | `{d.element_selector}` | {d.viewport}px | {d.actual} |")
        lines.append("")

    # Group diffs by section (using section_name tagged during audit)
    section_diffs = defaultdict(list)
    for d in all_diffs:
        if d.severity == "Unknown":
            continue  # Already shown above
        section_diffs[d.section_name].append(d)

    # Render each section
    for sec in sections:
        sec_name = sec["name"]
        diffs = section_diffs.get(sec_name, [])

        lines.append(f"## {sec_name}")
        theme_file = sec.get("themeFile", "")
        if theme_file:
            lines.append(f"**Theme file:** `theme/{theme_file}`")

        if screenshot_dir:
            slug = sec_name.lower().replace(" ", "-")
            lines.append(f"**Screenshots:** `{screenshot_dir}/{page_name.lower()}-{slug}-*.png` (section-level)")

        lines.append("")

        if not diffs:
            lines.append("No issues found.")
            lines.append("")
            continue

        # Group by category, then viewport
        cat_viewport_diffs = defaultdict(lambda: defaultdict(list))
        for d in diffs:
            cat_viewport_diffs[d.category][d.viewport].append(d)

        for category in ["Typography", "Sizes & Spacing", "Layout & Positioning", "Images", "Icons & SVGs", "Backgrounds & Visual", "Other"]:
            if category not in cat_viewport_diffs:
                continue

            for viewport in sorted(cat_viewport_diffs[category].keys(), reverse=True):
                vp_diffs = cat_viewport_diffs[category][viewport]
                lines.append(f"### {category} ({viewport}px)")
                lines.append("")
                lines.append("| Element | Property | Expected | Actual | Severity |")
                lines.append("|---------|----------|----------|--------|----------|")
                for d in vp_diffs:
                    lines.append(
                        f"| `{d.element_selector}` | {d.property} | {d.expected} | {d.actual} | {d.severity} |"
                    )
                lines.append("")

    lines.append("---")
    lines.append("*Generated by visual-qa skill. Run again after fixes to verify.*")
    lines.append("")

    return "\n".join(lines)


def save_report(
    content: str,
    page_name: str,
    output_dir: str = "docs/qa-reports",
) -> str:
    """Save report to file. Returns the file path."""
    os.makedirs(output_dir, exist_ok=True)
    now = datetime.now()
    slug = page_name.lower().replace(" ", "-")
    filename = f"visual-qa-{slug}-{now.strftime('%Y-%m-%d-%H%M')}.md"
    filepath = os.path.join(output_dir, filename)
    Path(filepath).write_text(content, encoding="utf-8")
    return filepath
```

- [ ] **Step 2: Test report generation with mock data**

Run: `python -c "
from scripts.diff_styles import StyleDiff
from scripts.report import generate_report
diffs = [
    StyleDiff('Title', '.hero__title', 'font-size', 'Typography', '64px', '58px', 'Critical', 1440),
    StyleDiff('Subtitle', '.hero__subtitle', 'letter-spacing', 'Typography', '2px', '1px', 'Notable', 1440),
    StyleDiff('Subtitle', '.hero__subtitle', 'color', 'Typography', 'rgb(139,115,85)', 'rgb(138,114,84)', 'Marginal', 1440),
]
sections = [{'name': 'Hero Slideshow', 'themeSelector': '.home-hero', 'themeFile': 'sections/hero-slideshow.liquid', 'elements': [{'name': 'Title', 'theme': '.hero__title'}, {'name': 'Subtitle', 'theme': '.hero__subtitle'}]}]
report = generate_report('Homepage', sections, diffs, [1440, 768, 480], 2, [])
print(report[:500])
"`
Expected: Markdown output with summary and table rows

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/visual-qa/scripts/report.py
git commit -m "feat(visual-qa): add Markdown report generator"
```

---

## Task 6: Main audit orchestrator (`audit.py`)

**Files:**
- Create: `.agents/skills/visual-qa/scripts/audit.py`
- Create: `.agents/skills/visual-qa/scripts/__init__.py`

- [ ] **Step 1: Create `scripts/__init__.py`**

Empty file to make scripts a package:
```python
```

- [ ] **Step 2: Implement `audit.py`**

Main CLI entry point that orchestrates the full audit workflow.

```python
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
    extract_image_info,
    extract_svg_info,
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
            print(f"\n  ⚠ Cannot reach Shopify dev server at {url}")
            print(f"  Please start it with: cd theme && shopify theme dev --store=scentsbysara-dev.myshopify.com")
            print(f"  Waiting... (attempt {attempt + 1}/{max_retries})")
        else:
            print(f"  Retrying... (attempt {attempt + 1}/{max_retries})")
        time.sleep(interval)

    print(f"\n  ✗ Could not reach {url} after {max_retries} attempts. Exiting.")
    sys.exit(1)


def run_dry_run(config: dict, page_filter: str | None, section_filter: str | None):
    """Validate config and list what would be audited."""
    defaults = config.get("defaults", {})
    pages = config.get("pages", [])

    print("\n  DRY RUN — Config validation")
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

    print("  ✓ Config is valid. No browser launched.")


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
        print(f"  ✗ Config not found: {config_path}")
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
    store_password = args.password or defaults.get("storePassword")

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
            print(f"\n  ✓ Audit complete. {len(report_paths)} report(s) generated.")
            for rp in report_paths:
                print(f"    - {rp}")

    finally:
        mockup_server.stop()


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/visual-qa/scripts/__init__.py .agents/skills/visual-qa/scripts/audit.py
git commit -m "feat(visual-qa): add main audit orchestrator CLI"
```

---

## Task 7: Scaffold mappings script (`scaffold_mappings.py`)

**Files:**
- Create: `.agents/skills/visual-qa/scripts/scaffold_mappings.py`

- [ ] **Step 1: Implement `scaffold_mappings.py`**

Scans `/html/` and `/theme/sections/` to generate initial `page-mappings.json` and supports `--diff` mode.

```python
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

        # Extract top-level section selectors (class-based)
        # Look for <section class="..." or <div class="..." at low nesting depth
        section_classes = re.findall(
            r'<(?:section|div|header|footer|main)\s+[^>]*class="([^"]+)"',
            content,
        )

        sections = []
        for cls_str in section_classes:
            classes = cls_str.split()
            # Use first meaningful class as selector
            primary = next((c for c in classes if not c.startswith("color-") and c != "container"), None)
            if primary:
                sections.append({
                    "name": primary.replace("-", " ").title(),
                    "mockupSelector": f".{primary}",
                    "themeSelector": f".{primary}",
                    "themeFile": "",
                    "elements": [],
                })

        # Deduplicate sections by mockupSelector
        seen = set()
        unique_sections = []
        for s in sections:
            if s["mockupSelector"] not in seen:
                seen.add(s["mockupSelector"])
                unique_sections.append(s)

        # Map page to theme route
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
        # Find class attributes in outermost elements
        classes = re.findall(r'class="([^"]*)"', content[:2000])  # First 2KB
        for cls_str in classes:
            for cls in cls_str.split():
                if not cls.startswith("color-") and not cls.startswith("{"):
                    class_to_file[cls] = liquid_file.name
                    break
            break  # Only first class attribute

    return class_to_file


def generate_config(html_dir: str, theme_dir: str) -> dict:
    """Generate initial page-mappings.json config."""
    pages = scan_html_pages(html_dir)
    theme_classes = scan_theme_sections(theme_dir)

    # Try to match section selectors to theme files
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
    """Compare existing config against current mockup state. Print drift report."""
    with open(config_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    # Scan current HTML pages
    current_pages = scan_html_pages(html_dir)
    existing_pages = {p["mockup"]: p for p in existing.get("pages", [])}
    current_page_files = {p["mockup"] for p in current_pages}
    existing_page_files = set(existing_pages.keys())

    has_drift = False

    # New pages
    new_pages = current_page_files - existing_page_files
    if new_pages:
        has_drift = True
        print("\n  NEW pages (not in config):")
        for p in sorted(new_pages):
            print(f"    - {p}")

    # Removed pages
    removed_pages = existing_page_files - current_page_files
    if removed_pages:
        has_drift = True
        print("\n  REMOVED pages (in config but not in /html/):")
        for p in sorted(removed_pages):
            print(f"    - {p}")

    # Check selectors in existing pages
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
        print("\n  ✓ No config drift detected.")
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
            print(f"  ✗ No existing config at {config_path}. Run without --diff first.")
            return
        diff_config(str(config_path), args.html_dir, args.theme_dir)
        return

    # Generate new config
    config = generate_config(args.html_dir, args.theme_dir)
    output = args.output or str(config_path)
    os.makedirs(os.path.dirname(output), exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"\n  ✓ Config generated: {output}")
    print(f"  Pages: {len(config['pages'])}")
    total_sections = sum(len(p['sections']) for p in config['pages'])
    print(f"  Sections: {total_sections}")
    print(f"\n  ⚠ Review and hand-edit the config — especially:")
    print(f"    - themeSelector values (may differ from mockup class names)")
    print(f"    - themeFile paths")
    print(f"    - Add element-level mappings to each section's 'elements' array")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test scaffold generation**

Run: `python .agents/skills/visual-qa/scripts/scaffold_mappings.py --html-dir html --theme-dir theme --output .agents/skills/visual-qa/config/page-mappings.json`
Expected: Config file generated with pages and sections detected from HTML files.

- [ ] **Step 3: Review and manually refine the generated config**

Open `.agents/skills/visual-qa/config/page-mappings.json` and verify:
- Page names and routes are correct
- Section selectors match between mockup and theme (update `themeSelector` where class names differ)
- `themeFile` references are correct
- Add key `elements` arrays for sections that need element-level auditing

Known selector mappings from codebase exploration:

| Mockup | Theme | Theme File |
|--------|-------|------------|
| `.home-hero` | `.home-hero` | `sections/hero-slideshow.liquid` |
| `.best-sellers` | `.featured-collection` | `sections/featured-collection.liquid` |
| `.commitment-section` | `.commitment-section` | `sections/commitment.liquid` |
| `.collections-section` | `.collections-grid` | `sections/collections-grid.liquid` |
| `.story-split` | `.split-view` | `sections/split-view.liquid` |
| `.testimonials-section` | `.testimonials-section` | `sections/testimonials.liquid` |
| `.shop-hero` | `.collection-page` | `sections/main-collection.liquid` |
| `.product-main` | `.product-page-section` | `sections/main-product.liquid` |
| `.scents-section` | `.scents-section` | `sections/scents-section.liquid` |
| `.cart-layout` | `.cart-page-section` | `sections/main-cart.liquid` |
| `.contact-section` | `.contact-section` | `sections/contact-form.liquid` |
| `.story-hero` (your-story) | `.story-form-section` | `sections/story-form.liquid` |
| `.community-stories` | `.story-grid-section` | `sections/story-grid.liquid` |
| `.quote-highlight` | `.quote-highlight` | `sections/quote-highlight.liquid` |

- [ ] **Step 4: Commit**

```bash
git add .agents/skills/visual-qa/scripts/scaffold_mappings.py .agents/skills/visual-qa/config/page-mappings.json
git commit -m "feat(visual-qa): add scaffold mappings script and initial config"
```

---

## Task 8: Implement `--image-diff` and `--svg-compare` flags

**Files:**
- Modify: `.agents/skills/visual-qa/scripts/audit.py`

The core audit loop (Task 6) accepts these flags but defers their implementation to this task. This keeps the core pipeline simple and testable first.

- [ ] **Step 1: Add image diff logic to `audit_page`**

Inside the viewport loop in `audit_page`, after the main style diff, add:

```python
# --- Image diff (optional) ---
if image_diff:
    for el in elements:
        mockup_ctx2 = create_browser_context(browser, vp_width)
        mp = mockup_ctx2.new_page()
        navigate_to_page(mp, f"{mockup_base_url}/{mockup_file}")
        mockup_img = extract_image_info(mp, el.get("mockup", ""))
        mockup_ctx2.close()

        theme_ctx2 = create_browser_context(browser, vp_width)
        tp = theme_ctx2.new_page()
        navigate_to_page(tp, f"{theme_base_url}{theme_path}", password=store_password)
        theme_img = extract_image_info(tp, el.get("theme", ""))
        theme_ctx2.close()

        if mockup_img and theme_img:
            # Compare aspect ratios
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
```

- [ ] **Step 2: Add SVG compare logic to `audit_page`**

```python
# --- SVG compare (optional) ---
if svg_compare:
    for el in elements:
        mockup_ctx3 = create_browser_context(browser, vp_width)
        mp = mockup_ctx3.new_page()
        navigate_to_page(mp, f"{mockup_base_url}/{mockup_file}")
        mockup_svg = extract_svg_info(mp, el.get("mockup", ""))
        mockup_ctx3.close()

        theme_ctx3 = create_browser_context(browser, vp_width)
        tp = theme_ctx3.new_page()
        navigate_to_page(tp, f"{theme_base_url}{theme_path}", password=store_password)
        theme_svg = extract_svg_info(tp, el.get("theme", ""))
        theme_ctx3.close()

        if mockup_svg and theme_svg:
            if mockup_svg["pathData"] != theme_svg["pathData"]:
                all_diffs.append(StyleDiff(
                    element_name=el["name"],
                    element_selector=el.get("theme", ""),
                    property="svg-paths",
                    category="Icons & SVGs",
                    expected=f"{len(mockup_svg['pathData'])} paths",
                    actual=f"{len(theme_svg['pathData'])} paths (content differs)",
                    severity="Notable",
                    viewport=vp_width,
                    section_name=sec_name,
                ))
```

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/visual-qa/scripts/audit.py
git commit -m "feat(visual-qa): implement --image-diff and --svg-compare flags"
```

---

## Task 9: Integration test — full audit run (renumbered from 8)

**Files:**
- No new files — testing the assembled tool end-to-end

**Prerequisites:** Shopify dev server running (`cd theme && shopify theme dev --store=scentsbysara-dev.myshopify.com`)

- [ ] **Step 1: Run dry-run to validate config**

Run: `python .agents/skills/visual-qa/scripts/audit.py --dry-run`
Expected: Lists all pages and sections from config, no errors.

- [ ] **Step 2: Run single-section audit**

Run: `python .agents/skills/visual-qa/scripts/audit.py --page homepage --section "Hero Slideshow" --tolerance 2 --password ahttey`
Expected: Completes without errors, generates report at `docs/qa-reports/visual-qa-homepage-*.md`

- [ ] **Step 3: Verify report content**

Read the generated report and verify:
- Summary counts are present
- Tables have correct columns (Element, Property, Expected, Actual, Severity)
- Screenshots exist in `docs/qa-reports/screenshots/`
- Theme file references are correct

- [ ] **Step 4: Run full-page audit**

Run: `python .agents/skills/visual-qa/scripts/audit.py --page homepage --password ahttey`
Expected: All homepage sections audited at 4 core viewports.

- [ ] **Step 5: Fix any bugs found during integration testing**

Debug and fix any issues with:
- Selector not found errors (update config or extraction logic)
- Timeout issues (increase wait times)
- Screenshot failures (check selector visibility)
- Report formatting issues

- [ ] **Step 6: Commit any bug fixes**

```bash
git add -u .agents/skills/visual-qa/
git commit -m "fix(visual-qa): integration test fixes"
```

---

## Task 10: Clean up replaced skills

**Files:**
- Delete: `.agents/skills/match-design/` (entire directory)
- Delete: `.agents/skills/pixel-perfect/` (entire directory)

- [ ] **Step 1: Verify visual-qa is working before deleting old skills**

Run: `python .agents/skills/visual-qa/scripts/audit.py --dry-run`
Expected: Works correctly.

- [ ] **Step 2: Delete old skills**

```bash
rm -rf .agents/skills/match-design/
rm -rf .agents/skills/pixel-perfect/
```

- [ ] **Step 3: Commit**

```bash
git add -A .agents/skills/match-design/ .agents/skills/pixel-perfect/
git commit -m "chore: remove match-design and pixel-perfect skills (replaced by visual-qa)"
```

---

## Task Dependency Graph

```
Task 1 (skeleton) ──┐
                     ├── Task 3 (extract) ──┐
Task 2 (server) ────┤                       ├── Task 6 (audit.py) ── Task 8 (image/svg) ── Task 9 (integration) ── Task 10 (cleanup)
                     ├── Task 4 (diff) ─────┤
                     └── Task 5 (report) ───┘
Task 7 (scaffold) ──────────────────────────┘
```

Tasks 1-5 and 7 can be parallelised. Task 6 depends on all of them. Tasks 8-10 are sequential.
