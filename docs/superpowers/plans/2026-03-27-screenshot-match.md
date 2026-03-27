# Screenshot Match Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a new `screenshot-match` agent skill that compares manually-exported Figma PNGs against the live Shopify theme using Claude Vision API, producing actionable Markdown QA reports.

**Architecture:** A Python CLI (`audit.py`) orchestrates the workflow: captures a Playwright screenshot of the live theme, sends both the Figma PNG and theme screenshot to Claude Vision API, parses the structured response into issues, optionally asks the user clarifying questions if the AI is uncertain, then generates a Markdown report. Config is a JSON file mapping Figma PNG filenames to theme URLs with design hints.

**Tech Stack:** Python 3.10+, Playwright (sync API), Anthropic Python SDK (`anthropic>=0.25.0`), Pillow (optional, for image copying), pytest

**Spec:** `docs/superpowers/specs/2026-03-27-screenshot-match-design.md`

---

## File Structure

```
.agents/skills/screenshot-match/
├── SKILL.md                        — Skill instructions for AI agents
├── config/
│   └── page-mappings.json          — Pages config: figma image → theme URL + hints
├── scripts/
│   ├── audit.py                    — CLI entry point & orchestrator
│   ├── capture_theme.py            — Playwright screenshot capture of live theme
│   ├── compare.py                  — Claude Vision API call + response parsing
│   ├── report.py                   — Markdown report generator
│   └── requirements.txt            — Python dependencies
└── tests/
    ├── test_compare.py             — Unit tests for parse_issues, detect_uncertainties
    └── test_report.py              — Unit tests for generate_report, save_report
```

---

## Task 1: Skill skeleton (SKILL.md, requirements.txt, config)

**Files:**
- Create: `.agents/skills/screenshot-match/SKILL.md`
- Create: `.agents/skills/screenshot-match/scripts/requirements.txt`
- Create: `.agents/skills/screenshot-match/config/page-mappings.json`

- [ ] **Step 1: Create `requirements.txt`**

```
playwright>=1.40.0
anthropic>=0.25.0
Pillow>=10.0.0
```

- [ ] **Step 2: Create `config/page-mappings.json`**

```json
{
  "defaults": {
    "themeBaseUrl": "http://127.0.0.1:9292",
    "figmaDir": "figma-exports",
    "storePassword": "",
    "hints": {
      "fontFamilies": ["Cormorant Garamond", "Jost"],
      "brandColors": ["#1a1a1a", "#f5f0eb", "#c9a96e"],
      "notes": ""
    }
  },
  "pages": [
    {
      "name": "Homepage",
      "figmaImage": "homepage-1440.png",
      "themeUrl": "/",
      "viewport": 1440
    }
  ]
}
```

- [ ] **Step 3: Create `SKILL.md`**

```markdown
---
name: screenshot-match
description: Visual QA audit comparing Figma PNG exports against live Shopify theme using Claude Vision API. Use when asked to compare, audit, or verify visual fidelity between Figma designs and the live theme. Produces actionable Markdown reports (Critical/Notable/Marginal) covering typography, spacing, colors, and layout.
---

# Screenshot Match Skill

Compare Figma design exports against the live Shopify theme using Claude Vision API.

## Prerequisites

Install dependencies (one-time):
```bash
pip install -r .agents/skills/screenshot-match/scripts/requirements.txt
playwright install chromium
```

Set API key:
```bash
export ANTHROPIC_API_KEY=sk-...
```

Ensure the Shopify dev server is running:
```bash
cd theme && shopify theme dev --store=scentsbysara-dev.myshopify.com
```

## Quick Start

```bash
# Audit all configured pages
python .agents/skills/screenshot-match/scripts/audit.py

# Audit specific page
python .agents/skills/screenshot-match/scripts/audit.py --page homepage

# Skip interactive questions (use hints only)
python .agents/skills/screenshot-match/scripts/audit.py --no-interactive

# Dry run (validate config, no browser/API)
python .agents/skills/screenshot-match/scripts/audit.py --dry-run
```

## CLI Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--page <name>` | all | Audit specific page (name from config) |
| `--url <url>` | from config | Override Shopify dev server URL |
| `--password <pwd>` | from config | Shopify store password |
| `--no-interactive` | off | Skip clarifying questions, use hints only |
| `--output <path>` | `docs/qa-reports/` | Report output directory |
| `--dry-run` | off | Validate config and list pages, no browser/API |

## Setup

