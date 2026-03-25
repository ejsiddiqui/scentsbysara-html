<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# QA Tasks — index.html (Homepage)

## Status: REVIEWED
## Audit Date: 2026-03-01
## Viewport Tested: 1440px | 1024px | 375px
## Reference Screenshots Used: `v3-hero.png`, `v2-header-hero.png`, `v2-best-sellers.png`, `v2-commitment.png`, `v2-collections.png`, `v2-collections-full.png`, `v2-our-story.png`, `v2-testimonials.png`, `v2-footer.png`, `home-page.png`, `footer-fix.png`, `mega-menu.png`, `mobile-full.png`, `mobile-header.png`, `v4-commitment-full.png`, `v5-commitment-full.png`, `v3-our-story-final.png`

---

## Section Checklist

### 1. Announcement Bar
- [x] Present in DOM — PASS
- [x] Dark mocha background (`#3F3229`) — PASS (uses `var(--color-mocha)`)
- [x] Sand text color (`#F9F6F2`) — PASS
- [x] Correct copy: "LAUNCHING MARCH 2026 - JOIN THE WAIT LIST FOR EARLY ACCESS" — PASS
- [x] Font: Suisse Int'l, 10px, letter-spacing 0.1em — PASS
- [ ] Fixed height `38px` clips two-line text at 375px — FAIL (see BUG-IDX-023, BUG-IDX-040)
- [ ] Announcement bar text says "WAIT LIST" (two words) — reference shows "WAITLIST" (one word) — MINOR FAIL

### 2. Header / Navigation
- [x] Present in DOM — PASS
- [ ] Header background is pure white `#ffffff` — FAIL (should be `var(--bg-primary)` = `#F9F6F2`) — see BUG-IDX-002
- [x] Header sticky positioning — PASS (`position: sticky; top: 0`)
- [x] Header scroll-hide/show logic — PASS (implemented in main.js)
- [x] Three-column header layout (search | logo | icons) — PASS
- [ ] Logo wordmark shows "SCENTS BY SARA" on desktop — FAIL: reference shows "BYSARA" on desktop header — see BUG-IDX-022
- [x] Mobile logo "BYSARA" exists and hidden on desktop — PASS
- [x] Search icon (left) — PASS
- [x] Account icon — PASS
- [x] Wishlist icon — PASS
- [x] Cart icon — PASS
- [x] Hamburger shown on mobile — PASS
- [x] Nav links present: SHOP, GIFTS, OUR STORY, YOUR STORY, CONTACT US — PASS (5 links)
- [ ] Nav does not include standalone "COLLECTIONS" link — MINOR FAIL (PRD expected section, only in mega menu)
- [x] SHOP has mega menu dropdown — PASS
- [x] Mega menu structure: 4 text columns + image column — PASS
- [ ] Mega menu background is pure white `#ffffff` — FAIL (should be `var(--bg-primary)`) — see BUG-IDX-004
- [ ] Mega menu image uses `product-2.png` instead of `mega-menu-image.png` — FAIL — see BUG-IDX-021
- [x] Nav font: uppercase, 11px, letter-spacing 0.1em — PASS
- [x] Search overlay exists with input and close button — PASS
- [ ] Search overlay background pure white — FAIL (should be sand) — see BUG-IDX-003
- [x] Mobile menu overlay exists — PASS
- [ ] Hamburger icon does not change to X when open — FAIL — see BUG-IDX-036
- [x] Header max height 94px (site-header only; total with announcement = 132px) — PASS for header element itself, but note announcement-bar is separate
- [x] All icon buttons have `aria-label` attributes — PASS
- [x] Mobile menu has close button — PASS

