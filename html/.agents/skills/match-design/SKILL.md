---
name: match-design
description: Convert a screenshot or wireframe into a pixel-accurate HTML/CSS/JS prototype and report any remaining visual deviations. Use when a user asks to replicate UI from an image, match spacing and alignment exactly, recreate visual hierarchy, or produce a frontend prototype that mirrors a provided reference.
---

# Match Design

Build image-matched frontend prototypes with strict visual comparison and explicit deviation reporting.

## Workflow

1. Read the reference first
- Open the screenshot or wireframe before writing code.
- Record viewport assumptions (desktop width, mobile width, DPR if known).
- If assumptions are missing, infer them conservatively and state them.

2. Audit all visual elements before coding
- Inventory layout structure and all visible elements.
- Capture measurements and relationships:
  - outer margins and section spacing
  - grid/column structure and alignment anchors
  - element widths/heights and aspect ratios
  - typography sizes, line heights, weights, and tracking
  - icon sizes, stroke weight, and padding
  - border radius, borders, shadows, and opacity
  - colors (hex/rgb estimates when exact values are unknown)
- Use `references/visual-audit-template.md` to keep the audit complete.

3. Plan implementation files
- Map each audited area to concrete files to edit.
- Keep structure semantic and maintainable (`index.html`, modular CSS, minimal JS).
- Only then start implementation.

4. Implement pixel-accurate HTML/CSS/JS
- Recreate the visual layout first, then refine micro-details.
- Use CSS custom properties for repeated values (spacing, colors, radii, font sizes).
- Preserve responsive behavior that follows the same visual intent.
- Update all relevant files, not only one stylesheet.

5. Self-review against the reference
- Compare implementation to the source point-by-point:
  - spacing
  - icon scale
  - column alignment
  - text widths and wrapping
  - colors and contrast
  - visual rhythm and hierarchy
- Verify both desktop and mobile states when the reference implies responsive behavior.

6. Report deviations before delivery
- Always list remaining mismatches, even if minor.
- For each deviation, include:
  - what differs
  - where it appears
  - expected vs actual (with numbers when possible)
  - likely fix path

## Operating Rules

- Do not start coding until the visual audit is complete.
- Prefer precise measurements over subjective phrases.
- Keep JS minimal and only for interactions present in the reference.
- If the image is ambiguous or partially cropped, state assumptions explicitly.
- If pixel-perfect parity is impossible (missing assets/fonts), still produce the closest match and document the gap.

## Output Contract

When finishing, present:
1. Files changed
2. What was matched exactly
3. Deviation list (required, can be "none" only after explicit check)

## References

- `references/visual-audit-template.md`: checklist for pre-code visual extraction and post-code comparison.