1. Export Figma frames as PNGs → drop into `figma-exports/` (repo root)
2. Add page entries to `.agents/skills/screenshot-match/config/page-mappings.json`
3. Set `ANTHROPIC_API_KEY` environment variable
4. Run the audit

## Workflow

1. Run audit → report at `docs/qa-reports/screenshot-match-<page>-<datetime>.md`
2. Answer any clarifying questions if prompted
3. Review report → pass to Claude or Codex to fix issues
4. Re-run to verify fixes

## Severity Levels

| Severity | Meaning |
|----------|---------|
| Critical | Wrong font-family, color channel diff >20, size diff >16px, missing element |
| Notable | Size diff 8–16px, color channel diff 10–20, layout misalignment |
| Marginal | Subtle diff within acceptable tolerance |
```

- [ ] **Step 4: Install dependencies**

Run: `pip install -r .agents/skills/screenshot-match/scripts/requirements.txt && playwright install chromium`
Expected: Dependencies install without errors.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/screenshot-match/SKILL.md .agents/skills/screenshot-match/scripts/requirements.txt .agents/skills/screenshot-match/config/page-mappings.json
git commit -m "feat(screenshot-match): add skill skeleton, config, and dependencies"
```

---

## Task 2: Theme screenshot capture (`capture_theme.py`)

**Files:**
- Create: `.agents/skills/screenshot-match/scripts/capture_theme.py`

- [ ] **Step 1: Create `capture_theme.py`**

```python
"""Capture a full-page screenshot of the live Shopify theme using Playwright."""

import os
from playwright.sync_api import Browser, Page


UNLOCK_SELECTOR = 'input[type="password"]'
UNLOCK_SUBMIT = 'button[type="submit"]'


def _unlock_store(page: Page, password: str) -> None:
    """Unlock a password-protected Shopify dev store if the password gate appears."""
    if page.query_selector(UNLOCK_SELECTOR):
        page.fill(UNLOCK_SELECTOR, password)
        page.click(UNLOCK_SUBMIT)
        page.wait_for_load_state("domcontentloaded")


def capture_theme_screenshot(
    browser: Browser,
    url: str,
    viewport_width: int,
    output_path: str,
    password: str | None = None,
) -> str:
    """
    Open the theme URL in Playwright, capture a full-page screenshot.
    Returns the path to the saved screenshot.
    """
    context = browser.new_context(viewport={"width": viewport_width, "height": 900})
    page = context.new_page()
    try:
        page.goto(url, wait_until="domcontentloaded")
        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass  # networkidle timeout is acceptable on complex pages
        if password:
            _unlock_store(page, password)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        page.screenshot(path=output_path, full_page=True)
        return output_path
    finally:
        context.close()
```

- [ ] **Step 2: Commit**

```bash
git add .agents/skills/screenshot-match/scripts/capture_theme.py
git commit -m "feat(screenshot-match): add Playwright theme screenshot capture"
```

---

## Task 3: Claude Vision comparison (`compare.py`) + unit tests

**Files:**
- Create: `.agents/skills/screenshot-match/scripts/compare.py`
- Create: `.agents/skills/screenshot-match/tests/test_compare.py`

- [ ] **Step 1: Write failing tests for `parse_issues` and `detect_uncertainties`**

Create `.agents/skills/screenshot-match/tests/test_compare.py`:

