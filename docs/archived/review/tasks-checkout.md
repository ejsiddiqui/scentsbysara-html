<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# QA Tasks — checkout.html (Checkout Page)

## Status: REVIEWED
## Audit Date: 2026-03-01
## Viewport Tested: 1440px | 1024px | 375px
## Reference: `screenshots/checkout-page.png`
## Method: Static HTML + CSS code analysis with reference screenshot comparison

---

## Section Checklist

### Header
- [ ] FAIL — **Minimal header (logo only)**: Full site header is included with mega menu, all icon buttons, search overlay, and mobile menu overlay. Spec requires logo-only header for checkout. (BUG-CHK-002)
- [ ] FAIL — **Header background colour**: Uses `#ffffff` pure white instead of `var(--bg-primary)` `#F9F6F2`. Brand violation. (BUG-CHK-018)
- [ ] FAIL — **Search overlay colour**: Uses `#ffffff` pure white. Brand violation. (BUG-CHK-017)
- [ ] PASS — **Logo present and centred**: Logo (`SCENTS BY SARA` text) centred correctly via `header-center` grid column.
- [ ] PASS — **Announcement bar**: Present and styled correctly with mocha background and sand text at correct 38px height.
- [ ] FAIL — **Unnecessary mega menu asset load**: `product-2.png` loaded inside mega menu on a checkout page. (BUG-CHK-012)

---

### Breadcrumbs
- [ ] FAIL — **Active state colour**: Uses undefined token `var(--text-base)` — will not render in brand mocha colour. (BUG-CHK-001)
- [ ] PASS — **Breadcrumb content**: BAG / INFORMATION / SHIPPING / PAYMENT — correct steps and correct active step.
- [ ] PASS — **Breadcrumb typography**: 10px uppercase with letter-spacing — matches reference screenshot.

---

### Contact Section
- [ ] FAIL — **Label colour**: Uses undefined `var(--text-base)` token. (BUG-CHK-001)
- [ ] PASS — **Email input**: Present, correct placeholder `your@email.com`, correct styling.
- [ ] PASS — **Newsletter checkbox**: Present and pre-checked. Label text matches reference.
- [ ] PASS — **Section heading `CONTACT`**: Correct size (24px), correct font (sans-serif via `.checkout-section h2`).

---

### Shipping Address Section
- [ ] FAIL — **Section spacing (mt-12)**: Utility class `mt-12` not defined in any CSS file — no top margin applied. (BUG-CHK-010)
- [ ] FAIL — **Label colour**: Uses undefined `var(--text-base)` token. (BUG-CHK-001)
- [ ] PASS — **Country/Region select**: Present with correct options (UK, US, Europe), custom chevron arrow via SVG data-URI.
- [ ] PASS — **First Name / Last Name row**: Present as two-column `form-row`.
- [ ] PASS — **Address input**: Present with placeholder `Street address`.
- [ ] PASS — **City / Postcode row**: Present as two-column `form-row`.
- [ ] PASS — **Save information checkbox**: Present and unchecked by default.
- [ ] FAIL — **Two-column form rows at 375px**: `form-row` does not collapse to single column on mobile — inputs become unusable at 375px. (BUG-CHK-024)

---

### Delivery Method Section
- [ ] FAIL — **MISSING SECTION**: Delivery Method section entirely absent from the page. Spec requires shipping method selector between address and payment. (BUG-CHK-006)

---

### Payment Section
- [ ] FAIL — **Section spacing (mt-12)**: Utility class `mt-12` not defined — no top margin applied. (BUG-CHK-010)
- [ ] FAIL — **Payment box border-radius**: `.payment-box` uses `border-radius: 4px` — violates 0px brand rule. (BUG-CHK-003)
- [ ] FAIL — **Input background colour**: Card fields use inline `style="background:#fff;"` — pure white, violates brand standard. (BUG-CHK-008)
- [ ] FAIL — **Payment icons missing in form**: No Visa/Mastercard/Amex logos shown at point of card entry. (BUG-CHK-015)
- [ ] PASS — **Card number input**: Present with correct placeholder `1234 5678 9012 3456`.
- [ ] PASS — **Expiry Date input**: Present with correct placeholder `MM / YY`.
- [ ] PASS — **Security Code input**: Present with correct placeholder `CVC`.
- [ ] FAIL — **Expiry/CVC row at 375px**: Two-column row not collapsed on mobile — fields become too narrow to use. (BUG-CHK-024, BUG-CHK-028)
- [ ] FAIL — **Security note colour**: Uses `text-muted` class which resolves correctly, but the `text-sm` class should match reference rendering.

---

