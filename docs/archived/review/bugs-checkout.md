<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# Bugs — checkout.html (Checkout Page)

> Audit Date: 2026-03-01
> Reference: `screenshots/checkout-page.png`
> Auditor: QA Visual Audit (Static HTML Analysis)

---

## Critical

### [BUG-CHK-001] Undefined CSS Token `--text-base` Causes Silent Color Fallback
- **File:** `assets/css/checkout.css` — lines 41, 67, 76, 117
- **Token used:** `var(--text-base)`
- **Status:** Token is NOT defined in `css/design-tokens.css`. The design tokens define `--text-primary` (mapped to `#3F3229` mocha) but there is no `--text-base` alias.
- **Impact:** All form labels, breadcrumb text, and checkbox labels will render in the browser's inherited/cascade fallback color (likely black `#000000`), violating the brand standard of warm neutral tones only. This is a brand color compliance failure.
- **Expected token:** `var(--text-primary)` or `var(--color-mocha)` (`#3F3229`)
- **Affected elements:** `.checkout-breadcrumbs a/span`, `.form-label`, `.form-input`, `.checkbox-group label`

---

### [BUG-CHK-002] Full Navigation Header Instead of Minimal Checkout Header
- **File:** `checkout.html` — lines 24–157
- **Description:** The page specification requires a minimal header (logo only, no full nav). The current implementation uses the full `site-header` component with: search icon, account icon, wishlist icon, cart icon, hamburger button, full desktop navigation (`header-bottom` with mega menu including SHOP / GIFTS / OUR STORY / YOUR STORY / CONTACT US), search overlay, and the complete mobile menu overlay (lines 434–456).
- **Reference screenshot:** Confirms a clean, simplified header: logo centred, no mega menu, no bottom nav bar visible (nav shows SHOP, OUR STORY, YOUR STORY, CONTACT US only — no GIFTS — and no mega menu hover state). The header in the reference is visually equivalent to the full site header without any bottom nav strip.
- **Impact:** On a checkout page, a full navigation with mega menus and all icon buttons creates distraction, increases abandonment risk, and deviates from standard e-commerce checkout UX pattern (lock the checkout). The mega menu image reference `assets/images/product-2.png` also loads unnecessarily.
- **Severity:** Critical — functional UX and scope deviation.

---

### [BUG-CHK-003] Payment Box Has `border-radius: 4px` — Violates 0px Sharp-Corners Brand Rule
- **File:** `assets/css/checkout.css` — line 126
- **Code:** `.payment-box { border-radius: 4px; }`
- **Brand standard:** `--radius-max: 0px` — all border-radius must be `0px` (sharp corners everywhere). The design token `--radius-max` exists specifically to enforce this.
- **Impact:** The payment card input box renders with rounded corners, inconsistent with the rest of the UI and brand guidelines.
- **Fix:** Change to `border-radius: 0` or `border-radius: var(--radius-max)`.

---

### [BUG-CHK-004] Summary Image Wrapper Has `border-radius: 4px` — Violates 0px Brand Rule
- **File:** `assets/css/checkout.css` — line 165
- **Code:** `.summary-img-wrap { border-radius: 4px; }`
- **Impact:** Product thumbnail boxes in the order summary render with rounded corners, violating the sharp-corners brand standard.
- **Fix:** Change to `border-radius: 0` or `border-radius: var(--radius-max)`.

---

## Major

### [BUG-CHK-005] Quantity Badge Uses `border-radius: 50%` — Violates 0px Brand Rule
- **File:** `assets/css/checkout.css` — line 181
- **Code:** `.qty-badge { border-radius: 50%; }`
- **Description:** The circular quantity badge on product thumbnails uses a 50% border-radius, rendering as a circle. Brand standard requires 0px radius.
- **Note:** This is a minor design judgment call — circular badges are a near-universal UX pattern for quantity indicators. However, it technically violates the stated brand standard. Flagged as Major for team awareness.
- **Fix:** Requires design decision. If brand standard is absolute, change to `border-radius: 0` and adjust badge dimensions to a square pill shape.

---

