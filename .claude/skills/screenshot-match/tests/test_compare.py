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