### CTA Button (Complete Order)
- [ ] PASS — **Button present**: "COMPLETE ORDER" button exists.
- [ ] PASS — **Button full width at desktop**: Renders full width via inline `style="width: 100%"`.
- [ ] PASS — **Button dark background**: Uses `.btn-solid` with `var(--color-mocha)` `#3F3229` — dark, close to spec.
- [ ] FAIL — **Button colour vs. spec**: Reference suggests slate `#2D2B27` for CTA, current uses mocha `#3F3229`. Minor mismatch. (BUG-CHK-016)
- [ ] FAIL — **`w-full` class undefined**: Class has no CSS definition — button relies entirely on inline style fallback. (BUG-CHK-009)
- [ ] FAIL — **Redundant inline style**: `style="width: 100%"` duplicates undefined `w-full` class intent. (BUG-CHK-020)
- [ ] PASS — **Zero border-radius on button**: `button { border-radius: var(--radius-max) }` in `layout.css` global reset enforces 0px.
- [ ] PASS — **Typography**: `COMPLETE ORDER` uppercase with letter-spacing, correct font.
- [ ] PASS — **Legal disclaimer text**: Present below button, 10px inline font-size, centred.

---

### Order Summary (Right Column)
- [ ] PASS — **"ORDER SUMMARY" heading**: Present at correct size with `font-sans` class.
- [ ] PASS — **Product line items**: Two products present (SHE IS LUST, SHE IS GRACE) with correct variant labels and prices.
- [ ] PASS — **Product images**: `product-1.png` and `product-3.png` both exist in `assets/images/`. No broken images.
- [ ] FAIL — **Product image wrapper border-radius**: `.summary-img-wrap` uses `border-radius: 4px` — violates 0px brand rule. (BUG-CHK-004)
- [ ] FAIL — **Quantity badge border-radius**: `.qty-badge` uses `border-radius: 50%` — violates 0px brand rule. (BUG-CHK-005)
- [ ] PASS — **Quantity badges**: Correct quantities (2 for SHE IS LUST, 1 for SHE IS GRACE). Correct mocha background and sand text.
- [ ] PASS — **Subtotal**: £60.78 — mathematically correct (£40.52 + £20.26 = £60.78).
- [ ] PASS — **Shipping**: £5.00.
- [ ] PASS — **Tax (VAT)**: £12.16.
- [ ] PASS — **Total**: £77.94 — mathematically correct (£60.78 + £5.00 + £12.16 = £77.94).
- [ ] PASS — **Grand total typography**: Correct 24px font size, `font-sans`.
- [ ] PASS — **Totals divider lines**: `border-top` on `.summary-totals` and `.summary-perks` — correct.
- [ ] PASS — **Perk items**: "Secure checkout" and "Free shipping over £50" with correct SVG icons.
- [ ] FAIL — **Right column min-height**: `min-height: 100vh` causes excessive page height and empty grey block on mobile. (BUG-CHK-011)
- [ ] FAIL — **Background colour**: `.order-summary-col` uses `var(--bg-secondary)` (`#E7E3DC` stone) — correct per brand. PASS on colour.

---

### Footer
- [ ] FAIL — **Full footer on checkout page**: A full multi-column footer with newsletter, social links, and 4 link columns is included. Standard checkout pages suppress the footer or show a minimal version. Adds distraction and page weight to a conversion-critical page.
- [ ] PASS — **Payment icons in footer**: `assets/images/payment-icons.png` referenced in footer — file exists.
- [ ] PASS — **Footer colours**: Uses `var(--bg-secondary)` and `var(--color-mocha)` — correct warm tones.
- [ ] PASS — **Footer copyright**: "© 2026 SCENTS BY SARA. ALL RIGHTS RESERVED" — current year correct.
- [ ] FAIL — **Footer grid at 375px**: Multi-column footer not fully collapsed below 768px. (BUG-CHK-027)

---

### Brand Standards Compliance
- [ ] FAIL — **`--text-base` token undefined**: Used 4 times in `checkout.css`, not defined in `design-tokens.css`. (BUG-CHK-001)
- [ ] FAIL — **0px border-radius**: Three violations — payment box (4px), summary image wrapper (4px), quantity badge (50%). (BUG-CHK-003, 004, 005)
- [ ] FAIL — **No pure white/black**: Header `#ffffff`, search overlay `#ffffff`, card input `#ffffff` via inline style. (BUG-CHK-008, 017, 018)
- [ ] PASS — **Font loading**: RL Limo via Adobe Typekit (`abn0bto.css`), Suisse Int'l via local woff2 files — both correctly loaded. Fonts exist in `assets/fonts/`.
- [ ] PASS — **Container max-width**: `.container` uses `var(--container-max)` (1920px) with `var(--gutter)` (100px at desktop) — correct.
- [ ] PASS — **Colour palette**: Sand, stone, mocha, slate, taupe — all used correctly across page where tokens are defined.

---

