<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# Bugs — cart.html (Cart Page)

> Audit Date: 2026-03-01
> Auditor: QA Agent
> Viewports Tested: 1440px | 1024px | 375px
> Reference: Brand guidelines (no dedicated cart screenshot exists)

---

## Critical

### [BUG-CRT-001] Cart table has no responsive breakpoints — overflows on mobile (375px)
- **Severity**: Critical
- **Viewport**: 375px (and any viewport < ~600px)
- **File**: `cart.html` — inline `<style>` block + missing responsive rules in `css/responsive.css`
- **Description**: The `.cart-table` is a standard HTML `<table>` with four columns (PRODUCT 50%, PRICE 15%, QUANTITY 20%, TOTAL 15%). No media query collapses or restructures the table for narrow viewports. At 375px the table either overflows horizontally (creating a horizontal scrollbar) or compresses columns so severely that quantity controls, price, and product names become illegible. The cart image thumbnail, qty stepper, and price columns cannot all fit within a ~375px content area at the defined column widths.
- **Expected**: Table should convert to a card-based stacked layout at ≤ 768px — product image + name/variant in one row, price/qty/total in a sub-row, remove link accessible.
- **Code Reference**: `cart.html` lines 258–315; no cart-specific rules exist in `css/responsive.css`.

---

