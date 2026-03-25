# Website QA Task List (All Pages)

## Scope
- Audited pages: `index.html`, `shop.html`, `product.html`, `checkout.html`, `cart.html`, `your-story.html`, `our-story.html`, `contact.html`
- Strategy: shared/repeating sections are listed once under **Shared Tasks** and referenced from each page

## Superseding Layout Contract (Authoritative)
These directives supersede conflicting older notes in task/review docs:
- `references/sections/` is the authoritative `1920px` design baseline.
- Add and enforce a `1920px` wide desktop breakpoint.
- For viewports above `1920px`, use boxed centered layout.
- Layout structure is section rows.
- Section baseline width is `1920px` while still allowing `width: 100%`.
- Default container width is `1800px` (`60px` left/right space inside 1920 section).
- `.container-full` is `100%` width with no side margins.

## Shared Tasks (Define Once, Reuse Everywhere)

- [x] **SHARED-010 (Critical): Implement the 1920 baseline + boxed-above-1920 layout contract**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHARED-010/
  - Date: 2026-03-01
  - Affects: all pages
  - Expected: section-row architecture with `1920` baseline, `1800` default container, `60px` side spacing, boxed behavior above 1920, and `.container-full` full-bleed behavior.
  - Actual: mixed/legacy sizing rules across docs and implementation cause inconsistent widths and gutters.
  - Fix: normalize layout tokens/utilities and section/container patterns to this contract before page-level polish.

- [x] **SHARED-011 (High): Re-anchor responsive behavior from 1920 references**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHARED-011/
  - Date: 2026-03-01
  - Affects: all pages
  - Expected: 1440/1024/768/375 are responsive adaptations of 1920 reference sections.
  - Actual: several adaptations appear tuned independently, causing drift from the 1920 baseline.
  - Fix: recalibrate responsive rules from the 1920 source first, then re-validate each page.

- [x] **SHARED-001 (High): Mobile menu overlay remains interactive/focusable while closed**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHARED-001/
  - Date: 2026-03-01
  - Affects: `index`, `shop`, `product`, `checkout`, `cart`, `your-story`, `our-story`, `contact`
  - Expected: closed off-canvas nav is inert and excluded from focus/AT tree
  - Actual: hidden mobile controls are still discoverable/focusable
  - Fix: add closed-state `inert` + `aria-hidden="true"` + `pointer-events:none`; enable only on open

- [x] **SHARED-002 (High): Shared header visual system mismatches references**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHARED-002/
  - Date: 2026-03-01
  - Affects: `index`, `shop`, `product`, `checkout`, `cart`
  - Expected: header height/scale/nav spacing match target references
  - Actual: compressed logo/nav rhythm; inconsistent structure (including extra nav item drift)
  - Fix: normalize shared header tokens (height, gaps, type scale, icon spacing) and nav schema

- [x] **SHARED-003 (Medium): Shared footer scale and spacing are off**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHARED-003/
  - Date: 2026-03-01
  - Affects: `index`, `shop`, `product`, `checkout`, `cart`, `your-story`, `our-story`, `contact`
  - Expected: footer hierarchy and spacing match reference rhythm
  - Actual: denser footer typography/spacing and icon sizing mismatch
  - Fix: retune shared footer type scale, vertical spacing, and icon dimensions

- [x] **SHARED-004 (High): Account/Wishlist header actions point to `#`**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHARED-004/
  - Date: 2026-03-01
  - Affects: all pages using shared header controls
  - Expected: valid routes/flows or hidden placeholders
  - Actual: click results in hash-only navigation (`#`)
  - Fix: wire real destinations or remove until implemented

- [x] **SHARED-005 (Medium): Shared surfaces use hardcoded pure white instead of tokens**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHARED-005/
  - Date: 2026-03-01
  - Affects: shared header/search/mega-menu surfaces
  - Expected: brand-tokenized neutral backgrounds
  - Actual: hardcoded `#fff/#ffffff`
  - Fix: replace raw hex with semantic tokens from design system

