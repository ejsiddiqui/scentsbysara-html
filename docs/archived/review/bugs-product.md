<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# Bugs — product.html (Product Detail Page)

Audit Date: 2026-03-01
Auditor: QA Visual Audit (Code + Reference Screenshot Analysis)
Reference Files: product-page.png, product-top.png, sents-section.png, our-commitment-product.png, you-may-like.png

---

## Critical

### [BUG-PRD-001] Missing gallery image height constraint — main image has no fixed aspect ratio
- **File**: `assets/css/product.css`, `.main-image-wrap`
- **Detail**: `.main-image-wrap` uses `flex: 1` with no explicit `aspect-ratio` or `min-height`. The reference screenshot (`product-top.png`) shows the main gallery image at a strict 3:4 portrait ratio. Without a fixed ratio the container collapses or stretches depending on the image loaded, causing the entire left column to behave unpredictably at all viewports.
- **Expected**: `aspect-ratio: 3 / 4` applied to `.main-image-wrap`
- **Actual**: No aspect ratio set; height derived from flex parent with `height: 100%` but `.product-gallery` has no fixed height constraint either
- **Impact**: Layout-breaking on desktop — product image may render very short or very tall depending on browser and image

### [BUG-PRD-002] Product layout not sticky — left gallery does not stick while right panel scrolls
- **File**: `assets/css/product.css`, `.product-gallery`
- **Detail**: The reference design (`product-top.png`) shows a classic sticky-left / scroll-right PDP layout — the gallery stays fixed in view while the user reads descriptions and uses selectors. No `position: sticky` or `top` offset is applied to `.product-gallery`.
- **Expected**: `.product-gallery { position: sticky; top: calc(var(--header-height) + 24px); align-self: flex-start; }`
- **Actual**: Gallery scrolls with the page — the image disappears from view as the user scrolls the form
- **Impact**: Core product page UX pattern broken; loss of parity with finalised reference design

### [BUG-PRD-003] Commitment section image asset missing — `our-commitment-left.png` does not exist
- **File**: `product.html`, line 335; `assets/images/`
- **Detail**: The HTML references `assets/images/our-commitment-left.png`. This file does NOT exist in `assets/images/` (confirmed by directory listing). The available file is `assets/images/our-commitment.png`. The commitment image column will render as a broken `<img>` with no fallback background, showing blank space on the left side of the section.
- **Expected**: `src="assets/images/our-commitment.png"` (or the correct renamed file)
- **Actual**: `src="assets/images/our-commitment-left.png"` — 404
- **Impact**: Visual section entirely broken — left half of commitment grid renders blank

### [BUG-PRD-004] Reviews section absent from HTML — reference design shows a 3-column reviews section
- **File**: `product.html`
- **Detail**: The reference full-page screenshot (`product-page.png`) clearly shows a "WHAT OUR CUSTOMERS ARE SAYING" block with 3-column review cards (Eunice Yumba, Lauren Buffett, Sara Goodall style layout with star ratings, review text, and date meta). The current HTML has only a single-testimonial centered slider (`.testimonials-section`) with one static quote. The 3-column `.reviews-section` grid with `.review-item` row layout is defined in the CSS (`assets/css/product.css` lines 407–444) but has no corresponding HTML markup.
- **Expected**: A `<section class="reviews-section container">` block with three `.review-item` rows containing reviewer name, star rating, review text, and date
- **Actual**: A simplified single-slide testimonial block replaces the full reviews grid
- **Impact**: Missing entire content section; major fidelity gap vs. reference

---

## Major

### [BUG-PRD-005] Product title font size inline override conflicts with design token
- **File**: `product.html`, line 193; `assets/css/product.css`, line 83
- **Detail**: The `<h1>` element has an inline `style="font-size: 40px"` applied. The CSS defines `.product-details h1 { font-size: 40px }` which matches, but `--text-h1` is set to `48px` in design tokens. The reference screenshot shows "SHE IS LUST" rendered at what appears to be closer to 48px relative to the subtitle and price. The inline style prevents scaling via media query tokens at `@media (max-width: 375px)` where `--text-h1` drops to 32px, as inline styles override CSS custom property references.
- **Expected**: Remove inline `style="font-size: 40px"` and rely on `.product-details h1` class or use `class="font-serif text-h1"` to respect token-driven scaling
- **Actual**: Inline font-size locks heading at 40px at all breakpoints