### 3. Hero Slider
- [x] Present in DOM — PASS
- [x] Full-bleed layout — PASS (`position: absolute`, covers section)
- [ ] 3 distinct hero images — FAIL: all 3 slides use identical `hero-bg.png` — see BUG-IDX-001
- [x] Hero headline present — PASS
- [ ] Headline text all-caps via CSS but reference shows mixed case — MINOR FAIL — see BUG-IDX-011
- [x] Hero subtext present — PASS
- [ ] Only 1 CTA button — FAIL: reference shows 2 CTAs; hero uses `.btn-solid` not `.btn-hero` — see BUG-IDX-010
- [ ] CTA reads "SHOP NOW" — FAIL: reference shows "EXPLORE COLLECTIONS" — see BUG-IDX-010
- [x] 3 slider dots present — PASS
- [x] Dot navigation JS implemented — PASS
- [x] Auto-advance (5-second interval) implemented — PASS
- [x] Touch/swipe events implemented — PASS
- [ ] No previous/next arrow buttons — FAIL — see BUG-IDX-008
- [x] Hero height: `calc(100vh - 132px)` with max-height 700px — PASS
- [x] Slider z-index: -1 (behind hero content) — PASS
- [x] Object-fit: cover on hero images — PASS

### 4. Best Sellers Strip
- [x] Present in DOM — PASS
- [x] "BEST SELLERS" heading — PASS
- [x] 4 product cards — PASS
- [x] Product images (product-1.png through product-4.png) — PASS (assets exist)
- [x] Product name, scent, price all present — PASS
- [x] 4-column grid at desktop — PASS
- [ ] Button text reads "SHOP NOW" — FAIL: reference shows "ADD TO BASKET" — see BUG-IDX-013
- [x] Product image hover scale effect — PASS
- [x] Image aspect ratio 4:5 — PASS
- [x] Text left-aligned, product info stacked — PASS
- [ ] No "ADD TO BASKET" button variant for wishlist/quick-add — FAIL
- [x] 2-column grid at 1024px — PASS (responsive.css)
- [x] 1-column grid at 480px — PASS (responsive.css)

### 5. Our Commitment Section
- [ ] Section layout matches reference — FAIL: current uses sand bg + two columns; reference shows dark mocha full-width bg — see BUG-IDX-005
- [x] Section present in DOM — PASS
- [x] Eyebrow label "OUR COMMITMENT" — PASS
- [x] Serif heading "INTENTIONAL DESIGN IN SCENT AND FORM." — PASS
- [x] 4 commitment items with titles and body text — PASS
- [x] "READ OUR STORY" link — PASS
- [ ] Background color: uses `var(--bg-primary)` (sand) — FAIL: should be dark mocha per references
- [ ] Image asset mismatch: uses `our-commitment-left.png` not `our-commitment.png` — FAIL — see BUG-IDX-006
- [ ] Heading alignment differs from reference — FAIL: reference centers heading across full width, current right-aligns in text column
- [ ] No eco-friendly / handmade / cruelty-free icons beside commitment items — FAIL: reference shows icon treatments
- [ ] Double gutter padding on `.commitment-text` — FAIL — see BUG-IDX-032

### 6. Collections Section
- [x] Present in DOM — PASS
- [ ] Missing "OUR COLLECTIONS" heading — FAIL — see BUG-IDX-017
- [ ] Only 2 collections — FAIL: reference shows 3 ("Custom", "Gold", "Plus Size") — see BUG-IDX-007
- [x] Collection images present: `custom-collections.png`, `gold-collections.png` — PASS
- [x] Collection titles present — PASS
- [x] Collection body text present — PASS
- [x] "DISCOVER NOW" CTA buttons (outline style) — PASS
- [x] Image aspect ratio 4:5 — PASS
- [x] Image hover scale effect — PASS
- [ ] Collection overlaid text labels not present — FAIL: reference shows text overlaid on image, current shows text below image — DESIGN DIFFERENCE

### 7. Rituals & Wellbeing Section
- [ ] Section ABSENT from index.html — FAIL (PRD Section 7 requirement missing) — see BUG-IDX-029

### 8. Sensory Science / Scent Story Section
- [ ] Section ABSENT from index.html — FAIL (PRD Section 8 requirement missing) — see BUG-IDX-030