- [x] **SHARED-006 (High): Mobile horizontal overflow on key shared layouts**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHARED-006/
  - Date: 2026-03-01
  - Affects: `index`, `cart`, story-family pages
  - Expected: no horizontal scrolling at mobile widths (`375px`, `390px`)
  - Actual: overflow present from header/hero/off-canvas and table layouts
  - Fix: tighten mobile breakpoints and width constraints; ensure off-canvas does not affect scroll width

- [x] **SHARED-007 (Medium): External links with `target="_blank"` missing `rel` hardening**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHARED-007/
  - Date: 2026-03-01
  - Affects: footer social links across pages
  - Expected: `rel="noopener noreferrer"`
  - Actual: missing `rel`
  - Fix: add secure `rel` on all `_blank` links

- [x] **SHARED-008 (High): Shared product-card visual baseline is inconsistent**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHARED-008/
  - Date: 2026-03-01
  - Affects: `index` best-sellers, `shop`, `product` related products
  - Expected: consistent card imagery treatment, text hierarchy, and pricing style
  - Actual: card styles and media treatment drift by page
  - Fix: define one shared product-card variant set and use it everywhere

- [x] **SHARED-009 (Medium): Shared product CTA behavior is non-functional as cart flow**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHARED-009/
  - Date: 2026-03-01
  - Affects: `shop`, `index`, `product` related
  - Expected: CTA should navigate or persist cart state
  - Actual: temporary label change with no durable cart update in shared flows
  - Fix: wire CTAs into cart state/navigation contract

## Page-Specific Tasks

### `index.html`
- Uses shared tasks: `SHARED-001`, `SHARED-002`, `SHARED-003`, `SHARED-006`, `SHARED-007`, `SHARED-008`
- [x] **IDX-001 (Critical): Remove QA overlay tooling from production**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/IDX-001/
  - Date: 2026-03-01
  - Actual: `assets/js/qa-overlay.js` is loaded and renders a visible debug button
- [x] **IDX-002 (High): Match section heights to homepage section references**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/IDX-002/
  - Date: 2026-03-01
  - Current vs reference at 1920: announcement `38/73`, header `94/207`, hero `700/958`, best-sellers `935/1074`, collections `1431/1742`, story split `700/1260`, testimonials `557/686`, footer `669/849`
- [x] **IDX-003 (High): Announcement bar misses right-side currency icon and correct typography rhythm**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/IDX-003/
  - Date: 2026-03-01
- [x] **IDX-004 (High): Header treatment does not match dark reference composition**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/IDX-004/
  - Date: 2026-03-01
- [x] **IDX-005 (High): Best-sellers section theme/content differs strongly from `4-best-seller.png`**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/IDX-005/
  - Date: 2026-03-01
- [x] **IDX-006 (High): Collections section theme/title taxonomy differs from `6-collections.png`**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/IDX-006/
  - Date: 2026-03-01

### `shop.html`
- Uses shared tasks: `SHARED-001`, `SHARED-002`, `SHARED-003`, `SHARED-008`, `SHARED-009`
- [x] **SHOP-001 (High): Missing framed composition/right rail from `shop-page.png`**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHOP-001/
  - Date: 2026-03-01
- [x] **SHOP-002 (Medium): Filter and sort controls are non-semantic clickable `div`s**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHOP-002/
  - Date: 2026-03-01
- [x] **SHOP-003 (Low): Sort label/copy density differs from reference**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/SHOP-003/
  - Date: 2026-03-01

### `product.html`
- Uses shared tasks: `SHARED-001`, `SHARED-002`, `SHARED-003`, `SHARED-008`
- [x] **PDP-001 (High): Product hero/gallery composition diverges from `product-page.png`**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/PDP-001/
  - Date: 2026-03-01
- [x] **PDP-002 (High): Right-side vertical ribbons are missing**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/PDP-002/
  - Date: 2026-03-01
- [x] **PDP-003 (Medium): `SCENTS` cards art direction/spacing differ from reference**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/PDP-003/
  - Date: 2026-03-01
