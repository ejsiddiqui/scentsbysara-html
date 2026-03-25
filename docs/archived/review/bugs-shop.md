<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# Bugs — shop.html (Shop Page)

> Audit date: 2026-03-01
> Auditor: QA Visual Audit (static HTML analysis + reference screenshot comparison)
> Reference screenshots used: `shop-page.png`, `footer-fix.png`, `mobile-full.png`

---

## Critical

- **[BUG-SHP-001] Missing pagination / load-more control**
  Only 6 product cards are hardcoded in the grid. The page has no pagination component, no "Load More" button, and no product count indicator (e.g. "Showing 6 of 12 products"). The reference `shop-page.png` shows a finished collection grid; a production shop page requires this control.

- **[BUG-SHP-002] Filter overlay uses pure white background (#ffffff) — violates brand standard**
  In `assets/css/shop.css` (lines 209, 267) the `.filter-overlay` and `.filter-footer` are set to `background-color: #fff`. Brand spec mandates no pure white; all backgrounds must be warm neutrals (`#F9F6F2` sand or `#E7E3DC` stone).

- **[BUG-SHP-003] Search overlay background is pure white (#ffffff) — violates brand standard**
  In `css/components.css` (line 149) `.search-overlay` uses `background-color: #ffffff`. Must be `var(--color-sand)` (`#F9F6F2`).

- **[BUG-SHP-004] Header background is pure white (#ffffff) — violates brand standard**
  In `css/components.css` (line 178) `.site-header` uses `background-color: #ffffff`. Reference screenshots (`header-hero.png`, `shop-page.png`) show a warm off-white header, not pure white.

- **[BUG-SHP-005] Mega menu image references non-existent asset**
  `shop.html` line 132: `<img src="assets/images/product-2.png">` is used in the mega menu image column. While this file exists, the brand-spec mega menu image should reference `assets/images/mega-menu-image.png` (which also exists in the repo). Using a product image in the nav mega menu is semantically and visually incorrect.

---

## Major

- **[BUG-SHP-006] All 6 product cards use the same product name "SHE IS TIMELESS"**
  Cards 1–6 all display `SHE IS TIMELESS` as the product name. This is placeholder/copy-paste content that was never differentiated. Products 3–6 should reflect distinct candle names from the product range (e.g. "She is Beauty", "She is Lust", "She is Strength", etc.) per the mega menu listings.

- **[BUG-SHP-007] Color swatch `swatch-white` uses pure white (#FFFFFF) — violates brand standard**
  In `assets/css/shop.css` (line 132) `.swatch-white` is `background-color: #FFFFFF`. This should be the nearest warm neutral (`#F9F6F2` or `#E7E3DC`) or a very light ivory to stay on-brand. Pure white is explicitly excluded by brand guidelines.

- **[BUG-SHP-008] Color swatch uses `border-radius: 50%` — violates brand standard (0px radius)**
  In `assets/css/shop.css` (line 118) `.swatch` has `border-radius: 50%`. The brand design system mandates `--radius-max: 0px` (sharp corners everywhere). Circular swatches conflict with this rule. Swatches should be square (0px radius).

- **[BUG-SHP-009] Slider dot elements use `border-radius: 50%` — violates brand standard**
  In `css/components.css` (lines 467, 676) `.dot` elements have `border-radius: 50%`. The `--radius-max: 0px` token applies globally; all interactive indicators should be square. (Note: dots are used in testimonial/hero sliders on this page's shared component sheet, not on shop.html itself, but any shared page that imports these will carry the violation.)

- **[BUG-SHP-010] Filter overlay is injected into `<body>` via JavaScript at runtime (shop.js line 73)**
  The filter panel DOM is created dynamically by `shop.js` with `document.body.appendChild(filterOverlay)`. This approach appends the overlay after the footer outside of semantic HTML flow. It cannot be server-rendered or indexed, breaks the DOM order, and creates z-index conflict risks. The filter overlay should be declared in HTML and toggled with a class.

- **[BUG-SHP-011] Filter overlay grid uses `grid-cols-3` class which is not defined in any CSS**
  In `shop.js` line 48 the injected filter markup uses `class="filter-grid grid-cols-3"`. The design token / layout system defines `grid-cols-4` and `grid-cols-2` but not `grid-cols-3`. The filter groups will not display in a grid — they will stack vertically as a single column inside `.filter-grid` (which uses `flex-direction: column`).

- **[BUG-SHP-012] `btn-shop-now` border color deviates from global product button standard**
  In `assets/css/shop.css` (line 186) `.btn-shop-now` border is `1px solid var(--color-clay)` (`#CEC5B8`). The global `.product-btn` in `css/components.css` (line 556) uses `1px solid var(--color-slate)` (`#2D2B27`). Both buttons perform the same function but have inconsistent border treatments.

- **[BUG-SHP-013] Sort dropdown only toggles between two states with a click — no actual dropdown UI**
  The `.sort-dropdown` in `shop.js` (lines 120–132) cycles between "PRICE (LOW TO HIGH)" and "PRICE (HIGH TO LOW)" on click with no visible options list, no ARIA roles (`role="listbox"`), and no keyboard accessibility. The reference `shop-page.png` shows a sort dropdown affordance labelled "SORT BY: PRICE". No "FEATURED" or "NEWEST" sort options are implemented.

- **[BUG-SHP-014] `main.js` scroll hide/show applies `header-hidden` transform to sticky header but announcement bar is not accounted for**
  When scrolling down, `header.classList.add('header-hidden')` translates the `.site-header` up by `-100%`. However the `.announcement-bar` sits outside `.site-header` and remains fixed at the top. This causes the announcement bar to be orphaned above the viewport when the header hides, creating a layout jump where content beneath fills the full 132px space unexpectedly.

- **[BUG-SHP-015] `shop-hero` paragraph has no max-width constraint**
  In `assets/css/shop.css` (line 21) the `max-width` for `.shop-hero p` is commented out (`/* max-width: 800px; */`). At 1440px–1920px viewports the paragraph text runs full-width across the entire container (up to 1720px content max), which is typographically excessive for body copy and breaks the editorial line-length standard of ~60–80ch.

---

## Minor

- **[BUG-SHP-016] `payment-icons.png` missing from assets/images directory**
  `shop.html` line 499 references `assets/images/payment-icons.png`. The `ls` of the assets directory confirms this file exists (`payment-icons.png`). However, `footer-fix.png` (the reference) shows individual payment brand logos (Amex, Visa, PayPal, Google Pay, Apple Pay, Mastercard, Klarna). The single image approach will break if the file is replaced without exact dimension matching, and individual SVG/icon components would be more maintainable.

- **[BUG-SHP-017] Typo in shop-hero paragraph — "meaning detail" should be "meaningful detail"**
  `shop.html` line 167: "each combines sculptural form with meaning detail and intentional craftsmanship." The word "meaning" should be "meaningful". This is visible copy-level content.

- **[BUG-SHP-018] `shop.html` title tag is "Shop All | Scents by Sara" — inconsistent capitalisation**
  The `<title>` (line 7) uses mixed case: "Shop All | Scents by Sara". Site convention seen across nav and announcement bar uses all-caps for "SCENTS BY SARA". The title tag should match the brand name casing: "Shop All | SCENTS BY SARA".

- **[BUG-SHP-019] `has-mega-menu` hover bridge uses negative margin trick (`margin-bottom: -30px`) which is fragile**
  In `css/components.css` (lines 258–260) `.has-mega-menu` uses `padding-bottom: 36px; margin-bottom: -30px` to bridge the hover gap between the nav link and the mega menu. This is a known fragile technique that can break if header height changes. A CSS-only pseudo-element bridge or a small JS-powered hover delay would be more robust.

- **[BUG-SHP-020] `shop.html` has no `<meta name="description">` tag**
  The `<head>` section (lines 4–14) contains no meta description, which affects SEO and social sharing previews.

- **[BUG-SHP-021] Active state on color swatches uses `transform: scale(1.2)` on circular elements**
  `.swatch.active` in `assets/css/shop.css` (lines 126–129) applies `transform: scale(1.2)` but as noted in BUG-SHP-008 swatches use `border-radius: 50%`, creating a circular scaled dot. If swatches are corrected to be square (0px radius), the scale animation will still apply — this is acceptable, but the active state border (`border-color: var(--color-mocha)`) should be verified visually after the border-radius fix.

- **[BUG-SHP-022] No `<link rel="canonical">` tag present in `<head>`**
  The page has no canonical URL defined. This is a standard SEO requirement for an ecommerce product listing page.

- **[BUG-SHP-023] `product-image-wrap` `aspect-ratio: 4/5` not applied consistently at mobile breakpoints**
  The `.product-image-wrap` in `css/components.css` (line 496) sets `aspect-ratio: 4/5`. At 375px with `grid-cols-4` collapsing to single column (via the 480px breakpoint rule in `responsive.css` line 151), the images expand to full width and the 4/5 ratio holds, but the very tall cards at single-column may feel unbalanced. No mobile-specific aspect ratio override is provided.

- **[BUG-SHP-024] Footer "SHOP ALL" column in reference has "Scar Collection" and "Sculpted Collection" links, but `shop.html` footer is missing these**
  Looking at `footer-fix.png` reference, the "SHOP ALL" footer column does not include "Scar Collection" or "Sculpted Collection". However the `shop.html` footer (lines 451–455) also does not include them. Cross-checking confirms the HTML matches the reference for this column — no bug. (Logged for verification purposes only; no action needed.)

---

## Responsive Issues

### 1024px (Tablet — Landscape)

- **[BUG-SHP-T01] Product grid collapses to 3 columns at 1024px — creates orphaned single card on last row**
  `responsive.css` (line 30) sets `.grid-cols-4` to `repeat(3, 1fr)` at 1024px. With 6 product cards, this yields 2 rows of 3. This is acceptable mathematically. However, if the product count is not a multiple of 3 (e.g. 5 or 7 products), an orphaned card will appear left-aligned with large whitespace. No flexbox fill or `justify-items` rule handles the partial last row.

- **[BUG-SHP-T02] Navigation completely hidden at 1024px — hamburger shown but no SHOP active indicator**
  `responsive.css` (line 35) hides `.header-bottom` (the nav row) at 1024px and shows the hamburger. However the active page ("SHOP") has no visual indicator in the mobile menu overlay. The `.mobile-nav-links` in `shop.html` shows "SHOP ALL" as first link but there is no `aria-current="page"` attribute or active class to signal the current page to users and screen readers.

- **[BUG-SHP-T03] Filter toolbar wraps awkwardly at 1024px — no responsive override provided**
  The `.filter-toolbar` is `display: flex; justify-content: space-between` with a `.sort-dropdown` minimum width of 280px. At 1024px with the gutter reduced to 48px, the filter button and sort dropdown may sit too close together or force a layout reflow. No specific 1024px override for `.filter-toolbar` exists in any stylesheet.

- **[BUG-SHP-T04] Footer grid collapses to 2-column layout but newsletter column spans 2 — "CUSTOMER SERVICE" column may overflow**
  `css/components.css` (line 1031) sets `.footer-main-grid` to `grid-template-columns: 1fr 1fr` at 1024px and `.footer-newsletter-col` spans 2 columns. With 5 columns (newsletter + 4 link columns), the remaining 4 link columns display as 2×2 grid. "CUSTOMER SERVICE" has 5 items and is the widest column — at 48px gutters this may overflow or cause text wrapping at each link item.

### 375px (Mobile — iPhone SE)

- **[BUG-SHP-M01] Product grid uses `grid-cols-4` which collapses to `1fr` only at 480px breakpoint — at exactly 375px it is already 1 column, which is correct, but the 480px rule feels too broad**
  The transition from 2 columns to 1 column happens at 480px, not 375px. On devices between 376px–480px (e.g. most Android mid-range phones), products show as 1 column. The breakpoint is correct for 375px but the intermediate 376–480px range shows 1 column where 2 columns might still fit.

- **[BUG-SHP-M02] `shop-hero` heading `font-size: 48px` is overridden to `32px` at 375px via design token `--text-h1: 32px` — but the h1 uses `.text-h1` class which relies on this token correctly. Acceptable.**
  The responsive token change at 375px (line 162–167 `responsive.css`) correctly reduces `--text-h1` to 32px. The `shop-hero .text-h1` rule in `shop.css` sets `font-size: 48px` as a direct pixel value, bypassing the CSS variable entirely. This means the 375px override token has NO EFFECT on the shop hero h1 — the heading will remain 48px on mobile, which is too large.

- **[BUG-SHP-M03] Filter toolbar at 375px — `.sort-dropdown` has `min-width: 280px` which exceeds available content width**
  At 375px with a 16px gutter (32px total), content width is 343px. The `.sort-dropdown` minimum width of 280px plus the `.filter-btn` (~100px) totals ~380px — wider than the viewport. This will cause horizontal overflow or push the sort dropdown below the filter button without a flex-wrap rule.

- **[BUG-SHP-M04] Footer bottom row becomes `display: block` at 1024px but BYSARA logo and payment icons stack vertically with no spacing rule**
  `responsive.css` (line 20) sets `.footer-bottom-row { display: block }` at 1024px. There is no margin or gap between `.footer-brand-wrap` and `.footer-payment-wrap` in this stacked state, causing the payment icons to immediately follow the copyright text with no breathing room.

- **[BUG-SHP-M05] Mobile menu "SHOP NOW" CTA button uses `.btn-outline` styling (transparent background, dark border) — inconsistent with primary CTA treatment**
  In `shop.html` (line 524) the mobile menu footer button is `.btn-outline`. On mobile, the primary CTA should be `.btn-solid` (dark fill) for higher contrast and conversion clarity, matching standard mobile commerce patterns and the overall brand hierarchy.

- **[BUG-SHP-M06] No touch/swipe interaction on product images at mobile viewport**
  The product cards do not implement any swipe-to-view-variant interaction on mobile. While not strictly a bug against the current static spec, in the reference design patterns for mobile ecommerce, product image swipe (to see color variants) is a standard expected behavior. This is a UX gap at 375px.


