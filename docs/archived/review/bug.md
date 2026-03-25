<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# Consolidated Bug Log — Scents by Sara (V3)

**Audit Date:** 2026-03-01
**Scope:** All 8 HTML pages — Visual fidelity + Responsive (1440px / 1024px / 375px)
**Total Bugs:** 225 across 8 pages

---

## Bug Count by Page

| Page | Critical | Major | Minor | Responsive | Total |
|---|---|---|---|---|---|
| index.html | 8 | 13 | 14 | 10 | **45** |
| shop.html | 5 | 10 | 8 | 6 | **33** |
| product.html | 4 | 8 | 8 | 9 | **29** |
| checkout.html | 4 | 8 | 8 | 8 | **28** |
| contact.html | 1 | 6 | 12 | 5 | **27** |
| our-story.html | 3 | 6 | 9 | 7 | **25** |
| your-story.html | 2 | 7 | 11 | 9 | **20** |
| cart.html | 2 | 8 | 8 | 0 | **18** |
| **TOTAL** | **29** | **66** | **78** | **54** | **225** |

---

## SECTION A — Cross-Cutting Issues (Global Fixes)

These bugs affect every page and must be fixed in shared CSS/JS files first.

---

### [GLOBAL-001] Header background is pure white — violates brand standard
- **Affects:** ALL pages
- **File:** `css/components.css` line 178
- **Current:** `background-color: #ffffff;`
- **Fix:** `background-color: var(--bg-primary);` (`#F9F6F2`)
- **Related:** BUG-IDX-002, BUG-SHP-004, BUG-PRD-016, BUG-CHK-018, BUG-CRT-002, BUG-OST-014, BUG-CNT-010

### [GLOBAL-002] Search overlay background is pure white — violates brand standard
- **Affects:** ALL pages
- **File:** `css/components.css` line 149
- **Current:** `background-color: #ffffff;`
- **Fix:** `background-color: var(--bg-primary);`
- **Related:** BUG-IDX-003, BUG-SHP-003, BUG-YST-008, BUG-OST-013, BUG-CNT-009

### [GLOBAL-003] Mega menu background is pure white — violates brand standard
- **Affects:** ALL pages
- **File:** `css/components.css` line 268
- **Current:** `background-color: #ffffff;`
- **Fix:** `background-color: var(--bg-primary);`
- **Related:** BUG-IDX-004, BUG-CNT-011

### [GLOBAL-004] Mega menu uses wrong image asset on all pages
- **Affects:** ALL pages
- **File:** Every HTML page, `<img src="assets/images/product-2.png">` inside `.mega-image-col`
- **Fix:** Replace with `src="assets/images/mega-menu-image.png"` — this dedicated asset exists and is unused
- **Related:** BUG-IDX-021, BUG-SHP-005, BUG-PRD-015, BUG-CHK-012, BUG-YST-009, BUG-OST-008, BUG-CNT-013

### [GLOBAL-005] `.font-sans` utility class is never defined anywhere in CSS
- **Affects:** ALL pages — any element using `class="font-sans"` renders in serif (RL Limo) instead of Suisse Int'l
- **File:** `css/layout.css` — missing rule
- **Fix:** Add `.font-sans { font-family: var(--font-sans); }` to `css/layout.css`
- **Critical impact confirmed on:** your-story, our-story, cart, checkout, contact; likely affects others
- **Related:** BUG-YST-001, BUG-CRT-012, BUG-OST-005 (where h1 is `font-sans` — should be `font-serif`)

### [GLOBAL-006] Slider dot indicators use `border-radius: 50%` — violates 0px radius brand rule
- **Affects:** ALL pages (shared component)
- **File:** `css/components.css` lines 467 and 675
- **Current:** `.dot { border-radius: 50%; }`
- **Fix:** `border-radius: 0;` — use square/rectangular dots consistent with brand
- **Related:** BUG-IDX-024, BUG-SHP-009, BUG-OST-017

### [GLOBAL-007] Footer grid has no mobile single-column collapse at 375px
- **Affects:** ALL pages
- **File:** `css/components.css` — footer `@media (max-width: 1024px)` collapses to `1fr 1fr` only; no further collapse
- **Fix:** Add to `css/responsive.css`:
  ```css
  @media (max-width: 480px) {
    .footer-main-grid { grid-template-columns: 1fr; }
    .footer-newsletter-col { grid-column: 1; }
  }
  ```