### [BUG-CHK-006] `DELIVERY METHOD` Section Missing from Form
- **File:** `checkout.html`
- **Description:** The checkout page specification requires three form sections: Contact Info, Shipping Address, and Delivery Method. The current HTML contains only Contact and Shipping Address sections. The Delivery Method step (shipping method selector, e.g. Standard / Express) is entirely absent.
- **Impact:** Incomplete checkout flow. User cannot select delivery method before being taken to payment.
- **Expected:** A section with radio buttons for shipping options (e.g. Standard Shipping £5.00, Express £10.00) between Shipping Address and Payment.

---

### [BUG-CHK-007] Announcement Bar Present on Checkout Page — Should Be Hidden
- **File:** `checkout.html` — lines 18–21
- **Description:** The announcement bar `LAUNCHING MARCH 2026 - JOIN THE WAIT LIST FOR EARLY ACCESS` is rendered above the header on the checkout page. The reference screenshot (`checkout-page.png`) shows the dark announcement bar at the very top, which matches the site-wide bar. However, on a checkout/conversion page, the announcement bar typically should be suppressed to eliminate distractions.
- **Reference:** The `checkout-page.png` screenshot does show the announcement bar present, so this matches the reference. This is flagged as a major UX concern for the team's review rather than a visual regression.
- **Status:** Matches reference screenshot visually but flagged for UX consideration.

---

