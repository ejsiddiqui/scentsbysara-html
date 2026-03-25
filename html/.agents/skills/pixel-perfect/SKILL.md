---
name: pixel-perfect
description: Achieve edge-to-edge pixel-perfect design fidelity across all pages. Use when verifying layout precision, spacing consistency, typography accuracy, color token compliance, and responsive parity against brand guidelines and reference screenshots.
---

# Pixel-Perfect Design

Ensure every page achieves true edge-to-edge, pixel-perfect fidelity to the brand system and reference screenshots.

## Workflow

1. Establish the reference baseline
   - Collect all reference screenshots or design files for the target page.
   - Record the viewport(s) they were captured at (default: 1440px desktop, 375px mobile).
   - Note any ambiguities, crops, or missing states.

2. Full-bleed and edge audit
   - Verify hero images, banners, and background sections extend full-width with zero unintended side gaps.
   - Confirm `max-width: 1440px` container is centered with equal side margins.
   - Check for horizontal overflow or scroll on every breakpoint.
   - Ensure all full-bleed sections have identical left/right alignment anchors.

3. Spacing system verification
   - Every spacing value must come from `tokens.css` or be a documented design variable.
   - Measure section-to-section gaps against the brand spec (generous `py-20` between sections).
   - Verify component internal padding and margin are consistent within and across pages.
   - Check gap values between repeated items (product cards, collection cards, etc.).
   - Flag any hardcoded magic numbers that should be tokenized.

4. Typography precision check
   - **Headings:** RL Limo serif — verify `font-family: rl-limo, sans-serif; font-weight: 400`.
   - **Body/UI:** Suisse Intl — verify `font-family: "Suisse Intl", sans-serif; font-weight: 400`.
   - Measure and compare: font-size, font-weight, line-height, letter-spacing, text-transform.
   - Verify text block max-widths and wrapping behavior match the reference.
   - Check that no fallback or system font is visible (font loading must succeed).

5. Color token compliance
   - Every color in the codebase must resolve to a CSS custom property from `tokens.css`.
   - No raw hex values outside of `tokens.css` `:root` block.
   - Verify key tokens:
     - `--bg-surface: #F9F6F2` (main background — never pure white)
     - `--bg-secondary: #E8E4DD` (cards/sections)
     - `--bg-ink: #2D2B27` (dark accents/footer)
     - `--text-primary: #3F3229` (primary text — never pure black)
     - `--text-muted: #A49483` (secondary text)
     - `--border: #CFC6B9` (dividers/borders)
   - Check gradients, shadows, and overlays for color consistency.

6. Border and radius enforcement
   - `border-radius` must be `0px` everywhere (micro `2px` max is tolerated only if explicitly justified).
   - Scan all CSS files for any `border-radius` value exceeding `2px` — this is a hard failure.
   - Verify button corners are sharp: uppercase text, 14px, `letter-spacing: 0.05em`.
   - Check input fields, cards, modals, and dropdowns — all must be sharp-cornered.

7. Component fidelity check
   - Product cards: image aspect ratio, title/price alignment, CTA placement.
   - Buttons: consistent sizing, padding, text-transform, hover states.
   - Icons: Lucide only, 24px, 1px stroke, color inherits from text.
   - Navigation: proper spacing between items, active/hover states.
   - Footer: column alignment, social icons, payment icons positioning.

8. Responsive parity audit
   - Test at 1440px, 1024px, 768px, 375px.
   - Verify stacking order on mobile matches design intent.
   - Check that touch targets are minimum 44×44px on mobile.
   - Confirm no content is cropped, hidden, or overflowing at any breakpoint.
   - Verify hamburger menu and mobile navigation behavior.

9. Final deviation report
   - Use `references/pixel-audit-checklist.md` for systematic comparison.
   - List every remaining mismatch with:
     - Location (page, section, element)
     - Expected (from reference/brand spec, with measurements)
     - Actual (from implementation, with measurements)
     - Severity (critical / minor / cosmetic)
     - Suggested fix

## Operating Rules

- Do not mark a page as "pixel-perfect" unless every item in the checklist has been verified.
- Use precise measurements (px, rem, %) — avoid subjective terms like "close enough" or "approximately".
- Screenshots from the browser tool at target viewports are the gold standard for verification.
- When the reference is ambiguous, state the assumption and choose the more conservative interpretation.
- All CSS changes must use existing design tokens. Create new tokens only if truly necessary and document why.
- Test with and without cached fonts to ensure font-loading does not cause layout shift.

## Output Contract

When finishing, present:
1. Pages verified (with viewport dimensions)
2. Items matched exactly (with measurements)
3. Deviation list (required — can be "none" only after explicit check of every checklist item)
4. Token changes (if any new CSS custom properties were added/modified)

## References

- `references/pixel-audit-checklist.md`: Page-by-page audit checklist for pixel-level verification.
