"""Compare extracted CSS styles and classify differences by severity."""

import re
from dataclasses import dataclass, field


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


COLOR_PROPERTIES = {
    "color", "background-color",
    "border-top-color", "border-right-color", "border-bottom-color", "border-left-color",
    "fill", "stroke",
}

NUMERIC_PROPERTIES = {
    "font-size", "font-weight", "line-height", "letter-spacing",
    "width", "height", "min-width", "max-width", "min-height", "max-height",
    "padding-top", "padding-right", "padding-bottom", "padding-left",
    "margin-top", "margin-right", "margin-bottom", "margin-left",
    "border-top-width", "border-right-width", "border-bottom-width", "border-left-width",
    "border-top-left-radius", "border-top-right-radius",
    "border-bottom-left-radius", "border-bottom-right-radius",
    "gap", "top", "right", "bottom", "left", "opacity",
    "flex-grow", "flex-shrink", "z-index", "aspect-ratio",
}

PROPERTY_CATEGORIES = {
    "Typography": {
        "font-family", "font-size", "font-weight", "font-style",
        "line-height", "letter-spacing", "text-transform",
        "color", "text-align", "text-decoration", "text-overflow", "white-space",
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
        "box-shadow", "aspect-ratio",
    },
    "Layout & Positioning": {
        "display", "flex-direction", "justify-content", "align-items", "gap",
        "flex-wrap", "flex-grow", "flex-shrink", "flex-basis",
        "grid-template-columns", "grid-template-rows",
        "position", "top", "right", "bottom", "left",
        "overflow", "overflow-x", "overflow-y", "z-index",
    },
    "Images": {
        "object-fit", "object-position",
    },
    "Icons & SVGs": {
        "fill", "stroke",
    },
    "Backgrounds & Visual": {
        "background-color", "background-image",
        "background-size", "background-position", "background-repeat",
        "opacity", "transform", "visibility",
    },
}


def _parse_rgb(value: str) -> tuple[int, int, int] | None:
    """Parse rgb(r,g,b) or hex color into (r, g, b)."""
    match = re.match(r"rgba?\(\s*(\d+),\s*(\d+),\s*(\d+)", value)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
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
    return None


def _get_category(prop: str) -> str:
    """Get the report category for a CSS property."""
    for category, props in PROPERTY_CATEGORIES.items():
        if prop in props:
            return category
    return "Other"


def classify_color_diff(expected: str, actual: str) -> tuple[str, float]:
    """Classify a color difference. Returns (severity, max_channel_diff)."""
    rgb_expected = _parse_rgb(expected)
    rgb_actual = _parse_rgb(actual)

    if rgb_expected is None or rgb_actual is None:
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


def classify_numeric_diff(expected: str, actual: str, tolerance: float) -> tuple[str, float]:
    """Classify a numeric difference. Returns (severity, diff_value)."""
    val_expected = _parse_numeric(expected)
    val_actual = _parse_numeric(actual)

    if val_expected is None or val_actual is None:
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
    """Compare styles for one element. Returns list of StyleDiff for each property that differs."""
    diffs = []

    for prop, expected in mockup_styles.items():
        actual = theme_styles.get(prop, "")
        category = _get_category(prop)

        if prop in COLOR_PROPERTIES:
            severity, _ = classify_color_diff(expected, actual)
        elif prop in NUMERIC_PROPERTIES:
            severity, _ = classify_numeric_diff(expected, actual, tolerance)
        else:
            severity = classify_nonnumeric_diff(expected, actual)

        if severity:
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
    """Compare extracted styles for all elements in a section."""
    all_diffs = []

    if len(mockup_results) != len(theme_results):
        # Log a warning — results may be mismatched
        import warnings
        warnings.warn(
            f"diff_sections: mockup has {len(mockup_results)} elements but theme has {len(theme_results)}. "
            "Trailing elements will be ignored. Check your page-mappings.json config.",
            stacklevel=2,
        )

    for mockup_el, theme_el in zip(mockup_results, theme_results):
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
            element_selector=theme_el["selector"],
            mockup_styles=mockup_el["styles"],
            theme_styles=theme_el["styles"],
            tolerance=tolerance,
            viewport=viewport,
        )
        all_diffs.extend(element_diffs)

    return all_diffs