```python
"""Unit tests for compare.py — parse_issues, detect_uncertainties, build_hints_text."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from compare import parse_issues, detect_uncertainties, build_hints_text, Issue


SAMPLE_RESPONSE = """
## Typography

| Element | Property | Expected (Figma) | Actual (Theme) | Severity |
|---------|----------|-----------------|----------------|----------|
| Hero heading | font-family | Cormorant Garamond | Jost | Critical |
| Body copy | font-size | 16px | 14px | Notable |
| Caption | color | #1a1a1a | #333333 | Marginal |

## Spacing & Layout

| Element | Property | Expected (Figma) | Actual (Theme) | Severity |
|---------|----------|-----------------|----------------|----------|
| Hero section | padding-top | 120px | 80px | Critical |
"""

UNCERTAIN_RESPONSE = """
The font appears to be Cormorant Garamond but it's unclear from the screenshot.
The button color possibly matches the brand color.
The heading size seems correct.
"""


def test_parse_issues_returns_correct_count():
    issues = parse_issues(SAMPLE_RESPONSE)
    assert len(issues) == 4


def test_parse_issues_typography_category():
    issues = parse_issues(SAMPLE_RESPONSE)
    typography = [i for i in issues if i.category == "Typography"]
    assert len(typography) == 3


def test_parse_issues_critical_severity():
    issues = parse_issues(SAMPLE_RESPONSE)
    critical = [i for i in issues if i.severity == "Critical"]
    assert len(critical) == 2


def test_parse_issues_correct_values():
    issues = parse_issues(SAMPLE_RESPONSE)
    hero = next(i for i in issues if i.element == "Hero heading")
    assert hero.property == "font-family"
    assert hero.expected == "Cormorant Garamond"
    assert hero.actual == "Jost"
    assert hero.severity == "Critical"
    assert hero.category == "Typography"


def test_parse_issues_spacing_category():
    issues = parse_issues(SAMPLE_RESPONSE)
    spacing = [i for i in issues if i.category == "Spacing & Layout"]
    assert len(spacing) == 1
    assert spacing[0].element == "Hero section"


def test_parse_issues_empty_response():
    issues = parse_issues("")
    assert issues == []


def test_parse_issues_no_valid_tables():
    issues = parse_issues("Some text with no tables at all.")
    assert issues == []


def test_detect_uncertainties_finds_markers():
    questions = detect_uncertainties(UNCERTAIN_RESPONSE)
    assert len(questions) >= 2


def test_detect_uncertainties_empty():
    questions = detect_uncertainties("The font is Cormorant Garamond. The padding is 120px.")
    assert questions == []


def test_build_hints_text_with_all_fields():
    hints = {
        "fontFamilies": ["Cormorant Garamond", "Jost"],
        "brandColors": ["#1a1a1a", "#f5f0eb"],
        "notes": "Dark mode only",
    }
    text = build_hints_text(hints)
    assert "Cormorant Garamond" in text
    assert "#1a1a1a" in text
    assert "Dark mode only" in text


def test_build_hints_text_empty_hints():
    text = build_hints_text({})
    assert text == ""


def test_build_hints_text_partial_hints():
    hints = {"fontFamilies": ["Jost"]}
    text = build_hints_text(hints)
    assert "Jost" in text
    assert "brandColors" not in text
```

- [ ] **Step 2: Run tests to confirm they fail**