- **Related:** BUG-IDX-045, BUG-SHP-M04, BUG-CRT-R06, BUG-YST-R06, BUG-OST-023, BUG-CNT-027, BUG-CHK-027

### [GLOBAL-008] Announcement bar scrolls away — not sticky with the header
- **Affects:** All pages — `--header-height: 132px` token accounts for 38px announcement + 94px nav, but only `.site-header` is `position: sticky`
- **Fix:** Either include `.announcement-bar` inside `.site-header` container, or apply `position: sticky; top: 0; z-index: var(--z-header)` to `.announcement-bar` with `.site-header { top: var(--announcement-height); }`
- **Related:** BUG-YST-007, BUG-OST-003

### [GLOBAL-009] `qa-overlay.js` dev script still wired up — injects debug button on every page
- **Affects:** `index.html` (confirmed); likely other pages
- **File:** `index.html` line 539: `<script src="assets/js/qa-overlay.js"></script>`
- **Fix:** Remove this script tag from all HTML pages before UAT/production
- **Related:** BUG-IDX-020

### [GLOBAL-010] Multiple CSS utility classes referenced across pages but never defined
- **Affects:** Multiple pages — silent failures (elements render with defaults, not design intent)
- **File:** `css/layout.css` — missing definitions
- **Missing classes and suggested fixes:**

| Class | Used on | Should resolve to |
|---|---|---|
| `.w-full` | cart, checkout | `width: 100%` |
| `.font-weight-normal` | your-story, our-story, contact | `font-weight: 400` |
| `.mt-12` | checkout | `margin-top: 48px` |
| `.mb-12` | your-story, contact | `margin-bottom: 48px` |
| `.text-md` | your-story | `font-size: var(--text-h2)` or `1.25rem` |
| `.pb-16` | your-story | `padding-bottom: 64px` |
| `.gap-8` | your-story | `gap: 32px` |
| `.tracking-widest` | your-story, contact | `letter-spacing: 0.15em` |
| `.align-end` | your-story, contact | redundant with `flex-between` |
| `.items-end` | cart | redundant with `flex-between` |
| `.mt-0` | your-story | `margin-top: 0` |
| `.pt-24`, `.pb-24` | contact | `padding-top/bottom: 96px` |
| `.font-size-normal` | cart | `font-size: var(--text-body)` |

---

## SECTION B — Structural Issues (Wrong/Missing Pages)

### [STRUCT-001] `contact.html` is a copy of `your-story.html` — contact page does not exist
- **File:** `contact.html`
- **Detail:** The entire page is the community story submission page. There is no contact form, no email address, no business hours. Any customer clicking "CONTACT US" in the nav lands on the wrong page.
- **Fix:** Build `contact.html` from scratch with: page header, contact form (Name / Email / Subject / Message), contact info section, and footer
- **Related:** BUG-CNT-001 through BUG-CNT-007

### [STRUCT-002] `our-story.html` is a duplicate of `your-story.html` — brand story page does not exist
- **File:** `our-story.html`
- **Detail:** Same title, same CSS, same content as `your-story.html`. The "OUR STORY" nav link routes customers to the wrong page. The brand founder narrative page (referenced in `screenshots/our-story-section.png`) is completely absent.
- **Fix:** Build `our-story.html` from scratch with the brand story content: editorial split layout "Grounded in Ritual. Embodied in Confidence.", founder story, brand values, pull quote, footer
- **Related:** BUG-OST-001, BUG-OST-002

---

## SECTION C — Per-Page Critical Bugs

### index.html

- **[BUG-IDX-001]** All 3 hero slides use the same image (`hero-bg.png`) — slider navigation is cosmetic only. Fix: assign distinct images (`Hero-slide-bg.png`, `bg2.png`, `hero-bg.png`) to each slide.
- **[BUG-IDX-005]** "Our Commitment" section design is completely wrong vs reference — dark mocha background with centered heading expected; sand-background 2-column grid implemented
- **[BUG-IDX-006]** `our-commitment-left.png` not in assets — actually `our-commitment.png` exists. Fix: update image src
- **[BUG-IDX-007]** Collections section shows only 2 cards (should be 3 per reference: Custom, Gold, Plus Size)
- **[BUG-IDX-008]** Hero slider has no prev/next arrows — dots only
- **[BUG-IDX-029]** PRD Section 7 (Rituals & Wellbeing) entirely absent from HTML
- **[BUG-IDX-030]** PRD Section 8 (Sensory Science) entirely absent from HTML
- **[BUG-IDX-031]** PRD Section 10 (standalone Newsletter block) absent — only embedded in footer

