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