### 9. Our Story Split Block
- [x] Present in DOM — PASS
- [x] Eyebrow label "OUR STORY" — PASS
- [x] Serif heading "GROUNDED IN RITUAL. EMBODIED IN CONFIDENCE." — PASS
- [x] Body text present — PASS
- [x] "READ MORE" CTA (btn-solid) — PASS
- [x] Split two-column layout — PASS
- [x] Background `bg-secondary` (stone `#E7E3DC`) on text block — PASS
- [ ] Right-column image: `sara.png` (founder portrait) — PARTIALLY PASS: v3 reference shows ambient/window photo, but sara.png (founder) may be correct version per latest design iteration — NEEDS CONFIRMATION
- [ ] Double-spacing above section (margin-top + prior section padding-bottom = 160px) — FAIL — see BUG-IDX-033
- [ ] Double-gutter on `container-editorial` inside text block — FAIL — see BUG-IDX-018
- [x] Single column at 1024px (stacked) — PASS

### 10. Testimonials Slider
- [x] Present in DOM — PASS
- [x] "CUSTOMER TESTIMONIALS" heading — PASS
- [x] Stars rating element — PASS
- [ ] Missing subtitle "What our customers are saying?" — FAIL — see BUG-IDX-014
- [x] 3 testimonial slides — PASS
- [x] Only slide 1 active by default — PASS
- [x] 3 slider dots — PASS
- [x] Dot click navigation — PASS
- [x] Auto-advance (6-second interval) — PASS
- [ ] Author displayed in all-caps — FAIL: reference shows sentence case with dash prefix — see BUG-IDX-015
- [ ] Quote marks positioned with `top: 50%` — problematic for multi-line quotes — FAIL — see BUG-IDX-016
- [ ] `.testimonial-content { padding: 0 100px }` will overflow/clip at 375px — FAIL — see BUG-IDX-044
- [x] Italic testimonial text — PASS
- [x] Star color: taupe `var(--color-taupe)` — PASS

### 11. Newsletter / Community Block (Standalone)
- [ ] Section ABSENT as standalone block — FAIL (PRD Section 10 requirement missing) — see BUG-IDX-031

### 12. Footer
- [x] Present in DOM — PASS
- [x] Background: stone `var(--bg-secondary)` — PASS
- [x] Newsletter column: heading, email input, subscribe button — PASS
- [x] Social icons: Instagram, Facebook, TikTok, Pinterest — PASS (4 present)
- [ ] Reference footer shows only Instagram, TikTok, Pinterest (no Facebook) — MINOR FAIL — see BUG-IDX-019
- [x] SHOP ALL column with 4 links — PASS
- [x] ABOUT US column with 3 links — PASS
- [x] GIFTING column with 3 links — PASS
- [x] CUSTOMER SERVICE column with 5 links — PASS
- [x] Divider rule — PASS
- [x] Footer bottom: BYSARA logo text + copyright — PASS
- [x] Payment methods image — PASS
- [ ] Newsletter form input height 64px, subscribe button 54px — PASS (in CSS)
- [ ] Footer grid proportions: `3.5fr` for newsletter may be too wide — FAIL — see BUG-IDX-028
- [ ] Social icons: SVG inline elements, `footer-social-group img` filter CSS does not apply to SVG — FAIL — see BUG-IDX-019
- [ ] No single-column footer responsive override at 375px — FAIL — see BUG-IDX-045

### 13. Production Readiness
- [ ] QA overlay script included in production HTML — FAIL — see BUG-IDX-020
- [x] Viewport meta tag present — PASS
- [x] Page title: "Scents by Sara | Luxury Bespoke Candles" — PASS
- [x] Adobe Typekit (RL Limo serif) loaded via CDN — PASS (link to use.typekit.net/abn0bto.css)
- [x] Suisse Int'l font-face declarations present for Regular, Light, Bold, Semibold — PASS
- [x] Font files exist in `assets/fonts/` — PASS
- [x] CSS files all linked: design-tokens, layout, components, responsive — PASS
- [x] main.js linked — PASS
- [x] No broken asset paths for product images (1–4) — PASS (files exist)
- [x] No broken path for `sara.png` — PASS
- [x] No broken path for `our-commitment-left.png` — PASS
- [x] No broken path for `custom-collections.png`, `gold-collections.png` — PASS
- [x] No broken path for `payment-icons.png` — PASS
- [ ] Hero uses same image for all 3 slides — FAIL (missing slide 2 & 3 unique images)
- [x] `overflow-x: hidden` on body — PASS

