# Footer Design

Date: 2026-03-28
Status: Approved

## Goal

Bring the Shopify footer in line with the HTML mockup at `1440px`, `1024px`, `768px`, `390px`, and `375px`, while keeping Shopify-native payment badges.

## Constraints

- Keep payment icons native to Shopify.
- Use the available mockup social icon assets from `html/assets/icons`.
- Do not change files in `html/`; they remain the design reference.
- Keep the footer as a Shopify section with existing menu settings and newsletter form behavior.

## Chosen Approach

Use the existing `theme/sections/footer.liquid` section and restyle/restructure it just enough to match the mockup. Replace the current inline social SVGs with the exact icon assets from the HTML reference. Preserve the existing footer settings, menu assignments, accordion behavior, and Shopify payment rendering.

## Why This Approach

- Lowest risk: no need to rebuild the footer section from scratch.
- Keeps theme editor compatibility intact.
- Solves the reported gaps directly: icon shape mismatch, spacing, typography, brand row, and responsive layout.
- Allows verification against the existing visual QA workflow and targeted Playwright captures.

## Required Changes

### Social Icons

- Replace inline SVG social icons with image assets from `html/assets/icons`.
- Ensure icon colour and shape match the mockup.
- Keep links conditional on Shopify social URLs being configured.
- Match mobile and desktop icon sizing and spacing.

### Newsletter Block

- Match heading typography to the mockup.
- Match input/button sizing and spacing.
- Keep accessibility label and newsletter form behavior intact.

### Menu Columns

- Match desktop menu heading styling and divider treatment.
- Keep accordion behavior on smaller breakpoints.
- Tighten vertical spacing on mobile.

### Brand and Bottom Row

- Restore the desktop wordmark display and match bottom-row layout.
- Keep the mobile symbol mark.
- Match copyright positioning and styling as closely as possible.
- Retain Shopify-native payment badges on desktop/tablet and hide them on mobile to match the mockup behavior.

### Responsive Rules

- `1440px` and `1024px`: desktop layout with visible socials and brand wordmark.
- `768px`: tablet layout should be expanded and branded, closer to the mockup rather than the current collapsed mobile treatment.
- `390px` and `375px`: mobile accordion layout with tighter spacing and corrected bottom alignment.

## Verification Strategy

- Add a focused footer verification script using Playwright that checks:
  - social icons render
  - desktop logo renders above mobile breakpoint
  - mobile logo renders at mobile breakpoint
  - footer proportions and key elements are within target ranges
- Run `shopify theme check`.
- Capture fresh footer screenshots at `1440px`, `1024px`, `768px`, `390px`, and `375px`.