### [BUG-PRD-006] Price position incorrect — price should appear inline right of subtitle, not in flex-between row
- **File**: `product.html`, lines 194–201
- **Detail**: In the reference (`product-top.png`), the price `£20.26` sits at the top-right of the right panel, level with the subtitle "STRETCH MARK BODY CANDLE", forming a horizontal pair. The current HTML wraps subtitle and price in `.flex-between`, but the price element also has an inline `style="font-size: 14px"`. The CSS defines `.product-details .price { font-size: 18px }` which is overridden by the inline style. Price reads smaller than designed.
- **Expected**: Price at `font-size: 18px` per CSS definition, inline style removed
- **Actual**: Inline `font-size: 14px` overrides the CSS rule

### [BUG-PRD-007] Colour swatch label uses "Chestnut" in spec but "Ebony" in JavaScript
- **File**: `assets/js/product.js`, line 38
- **Detail**: The brand specification lists colour names as Caramel, Chestnut, and Ivory. The HTML labels currently show "CARAMEL" (tan swatch selected). However, in `product.js`, when the dark brown swatch (`.swatch-brown`) is selected, the JS sets the label to `EBONY` rather than `CHESTNUT`. This is a copy/naming mismatch.
- **Expected**: `swatch.classList.contains('swatch-brown') ? 'CHESTNUT' : 'IVORY'`
- **Actual**: Brown swatch resolves to `'EBONY'`

### [BUG-PRD-008] Scents section image uses `hero-bg.png` as placeholder for both cards — editorial photos missing
- **File**: `product.html`, lines 288 and 308
- **Detail**: Both scent cards (Vanilla and Lavender) use `assets/images/hero-bg.png` as the background image. The Lavender card applies a CSS filter to distinguish it, but the Vanilla card has no unique editorial photo. The reference screenshot (`sents-section.png`) shows distinct photography — vanilla beans for Vanilla, lavender sprigs for Lavender. Dedicated scent photography assets are not present in `assets/images/`.
- **Expected**: Dedicated scent editorial photos (e.g. `scent-vanilla.jpg`, `scent-lavender.jpg`)
- **Actual**: Same generic hero background used for both, with a CSS hue-rotate filter as a workaround for lavender

### [BUG-PRD-009] Scents section lacks top/bottom padding — content abuts adjacent sections without breathing room
- **File**: `assets/css/product.css`, lines 264–267
- **Detail**: `.scents-section { padding: 0; }` sets zero padding. The section title "SCENTS" has `margin-bottom: 64px` but no top spacing is applied, meaning the scents section immediately follows the product main section without the standard `--space-section: 80px` gap. The reference shows clear top padding above the "SCENTS" heading.
- **Expected**: `.scents-section { padding: var(--space-section) 0; }`
- **Actual**: `padding: 0` — no vertical breathing room

### [BUG-PRD-010] "You May Also Like" — first product card shows strikethrough price, others do not
- **File**: `product.html`, lines 367–370
- **Detail**: Product Card 1 shows a strikethrough `£20.26` alongside the live price `£20.26` — a sale price presentation with both values identical, which is semantically wrong (identical prices should never use a strikethrough). Cards 2–4 show the price without strikethrough. The reference screenshot (`you-may-like.png`) shows Card 1 with a strikethrough "£20.26" and a live "£20.26", suggesting a sale price was intended to be different. All four cards should be consistent.
- **Expected**: Either a genuinely different original price (e.g. `£24.00`) with a sale price, or remove the strikethrough markup entirely if no discount exists
- **Actual**: Strikethrough and live prices are identical on Card 1; inconsistent with Cards 2–4

### [BUG-PRD-011] Commitment section `margin-top: 80px` creates gap rather than using section padding
- **File**: `assets/css/product.css`, lines 332–337
- **Detail**: `.product-commitment-grid { margin-top: 80px; }` pushes the commitment grid down from the scents section, but this relies on the scents section having no bottom padding (BUG-PRD-009). If scents section padding is fixed, the gap doubles. The commitment section should use its own vertical padding pattern instead of a top margin.
- **Expected**: Standardised section padding rather than margin coupling
- **Actual**: Layout is fragile — coupled to scents section having zero padding

### [BUG-PRD-012] `.accordion` border uses `var(--bg-secondary)` making it nearly invisible
- **File**: `assets/css/product.css`, line 213
- **Detail**: `.accordion { border-top: 1px solid var(--bg-secondary); }` uses the stone background colour `#E7E3DC` as the border. Since `.accordion-wrapper .accordion` has `background-color: var(--bg-secondary)`, the 1px border at the top blends into the card background of the preceding element. The visual separator between accordion blocks is effectively invisible. The reference shows clear visible separators between each accordion card.
- **Expected**: `border-top: 1px solid var(--color-clay)` or `1px solid var(--border-light)`
- **Actual**: Border colour matches background — no visible divider between accordion cards

