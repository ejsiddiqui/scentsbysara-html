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
