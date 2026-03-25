<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# QA Tasks — cart.html (Cart Page)

## Status: REVIEWED
## Viewport Tested: 1440px | 1024px | 375px
## Audit Date: 2026-03-01

---

## Section Checklist

### 1. Announcement Bar
- [x] Present and visible
- [x] Correct dark mocha (#3F3229) background with sand (#F9F6F2) text
- [x] Correct copy: "LAUNCHING MARCH 2026 - JOIN THE WAIT LIST FOR EARLY ACCESS"
- [x] Font: Suisse Int'l, 10px, uppercase, letter-spacing 0.1em
- [x] Height: 38px — PASS
- [ ] Text overflow / truncation handling at 375px — FAIL (BUG-CRT-R05)

### 2. Header / Nav
- [x] Announcement bar present above sticky header
- [x] Three-column grid layout: search | logo | icons
- [x] Logo "SCENTS BY SARA" in RL Limo serif — renders correctly
- [x] Header icons: search, account, wishlist, cart — all present
- [x] Mega menu on SHOP link — structure present (hover interaction not audited in static view)
- [ ] Header background colour — FAIL: uses #ffffff (pure white) instead of brand warm neutral (BUG-CRT-002)
- [ ] Desktop nav hidden at ≤1024px — FAIL: breakpoint boundary issue at exactly 1024px (BUG-CRT-R01)
- [ ] Mobile hamburger visible at ≤1024px — conditional pass (appears when desktop nav hides)
- [x] Header max height 94px (sticky portion) within 132px total with announcement bar — PASS
- [x] Border-radius: 0px on all header elements — PASS

### 3. Cart Title / Page Heading
- [x] "YOUR BAG" heading present in RL Limo serif — PASS
- [x] "CONTINUE SHOPPING" link present in header row — PASS (but placement is suboptimal — BUG-CRT-005)
- [ ] H1 font-size — FAIL: uses hardcoded 32px instead of token `--text-h1` (48px) or declared `--text-h2` — typographic hierarchy broken (BUG-CRT-015)
- [x] Cart header separator (border-bottom) present — PASS

### 4. Cart Line Items Table
- [x] Table structure present with thead (PRODUCT, PRICE, QUANTITY, TOTAL)
- [x] Two line items rendered: "SHE IS LUST" and "SHE IS GRACE"
- [x] Product thumbnail images present (product-1.png, product-3.png)
- [x] Product name in uppercase sans-serif — PASS
- [x] Variant info (scent · size) in muted micro text — PASS
- [x] REMOVE link present per line item — PASS
- [x] Quantity stepper (+/- with input) present per line item — PASS
- [x] Qty stepper border uses `--border-heavy` (mocha) — PASS
- [x] Line total displayed and right-aligned — PASS
- [x] Divider border between rows — PASS
- [ ] Product name "SHE IS GRACE" — FAIL: does not exist in product catalogue (BUG-CRT-007)
- [ ] Table responsive at mobile (375px) — FAIL: no responsive breakpoints, critical overflow (BUG-CRT-001, BUG-CRT-R04)
- [ ] `.font-sans` class on product `<h3>` — FAIL: class undefined in stylesheets; resolution is accidental (BUG-CRT-012)
- [ ] `font-weight-normal` and `text-md` classes on `<h3>` — FAIL: neither class is defined in design system
- [ ] Total column `text-align: right` — uses inline style, not a CSS class (BUG-CRT-010)
- [ ] Qty stepper button states (hover/focus) — FAIL: no hover or focus styles defined (BUG-CRT-011)

### 5. Order Summary Box
- [x] Summary box present with `--bg-secondary` (stone) background — PASS
- [x] SUBTOTAL row with label and price (£60.78) — PASS
- [x] Shipping note ("Taxes and shipping calculated at checkout") — PASS
- [x] Sharp corners (0px border-radius) — PASS
- [ ] Summary box full-width on mobile — PARTIAL FAIL: right-aligned with large whitespace gap on left at 1024px (BUG-CRT-R03)
- [ ] "PROCEED TO CHECKOUT" CTA label — FAIL: button reads "CHECKOUT" (BUG-CRT-004)
- [ ] `w-full` CSS class on checkout button — FAIL: class not defined in any stylesheet (BUG-CRT-004)
- [ ] "Continue Shopping" secondary CTA below checkout button — FAIL: missing below summary (BUG-CRT-005)
- [ ] Grand total row — ABSENT: no separate grand total row displaying tax/total after shipping — only subtotal shown

### 6. CTA: Proceed to Checkout
- [x] Dark mocha button present — PASS (colour correct: `var(--color-mocha)`)
- [x] Button links to checkout.html — PASS
- [x] Button uppercase Suisse Int'l text — PASS
- [x] Button border-radius: 0px (sharp corners) — PASS
- [ ] Button label — FAIL: reads "CHECKOUT" not "PROCEED TO CHECKOUT" (BUG-CRT-004)
- [ ] Width handling — PARTIAL: `w-full` undefined class, relies on inline style (BUG-CRT-004)

### 7. Continue Shopping Link
- [x] Link present in cart header row — PASS (structurally)
- [ ] Link position — FAIL: only appears at top of page in cart header, not below the checkout CTA (BUG-CRT-005)
- [x] Links to shop.html — PASS
- [x] Styled as micro muted underline text — matches brand micro link style — PASS

### 8. Footer
- [x] Footer present with `--bg-secondary` (stone) background — PASS
- [x] Newsletter column: heading "JOIN OUR NEWSLETTER" in RL Limo serif — PASS
- [x] Newsletter form: email input + SUBSCRIBE button — PASS
- [x] Social icons: Instagram, Facebook, TikTok, Pinterest — all present as SVG icons — PASS
- [x] Footer link columns: SHOP ALL, ABOUT US, GIFTING, CUSTOMER SERVICE — all present — PASS
- [x] Footer divider rule present — PASS
- [x] Footer bottom row: BYSARA logo + copyright + payment icons — all present — PASS
- [x] Copyright text correct: "2026 SCENTS BY SARA. ALL RIGHTS RESERVED" — PASS
- [x] Payment icons image present (payment-icons.png) — PASS
- [ ] Footer single-column at 375px — FAIL: no mobile single-column breakpoint, two-column grid persists (BUG-CRT-R06)
- [ ] Payment icons legibility at 32px height on mobile — UNVERIFIED: needs visual check at actual mobile device render

### 9. Brand Standards Compliance
- [x] Color palette: sand (#F9F6F2) background — PASS
- [x] Color palette: stone (#E7E3DC) for secondary backgrounds — PASS
- [x] Color palette: mocha (#3F3229) for text and CTAs — PASS
- [x] Color palette: taupe (#A39382) for muted text — PASS
- [ ] No pure white — FAIL: header uses #ffffff (BUG-CRT-002)
- [x] Serif font (RL Limo) for headings — PASS: logo, "YOUR BAG", footer logo use font-serif
- [x] Sans-serif font (Suisse Int'l) for body and UI text — PASS
- [x] All border-radius: 0px — PASS in cart elements; checkout.css import introduces 4px violations (BUG-CRT-014)
- [x] Container max-width (1920px) — PASS
- [x] Gutter: 80px at 1440px (from responsive.css token override) — PASS
- [ ] Cart page specific gutter at 375px — PASS at token level but fails in practice due to table overflow

### 10. Missing / Non-Functional Elements
- [ ] Empty state: no empty cart message or state handled — if no items, the page renders an empty table with no guidance
- [ ] Promo code / discount input — absent from cart page (may be intentional for MVP)
- [ ] Cart item count badge on cart icon in header — icon present but no badge showing current item count
- [ ] Quantity stepper interactivity — buttons present but no JS handler visible in cart.html (JS is in main.js — needs verification)
- [ ] Remove item functionality — REMOVE links present but no JS handler visible in cart.html

---

## Summary

**18 bugs found (2 critical, 8 major, 8 minor)**

| Severity | Count | Bug IDs |
|---|---|---|
| Critical | 2 | BUG-CRT-001, BUG-CRT-R04 |
| Major | 8 | BUG-CRT-003, BUG-CRT-004, BUG-CRT-005, BUG-CRT-006, BUG-CRT-007, BUG-CRT-008, BUG-CRT-R01, BUG-CRT-R02, BUG-CRT-R03, BUG-CRT-R06 |
| Minor | 8 | BUG-CRT-002 (brand violation), BUG-CRT-009, BUG-CRT-010, BUG-CRT-011, BUG-CRT-012, BUG-CRT-013, BUG-CRT-014, BUG-CRT-015, BUG-CRT-R05 |

> Note: BUG-CRT-002 (pure white header) is classified as Minor for the cart page audit because it is a shared component issue affecting all pages — it should be tracked as a global/systemic fix rather than a cart-specific critical.

### Top Priority Fixes (Pre-Launch Blockers)
1. **BUG-CRT-001 / BUG-CRT-R04** — Implement responsive cart layout (table → cards at ≤768px)
2. **BUG-CRT-004** — Rename checkout button to "PROCEED TO CHECKOUT" and define `w-full` class
3. **BUG-CRT-007** — Replace "SHE IS GRACE" with a valid catalogue product name
4. **BUG-CRT-005** — Add "CONTINUE SHOPPING" secondary CTA below checkout button in summary box
5. **BUG-CRT-R06** — Add single-column footer layout at ≤480px
6. **BUG-CRT-002** — Replace `#ffffff` header background with `var(--bg-primary)` (#F9F6F2) across all shared components