Run: `pytest .agents/skills/screenshot-match/tests/test_compare.py -v`
Expected: `ModuleNotFoundError: No module named 'compare'` (file doesn't exist yet)

- [ ] **Step 3: Create `compare.py`**

```python
"""Compare Figma screenshot vs theme screenshot using Claude Vision API."""

import base64
import re
from dataclasses import dataclass

import anthropic


UNCERTAINTY_MARKERS = [
    "appears to be", "possibly", "unclear", "hard to tell",
    "difficult to determine", "seems like", "might be",
]

CATEGORIES = ["Typography", "Spacing & Layout", "Colors & Backgrounds", "Components & Sizing"]

SYSTEM_PROMPT = """You are a visual QA reviewer comparing a Figma design screenshot against a live website screenshot.

Your job is to identify specific visual differences between the two images.

Output ONLY Markdown tables grouped by these categories (include only categories that have differences):
- Typography
- Spacing & Layout
- Colors & Backgrounds
- Components & Sizing

Each table must have exactly these columns: Element | Property | Expected (Figma) | Actual (Theme) | Severity

Severity rules:
- Critical: wrong font-family, color channel diff >20, size diff >16px, missing element
- Notable: size diff 8-16px, color channel diff 10-20, layout misalignment
- Marginal: subtle diff within acceptable tolerance

Be specific with values. Use px for sizes, hex codes for colors, exact font names.
If you are uncertain about any value, say so explicitly using phrases like "appears to be" or "unclear"."""


@dataclass
class Issue:
    element: str
    property: str
    expected: str
    actual: str
    severity: str
    category: str


def encode_image(path: str) -> str:
    """Base64-encode an image file for the API."""
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def build_hints_text(hints: dict) -> str:
    """Format hints dict into a context string for the prompt."""
    lines = []
    if hints.get("fontFamilies"):
        lines.append(f"Font families used in design: {', '.join(hints['fontFamilies'])}")
    if hints.get("brandColors"):
        lines.append(f"Brand colors: {', '.join(hints['brandColors'])}")
    if hints.get("notes"):
        lines.append(f"Notes: {hints['notes']}")
    return "\n".join(lines)


def parse_issues(text: str) -> list[Issue]:
    """Parse Markdown category headers and table rows from Claude response into Issue objects."""
    issues = []
    current_category = None

    for line in text.splitlines():
        # Detect category section headers (## Typography, ## Spacing & Layout, etc.)
        stripped = line.strip()
        for cat in CATEGORIES:
            if stripped.startswith("##") and cat.lower() in stripped.lower():
                current_category = cat
                break

        # Parse table data rows
        if stripped.startswith("|") and current_category:
            parts = [p.strip() for p in stripped.split("|")[1:-1]]
            if len(parts) != 5:
                continue
            element, prop, expected, actual, severity = parts
            # Skip header row and separator row
            if element in ("Element", "") or set(element) <= {"-", " "}:
                continue
            if severity not in ("Critical", "Notable", "Marginal"):
                continue
            issues.append(Issue(
                element=element,
                property=prop,
                expected=expected,
                actual=actual,
                severity=severity,
                category=current_category,
            ))

    return issues


def detect_uncertainties(text: str) -> list[str]:
    """Return sentences that contain uncertainty markers."""
    sentences = re.split(r"[.!?\n]", text)
    return [
        s.strip()
        for s in sentences
        if s.strip() and any(marker in s.lower() for marker in UNCERTAINTY_MARKERS)
    ]


def compare_screenshots(
    figma_path: str,
    theme_path: str,
    hints: dict,
    client: anthropic.Anthropic,
    extra_context: str = "",
) -> tuple[list[Issue], str]:
    """
    Send both screenshots to Claude Vision API.
    Returns (issues, raw_response_text).
    """
    figma_b64 = encode_image(figma_path)
    theme_b64 = encode_image(theme_path)

    hints_text = build_hints_text(hints)
    user_text = "Compare these two screenshots.\n\n"
    if hints_text:
        user_text += f"Design context:\n{hints_text}\n\n"
    if extra_context:
        user_text += f"Additional context from reviewer:\n{extra_context}\n\n"
    user_text += (
        "First image is the Figma design (expected). "
        "Second image is the live theme (actual).\n"
        "List all visual differences."
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": "image/png", "data": figma_b64},
                    },
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": "image/png", "data": theme_b64},
                    },
                    {"type": "text", "text": user_text},
                ],
            }
        ],
    )

    raw = response.content[0].text
    issues = parse_issues(raw)
    return issues, raw
```

- [ ] **Step 4: Run tests and confirm they pass**

Run: `pytest .agents/skills/screenshot-match/tests/test_compare.py -v`
Expected: All 12 tests pass.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/screenshot-match/scripts/compare.py .agents/skills/screenshot-match/tests/test_compare.py
git commit -m "feat(screenshot-match): add Claude Vision comparison module with unit tests"
```

---

## Task 4: Markdown report generator (`report.py`) + unit tests

**Files:**
- Create: `.agents/skills/screenshot-match/scripts/report.py`
- Create: `.agents/skills/screenshot-match/tests/test_report.py`

- [ ] **Step 1: Write failing tests for `generate_report` and `save_report`**

Create `.agents/skills/screenshot-match/tests/test_report.py`:

```python
"""Unit tests for report.py — generate_report, save_report."""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from compare import Issue
from report import generate_report, save_report


def make_issues():
    return [
        Issue(element="Hero heading", property="font-family", expected="Cormorant Garamond", actual="Jost", severity="Critical", category="Typography"),
        Issue(element="Hero section", property="padding-top", expected="120px", actual="80px", severity="Critical", category="Spacing & Layout"),
        Issue(element="Body copy", property="font-size", expected="16px", actual="14px", severity="Notable", category="Typography"),
        Issue(element="Caption", property="color", expected="#1a1a1a", actual="#333333", severity="Marginal", category="Colors & Backgrounds"),
    ]


def test_generate_report_contains_page_name():
    report = generate_report("Homepage", "figma-exports/homepage-1440.png", "http://127.0.0.1:9292/", 1440, make_issues())
    assert "Homepage" in report


def test_generate_report_summary_counts():
    report = generate_report("Homepage", "figma-exports/homepage-1440.png", "http://127.0.0.1:9292/", 1440, make_issues())
    assert "Critical: 2" in report
    assert "Notable: 1" in report
    assert "Marginal: 1" in report


def test_generate_report_contains_typography_section():
    report = generate_report("Homepage", "figma-exports/homepage-1440.png", "http://127.0.0.1:9292/", 1440, make_issues())
    assert "## Typography" in report
    assert "Cormorant Garamond" in report
    assert "Jost" in report


def test_generate_report_contains_spacing_section():
    report = generate_report("Homepage", "figma-exports/homepage-1440.png", "http://127.0.0.1:9292/", 1440, make_issues())
    assert "## Spacing & Layout" in report
    assert "padding-top" in report


def test_generate_report_no_issues():
    report = generate_report("Homepage", "figma-exports/homepage-1440.png", "http://127.0.0.1:9292/", 1440, [])
    assert "Critical: 0" in report
    assert "No differences detected" in report


def test_generate_report_parse_error():
    report = generate_report(
        "Homepage", "figma-exports/homepage-1440.png", "http://127.0.0.1:9292/", 1440,
        [], raw_response="raw AI text", parse_error=True
    )
    assert "[PARSE ERROR]" in report
    assert "raw AI text" in report


def test_generate_report_skips_empty_categories():
    issues = [
        Issue(element="H1", property="font-size", expected="48px", actual="40px", severity="Notable", category="Typography"),
    ]
    report = generate_report("Homepage", "figma-exports/homepage-1440.png", "http://127.0.0.1:9292/", 1440, issues)
    assert "## Typography" in report
    assert "## Colors & Backgrounds" not in report


def test_save_report_creates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        content = "# Test Report"
        path = save_report(content, "Homepage", tmpdir)
        assert os.path.exists(path)
        assert path.endswith(".md")
        assert "screenshot-match-homepage-" in path


def test_save_report_content_matches():
    with tempfile.TemporaryDirectory() as tmpdir:
        content = "# Test Report\n\nSome content"
        path = save_report(content, "Homepage", tmpdir)
        with open(path, encoding="utf-8") as f:
            assert f.read() == content


def test_save_report_creates_output_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        nested = os.path.join(tmpdir, "nested", "dir")
        path = save_report("content", "Page", nested)
        assert os.path.exists(path)
```

- [ ] **Step 2: Run tests to confirm they fail**

Run: `pytest .agents/skills/screenshot-match/tests/test_report.py -v`
Expected: `ModuleNotFoundError: No module named 'report'`

- [ ] **Step 3: Create `report.py`**

```python
"""Generate Markdown QA reports from screenshot comparison results."""

import os
from datetime import datetime

from compare import Issue


CATEGORIES = ["Typography", "Spacing & Layout", "Colors & Backgrounds", "Components & Sizing"]


def generate_report(
    page_name: str,
    figma_path: str,
    theme_url: str,
    viewport: int,
    issues: list[Issue],
    raw_response: str | None = None,
    parse_error: bool = False,
    figma_screenshot_path: str | None = None,
    theme_screenshot_path: str | None = None,
) -> str:
    """Generate a Markdown report string from a list of issues."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Screenshot Match Report — {page_name} — {now}",
        "",
        f"**Figma source:** {figma_path}",
        f"**Theme URL:** {theme_url}",
        f"**Viewport:** {viewport}px",
        "",
    ]

    if figma_screenshot_path:
        lines.append(f"**Figma screenshot:** {figma_screenshot_path}")
    if theme_screenshot_path:
        lines.append(f"**Theme screenshot:** {theme_screenshot_path}")
    if figma_screenshot_path or theme_screenshot_path:
        lines.append("")

    critical = sum(1 for i in issues if i.severity == "Critical")
    notable = sum(1 for i in issues if i.severity == "Notable")
    marginal = sum(1 for i in issues if i.severity == "Marginal")

    lines += [
        "## Summary",
        f"- Critical: {critical}",
        f"- Notable: {notable}",
        f"- Marginal: {marginal}",
        "",
        "---",
        "",
    ]

    if parse_error:
        lines += [
            "## [PARSE ERROR]",
            "",
            "Claude's response could not be parsed into structured issues. Raw response below:",
            "",
            "```",
            raw_response or "",
            "```",
            "",
        ]
        return "\n".join(lines)

    for cat in CATEGORIES:
        cat_issues = [i for i in issues if i.category == cat]
        if not cat_issues:
            continue
        lines += [
            f"## {cat}",
            "",
            "| Element | Property | Expected (Figma) | Actual (Theme) | Severity |",
            "|---------|----------|-----------------|----------------|----------|",
        ]
        for issue in cat_issues:
            lines.append(
                f"| {issue.element} | {issue.property} | {issue.expected} | {issue.actual} | {issue.severity} |"
            )
        lines.append("")

    if not issues:
        lines.append("_No differences detected._")
        lines.append("")

    return "\n".join(lines)


def save_report(content: str, page_name: str, output_dir: str) -> str:
    """Save report content to disk. Returns the file path."""
    os.makedirs(output_dir, exist_ok=True)
    slug = page_name.lower().replace(" ", "-")
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"screenshot-match-{slug}-{timestamp}.md"
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
```

- [ ] **Step 4: Run tests and confirm they pass**

Run: `pytest .agents/skills/screenshot-match/tests/test_report.py -v`
Expected: All 10 tests pass.

- [ ] **Step 5: Run all tests together**

Run: `pytest .agents/skills/screenshot-match/tests/ -v`
Expected: All 22 tests pass.

- [ ] **Step 6: Commit**

```bash
git add .agents/skills/screenshot-match/scripts/report.py .agents/skills/screenshot-match/tests/test_report.py
git commit -m "feat(screenshot-match): add report generator with unit tests"
```

---

## Task 5: CLI orchestrator (`audit.py`)

**Files:**
- Create: `.agents/skills/screenshot-match/scripts/audit.py`

- [ ] **Step 1: Create `audit.py`**

```python
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
```

- [ ] **Step 2: Run dry-run to verify config validation works**

Run: `python .agents/skills/screenshot-match/scripts/audit.py --dry-run`
Expected output includes:
```
  DRY RUN — Config validation
  Theme URL: http://127.0.0.1:9292
  Figma dir: figma-exports
  ...
  [OK] Config valid. No browser or API calls made.
```

- [ ] **Step 3: Run all tests to confirm nothing broken**

Run: `pytest .agents/skills/screenshot-match/tests/ -v`
Expected: All 22 tests pass.

- [ ] **Step 4: Commit**

```bash
git add .agents/skills/screenshot-match/scripts/audit.py
git commit -m "feat(screenshot-match): add CLI orchestrator with dry-run and interactive questions"
```

---

## Task 6: Integration test

**Files:**
- No new files — testing assembled tool end-to-end

**Prerequisites:**
- Shopify dev server running: `cd theme && shopify theme dev --store=scentsbysara-dev.myshopify.com`
- `ANTHROPIC_API_KEY` set
- At least one Figma PNG in `figma-exports/` matching a config entry

- [ ] **Step 1: Verify dry-run**

Run: `python .agents/skills/screenshot-match/scripts/audit.py --dry-run --page homepage`
Expected: Lists homepage config, prints `[OK] Config valid.`

- [ ] **Step 2: Create a placeholder Figma PNG for smoke test**

If no real Figma PNG is available yet, create a 1440×900 solid-colour placeholder:

```python
# Run this once in a Python shell
from PIL import Image
import os
os.makedirs("figma-exports", exist_ok=True)
img = Image.new("RGB", (1440, 900), color=(245, 240, 235))
img.save("figma-exports/homepage-1440.png")
print("Created figma-exports/homepage-1440.png")
```

- [ ] **Step 3: Run single-page audit**

Run: `python .agents/skills/screenshot-match/scripts/audit.py --page homepage --no-interactive --password ahttey`
Expected:
- Captures theme screenshot
- Calls Claude Vision API
- Saves report to `docs/qa-reports/screenshot-match-homepage-*.md`
- Prints summary: `[C:N N:N M:N]`

- [ ] **Step 4: Verify report content**

Read the generated report and confirm:
- Header contains page name, figma source, theme URL, viewport
- Summary section has Critical/Notable/Marginal counts
- At least one category table is present (or `_No differences detected._`)
- Screenshots listed in report header
- No Python tracebacks in output

- [ ] **Step 5: Fix any bugs found during integration testing**

Common issues to check:
- Image encoding errors (JPEG vs PNG media type) — ensure `media_type` matches actual file format
- Path resolution errors on Windows (use `Path` objects, not string concatenation)
- API timeout (increase `max_tokens` if response is cut off)

- [ ] **Step 6: Commit any fixes**

```bash
git add -u .agents/skills/screenshot-match/
git commit -m "fix(screenshot-match): integration test fixes"
```

---

## Task Dependency Graph

```
Task 1 (skeleton) ──┐
Task 2 (capture) ───┤
Task 3 (compare) ───┼── Task 5 (audit.py) ── Task 6 (integration)
Task 4 (report) ────┘
```

Tasks 1–4 are independent and can be parallelised. Task 5 depends on all of them. Task 6 requires Task 5.