- [x] **PDP-004 (High): Selected variant state does not carry into cart line item**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/PDP-004/
  - Date: 2026-03-01
- [x] **PDP-005 (Medium): Colour label does not update when swatches change**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/PDP-005/
  - Date: 2026-03-01
- [x] **PDP-006 (Medium): Testimonial dots are inert on PDP testimonial block**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/PDP-006/
  - Date: 2026-03-01

### `checkout.html`
- Uses shared tasks: `SHARED-001`, `SHARED-002`, `SHARED-003`
- [x] **CKO-001 (High): Checkout column proportions differ from `checkout-page.png`**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/CKO-001/
  - Date: 2026-03-01
- [x] **CKO-002 (Medium): Order summary line-item mapping/presentation drift**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/CKO-002/
  - Date: 2026-03-01
- [x] **CKO-003 (High): Marketing opt-in checkbox is pre-checked**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/CKO-003/
  - Date: 2026-03-01
- [x] **CKO-004 (High): Submit provides no visible validation feedback on empty/invalid form**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/CKO-004/
  - Date: 2026-03-01
- [x] **CKO-005 (High): Payment fields accept invalid formats without enforcement**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/CKO-005/
  - Date: 2026-03-01
- [x] **CKO-006 (Medium): Checkout flow includes heavy global footer/newsletter instead of focused checkout layout**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/CKO-006/
  - Date: 2026-03-01

### `cart.html`
- Uses shared tasks: `SHARED-002`, `SHARED-003`, `SHARED-004`, `SHARED-005`, `SHARED-006`
- [x] **CART-001 (Critical): Quantity controls do not update line totals/subtotal**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/CART-001/
  - Date: 2026-03-01
- [x] **CART-002 (High): Remove action does not remove items or recompute totals**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/CART-002/
  - Date: 2026-03-01
- [x] **CART-003 (High): Cart table breaks on mobile; requires stacked responsive cart layout**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/CART-003/
  - Date: 2026-03-01

### `your-story.html`
- Uses shared tasks: `SHARED-001`, `SHARED-003`, `SHARED-006`
- [x] **YS-001 (Medium): Story form lacks robust submission flow/validation (shared with cloned pages)**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/YS-001/
  - Date: 2026-03-01

### `our-story.html`
- Uses shared tasks: `SHARED-001`, `SHARED-003`, `SHARED-006`
- [x] **OUR-001 (Critical): Page content is cloned from `your-story` instead of dedicated Our Story content**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/OUR-001/
  - Date: 2026-03-01
- [x] **OUR-002 (High): Metadata/styling are not Our Story specific (title and stylesheet mismatch)**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/OUR-002/
  - Date: 2026-03-01

### `contact.html`
- Uses shared tasks: `SHARED-001`, `SHARED-003`, `SHARED-006`
- [x] **CONTACT-001 (Critical): Page content is cloned from `your-story` instead of contact experience**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/CONTACT-001/
  - Date: 2026-03-01
- [x] **CONTACT-002 (High): Metadata/styling are not Contact specific (title and stylesheet mismatch)**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/CONTACT-002/
  - Date: 2026-03-01

### Cross-Page Critical
- [x] **TPL-001 (Critical): `your-story.html`, `our-story.html`, and `contact.html` are byte-identical templates**
  - Completion: Implemented and validated with agent-browser QA artifacts.
  - Evidence: docs/qa/implementation/TPL-001/
  - Date: 2026-03-01
  - Expected: distinct templates and content per route
  - Actual: identical HTML and identical rendered screenshots across all three routes
  - Fix: split into dedicated page templates and route-specific content modules

## Evidence Paths
- Index: `docs/qa/index/`
- Shop: `docs/qa/shop/`
- Product: `docs/qa/product/`
- Checkout: `docs/qa/checkout/`
- Cart: `docs/qa/cart/`
- Your Story: `docs/qa/your-story/`
- Our Story: `docs/qa/our-story/`
- Contact: `docs/qa/contact/`