### Accessibility
- [ ] PASS — **Form labels**: All inputs have corresponding `<label>` elements with matching `for`/`id` pairs.
- [ ] PASS — **Icon buttons**: All `<button>` elements have `aria-label` attributes.
- [ ] PASS — **Hamburger button**: Has `aria-expanded="false"` attribute.
- [ ] FAIL — **Colour contrast risk**: `var(--text-base)` falls back to an undefined colour — form labels may render in incorrect contrast ratio if browser defaults to black on sand background.

---

### Asset Check
- [ ] PASS — `assets/images/product-1.png` — exists (used for SHE IS LUST)
- [ ] PASS — `assets/images/product-3.png` — exists (used for SHE IS GRACE)
- [ ] PASS — `assets/images/payment-icons.png` — exists (footer payment row)
- [ ] PASS — `assets/images/product-2.png` — exists (mega menu — unnecessary load)
- [ ] PASS — `assets/fonts/SuisseIntl-Regular.woff2` — exists
- [ ] PASS — `assets/fonts/SuisseIntl-Light.woff2` — exists
- [ ] PASS — `assets/fonts/SuisseIntl-Bold.woff2` — exists
- [ ] PASS — Adobe Typekit link — `https://use.typekit.net/abn0bto.css` — external CDN, cannot verify without browser
- [ ] PASS — `assets/js/main.js` — exists (handles scroll + mobile menu)
- [ ] FAIL — No checkout-specific JS validation (no client-side form validation, no card formatting, no field masking)

---

## Responsive Summary

### 1440px Desktop
- Layout: Two-column grid (form left, summary right 400px fixed) — renders correctly
- Header: Full site header renders — should be minimal for checkout
- Typography: All sizes appropriate at this viewport
- Gutters: 80px (correct per responsive.css 1440px override)
- Issues: BUG-CHK-001, 002, 003, 004, 005, 006, 008, 009, 010, 011, 012, 013, 016, 017, 018, 019

### 1024px Tablet
- Layout: Two-column grid still active at exactly 1024px (`min-width: 1024px`)
- Gutters: 48px
- Navigation: `header-bottom` hidden, hamburger visible — correct
- Issues: BUG-CHK-021 (cramped form rows), BUG-CHK-022 (100vh min-height), BUG-CHK-023 (no responsive overrides for checkout)

### 375px Mobile
- Layout: Single-column (summary below form)
- Gutters: 16px
- Critical: BUG-CHK-024 (form-row not stacking — CRITICAL usability failure)
- Issues: BUG-CHK-024, 025, 026, 027, 028

---

## Summary

**28 bugs found across the checkout page**

| Severity | Count | Bug IDs |
|----------|-------|---------|
| Critical | 4 | BUG-CHK-001, 002, 003, 004 |
| Major | 8 | BUG-CHK-005, 006, 007, 008, 009, 010, 011, 012 |
| Minor | 7 | BUG-CHK-013, 014, 015, 016, 017, 018, 019, 020 |
| Responsive (1024px) | 3 | BUG-CHK-021, 022, 023 |
| Responsive (375px) | 5 | BUG-CHK-024, 025, 026, 027, 028 |

---

## Priority Action List (Fix Order)

1. **[P0]** Define `--text-base` token in `design-tokens.css` OR replace all `var(--text-base)` with `var(--text-primary)` in `checkout.css` (BUG-CHK-001)
2. **[P0]** Add `flex-direction: column` override for `.form-row` at ≤768px in `responsive.css` (BUG-CHK-024 — mobile form unusable)
3. **[P0]** Replace full site header with a minimal checkout header (logo only + cart icon) (BUG-CHK-002)
4. **[P1]** Fix all `border-radius` violations: payment box, summary img wrap, qty badge (BUG-CHK-003, 004, 005)
5. **[P1]** Add Delivery Method form section between Shipping Address and Payment (BUG-CHK-006)
6. **[P1]** Define `.w-full` utility in `layout.css` and define `.mt-12` utility (BUG-CHK-009, 010)
7. **[P1]** Remove inline `style="background:#fff;"` on card inputs — replace with CSS class using `var(--bg-primary)` (BUG-CHK-008)
8. **[P1]** Reduce or eliminate `min-height: 100vh` on `.order-summary-col` (BUG-CHK-011)
9. **[P2]** Add checkout-specific responsive overrides for form padding, payment box, order summary at 768px and 375px (BUG-CHK-023)
10. **[P2]** Fix mobile stack order — order summary should appear above form at 375px (BUG-CHK-026)
11. **[P2]** Replace `#ffffff` header and search overlay backgrounds with warm neutral tokens (BUG-CHK-017, 018)
12. **[P3]** Add payment trust icons (Visa/Mastercard/etc.) near payment form (BUG-CHK-015)
13. **[P3]** Remove or suppress the full footer on checkout — replace with minimal legal footer (BUG-CHK implicit)
14. **[P3]** Remove unnecessary mega menu HTML and `product-2.png` from checkout page (BUG-CHK-012)