### shop.html

- **[BUG-SHP-001]** No pagination / load-more control — 6 hardcoded products, no way to load more
- **[BUG-SHP-002]** Filter overlay background is pure white (`#fff`) — brand violation
- **[BUG-SHP-006]** All 6 product cards share the same name "SHE IS TIMELESS" — placeholder not differentiated
- **[BUG-SHP-008]** Color swatches use `border-radius: 50%` — violates 0px radius rule
- **[BUG-SHP-010]** Filter overlay DOM injected at runtime by JS (not declared in HTML) — breaks rendering, indexability
- **[BUG-SHP-011]** Injected filter uses `grid-cols-3` CSS class which is not defined — filter groups will not grid
- **[BUG-SHP-M02]** Shop hero H1 uses hardcoded `font-size: 48px` bypassing token — stays 48px on mobile (should scale to 32px)
- **[BUG-SHP-M03]** Sort dropdown `min-width: 280px` + filter button exceeds 375px viewport width — horizontal overflow

### product.html

- **[BUG-PRD-001]** `.main-image-wrap` has no `aspect-ratio: 3/4` — image collapses/stretches depending on browser
- **[BUG-PRD-002]** Gallery is not `position: sticky` — scrolls away during product interaction
- **[BUG-PRD-003]** `our-commitment-left.png` does not exist — broken image placeholder in commitment section
- **[BUG-PRD-004]** Reviews section (3-col grid, "WHAT OUR CUSTOMERS ARE SAYING") CSS exists but HTML is completely absent — replaced by a single testimonial quote
- **[BUG-PRD-R05]** No product-page-specific mobile CSS at all — zero overrides for gallery, selectors, CTA row, accordions at 375px

### checkout.html

- **[BUG-CHK-001]** `--text-base` CSS token used 4x in `checkout.css` but never defined in `design-tokens.css` — form labels fall back to black
- **[BUG-CHK-002]** Full site header with mega menu used instead of minimal checkout header (logo only)
- **[BUG-CHK-003]** `.payment-box { border-radius: 4px }` — violates 0px rule
- **[BUG-CHK-004]** `.summary-img-wrap { border-radius: 4px }` — violates 0px rule
- **[BUG-CHK-006]** Delivery Method section entirely missing from checkout flow
- **[BUG-CHK-024]** `.form-row` (two-column inputs) has no mobile collapse — inputs ~116px wide at 375px, practically untappable

### cart.html

- **[BUG-CRT-001]** Cart `<table>` has zero responsive CSS — completely unusable at 375px (overflows horizontally)
- **[BUG-CRT-002]** Header pure white (see GLOBAL-001)
- **[BUG-CRT-007]** Second cart line item named "SHE IS GRACE" — this product does not exist in the catalogue

---

## SECTION D — Selected Major Bugs by Page

### index.html Major

- **[BUG-IDX-009]** Nav shows GIFTS but not COLLECTIONS — mismatch with reference and PRD
- **[BUG-IDX-010]** Hero has only 1 CTA button — reference shows 2 ("SHOP NOW" + "EXPLORE COLLECTIONS")
- **[BUG-IDX-013]** Product card buttons read "SHOP NOW" — reference shows "ADD TO BASKET"
- **[BUG-IDX-016]** Quote marks positioned `top: 50%` absolute — overlaps multi-line testimonial text
- **[BUG-IDX-017]** Collections section missing "OUR COLLECTIONS" heading entirely
- **[BUG-IDX-022]** Desktop logo reads "SCENTS BY SARA" — reference shows "BYSARA"
- **[BUG-IDX-044]** `.testimonial-content { padding: 0 100px }` leaves only 175px of text width at 375px

### shop.html Major

- **[BUG-SHP-007]** `.swatch-white` uses pure `#FFFFFF` — brand violation
- **[BUG-SHP-013]** Sort dropdown is a click-toggle between 2 values, not a real dropdown — no ARIA roles
- **[BUG-SHP-015]** Shop hero paragraph text runs full-width (max-width commented out) — up to 1720px wide at desktop

### product.html Major

