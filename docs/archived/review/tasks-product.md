<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# QA Tasks — product.html (Product Detail Page)

## Status: REVIEWED
## Audit Date: 2026-03-01
## Viewport Tested: 1440px | 1024px | 375px
## Method: Code + CSS audit against reference screenshots (product-page.png, product-top.png, sents-section.png, our-commitment-product.png, you-may-like.png)

---

## Section Checklist

### 1. Announcement Bar
- [x] Present — renders as dark mocha bar with correct text "LAUNCHING MARCH 2026 - JOIN THE WAIT LIST FOR EARLY ACCESS"
- [x] Font size, letter-spacing, uppercase all correct
- [x] Correct background `var(--color-mocha)` and text `var(--color-sand)`
- [x] Height `38px` as per token `--announcement-height`

### 2. Header / Navigation
- [x] Logo "SCENTS BY SARA" present and centered
- [x] Search, Account, Wishlist, Cart icons in right rail — correct
- [x] Desktop nav present: SHOP / GIFTS / OUR STORY / YOUR STORY / CONTACT US
- [x] Mega menu HTML structure present (POPULAR / BODY CANDLES / SHOP BY SIZE / SHOP BY COLLECTION columns)
- [x] Mobile hamburger button present, hidden on desktop via CSS
- [x] Mobile menu overlay with full-screen slide-in panel present
- [ ] FAIL — Header background is pure white `#ffffff`, violates brand no-pure-white standard (see BUG-PRD-016)
- [ ] FAIL — Mega menu image uses `product-2.png` instead of dedicated `mega-menu-image.png` asset (see BUG-PRD-015)
- [x] Sticky header behaviour wired in `main.js` — hide on scroll down, reveal on scroll up

### 3. Breadcrumb
- [x] Present: "SHOP / BODY CANDLES / SHE IS LUST"
- [x] Uppercase, micro text with letter-spacing
- [x] Links to `shop.html`
- [x] Active crumb "SHE IS LUST" in darker tone
- [ ] MINOR — Active crumb uses inline `color: var(--color-slate)` overriding the `text-primary` class (see BUG-PRD-013)

### 4. Product Section — Gallery (Left Column)
- [x] Main image present: `product-1.png`
- [x] Three thumbnails present: `product-1.png`, `product-2.png`, `product-4.png`
- [x] First thumbnail has `.active` class (border active state)
- [x] Wishlist heart icon present in top-right of gallery, filled with `#A39382` (warm taupe tone)
- [x] Thumbnail JS swap logic functional (`product.js`)
- [x] Thumbnail grid 3-col with square `aspect-ratio: 1/1` — correct
- [ ] CRITICAL — Main image has no `aspect-ratio` constraint; gallery height is undefined (see BUG-PRD-001)
- [ ] CRITICAL — Gallery is not sticky; it scrolls with the page (see BUG-PRD-002)

### 5. Product Section — Form (Right Column)
- [x] Product title "SHE IS LUST" in serif font, uppercase
- [x] Subtitle "STRETCH MARK BODY CANDLE" in micro uppercase sans-serif
- [x] Price "£20.26" displayed
- [ ] MAJOR — Price font-size overridden by inline style to 14px instead of CSS-defined 18px (see BUG-PRD-006)
- [ ] MAJOR — Product title inline font-size 40px locks heading at fixed size, bypasses responsive token (see BUG-PRD-005)