---

## Summary

**45 bugs found (8 Critical, 13 Major, 24 Minor/Responsive)**

| Severity | Count | Bug IDs |
|----------|-------|---------|
| Critical | 8 | BUG-IDX-001 through BUG-IDX-008 |
| Major | 13 | BUG-IDX-009 through BUG-IDX-020 |
| Minor / Cosmetic | 14 | BUG-IDX-021 through BUG-IDX-033 |
| Responsive — 1440px | 2 | BUG-IDX-034, BUG-IDX-035 |
| Responsive — 1024px | 4 | BUG-IDX-036 through BUG-IDX-039 |
| Responsive — 375px | 6 | BUG-IDX-040 through BUG-IDX-045 |

---

## Priority Fix Order

### P0 — Fix Before Any Screenshot / Review Presentation
1. **BUG-IDX-001** — All hero slides use the same image. Assign unique images to slides 2 and 3.
2. **BUG-IDX-002, 003, 004** — Replace all `#ffffff` hard-coded backgrounds with `var(--bg-primary)`.
3. **BUG-IDX-020** — Remove `qa-overlay.js` script tag from `index.html`.
4. **BUG-IDX-005** — Rebuild "Our Commitment" section to match dark mocha background design from references.
5. **BUG-IDX-007, 017** — Add missing "OUR COLLECTIONS" heading and third collection card.

### P1 — Fix Before UAT
6. **BUG-IDX-010** — Add second CTA button to hero; update text to "EXPLORE COLLECTIONS" / use `.btn-hero`.
7. **BUG-IDX-013** — Change product card button text from "SHOP NOW" to "ADD TO BASKET".
8. **BUG-IDX-014** — Add testimonial subtitle text "What our customers are saying?".
9. **BUG-IDX-015** — Fix testimonial author format to sentence case with dash prefix.
10. **BUG-IDX-022** — Change desktop logo from "SCENTS BY SARA" to "BYSARA".
11. **BUG-IDX-040, 044** — Fix announcement bar to use `min-height`; fix testimonial content padding for mobile.

### P2 — Fix Before Launch
12. **BUG-IDX-008** — Add hero slider prev/next arrow buttons.
13. **BUG-IDX-019** — Fix footer social icons (use img assets or correct SVG filter; remove Facebook if not in reference).
14. **BUG-IDX-021** — Replace mega menu image with `mega-menu-image.png`.
15. **BUG-IDX-018, 025, 032, 033** — Resolve double-padding/margin bugs across sections.
16. **BUG-IDX-029, 030, 031** — Add missing PRD sections: Rituals & Wellbeing, Sensory Science, standalone Newsletter block.
17. **BUG-IDX-036** — Add hamburger-to-X icon animation for mobile menu toggle.
18. **BUG-IDX-045** — Add single-column footer override at 375px.

---

## Missing Sections vs PRD

| PRD Section | Present in index.html | Notes |
|-------------|----------------------|-------|
| 1. Announcement Bar | YES | Minor text issue |
| 2. Header/Nav with mega menu | YES | Multiple issues |
| 3. Hero Slider (3 slides) | PARTIAL | Same image all 3 slides; 1 CTA not 2 |
| 4. Bestsellers strip | YES | Wrong button text |
| 5. Brand Story / Founder split | YES | Double-padding issues |
| 6. Collections overview | PARTIAL | Only 2 of 3 collections; missing heading |
| 7. Rituals & Wellbeing teaser | NO | Section entirely absent |
| 8. Sensory Science / Scent Story | NO | Section entirely absent |
| 9. Testimonials slider | YES | Missing subtitle; author format wrong |
| 10. Newsletter / Community block | NO | Only in footer, not standalone |
| 11. Footer (3-column) | PARTIAL | Social icon issues; mobile stacking |