### [BUG-CRT-002] Header `background-color: #ffffff` — pure white violates brand standard
- **Severity**: Critical
- **Viewport**: All
- **File**: `css/components.css` line 178
- **Description**: `.site-header` is styled with `background-color: #ffffff` (pure white). The brand standard explicitly prohibits pure white — all surfaces must use warm neutral tones from the brand palette (`--color-sand: #F9F6F2`, `--color-stone: #E7E3DC`). The search overlay (`.search-overlay`) also uses `background-color: #ffffff` (line 149). These are carried from the shared component stylesheet affecting all pages including cart.
- **Expected**: Header background should use `var(--bg-primary)` (#F9F6F2 sand) or at minimum `#FAFAF8` — a warm near-white. Search overlay likewise should match.
- **Code Reference**: `css/components.css` lines 149, 178.

---

## Major

### [BUG-CRT-003] Cart summary box not full-width on mobile — `max-width: 480px` with `margin-left: auto` creates misaligned block at 375px
- **Severity**: Major
- **Viewport**: 375px
- **File**: `cart.html` inline `<style>` block (lines 93–104)
- **Description**: `.cart-summary-box` has `max-width: 480px` and `margin-left: auto`. On mobile the content area is ~343px (375px - 2x16px gutter), which is narrower than 480px, so the max-width constraint has no effect — the box fills available width correctly. However, `margin-left: auto` combined with the parent context means the box remains right-aligned rather than being naturally centred or full-width as expected for a mobile order summary. The summary should span full container width on mobile and be clearly separated from the table above it.
- **Expected**: On mobile, `.cart-summary-box` should be `width: 100%`, left-margin reset to 0, with adequate top spacing.
- **Code Reference**: `cart.html` lines 93–99.

### [BUG-CRT-004] Checkout button labelled "CHECKOUT" instead of "PROCEED TO CHECKOUT" — missing call-to-action clarity
- **Severity**: Major
- **Viewport**: All
- **File**: `cart.html` line 323
- **Description**: The primary CTA button reads "CHECKOUT". Standard ecommerce UX practice (and the PRD spec for the cart page) calls for "PROCEED TO CHECKOUT" which is more explicit and reassuring on a cart page. Additionally, the button uses `<a href="checkout.html">` with inline `style="width: 100%;"` alongside the class `w-full block text-center` — the utility class `w-full` is not defined in any stylesheet (`css/layout.css`, `css/components.css`, `css/responsive.css`, or `css/design-tokens.css`), meaning the width is only enforced by the inline style. This is a fragile pattern.
- **Expected**: Button label should read "PROCEED TO CHECKOUT". The `w-full` class should either be defined or the inline style consolidated.
- **Code Reference**: `cart.html` line 323.

### [BUG-CRT-005] Missing "Continue Shopping" as a distinct secondary section — only a micro-link in the header row
- **Severity**: Major
- **Viewport**: All
- **File**: `cart.html` lines 253–256
- **Description**: "CONTINUE SHOPPING" is placed as a small `text-micro text-muted underline` link in the `.cart-header` flex row, right-aligned next to the "YOUR BAG" heading. It is functionally correct but visually subordinate to the point of being easy to miss. Per brand UX standards for a luxury cart page, there should be a secondary CTA below the checkout button — a clear, styled link or `btn-outline` reading "CONTINUE SHOPPING" — so customers can easily return to shopping without hunting for a small link at the top of the page.
- **Expected**: A second "CONTINUE SHOPPING" link should appear below the `.cart-summary-box` checkout button, styled as an `btn-outline` or at minimum a prominent underlined link, full-width on the summary box.
- **Code Reference**: `cart.html` lines 253–256 (only instance of continue shopping).

### [BUG-CRT-006] `.cart-header` uses `flex-between items-end` — `items-end` class is undefined
- **Severity**: Major
- **Viewport**: All
- **File**: `cart.html` line 253; `css/layout.css`
- **Description**: The `.cart-header` div uses classes `flex-between items-end`. The class `flex-between` is defined in `css/layout.css` (line 161) and includes `align-items: flex-end` already. The additional class `items-end` is not defined anywhere in the stylesheets. This is a dangling utility class with no effect — but suggests either the developer intended a separate utility or made an error. The `flex-between` definition itself has `align-items: flex-end` baked in, which may not always be appropriate for this header (the H1 and micro-link are being baseline-aligned rather than top-aligned).
- **Expected**: Remove the undefined `items-end` class. Evaluate whether `flex-between` (which has hardcoded `align-items: flex-end`) is the right choice, or define a separate utility for alignment control.
- **Code Reference**: `cart.html` line 253; `css/layout.css` lines 161–165.

### [BUG-CRT-007] Product image reference `product-3.png` ("She is Grace") — no "She is Grace" product exists in the catalogue
- **Severity**: Major
- **Viewport**: All
- **File**: `cart.html` line 295
- **Description**: The second cart item is labelled "SHE IS GRACE" with variant "IVORY · CURVY" and references `assets/images/product-3.png`. Based on the nav mega menu and site copy, the product range is: She is Timeless, She is Beauty, She is Lust, She is Strength, She is Power, She is You. "She is Grace" does not exist in the defined product catalogue. This is a placeholder naming inconsistency that must be corrected before launch.
- **Expected**: Cart line items should reference real, named products from the catalogue. Replace "SHE IS GRACE" with a valid product name (e.g., "SHE IS TIMELESS").
- **Code Reference**: `cart.html` lines 293–313.

### [BUG-CRT-008] `payment-icons.png` in footer — asset exists but may render incorrectly at small sizes
- **Severity**: Major
- **Viewport**: 375px
- **File**: `cart.html` line 419; `css/components.css` line 1024
- **Description**: The footer payment icons image (`assets/images/payment-icons.png`) is constrained to `height: 32px; width: auto`. At 375px mobile viewport, the `.footer-bottom-row` uses `display: flex; justify-content: space-between` but the responsive.css overrides this to `display: block` at 1024px (line 20). When displayed as a block, the payment icons row becomes a stacked layout — the payment icons image drops below the brand/copyright text, which is acceptable layout-wise, but the image may appear undersized or poorly cropped depending on aspect ratio of the source PNG. No `max-width` is defined for the payment icons image at mobile.
- **Expected**: Add `max-width: 100%` to `.payment-methods-img` and verify the image asset renders legibly at 32px height on mobile.
- **Code Reference**: `css/components.css` lines 1024–1028; `css/responsive.css` line 20.

---

## Minor

### [BUG-CRT-009] Cart page `padding-top: 80px` on `.cart-page` — no compensation for sticky header height
- **Severity**: Minor
- **Viewport**: All
- **File**: `cart.html` inline `<style>` block (line 17)
- **Description**: `.cart-page` has `padding-top: 80px`. The sticky header is 94px tall (set in `css/components.css` line 181) and the announcement bar is 38px (total: 132px). Since the announcement bar is not sticky (only the `.site-header` is), the effective header height after scroll is 94px. The 80px `padding-top` on the cart page is 14px short of the sticky header height — meaning on initial load before any scroll the cart content begins 14px too high, potentially hiding slightly behind the sticky header.
- **Expected**: `padding-top` should be at minimum `94px` (matching the sticky `.site-header` height), or use `padding-top: var(--header-height)` for token-based alignment. A better approach is `padding-top: 120px` to give clear separation between header bottom and page title.
- **Code Reference**: `cart.html` line 17; `css/components.css` line 181.

### [BUG-CRT-010] `.cart-table th` column for TOTAL uses inline `text-align: right` on `<th>` but relies on `<td>` also having inline style — no CSS class
- **Severity**: Minor
- **Viewport**: All
- **File**: `cart.html` lines 264, 289, 312
- **Description**: The TOTAL column header `<th>` and both price `<td>` cells use inline `style="text-align: right;"`. This is inconsistent with the rest of the codebase which uses utility classes or component styles. If the table is later restyled or refactored (especially for mobile card layout), these inline styles will conflict.
- **Expected**: Define a `.col-total` or `.text-right` utility class in `css/layout.css` and apply it consistently to the TOTAL column header and data cells.
- **Code Reference**: `cart.html` lines 264, 289, 312.

### [BUG-CRT-011] `.qty-selector button` has no explicit font-family or color — may inherit unexpected styles
- **Severity**: Minor
- **Viewport**: All
- **File**: `cart.html` inline `<style>` block (lines 81–83)
- **Description**: The quantity stepper `+` and `-` buttons inside `.qty-selector` have `padding: 8px 12px` but no explicit `font-family`, `font-size`, `color`, or `background-color`. While `button` elements inherit font via `css/layout.css` (line 47 — `font: inherit`), the visual rendering of `-` and `+` glyphs depends entirely on browser default button rendering. There is no hover state, active state, or focus indicator defined for these buttons.
- **Expected**: Add explicit `color: var(--color-mocha)`, `background: transparent`, and a `:hover` or `:focus-visible` state for `.qty-selector button`. Add a `:focus-visible` outline for keyboard accessibility.
- **Code Reference**: `cart.html` lines 81–83.

### [BUG-CRT-012] Cart product `<h3>` uses class `font-sans` but `<h3>` elements are globally assigned `font-family: var(--font-serif)` — specificity conflict
- **Severity**: Minor
- **Viewport**: All
- **File**: `cart.html` lines 275, 298; `css/layout.css` lines 64–71
- **Description**: `css/layout.css` applies `font-family: var(--font-serif)` to all `h1, h2, h3, .font-serif` elements (line 64). In the cart, the product name `<h3>` elements have `class="font-sans text-md font-weight-normal mb-2"` to override this to sans-serif. However `font-sans` (defined in `css/layout.css`) is not mapped to a font-family property directly — the class `.font-sans` does not appear to be defined anywhere in the CSS files as a rule. The product name renders in the correct sans-serif font only if the browser falls through to the body font-family, which happens to be `var(--font-sans)`. This is accidental specificity resolution rather than intentional styling.
- **Expected**: Define `.font-sans { font-family: var(--font-sans); }` explicitly in `css/layout.css` to make the intent clear and prevent future regressions. Additionally, `font-weight-normal` and `text-md` classes do not appear to be defined in the design system — these should be verified or replaced with valid utility classes.
- **Code Reference**: `cart.html` lines 275, 298; `css/layout.css`.

### [BUG-CRT-013] Cart img thumbnail uses `height: 80%` with `object-fit: contain` — may produce off-brand tall whitespace in image box
- **Severity**: Minor
- **Viewport**: All
- **File**: `cart.html` inline `<style>` block (lines 68–71)
- **Description**: `.cart-img-wrap img` is set to `height: 80%` with `object-fit: contain`. The `.cart-img-wrap` is `120px × 120px`. The image will be constrained to 96px tall, centred within the 120px box, but with `object-fit: contain` on a non-square candle product image (tall portrait format), there will be horizontal letterboxing whitespace on the sides. The product images are portrait-oriented candle shots, so this will produce visible side padding rather than filling the box.
- **Expected**: Use `width: 100%; height: 100%; object-fit: cover;` if the product image framing is designed to fill, or `width: auto; height: 80%; object-fit: contain; margin: auto;` if whitespace is acceptable. The `.cart-img-wrap` background colour (`var(--bg-secondary)`) provides a warm fill which softens the whitespace — but this should be a deliberate choice.
- **Code Reference**: `cart.html` lines 58–71.

### [BUG-CRT-014] `checkout.css` is imported from `assets/css/checkout.css` — `.payment-box` has `border-radius: 4px` violating brand's 0px radius rule
- **Severity**: Minor
- **Viewport**: All
- **File**: `assets/css/checkout.css` line 125; `css/design-tokens.css` line 48
- **Description**: Even though `checkout.css` is primarily a checkout page stylesheet, it is imported by `cart.html` (line 13). The `.payment-box` rule within it has `border-radius: 4px`. The brand standard enforces `--radius-max: 0px` (strict sharp corners everywhere). The `.payment-box` rule applies to checkout content not present on the cart page, so this does not visually impact the cart, but importing `checkout.css` on the cart page introduces scoped risk and adds unnecessary stylesheet weight.
- **Expected**: Remove the `checkout.css` import from `cart.html` entirely, or extract only the shared rules (if any) into the main `components.css`. The `.summary-img-wrap` in checkout.css also has `border-radius: 4px` — violating brand standards.
- **Code Reference**: `cart.html` line 13; `assets/css/checkout.css` lines 125, 166.

### [BUG-CRT-015] Cart page title "YOUR BAG" h1 font-size is 32px — conflicts with token scale
- **Severity**: Minor
- **Viewport**: All
- **File**: `cart.html` inline `<style>` block (lines 26–28)
- **Description**: `.cart-header h1` has `font-size: 32px` defined inline. The design token for `--text-h1` is `48px` and `--text-h2` is `32px`. A cart page title in RL Limo serif should likely be a proper H1 at 48px for typographic hierarchy — or explicitly use `--text-h2` token if the smaller size is intentional. As written, the 32px override creates a visual inconsistency: the H1 heading appears the same size as an H2, undermining the page hierarchy.
- **Expected**: Either set `font-size: var(--text-h1)` (48px) for a proper hero heading, or if 32px is the intended design decision, apply `class="font-serif text-h2"` to the element and remove the inline override — use token classes rather than hardcoded px values.
- **Code Reference**: `cart.html` lines 26–28, 254.

---

## Responsive Issues

### 1024px (Tablet)

#### [BUG-CRT-R01] Desktop nav (`header-bottom`) still visible at exactly 1024px — breakpoint boundary error
- **Severity**: Major (responsive)
- **Viewport**: 1024px
- **File**: `css/responsive.css` line 15; `css/components.css` line 234
- **Description**: The desktop navigation (`.header-bottom`) is hidden via `display: none` in the `@media (max-width: 1024px)` block. At exactly 1024px viewport width, the media query triggers and the nav is hidden — but the hamburger button appears. At viewports of 1025px the full desktop nav is shown, including SHOP, GIFTS, OUR STORY, YOUR STORY, CONTACT US. The screenshot captured at the 1024px breakpoint shows the desktop nav is still visible, suggesting the browser window inner width is slightly above 1024px content width due to scrollbar or window chrome. The effective breakpoint should be shifted to `max-width: 1100px` or implemented more robustly.
- **Expected**: The desktop/mobile nav transition should be clean. Either raise the breakpoint to 1100px or use a container-query approach. The hamburger must also be confirmed visible and tappable when the desktop nav hides.

#### [BUG-CRT-R02] Cart table columns compress dangerously at 1024px — no responsive adaptation
- **Severity**: Major (responsive)
- **Viewport**: 1024px
- **File**: `cart.html` inline styles; `css/responsive.css`
- **Description**: At 1024px with 48px gutters (96px total), the effective content width is approximately 928px. The cart table distributes: PRODUCT (50% = 464px), PRICE (15% = 139px), QUANTITY (20% = 186px), TOTAL (15% = 139px). The QUANTITY column at 186px wide contains a 100px qty selector — this works, but it leaves unused space. More critically, if any column content wraps (long product names), the table becomes visually unbalanced. No responsive rules adjust column widths at this breakpoint.
- **Expected**: At 1024px, consolidate the table to show PRODUCT (60%), QUANTITY+PRICE combined or rearranged, and TOTAL. Or begin transitioning to a card layout at this breakpoint.

#### [BUG-CRT-R03] Cart summary box right-aligned at 1024px — creates wide whitespace on left
- **Severity**: Minor (responsive)
- **Viewport**: 1024px
- **File**: `cart.html` inline `<style>` (lines 93–99)
- **Description**: `.cart-summary-box` has `max-width: 480px` and `margin-left: auto`. At 1024px this means the summary is right-aligned with roughly 448px of blank space to its left. A luxury cart page at this viewport should either centre the summary box or make it full-width. The current right-aligned treatment looks structurally weak at tablet widths.
- **Expected**: At `max-width: 1024px` add a rule: `.cart-summary-box { max-width: 100%; margin-left: 0; }` so the summary spans the full content width.

### 375px (Mobile)

#### [BUG-CRT-R04] Cart table completely unresponsive at 375px — critical layout overflow
- **Severity**: Critical (responsive)
- **Viewport**: 375px
- **File**: `cart.html`; `css/responsive.css`
- **Description**: This is the mobile manifestation of BUG-CRT-001. The cart table's four-column layout has no mobile breakpoint. At 375px (with 32px total gutters = 343px content width), the PRODUCT column alone at 50% would be 171px — not enough to display a 120px image plus product name/variant text side by side. The PRICE, QUANTITY, and TOTAL columns each receive approximately 51–68px, making the quantity stepper (100px wide) overflow its allocated column entirely. The table overflows horizontally.
- **Expected**: At ≤ 768px, the cart table must be restructured. Recommended approach: hide the `<thead>`, convert each `<tr>` into a flex card with product image on the left and all text/price/qty details stacked on the right, with the remove link and total at the bottom of each card.

#### [BUG-CRT-R05] Announcement bar text truncated or wraps awkwardly at 375px
- **Severity**: Minor (responsive)
- **Viewport**: 375px
- **File**: `cart.html` line 112; `css/components.css` lines 123–138
- **Description**: The announcement bar text "LAUNCHING MARCH 2026 - JOIN THE WAIT LIST FOR EARLY ACCESS" at 10px with `letter-spacing: 0.1em` is approximately 280px wide — tight but should fit within 375px with 20px padding. However, the bar has `height: var(--announcement-height)` fixed at 38px with `display: flex; align-items: center`. If the text wraps to two lines (on very narrow or if font rendering adds width), the bar will clip content. No `white-space: nowrap` or `overflow: hidden` is set.
- **Expected**: Add `white-space: nowrap; overflow: hidden; text-overflow: ellipsis;` to `.announcement-bar` to prevent multi-line wrapping within the fixed-height bar. Or add a responsive rule to shorten the text at mobile (via a data attribute + CSS content trick, or by truncation logic).

#### [BUG-CRT-R06] Footer link columns at 375px — no single-column mobile layout defined
- **Severity**: Major (responsive)
- **Viewport**: 375px
- **File**: `css/components.css` lines 1031–1040; `css/responsive.css`
- **Description**: The footer `.footer-main-grid` collapses to `1fr 1fr` (two columns) at `max-width: 1024px` in `css/components.css`. At 375px the two-column grid is still in effect — meaning five columns worth of links squeeze into two columns with 16–20px gutters. The link text "Plus Size Body Candles" and "Corporate Gifting" are likely wrapping mid-word or truncating. There is no `@media (max-width: 480px)` or `@media (max-width: 375px)` rule that collapses the footer to a single column.
- **Expected**: Add `@media (max-width: 480px) { .footer-main-grid { grid-template-columns: 1fr; } }` so each footer section stacks vertically on mobile. The newsletter col already spans 2 columns at 1024px but at single-column that span should be removed.

