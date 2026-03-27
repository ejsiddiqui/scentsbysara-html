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
