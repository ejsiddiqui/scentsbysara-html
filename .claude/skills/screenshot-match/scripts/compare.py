"""Parsing and data structures for screenshot comparison results.

The visual comparison itself is performed by Claude Code reading both images
directly — no external API call needed.
"""

import re
from dataclasses import dataclass


UNCERTAINTY_MARKERS = [
    "appears to be", "possibly", "unclear", "hard to tell",
    "difficult to determine", "seems like", "might be",
]

CATEGORIES = ["Typography", "Spacing & Layout", "Colors & Backgrounds", "Components & Sizing"]


@dataclass
class Issue:
    element: str
    property: str
    expected: str
    actual: str
    severity: str
    category: str


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
    """Parse Markdown category headers and table rows into Issue objects."""
    issues = []
    current_category = None

    for line in text.splitlines():
        stripped = line.strip()
        for cat in CATEGORIES:
            if stripped.startswith("##") and cat.lower() in stripped.lower():
                current_category = cat
                break

        if stripped.startswith("|") and current_category:
            parts = [p.strip() for p in stripped.split("|")[1:-1]]
            if len(parts) != 5:
                continue
            element, prop, expected, actual, severity = parts
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