### [BUG-CHK-008] Inline `style` Overrides Used on Multiple Form Inputs — Hard to Maintain
- **File:** `checkout.html` — lines 237, 243, 247, 253
- **Description:** Multiple inline `style` attributes are used directly on form elements:
  - Line 237: `style="background:#fff;"` on card number input
  - Line 243: `style="background:#fff;"` on expiry input
  - Line 247: `style="background:#fff;"` on CVC input
  - Line 253: `style="width: 100%;"` on the Complete Order button (duplicate, already has `w-full` class that doesn't exist in CSS — see BUG-CHK-009)
- **Impact:** These inline styles cannot be overridden by media queries or theming, creating maintenance debt and potential responsive issues. White `#fff` on inputs also technically uses a pure-white colour, violating the brand's "no pure black or white" guideline.
- **Brand violation:** Input backgrounds should use `var(--bg-primary)` (`#F9F6F2`) or a warm white, not `#ffffff`.

---

### [BUG-CHK-009] CSS Utility Class `w-full` Not Defined Anywhere
- **File:** `checkout.html` — line 253; `checkout.css`, `layout.css`, `components.css`, `responsive.css`
- **Code:** `<button class="btn-solid mt-4 w-full" style="width: 100%;">`
- **Description:** The class `w-full` is applied to the "COMPLETE ORDER" button but is not defined in any of the four CSS files loaded by checkout.html (`design-tokens.css`, `layout.css`, `components.css`, `responsive.css`) nor in `checkout.css`. The button only works at full width due to the fallback inline `style="width: 100%;"`.
- **Impact:** Reliance on undefined class with inline style fallback. If the inline style is ever removed, the button will not be full-width.
- **Fix:** Either define `.w-full { width: 100%; }` in `layout.css`, or remove the class and keep the inline style (though inline styles should be avoided per BUG-CHK-008).

---

### [BUG-CHK-010] CSS Utility Class `mt-12` Not Defined Anywhere
- **File:** `checkout.html` — lines 184, 229; `layout.css`
- **Code:** `<div class="checkout-section mt-12">` (appears twice)
- **Description:** The class `mt-12` is applied to checkout sections but is not defined in any loaded CSS file. The `layout.css` defines spacing utilities up to `mt-8` (32px) but not `mt-12`. This means the top margin between form sections is silently 0px.
- **Impact:** The Contact, Shipping Address, and Payment sections lose their intended vertical separation. All three sections will appear stacked with no spacing between them, creating a visually cramped layout.
- **Fix:** Add `.mt-12 { margin-top: 48px; }` to `layout.css`, or replace with `.checkout-section { margin-bottom: 48px; }` which is already defined in `checkout.css` line 46 (though this relies on bottom margin on the element itself, not top on the next — which should work, but `mt-12` is redundant if the section already has `margin-bottom: 48px`). The redundant class should be removed to avoid confusion.

---

### [BUG-CHK-011] Order Summary Column Has `min-height: 100vh` — Causes Excessive Page Height
- **File:** `assets/css/checkout.css` — line 134
- **Code:** `.order-summary-col { min-height: 100vh; }`
- **Description:** The right column (order summary) is set to a minimum height of 100 viewport heights. When the content in the right column is shorter than 100vh (which it almost always is for a 2-item order), this forces the entire checkout layout to expand to full viewport height. This creates a large empty beige region below the perk items in the right column.
- **Reference screenshot:** Shows the right column extending down the full page height with empty space below the "Free shipping over £50" perk — visible in the screenshot. While this may be intentional for visual balance, it is flagged as it inflates page height and can cause scroll issues on shorter viewports.
- **Impact:** On tablet and mobile where columns stack, this min-height will cause a blank 100vh empty grey block where the summary column renders before the form.

---

### [BUG-CHK-012] `product-2.png` Mega Menu Image Loaded on Checkout Page (Unnecessary Asset)
- **File:** `checkout.html` — line 132
- **Code:** `<img src="assets/images/product-2.png" alt="Featured Body Candles">`
- **Description:** The mega menu image is part of the full navigation structure copied to the checkout page. This image loads on every checkout page load even though the mega menu is never triggered on checkout. This is dead weight.
- **Impact:** Unnecessary network request, slows page load for conversion-critical page.

---

## Minor

### [BUG-CHK-013] Checkout Breadcrumb: `INFORMATION` Active State Lacks Visual Distinction
- **File:** `assets/css/checkout.css` — lines 40–43
- **Description:** The `.active` breadcrumb class only changes `color: var(--text-base)` (which is broken per BUG-CHK-001). Even with the correct colour, the active breadcrumb has no underline, font-weight change, or other visual differentiation beyond colour. The reference screenshot shows "INFORMATION" in a slightly darker tone — acceptable, but a subtle underline or weight would improve clarity.
- **Severity:** Minor UX/accessibility issue.

---

### [BUG-CHK-014] `GIFTS` Navigation Link Present in Desktop Nav but Missing from Reference
- **File:** `checkout.html` — line 137; Reference: `checkout-page.png`
- **Description:** The desktop nav in the HTML includes `<a href="shop.html">GIFTS</a>` as a standalone link. The reference screenshot shows only: SHOP | OUR STORY | YOUR STORY | CONTACT US — no GIFTS link.
- **Impact:** Minor content mismatch vs. reference. If the nav is intended to be suppressed on checkout, this entire nav section should be removed (see BUG-CHK-002). If it is kept, the GIFTS link should be added to match the full site nav, or removed to match the reference.

---

### [BUG-CHK-015] Payment Section Has No Payment Method Icons / Brand Logos Above Card Fields
- **File:** `checkout.html` — lines 229–256
- **Description:** The checkout spec requires payment icons to be visible on the checkout form. The current payment section shows only raw card number/expiry/CVC inputs with no Visa/Mastercard/Amex/Apple Pay icons displayed near the payment form. Payment icons only appear in the footer (`assets/images/payment-icons.png`).
- **Reference screenshot:** The reference does not show payment logos in the payment form section either. Flagged as a spec deviation vs. the stated brief requirements.
- **Impact:** Users lack trust signals at the point of card entry.

---

### [BUG-CHK-016] `COMPLETE ORDER` Button Uses `btn-solid` Which Applies `background-color: var(--color-mocha)` — But Reference Shows Near-Black `#2D2B27` (Slate)
- **File:** `checkout.html` line 253; `css/components.css` lines 33–37
- **Description:** The `.btn-solid` class sets `background-color: var(--color-mocha)` which is `#3F3229`. The reference screenshot shows the CTA button in a very dark near-black tone consistent with `var(--color-slate)` (`#2D2B27`). While these are visually close, the slate is the designated CTA dark colour per brand spec.
- **Impact:** Minor visual discrepancy. Could be resolved by using `.btn-hero` or adding a checkout-specific button override.

---

### [BUG-CHK-017] Search Overlay Background Uses Pure White `#ffffff` — Brand Violation
- **File:** `css/components.css` — line 149
- **Code:** `.search-overlay { background-color: #ffffff; }`
- **Description:** The search overlay uses pure white `#ffffff`, violating the brand standard of "no pure black or white — all warm neutral tones." Should use `var(--bg-primary)` (`#F9F6F2`) or `var(--color-stone)`.
- **Note:** The search overlay is present in the checkout page header (since the full header is included). This is a global component bug surfaced by BUG-CHK-002.

---

### [BUG-CHK-018] Site Header Uses `background-color: #ffffff` — Brand Violation
- **File:** `css/components.css` — line 178
- **Code:** `.site-header { background-color: #ffffff; }`
- **Description:** The site header background is pure white. Per brand guidelines, no pure white should be used. Should be `var(--bg-primary)` (`#F9F6F2`). Reference screenshot shows a very light warm cream header that matches sand, not pure white.
- **Note:** This is a global component bug, manifests on checkout due to the full header being included.

---

### [BUG-CHK-019] `font-sans` Class Applied to `h2` Tags Within Checkout Sections — Conflicts with Global `h2` Serif Rule
- **File:** `checkout.html` — lines 261, 271; `assets/css/checkout.css` — line 49; `css/layout.css` — lines 64–71
- **Description:** The `checkout-section h2` rule applies `font-family: var(--font-sans)` via CSS, but `h2` elements globally are set to `font-family: var(--font-serif)` in `layout.css`. The checkout CSS correctly overrides this for the form section headings (CONTACT, SHIPPING ADDRESS, PAYMENT). However, the ORDER SUMMARY `h2` has class `font-sans` applied in HTML (`<h2 class="font-sans">ORDER SUMMARY</h2>`), while it is also governed by `.order-summary-col h2` — which only sets font-size and weight, not font-family. The `font-sans` class adds `font-family: var(--font-sans)` which is correct. But the comment in `checkout.css` line 50 reads `/* Looks like sans-serif here */` suggesting uncertainty about the intended font. In the reference screenshot, section headings (CONTACT, SHIPPING ADDRESS, ORDER SUMMARY) all appear in a clean sans-serif.
- **Impact:** If the `font-sans` class is removed from the ORDER SUMMARY h2, it would fall back to the global serif rule. Low risk currently but architectural inconsistency.

---

### [BUG-CHK-020] `COMPLETE ORDER` Button Has Redundant Class and Inline Style (`mt-4 w-full` + `style="width:100%"`)
- **File:** `checkout.html` — line 253
- **Description:** The button carries `class="btn-solid mt-4 w-full"` plus `style="width: 100%;"`. The `w-full` class is undefined (BUG-CHK-009), and the inline style duplicates the intent. Clean this up to a single source of truth.

---

## Responsive Issues

### 1024px (Tablet)

#### [BUG-CHK-021] Checkout Grid Switches to Two-Column at 1024px But `checkout-form-col` Padding Becomes Too Tight
- **File:** `assets/css/checkout.css` — lines 16–20, 23–26
- **Description:** At 1024px, the grid switches from single column to `1fr 400px`. The left column has `padding-right: 48px` hardcoded. At 1024px the gutter compresses to 48px (from responsive.css). Combined with the 400px fixed right column, the left form column becomes very narrow, leaving minimal breathing room for form labels and inputs across two columns (`form-row`).
- **No responsive override** exists for `checkout-form-col` padding or `form-row` stacking at tablet.
- **Impact:** Two-column form rows (First Name/Last Name, City/Postcode, Expiry/CVC) will be very cramped at 1024px.

---

#### [BUG-CHK-022] `order-summary-col min-height: 100vh` Creates Giant Empty Block When Stacked at Tablet
- **File:** `assets/css/checkout.css` — line 134
- **Description:** At viewport widths below the breakpoint where the grid becomes single column (which is `min-width: 1024px` — so exactly at 1024px the two-column layout still applies, but just below it stacks). When stacked, the order summary column renders as a full 100vh tall grey block above or below the form. The summary has very little content, so ~80% of this block is dead white/grey space.
- **Impact:** On tablet portrait (768px) and below, the summary column will occupy an entire screen height of empty space.

---

#### [BUG-CHK-023] No `checkout-form-col` Responsive Override for Padding at Tablet
- **File:** `assets/css/checkout.css`
- **Description:** There are no media query overrides in `checkout.css` for `.checkout-form-col`, `.payment-box`, `.order-summary-col`, or `.form-row` at 1024px or 768px. The entire checkout layout has zero responsive CSS beyond the grid column switch at 1024px.
- **Impact:** Form padding, payment box padding (32px), and order summary padding (64px 48px) remain identical across all viewports.

---

### 375px (Mobile)

#### [BUG-CHK-024] `form-row` (Two-Column Input Rows) Not Collapsed to Single Column on Mobile
- **File:** `assets/css/checkout.css` — lines 92–99; `css/responsive.css`
- **Description:** `.form-row { display: flex; gap: 16px; }` has no mobile override anywhere in the codebase. At 375px, the First Name/Last Name, City/Postcode, and Expiry Date/Security Code pairs will render side-by-side in extremely narrow columns (~155px each after gutters), making it nearly impossible to tap and type in the fields.
- **Expected:** `.form-row` should stack to `flex-direction: column` below 768px.
- **Impact:** Critical mobile usability failure — form is practically unusable at 375px.

---

#### [BUG-CHK-025] `COMPLETE ORDER` Button Width Relies on Inline Style — May Not Render Full-Width at 375px if Style Stripped
- **File:** `checkout.html` — line 253
- **Description:** Without `w-full` class being defined, the full-width button depends entirely on the inline style. The `btn-solid` default sizing from `components.css` uses `padding: 18px 40px` with `display: inline-flex` — meaning without the inline style, the button would only be as wide as its text content.
- **Impact:** If the inline style is ever stripped (by a Shopify theme override, CMS sanitisation, etc.), the CTA button becomes a small centred button instead of full-width.

---

#### [BUG-CHK-026] Order Summary Column Renders Below Form at Mobile (Stack Order Not Defined)
- **File:** `assets/css/checkout.css` — lines 9–20
- **Description:** The grid uses `grid-template-columns: 1fr` by default (mobile first), switching to two-column at 1024px+. This means on mobile the order summary column (`order-summary-col`) appears below the form (`checkout-form-col`) because it is the second element in DOM order. Standard checkout UX places the order summary above the form on mobile so users can confirm what they are purchasing before filling out details.
- **Expected:** On mobile, the order summary should appear first (above the form). This requires either reordering the DOM or using `order` CSS property.
- **Impact:** Users must scroll through the entire form to find their order details at the bottom.

---

#### [BUG-CHK-027] Footer Full Width Newsletter and Multi-Column Grid Renders at 375px Without Adequate Stacking
- **File:** `css/components.css` — line 891; `css/responsive.css`
- **Description:** The footer `footer-main-grid` collapses to `1fr 1fr` at 1024px but there is no override below 768px to collapse to single column. At 375px, the footer renders as two columns. The newsletter column spans both columns (correct), but the four link columns render as 2x2 grid at 375px, creating very narrow columns with truncated text.
- **Note:** The footer is included on the checkout page (lines 337–432), adding significant visual weight to a conversion-focused page.

---

#### [BUG-CHK-028] `payment-box` Padding of `32px` Not Reduced on Mobile
- **File:** `assets/css/checkout.css` — line 124
- **Code:** `.payment-box { padding: 32px; }`
- **Description:** No responsive override reduces this padding at mobile viewports. At 375px with a 16px gutter, the payment box inner content area is: 375 - (16px gutter × 2) - (32px padding × 2) = 263px. This is workable but very tight for the two-column Expiry/CVC row inside the payment box (each input would be ~116px wide). Combined with BUG-CHK-024, the inputs become nearly untappable.

---

*Total bugs identified: 28*
*(6 Critical/Major combined: BUG-CHK-001, 002, 003, 004, 006, 024)*

