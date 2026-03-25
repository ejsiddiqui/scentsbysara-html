<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# Fix Plan — Scents by Sara V3

**Created:** 2026-03-01
**Based on:** QA Audit covering all 8 pages (225 total bugs)
**Approach:** Structured into 6 phases. Each phase is a documented plan — no code changes until approved.

---

## Phase 0 — Structural (Build Missing Pages)

*Highest priority — two pages serve entirely wrong content.*

### 0.1 — Rebuild `contact.html`
**Current state:** Exact copy of `your-story.html` — wrong title, wrong heading, wrong content, wrong stylesheet.
**Required content:**
- Page header: "CONTACT US" or "GET IN TOUCH" in RL Limo serif
- Contact form fields: Name, Email, Subject / Order Number, Message (textarea), Submit CTA ("SEND MESSAGE")
- Contact info block: email address, social media links, business hours
- Standard header/footer (matching other pages)
- New stylesheet `assets/css/contact.css` (do not reuse `your-story.css`)

### 0.2 — Rebuild `our-story.html`
**Current state:** Exact duplicate of `your-story.html` with wrong title and wrong nav routing.
**Required content (reference: `screenshots/our-story-section.png`, `v2-our-story.png`, `v3-our-story-final.png`):**
- Hero with brand headline ("GROUNDED IN RITUAL. EMBODIED IN CONFIDENCE." or equivalent)
- Founder story split block (Sara's photo + brand origin narrative)
- Brand values / mission section
- Editorial pull quote
- Brand credentials (Vegan, Handmade, Cruelty-Free, Eco-conscious)
- Standard header/footer
- New stylesheet `assets/css/our-story.css`

---

## Phase 1 — Global CSS Fixes

*Small effort, maximum impact — fixes apply across all 8 pages instantly.*

### 1.1 — Fix pure white backgrounds (`css/components.css`)
| Line | Selector | Current | Fix |
|---|---|---|---|
| 149 | `.search-overlay` | `background-color: #ffffff` | `background-color: var(--bg-primary)` |
| 178 | `.site-header` | `background-color: #ffffff` | `background-color: var(--bg-primary)` |
| 268 | `.mega-menu` | `background-color: #ffffff` | `background-color: var(--bg-primary)` |

### 1.2 — Add `.font-sans` utility class (`css/layout.css`)
Add after existing heading rules:
```css
.font-sans { font-family: var(--font-sans); }
```
This single line fixes typography on your-story, our-story, cart, contact, and any element using this class sitewide.

### 1.3 — Fix slider dot border-radius (`css/components.css`)
Change lines 467 and 675:
```css
.dot { border-radius: 0; }  /* was: 50% */
```

### 1.4 — Fix `checkout.css` border-radius violations (`assets/css/checkout.css`)
```css
.payment-box { border-radius: 0; }       /* was: 4px */
.summary-img-wrap { border-radius: 0; }  /* was: 4px */
.qty-badge { border-radius: 0; }         /* was: 50% */
```

### 1.5 — Replace mega menu image on all HTML pages
Search and replace across all 8 HTML files:
- Find: `src="assets/images/product-2.png"` (inside `.mega-image-col`)
- Replace: `src="assets/images/mega-menu-image.png"`

### 1.6 — Add missing CSS utility classes (`css/layout.css`)
Add the following utility definitions:
```css
.w-full         { width: 100%; }
.font-weight-normal { font-weight: 400; }
.mt-0           { margin-top: 0; }
.mt-12          { margin-top: 48px; }
.mb-12          { margin-bottom: 48px; }
.pb-16          { padding-bottom: 64px; }
.pt-24          { padding-top: 96px; }
.pb-24          { padding-bottom: 96px; }
.text-md        { font-size: var(--text-h3); }
.gap-8          { gap: 32px; }
.tracking-widest { letter-spacing: 0.15em; }
.text-right     { text-align: right; }
```
Remove redundant `.align-end` and `.items-end` usages (already covered by `flex-between`).

### 1.7 — Add mobile footer single-column collapse (`css/responsive.css`)
```css
@media (max-width: 480px) {
  .footer-main-grid {
    grid-template-columns: 1fr;
  }
  .footer-newsletter-col {
    grid-column: 1;
  }
}
```

### 1.8 — Fix announcement bar sticky behaviour (`css/components.css`)
Two options (choose one):
- **Option A:** Make `.announcement-bar` sticky:
  ```css
  .announcement-bar { position: sticky; top: 0; z-index: calc(var(--z-header) + 1); }
  .site-header { top: var(--announcement-height); } /* 38px */
  ```
- **Option B:** Include announcement bar inside `.site-header` container so it sticks together.

Also fix height to `min-height`:
```css
.announcement-bar { min-height: var(--announcement-height); height: auto; }
```

### 1.9 — Remove dev QA overlay script
Remove from `index.html` (and any other pages where it appears):
```html
<!-- Remove: -->
<script src="assets/js/qa-overlay.js"></script>
```

### 1.10 — Define `--text-base` token (`css/design-tokens.css`)
Add to `:root`:
```css
--text-base: var(--text-primary);  /* #3F3229 — used in checkout.css */
```

---

## Phase 2 — Critical Per-Page Fixes

### index.html

**2.1 — Hero slider: unique images per slide**
Assign distinct background images to each of the 3 `.hero-slide` elements:
- Slide 1: `hero-bg.png` (existing)
- Slide 2: `Hero-slide-bg.png` (existing in assets)
- Slide 3: `bg2.webp` (existing in assets)

**2.2 — Hero: add second CTA button**
Add below the existing "SHOP NOW" button:
```html
<a href="shop.html" class="btn-outline">EXPLORE COLLECTIONS</a>
```

**2.3 — Hero: add prev/next arrow controls**
Add arrow buttons to `.home-hero` HTML and wire up in `main.js`:
```html
<button class="hero-prev" aria-label="Previous slide">←</button>
<button class="hero-next" aria-label="Next slide">→</button>
```

**2.4 — Commitment section: redesign to match reference**
Replace current sand-background 2-column layout with dark mocha background as seen in `v4-commitment-full.png` / `v5-commitment-full.png`:
- Background: `var(--color-mocha)` (`#3F3229`)
- Centered section heading "OUR COMMITMENT"
- Icon-based credential items (Eco-Friendly, Handmade, Cruelty-Free, Clean Formulations)
- Right-side editorial image

**2.5 — Collections: add missing third card + heading**
- Add "OUR COLLECTIONS" `<h2>` heading above the grid
- Add third collection card (Plus Size) using `plus-size-collections.png`
- Change grid from `grid-cols-2` to `grid-cols-3`

**2.6 — Add missing PRD sections (Rituals & Wellbeing + Sensory Science)**
Insert two new sections between Collections and Our Story:
- **Rituals & Wellbeing teaser:** 3 editorial content blocks (Rituals for Confidence, Evening Unwind, Morning Reset) with calm copy + warm imagery + "Explore Rituals" CTA
- **Sensory Science section:** Quiet infographic-style, 3-4 Lucide icon points (Clean formulations, Mood-support scent science, Handmade + cruelty-free, Eco-conscious rituals)

**2.7 — Add standalone Newsletter/Community block**
Add above footer: "Join the Ritual" headline + email form with primary brand CTA.

**2.8 — Fix Our Story image reference**
Update to use correct reference image as per `v3-our-story-final.png`.

**2.9 — Product card button text**
Change all `.product-btn` from "SHOP NOW" to "ADD TO BASKET".

**2.10 — Testimonials: fix formatting**
- Add subtitle "What our customers are saying?" below section heading
- Change author format from "EUNICE YUMBA" to "— Eunice Yumba" (sentence case, dash prefix)
- Fix quote mark positioning from `top: 50%` to `top: 0` or `top: -12px`

**2.11 — Fix footer newsletter column ratio**
Change `3.5fr` to `2fr` in `.footer-main-grid` template.

### product.html

**2.12 — Add gallery `aspect-ratio` + sticky**
```css
.main-image-wrap { aspect-ratio: 3 / 4; }
.product-gallery { position: sticky; top: calc(var(--header-height) + 24px); align-self: flex-start; }
```

**2.13 — Fix commitment image reference**
Line 335: change `our-commitment-left.png` → `our-commitment.png`

**2.14 — Build reviews section HTML**
Add a `<section class="reviews-section container">` block with 3 `.review-item` rows matching the CSS already defined in `product.css`. Reference: `product-page.png`.

**2.15 — Fix accordion border colour**
```css
.accordion { border-top: 1px solid var(--border-light); } /* was: var(--bg-secondary) */
```

**2.16 — Remove inline font-size overrides**
Remove `style="font-size: 40px"` from product `<h1>` and `style="font-size: 14px"` from price element.

**2.17 — Fix swatch label "EBONY" → "CHESTNUT"**
In `assets/js/product.js` line 38: update label lookup for `.swatch-brown`.

### checkout.html

**2.18 — Replace full header with minimal checkout header**
Remove the full site nav from `checkout.html`. Replace with a minimal header containing only the centred logo + cart icon.

**2.19 — Add Delivery Method section**
Add a form section between Shipping Address and Payment with radio buttons for shipping options (Standard / Express).

**2.20 — Remove inline `style="background:#fff;"` from card inputs**
Add to `checkout.css`: `.payment-box input { background-color: var(--bg-primary); }`

### cart.html

**2.21 — Add cart table responsive layout**
Add to `css/responsive.css`:
```css
@media (max-width: 768px) {
  .cart-table thead { display: none; }
  .cart-table tr { display: flex; flex-wrap: wrap; padding: 16px 0; border-bottom: 1px solid var(--border-light); }
  .cart-table td { display: block; }
  /* image + product info row, qty + price + total sub-row */
}
```

**2.22 — Fix cart summary box at 1024px**
```css
@media (max-width: 1024px) {
  .cart-summary-box { max-width: 100%; margin-left: 0; }
}
```

**2.23 — Fix fake product name**
Replace "SHE IS GRACE" with a real product from the catalogue (e.g. "SHE IS TIMELESS").

---

## Phase 3 — Major Polish Fixes

### All Pages

**3.1 — Fix filter overlay on `shop.html`**
- Move filter overlay HTML from JS injection into `shop.html` markup (declare in HTML, toggle with CSS class)
- Define `.grid-cols-3` in `css/layout.css` or change filter markup to use `.grid-cols-4` (which exists)
- Fix swatch `border-radius: 50%` → `0` in `assets/css/shop.css`
- Fix `.swatch-white` from `#FFFFFF` to `var(--bg-primary)`
- Uncomment `.shop-hero p { max-width: 800px; }` in `shop.css`

**3.2 — Fix shop hero heading token bypass**
In `assets/css/shop.css`: remove hardcoded `font-size: 48px` on `.text-h1`, rely on token.

**3.3 — Fix sort dropdown at mobile**
In `assets/css/shop.css`: add `@media (max-width: 480px) { .sort-dropdown { min-width: 100%; } .filter-toolbar { flex-direction: column; } }`

**3.4 — Fix your-story.html split-belief section mobile**
Add to `assets/css/your-story.css`:
```css
@media (max-width: 768px) {
  .split-belief .container { flex-direction: column; gap: 32px; }
  .split-left, .split-right { max-width: 100%; }
  .split-divider { display: none; }
}
```

**3.5 — Fix your-story form inline grid override**
Remove inline `style="display: grid; grid-template-columns: 1fr 1fr..."` from form row. Use `.grid-cols-2` class only (already has responsive collapse).

**3.6 — Add product-page mobile CSS**
Add comprehensive mobile overrides to `css/responsive.css` for:
- `.add-to-cart-row { flex-direction: column; }` at 768px
- `.btn-add-bag { width: 100%; }` at 768px
- `.commitment-content-col { padding: 48px 24px; }` at 768px
- `.product-commitment-grid { grid-template-columns: 1fr; }` at 768px
- `.main-image-wrap { max-height: 500px; }` at 1024px

**3.7 — Fix checkout form-row mobile collapse**
Add to `assets/css/checkout.css`:
```css
@media (max-width: 768px) {
  .form-row { flex-direction: column; }
  .order-summary-col { min-height: auto; order: -1; } /* show above form on mobile */
}
```

**3.8 — Fix checkout `order-summary-col min-height: 100vh`**
Change to `min-height: auto` — the current value forces blank space.

---

## Phase 4 — Logo, Navigation, Copy Fixes

**4.1 — Logo wordmark**
Align "BYSARA" vs "SCENTS BY SARA" usage with reference screenshots. Consider using `logo.svg` asset (already in assets, currently unused) for desktop header.

**4.2 — Navigation labels**
Verify nav items against reference: SHOP | COLLECTIONS | OUR STORY | YOUR STORY | CONTACT US. Remove/rename GIFTS if not in reference design.

**4.3 — Cart CTA text**
Change "CHECKOUT" → "PROCEED TO CHECKOUT".

**4.4 — Add "Continue Shopping" CTA to cart**
Add `<a href="shop.html" class="btn-outline" style="width:100%; text-align:center; margin-top:12px;">CONTINUE SHOPPING</a>` below checkout button in `.cart-summary-box`.

**4.5 — Fix typos**
- `shop.html`: "meaning detail" → "meaningful detail"
- `product.html`: "Phtalates-Free" → "Phthalates-Free"

**4.6 — Fix `.swatch-white` naming**
Rename class to `.swatch-ivory` across `product.html`, `product.css`, and `product.js` for semantic clarity.

**4.7 — Fix ys-badge raw newlines**
Remove HTML whitespace from inside all `.ys-badge` elements so text renders on one line.

**4.8 — Add active nav state to current page**
Add `aria-current="page"` and CSS `.nav-links a[aria-current="page"]` underline style on the active nav link of each page.

---

## Phase 5 — Asset Production

**5.1 — Hero slide images (index.html)**
Source or produce 2 additional hero images for slides 2 and 3 — distinct body candle compositions.

**5.2 — Scent editorial photography (product.html)**
Source dedicated photography for the two scent cards:
- Vanilla: warm editorial with vanilla bean/candle warmth
- Lavender: cool floral editorial

**5.3 — Community/lifestyle photography (your-story.html)**
Replace `product-1.png` through `product-4.png` in story cards with lifestyle/UGC-style photography showing the product in human context.

**5.4 — `our-commitment-left.png` (product.html)**
Either rename `our-commitment.png` to `our-commitment-left.png`, or update the HTML reference in `product.html` line 335 to `our-commitment.png`.

---

## Implementation Sequence (Recommended)

```
Phase 1 (Global CSS) → Phase 0 (New pages) → Phase 2 (Critical per-page)
     ↓
Phase 3 (Major polish + Responsive)
     ↓
Phase 4 (Copy + navigation fixes)
     ↓
Phase 5 (Asset production) → Final QA pass
```

Phase 1 first because it fixes the most bugs across all pages with the least effort. Phase 0 second because two nav destinations are entirely broken. Phase 5 last because it requires asset production work outside the codebase.

---

## Quick Win Summary

These changes fix the most bugs for the least effort:

| Change | File | Bugs Fixed |
|---|---|---|
| `.font-sans { font-family: var(--font-sans); }` | `css/layout.css` | ~15 typography bugs across 4+ pages |
| Header/search/mega-menu: `#ffffff` → `var(--bg-primary)` | `css/components.css` | ~20 colour bugs across all 8 pages |
| Mega menu image: `product-2.png` → `mega-menu-image.png` | All 8 HTML files | 8 bugs (1 per page) |
| Footer 375px `grid-template-columns: 1fr` | `css/responsive.css` | 7 responsive bugs across all pages |
| Add all missing utility classes | `css/layout.css` | ~15 undefined-class bugs |
| **Total** | | **~65 bugs resolved by ~10 lines of CSS** |

---

*This is a documented plan only — no code has been changed. Approve this plan before implementation begins.*