- **[BUG-PRD-005]** Product title `<h1>` has inline `font-size: 40px` — prevents responsive token scaling at mobile
- **[BUG-PRD-006]** Price inline `font-size: 14px` overrides CSS 18px rule
- **[BUG-PRD-007]** Dark brown swatch labeled "EBONY" in JS — brand spec calls it "CHESTNUT"
- **[BUG-PRD-008]** Both scent cards use `hero-bg.png` — no dedicated vanilla/lavender editorial photography
- **[BUG-PRD-012]** Accordion border uses `var(--bg-secondary)` (same colour as background) — separators are invisible

### checkout.html Major

- **[BUG-CHK-005]** Qty badge uses `border-radius: 50%` — violates 0px rule
- **[BUG-CHK-008]** Card number/expiry/CVC inputs have `style="background:#fff;"` — pure white inline styles
- **[BUG-CHK-011]** Order summary column has `min-height: 100vh` — creates large blank block on mobile
- **[BUG-CHK-026]** On mobile, order summary renders below form — standard UX places it above

### cart.html Major

- **[BUG-CRT-004]** CTA reads "CHECKOUT" instead of "PROCEED TO CHECKOUT"
- **[BUG-CRT-005]** "Continue Shopping" is only a micro-link in the header row — no secondary CTA after checkout button
- **[BUG-CRT-006]** `items-end` class used on `.cart-header` — undefined
- **[BUG-CRT-R03]** Cart summary box `margin-left: auto` creates ~448px dead whitespace at 1024px

### your-story.html Major

- **[BUG-YST-005]** Split-belief section is `flex-wrap: nowrap` — minimum 820px layout in a 375px viewport = severe horizontal overflow
- **[BUG-YST-006]** Form name/email row uses inline `grid-template-columns: 1fr 1fr` — overrides responsive CSS collapse at mobile
- **[BUG-YST-010]** Story cards use product shots — reference shows lifestyle/UGC photography

### our-story.html Major (beyond STRUCT-002)

- **[BUG-OST-003]** Announcement bar not sticky (see GLOBAL-008)
- **[BUG-OST-007]** Story cards use product images — not community/lifestyle photography

---

## SECTION E — Selected Minor Bugs

- **[BUG-SHP-017]** Typo in shop hero paragraph: "meaning detail" → "meaningful detail"
- **[BUG-PRD-014]** Typo in commitment list: "Phtalates-Free" → "Phthalates-Free"
- **[BUG-PRD-019]** `.swatch-white` class used for an `#EAE5DE` ivory colour — naming confusion
- **[BUG-IDX-023]** Announcement bar `height: 38px` is fixed — should be `min-height` to allow wrapping on mobile
- **[BUG-IDX-025]** `.hero-content` has both `container` class and redundant identical CSS — right padding nullified
- **[BUG-CRT-009]** Cart `padding-top: 80px` is 14px short of sticky header height (94px) — content clips behind header
- **[BUG-CRT-015]** Cart H1 "YOUR BAG" uses hardcoded `32px` — should be `--text-h1` (48px) per token scale
- **[BUG-YST-018]** Badge text has raw HTML newlines — "SHE IS GRACE" renders as "SHE / IS GRACE" on two lines
- **[BUG-YST-019]** Footer "GIFTING" column links "Your Story" to itself — self-referential misclassification
- **[BUG-OST-015]** Character counter shows "0 characters" but has no JS — decorative only
- **[BUG-OST-016]** Form `text-align: center` cascades from parent — form fields appear centred instead of left-aligned

---

## SECTION F — Responsive Summary

### Systemic Responsive Failures

| Issue | Pages Affected | Fix Location |
|---|---|---|
| Footer no 375px single-column rule | All pages | `css/responsive.css` |
| Announcement bar not sticky | All pages | `css/components.css` |
| Split-belief section overflows at 375px | your-story, our-story, contact | `assets/css/your-story.css` + media query |
| Two-column form inputs not collapsing on mobile | your-story, our-story, contact, checkout | Per-page CSS + remove inline grid styles |
| Product grid `padding: 0 100px` testimonial not responsive | index | `css/components.css` |
| Cart table has no mobile card-layout fallback | cart | New responsive rule in `css/responsive.css` |
| Checkout form rows not collapsing on mobile | checkout | `assets/css/checkout.css` + media query |

---

*Report generated: 2026-03-01 | Auditors: 8 parallel QA agents*