---

## Minor

### [BUG-PRD-013] Breadcrumb active item uses hardcoded `color: var(--color-slate)` via inline style
- **File**: `product.html`, line 166
- **Detail**: `<span class="text-primary" style="color: var(--color-slate)">SHE IS LUST</span>` — the `text-primary` class maps to `--color-mocha` but is immediately overridden by an inline `color: var(--color-slate)`. The distinction is subtle (#3F3229 vs #2D2B27) but inconsistent. Should use a single source of truth for the active breadcrumb colour.
- **Expected**: Remove inline style; define `.breadcrumbs .active` or use `.text-primary` cleanly
- **Actual**: Class and inline style conflict

### [BUG-PRD-014] Typo in commitment list — "Phtalates-Free" should be "Phthalates-Free"
- **File**: `product.html`, line 346
- **Detail**: `<span class="commitment-list-item">Phtalates-Free</span>` — missing the second 'h' in "Phthalates"
- **Expected**: "Phthalates-Free"
- **Actual**: "Phtalates-Free"

### [BUG-PRD-015] Mega menu image references `product-2.png` instead of a dedicated mega menu image
- **File**: `product.html`, line 133
- **Detail**: The mega menu image column (`<img src="assets/images/product-2.png">`) uses a product image. An asset `assets/images/mega-menu-image.png` exists in the repo and is the intended editorial image for the mega menu dropdown.
- **Expected**: `src="assets/images/mega-menu-image.png"`
- **Actual**: `src="assets/images/product-2.png"`

### [BUG-PRD-016] Header background is pure white `#ffffff` — violates brand no-pure-white standard
- **File**: `assets/css/components.css`, line 178 and line 267
- **Detail**: `.site-header { background-color: #ffffff; }` and `.search-overlay { background-color: #ffffff; }` both use pure white. Brand standards specify no pure white — all surfaces should use warm neutral tones (minimum `--color-sand: #F9F6F2`).
- **Expected**: `background-color: var(--color-sand)` or `#FAFAF8`
- **Actual**: `#ffffff`

### [BUG-PRD-017] `selector-group mt-8` — first colour swatch group uses `mt-8` but subsequent groups use `mt-6`, creating unequal spacing
- **File**: `product.html`, lines 203 and 212
- **Detail**: The colour selector group has class `mt-8` (32px top margin) while the body shape and scent groups have `mt-6` (24px). The reference screenshot shows uniform spacing between all selector groups. The first group is 8px taller than the rest, making the spacing inconsistent above the colour swatches.
- **Expected**: All selector groups should use the same vertical margin — `mt-6` uniformly, or as defined in `.selector-group { margin-bottom: 32px }` without extra `mt-` utility overrides
- **Actual**: Inconsistent 32px / 24px top margins across selector groups

### [BUG-PRD-018] Add-to-cart row `margin-top: 40px` inside `.add-to-cart-row` creates double spacing when combined with `selector-group mt-6`
- **File**: `assets/css/product.css`, line 172
- **Detail**: `.add-to-cart-row { margin-top: 40px; }` adds 40px above the quantity/add-to-bag row. The parent `.selector-group` already has `margin-bottom: 32px`. Combined spacing of 72px between the last selector and the CTA is excessive and inconsistent with the tighter layout shown in the reference screenshot.
- **Expected**: Remove `margin-top` from `.add-to-cart-row` and rely on `.selector-group`'s `margin-bottom` alone
- **Actual**: 72px compound gap above the Add to Bag button

### [BUG-PRD-019] Colour swatch label uses lowercase "third colour" naming — inconsistent with the dark swatch
- **File**: `product.html`, line 206
- **Detail**: The swatch `div.swatch-white` represents "Ivory" but the class name is `.swatch-white` while the actual colour shown is `#EAE5DE`, a warm cream — not white. The naming creates confusion and the JavaScript also computes it as `IVORY` on click but the visual is not white.
- **Expected**: Rename to `.swatch-ivory` for semantic clarity across HTML, CSS, and JS
- **Actual**: `.swatch-white` used for a non-white ivory/cream tone

### [BUG-PRD-020] Footer social icons use SVG inline with `fill="currentColor"` but parent link has no explicit colour set
- **File**: `product.html`, lines 482–504; `assets/css/components.css`
- **Detail**: The footer social links (`<a>` tags in `.footer-social-group`) have no explicit `color` defined. `currentColor` inherits from the parent, which is `var(--color-mocha)` via `.site-footer`. This works correctly but there is an unused CSS rule in `components.css` line 955–960 targeting `.footer-social-group img` (for PNG-based icons) that applies a filter — this rule is dead code since the HTML now uses SVGs. Not a visual break but dead CSS.
- **Expected**: Remove `.footer-social-group img` filter rule, or document the intent
- **Actual**: Dead CSS rule left from a prior icon implementation

---

## Responsive Issues

### 1024px (Tablet)

#### [BUG-PRD-R01] Product main grid collapses to single column but gallery and form have no tablet-specific spacing
- **File**: `css/responsive.css`, line 64–68
- **Detail**: At 1024px, `.grid-cols-2 { grid-template-columns: 1fr; }` stacks the gallery above the form correctly. However, no tablet-specific styles exist for `.product-gallery`, `.product-details`, or `.product-main` to adjust padding, image size, or spacing. The main image will attempt to fill the full column width at 100% — on a 1024px viewport with 48px gutters, this means an ~928px wide image, which is too large for the 3:4 ratio and will likely appear disproportionately tall.
- **Expected**: Tablet-specific max-height or aspect-ratio constraint on `.main-image-wrap` (e.g. `max-height: 500px`)
- **Impact**: Gallery image renders at excessive height; form is pushed far below the fold

#### [BUG-PRD-R02] "You May Also Like" shows 3-column grid at 1024px — should be 2 columns
- **File**: `css/responsive.css`, line 29–31
- **Detail**: At `max-width: 1024px`, `.grid-cols-4 { grid-template-columns: repeat(3, 1fr); }` — 3 columns with 4 product cards leaves one card orphaned on its own row, creating an asymmetric layout.
- **Expected**: At 1024px, related products should display as 2 columns: `grid-template-columns: repeat(2, 1fr)`
- **Actual**: 3-column override at tablet leaves fourth card alone on row 2

#### [BUG-PRD-R03] Scent cards in `.scents-section .grid-cols-2` also collapse to 1 column at 1024px — scent section becomes single tall column instead of side-by-side editorial
- **File**: `css/responsive.css`, line 64–68
- **Detail**: The generic `.grid-cols-2` collapse rule affects the scent section. At 1024px, the two editorial scent cards stack vertically. Each card at `aspect-ratio: 1 / 0.85` will render at full column width (~928px) and become excessively tall for a card-style layout. A scent section specific override is needed.
- **Expected**: Scent cards should either remain 2-column until 768px or have a max-height cap applied
- **Actual**: Tall stacked cards that break the editorial feel at tablet

#### [BUG-PRD-R04] Commitment grid `.product-commitment-grid` has no tablet breakpoint — remains 50/50 split at 1024px with very narrow columns
- **File**: `assets/css/product.css`, lines 332–353
- **Detail**: `.product-commitment-grid { grid-template-columns: 1fr 1fr; }` has no responsive override. At 1024px with 48px gutters, each column is approximately 464px wide. The content column has `padding: 120px 80px` — at 464px wide, the 80px side padding leaves only ~304px for content, making the heading and text very cramped.
- **Expected**: At 1024px: `grid-template-columns: 1fr` (stack), or reduce `.commitment-content-col` padding to `60px 40px`
- **Actual**: Cramped side-by-side layout with insufficient content width

### 375px (Mobile)

#### [BUG-PRD-R05] No product-page-specific mobile styles — critical omission
- **File**: `css/responsive.css`
- **Detail**: The responsive stylesheet has no rules targeting `.product-gallery`, `.product-details`, `.add-to-cart-row`, `.qty-selector`, `.pill-group`, `.color-swatches-lg`, `.accordion-wrapper`, or `.scents-section` at mobile breakpoints (768px or below). All product-specific layout relies on default stacking only. Critical issues expected:
  - `.add-to-cart-row` displays the quantity stepper and button side-by-side — at 375px with 20px gutters this leaves ~335px total. The qty-selector is fixed at 120px width, leaving ~199px for the `btn-add-bag` — not full width as required
  - `.pill-group` with 3 pills (SLIM/CURVY/PLUS-SIZE) at equal flex:1 — on 335px this gives ~104px each which may barely fit, but text could wrap inside pill buttons
  - `.commitment-content-col { padding: 120px 80px }` is severely over-padded for a 375px screen — 80px side padding on a 375px viewport leaves only 215px for content
- **Impact**: Multiple elements will be cramped, overlapping, or require horizontal scrolling

#### [BUG-PRD-R06] "Add to Bag" button does not go full width on mobile
- **File**: `assets/css/product.css`, `.add-to-cart-row`; `css/responsive.css`
- **Detail**: At mobile, the CTA "Add to Bag" button is expected to span the full width (per brand pattern and reference design). No mobile override exists to make `.add-to-cart-row { flex-direction: column }` with `.btn-add-bag { width: 100% }`. The quantity stepper and button remain in a flex row.
- **Expected**: At `max-width: 768px`: `.add-to-cart-row { flex-direction: column }` and `.btn-add-bag { width: 100%; }`
- **Actual**: Side-by-side layout maintained at mobile — button is approximately 60% width

#### [BUG-PRD-R07] Scent section title inherits `.scent-name.text-hero` at 56px — too large for 375px
- **File**: `assets/css/product.css`, line 303–307; `product.html`, lines 290, 311
- **Detail**: `<h3 class="font-serif scent-name text-hero">VANILLA</h3>` — `.text-hero` resolves to `font-size: var(--text-hero)` which drops to 40px at 375px via the token override. However `.scent-name` overrides `font-size: 28px` which would cap this — the specificity battle means `text-hero` (set in layout.css on `.text-hero`) may win depending on cascade order. Either way 28px–40px serif uppercase inside a card with 48px padding on a 375px screen is problematic.
- **Expected**: Explicit mobile override: `.scent-name { font-size: 22px }` at `max-width: 375px`
- **Actual**: Potential oversized heading inside narrow card

#### [BUG-PRD-R08] `.commitment-content-col { padding: 120px 80px }` is not responsive — will cause severe content overflow at mobile
- **File**: `assets/css/product.css`, line 350
- **Detail**: No responsive override for `.commitment-content-col` padding. At 375px viewport with `--gutter: 16px` for the page container, the commitment section uses `width: 100%` without a container wrapper, so the grid breaks the gutter system entirely. The 80px side padding on a column that itself may be 375px wide leaves only 215px for text — and at mobile the grid should stack, not remain 50/50.
- **Expected**: Mobile override: `grid-template-columns: 1fr` on `.product-commitment-grid`, with `.commitment-content-col { padding: 48px 24px }`
- **Actual**: Grid stays 2-column (no breakpoint defined) with extreme padding — commitment text is severely clipped or wraps unusably

#### [BUG-PRD-R09] `.grid-cols-4` for related products collapses to 1 column at 480px — at 375px shows single column correctly, but `shop-card` has `margin-bottom: 48px` from `shop.css` creating excessive whitespace between single-column cards
- **File**: `assets/css/shop.css`, line 79
- **Detail**: On mobile, the 4 related product cards display in a single column (correct). However `.shop-card { margin-bottom: 48px }` stacks 48px below each card. Combined with the grid `gap: var(--space-md)` (16px), there is ~64px of vertical separation between each card — too spacious for a mobile context where efficient scrolling is needed.
- **Expected**: Override `.shop-card { margin-bottom: 24px }` at `max-width: 480px`
- **Actual**: Excessive 48–64px gap between stacked product cards

---

## Notes

- **Font loading**: RL Limo loaded via Adobe Typekit (`https://use.typekit.net/abn0bto.css`) — will fail in offline/local file:// mode. All serif headings will fall back to system serif. Not a production bug but worth noting for local QA review.
- **JavaScript**: Product interactions (accordion toggle, thumbnail swap, quantity stepper, colour label update) are correctly implemented and functional. No JS errors expected under normal conditions.
- **Asset inventory confirmed present**: `product-1.png`, `product-2.png`, `product-3.png`, `product-4.png`, `hero-bg.png`, `payment-icons.png`, `our-commitment.png` (note: `our-commitment-left.png` is MISSING — see BUG-PRD-003).
- **Border-radius compliance**: `.swatch-lg { border-radius: 50% }` and `.dot { border-radius: 50% }` are intentional circular exceptions. `.pill-btn` has no border-radius (correct — sharp corners). No violations of the `--radius-max: 0px` rule detected for rectangular elements.
- **Color compliance**: Body and section backgrounds use `--bg-primary` (#F9F6F2) correctly. Main violation is the header `#ffffff` (BUG-PRD-016). All text uses warm mocha/slate tones — no pure black detected.