### 6. Colour Swatches
- [x] Three swatches present: Ivory (#EAE5DE), Caramel (#C99B6A), Dark Brown (#6A4232)
- [x] Caramel swatch has `.selected` class (correct default)
- [x] Selected swatch shows `box-shadow` ring with gap — matches reference
- [x] JS updates colour label on click
- [ ] MAJOR — Dark brown swatch JS label resolves to "EBONY" — should be "CHESTNUT" (see BUG-PRD-007)
- [ ] MINOR — `.swatch-white` class used for an ivory/cream colour — semantic misnaming (see BUG-PRD-019)
- [x] Swatches are circular `border-radius: 50%` — acceptable exception to 0px radius rule

### 7. Size Toggles
- [x] Three pills present: SLIM / CURVY / PLUS-SIZE
- [x] PLUS-SIZE has `.selected` class by default — correct
- [x] Pill buttons use sharp corners (no border-radius) — brand compliant
- [x] JS toggles selection and updates label correctly
- [x] Selected state uses `--bg-secondary` fill — visible contrast achieved

### 8. Scent Toggles
- [x] Two pills present: VANILLA / LAVENDER
- [x] VANILLA has `.selected` class by default — correct
- [x] JS toggles selection and updates label correctly
- [x] Consistent styling with size toggles

### 9. Quantity Stepper
- [x] `-` / number input / `+` stepper present
- [x] Input is readonly (prevents freetext entry) — correct
- [x] JS increments and decrements correctly; min value = 1
- [x] Stepper is 120px wide with border — correct

### 10. Add to Bag CTA Button
- [x] Dark CTA button present: "ADD TO BAG - £20.26"
- [x] Uses `.btn-solid` + `.btn-add-bag` classes
- [x] Correct mocha background `var(--color-mocha)`, sand text `var(--color-sand)`
- [x] JS shows "ADDED TO BAG" feedback for 2 seconds on click
- [x] Price updates dynamically when quantity changes
- [ ] MINOR — `margin-top: 40px` on `.add-to-cart-row` creates excessive 72px gap above button (see BUG-PRD-018)
- [ ] RESPONSIVE — Button is not full-width on mobile (see BUG-PRD-R06)

### 11. Accordions
- [x] Four accordions present: DESCRIPTION / CRAFT & INTENTION / HOW TO USE / DIMENSIONS & INGREDIENTS
- [x] DESCRIPTION accordion is open by default (`.static-block` with `display:block` on body)
- [x] Remaining three collapsed by default
- [x] Accordion cards have `background-color: var(--bg-secondary)` — stone background
- [x] JS toggles open/close and closes others when a new one opens
- [x] Plus/minus indicator appended via `::after` pseudo-element
- [x] `.static-block .accordion-header::after { content: none }` correctly hides toggle indicator on always-open block
- [ ] MAJOR — Accordion border-top uses `var(--bg-secondary)` — invisible separator (see BUG-PRD-012)

### 12. Scents Section
- [x] Section present with "SCENTS" heading
- [x] Two scent cards: VANILLA and LAVENDER
- [x] Top / Heart / Base notes text present for both scents
- [x] Notes stack at bottom of card with `margin-top: auto` — correct editorial layout
- [x] Lavender card has CSS hue-rotate filter to differentiate from Vanilla background
- [ ] MAJOR — Both scent cards use same `hero-bg.png` — no dedicated editorial photography (see BUG-PRD-008)
- [ ] MAJOR — Section has `padding: 0` — no breathing room from adjacent sections (see BUG-PRD-009)
- [x] Scent card text is white — legible over dark background image

### 13. Our Commitment Section
- [ ] CRITICAL — Image asset `our-commitment-left.png` is missing; will render as broken image (see BUG-PRD-003)
- [x] Right content column structure present: eyebrow, heading, description, credentials list
- [x] Credentials list: Vegan / Paraben-Free / Phtalates-Free / IFRA-Certified
- [ ] MINOR — Typo "Phtalates-Free" should be "Phthalates-Free" (see BUG-PRD-014)
- [x] Heading matches reference: "INTENTIONAL DESIGN IN SCENT AND DESIGN."
- [x] Right column has warm `#EBE8E3` background — close to brand stone tone
- [ ] MAJOR — Section has no responsive breakpoint at 1024px or mobile (see BUG-PRD-R04, BUG-PRD-R08)

### 14. You May Also Like Section
- [x] Section heading "YOU MAY ALSO LIKE" present, centered
- [x] Four product cards in a 4-column grid
- [x] Each card has image, product name, description, price, and "SHOP NOW" button
- [x] Cards link to `product.html` (self-referential placeholder — acceptable for static prototype)
- [x] Warm background `#E8E6E1` on image containers with candle image padding — correct
- [ ] MAJOR — Card 1 shows strikethrough price with identical live price — incorrect sale state (see BUG-PRD-010)
- [x] "SHOP NOW" button uses `.btn-shop-now` class with correct outline styling
- [ ] RESPONSIVE — 3-column at 1024px leaves orphaned 4th card (see BUG-PRD-R02)

### 15. Reviews / Testimonials Section
- [ ] CRITICAL — Full 3-column reviews grid is absent; replaced with a single slide testimonial (see BUG-PRD-004)
- [x] Single testimonial present with quote, author name "EUNICE YUMBA", and 3 slider dots
- [x] Slider dots styled correctly
- [x] Section has `padding: 100px 0` via `.testimonials-section` — adequate vertical spacing
- [x] Background is `--bg-primary` (sand) — correct

### 16. Footer
- [x] Newsletter column with email input, SUBSCRIBE button, social icons (Instagram, Facebook, TikTok, Pinterest)
- [x] Four link columns: SHOP ALL / ABOUT US / GIFTING / CUSTOMER SERVICE
- [x] Links are correct and functional (link to appropriate pages)
- [x] Divider rule present between main grid and bottom row
- [x] Bottom row: "BYSARA" logo text, copyright, payment icons image
- [x] Footer background `--bg-secondary` (stone) — correct
- [x] Social icons use inline SVG with `fill="currentColor"` — correct
- [ ] MINOR — Dead CSS rule for `.footer-social-group img` targeting non-existent PNG icons (see BUG-PRD-020)
- [x] Footer responsive: collapses to 2-column grid at 1024px, newsletter spans 2 columns — correct

---

## JavaScript Functionality Checklist

- [x] Gallery thumbnail swap — functional
- [x] Colour swatch selection — functional (label update has naming bug, see BUG-PRD-007)
- [x] Shape pill toggle — functional
- [x] Scent pill toggle — functional
- [x] Quantity stepper decrement/increment with min=1 guard — functional
- [x] Add to Bag price recalculation — functional
- [x] Add to Bag "ADDED TO BAG" feedback with 2s timeout — functional
- [x] Accordion open/close with mutual exclusion — functional
- [x] Header hide on scroll down / reveal on scroll up — functional (main.js)
- [x] Mobile hamburger toggle with body scroll lock — functional (main.js)
- [x] Search overlay toggle — functional (main.js)

---

## Asset Status

| Asset | Status | Notes |
|---|---|---|
| `assets/images/product-1.png` | OK | Main + thumbnail 1 |
| `assets/images/product-2.png` | OK | Thumbnail 2; also misused in mega menu |
| `assets/images/product-4.png` | OK | Thumbnail 3 |
| `assets/images/product-3.png` | OK | Related product card 3 |
| `assets/images/hero-bg.png` | OK (misused) | Used as scent card background (placeholder) |
| `assets/images/our-commitment-left.png` | MISSING | Critical — commitment section broken |
| `assets/images/our-commitment.png` | OK | Available but not used in product.html |
| `assets/images/payment-icons.png` | OK | Footer |
| `assets/images/mega-menu-image.png` | OK (unused) | Should be used in mega menu |
| Scent editorial photography | MISSING | Vanilla and Lavender-specific images needed |
| `assets/fonts/SuisseIntl-Regular.woff2` | Assumed OK | Not directly verified |
| Adobe Typekit (RL Limo) | External CDN | Fails offline; plan for fallback |

---

## Summary

**20 bugs found (4 critical, 8 major, 8 minor/responsive)**

| Severity | Count | IDs |
|---|---|---|
| Critical | 4 | BUG-PRD-001, BUG-PRD-002, BUG-PRD-003, BUG-PRD-004 |
| Major | 8 | BUG-PRD-005 through BUG-PRD-012 |
| Minor | 8 | BUG-PRD-013 through BUG-PRD-020 |
| Responsive 1024px | 4 | BUG-PRD-R01 through BUG-PRD-R04 |
| Responsive 375px | 5 | BUG-PRD-R05 through BUG-PRD-R09 |

**Sections Passing (no bugs):** Announcement Bar, Size Toggles, Scent Toggles, Quantity Stepper, Footer structure
**Sections Failing:** Gallery sticky + ratio, Commitment image, Reviews grid, Scent photography, Responsive layout, Header white background

**Recommended Fix Priority:**
1. Replace missing `our-commitment-left.png` asset (or correct the src path) — BUG-PRD-003
2. Add `position: sticky` and `aspect-ratio: 3/4` to gallery — BUG-PRD-001, BUG-PRD-002
3. Build the 3-column reviews section HTML — BUG-PRD-004
4. Add product-specific responsive CSS for mobile breakpoints — BUG-PRD-R05 through BUG-PRD-R09
5. Fix commitment section responsiveness — BUG-PRD-R04, BUG-PRD-R08
6. Commission dedicated scent photography assets — BUG-PRD-008
7. Fix price font-size and title inline style overrides — BUG-PRD-005, BUG-PRD-006
8. Fix colour label naming (Ebony → Chestnut) — BUG-PRD-007
9. Fix typo "Phtalates-Free" — BUG-PRD-014
10. Replace mega menu image src — BUG-PRD-015

