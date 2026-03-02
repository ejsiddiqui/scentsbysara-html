# Product Page QA Report

## Scope
- Target file: `product.html`
- Reference set: `references/product-page/1-product.png` to `5-reviews.png`
- Current captures: `docs/tasks/product-qa/*-current.png`
- Test date: 2026-03-02

## Evidence Summary
- Section size comparison:
  - `1-product`: ref `1920x1466`, current `1920x1470`
  - `2-scents`: ref `1919x1052`, current `1920x892`
  - `3-our-commitment`: ref `1920x960`, current `1920x1060`
  - `4-you-may-also-like`: ref `1919x873`, current `1920x916`
  - `5-reviews`: ref `1920x1044`, current `1920x570`
- Responsive sweep (`1920/1440/1024/768/390/375`): no console errors, no horizontal overflow (`docs/tasks/product-qa/viewport-report.json`).

## Bugs Found
1. Critical: PDP hero/gallery uses incorrect image treatment for the reference.
- Expected: neutral product-background shots with centered cutout candles and matching thumbnail set.
- Actual: lifestyle bedding image appears as the main PDP image.
- Evidence: `references/product-page/1-product.png` vs `docs/tasks/product-qa/1-product-current.png`.

2. Critical: Scents section does not match visual structure or height.
- Expected: two equal cards with vanilla-stick/lavender backgrounds and taller section (`~1052px`).
- Actual: different imagery, darker overlays, smaller block (`892px`).
- Evidence: `2-scents` reference/current pair.

3. Major: Commitment section typography and spacing hierarchy are off.
- Expected: larger serif headline, tighter content block, balanced right-column rhythm.
- Actual: oversized empty area and compressed text block; section height inflated by ~100px.
- Evidence: `3-our-commitment` reference/current pair.

4. Critical: “You may also like” card system diverges from reference.
- Expected: neutral card backgrounds, product-first composition, `SHOP NOW` CTA style, first card includes struck old price.
- Actual: lifestyle imagery, different card component behavior, `ADD TO BAG` CTA pattern.
- Evidence: `4-you-may-also-like` reference/current pair.

5. Critical: Reviews section is missing; incorrect component is rendered.
- Expected: multi-row review list with reviewer/location, review body, and right-side star rating.
- Actual: homepage testimonial slider component, wrong layout and half expected height.
- Evidence: `5-reviews` reference/current pair.

6. Major: Vertical transition between related-products and reviews is broken.
- Expected: clean section boundary and heading flow.
- Actual: review heading overlaps with preceding card area in captured section.
- Evidence: `docs/tasks/product-qa/5-reviews-current.png`.

## Root Cause Summary
- Shared shop/testimonial components were reused in PDP where dedicated reference-specific sections were required.
- Product asset mapping drifted: PDP hero now references lifestyle product images instead of isolated product renders.
- Section-specific spacing/typography values are not fully aligned to the product reference set.
