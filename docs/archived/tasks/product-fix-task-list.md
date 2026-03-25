# Product Page Fix Task List

## Objective
Bring `product.html` in line with `references/product-page/*` while preserving shared homepage header/footer patterns.

## Tasks
- [x] P1: Replace PDP hero gallery imagery and thumbnail sources with isolated candle renders; retune gallery sizing/fit.
- [x] P1: Rebuild the scents section visuals and spacing to match the reference composition and height.
- [x] P1: Rework “You may also like” cards to reference-specific layout (`SHOP NOW`, pricing treatment, card background behavior).
- [x] P1: Replace testimonial slider block with a dedicated multi-row reviews section.
- [x] P2: Tighten commitment section spacing/typography scale to match reference rhythm.
- [x] P2: Remove/adjust style collisions causing review-heading overlap near section boundaries.
- [x] P2: Remove inline style overrides in product markup where CSS class rules should own layout.
- [x] P3: Re-run desktop section captures and viewport sweep; attach updated QA evidence under `docs/tasks/product-qa/`.

## Acceptance Criteria
- Section-by-section captures are visually aligned to `1-product` through `5-reviews`.
- No console errors.
- No horizontal overflow at `1920`, `1440`, `1024`, `768`, `390`, `375`.
- Product interactions still work: thumbnail swap, selectors, quantity, add-to-bag.
