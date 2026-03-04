# Spacing System Guidelines

This document provides the foundational math for spatial relationships on the Scents by Sara frontend.

## 1. Absolute Token Usage
To achieve Pixel Perfect status, "magic numbers" (`27px`, `19px`) are strictly forbidden. The layout is managed via an 8-point base scale mapped to CSS variables.

### The Foundation Scale
- `--space-xs`: `4px` (`0.25rem`) -> Input padding modifiers, icon gaps.
- `--space-sm`: `8px` (`0.5rem`) -> Minor text clustering, button internal gaps.
- `--space-md`: `16px` (`1rem`) -> Standard grid gaps, paragraph separations.
- `--space-lg`: `32px` (`2rem`) -> Subsection boundaries, complex element separation.
- `--space-xl`: `64px` (`4rem`) -> Major structural padding, grid gutter defaults.
- `--space-2xl`: `96px` (`6rem`) -> Standard section vertical padding on Desktop.
- `--space-3xl`: `128px` (`8rem`) -> Massive hero whitespace breathing room.

## 2. Bounding Constraints & The 100px Rule
- On desktops larger than `1024px`, the bounding gutter on the left and right sides of the UI MUST equal `100px`.
- CSS variable: `--gutter-desk: 100px;`
- This is the single most important rule for the horizontal "frame" of the editorial look.
- On smaller viewports, it scales to `48px` (tablet) and `20px` (mobile).

## 3. Top-Bottom Padding Logic
A common mistake in beginner layouts is inconsistent vertical rhythm.
- Standard sections: `padding: var(--space-2xl) 0;` (e.g., The best-sellers section).
- Dense sections: `padding: var(--space-xl) 0;`
- The top and bottom padding should always be mirror-symmetrical unless an overlapping design logic is specifically mandated by the reference.
