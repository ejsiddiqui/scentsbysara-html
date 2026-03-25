<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# QA Final Report — Scents by Sara V3

**Audit Date:** 2026-03-01
**Scope:** All 8 HTML pages
**Audited By:** 8 parallel QA agents (visual + code analysis)
**Viewports:** 1440px (desktop) | 1024px (tablet) | 375px (mobile)
**References Used:** 50+ screenshots in `/screenshots/` + `brand-guidelines.md` + `prd.md`

---

## Executive Summary

The V3 static site has a **solid structural and typographic foundation** — the CSS design token system, RL Limo serif headings, Suisse Int'l body text, warm neutral colour palette, and 0px border-radius brand rule are all architecturally correct and consistently applied in the majority of sections.

However, the site contains **225 bugs across 8 pages** — including 29 critical issues, 2 pages that are entirely wrong content, 3 PRD-required homepage sections that are completely missing, and systemic responsive failures affecting every page.

**The site is not production-ready.** At current state it would fail a basic QA pass on every page.

---

## Overall Verdict by Page

| Page | Verdict | Critical | Total Bugs | Key Blocker |
|---|---|---|---|---|
| index.html | ❌ FAIL | 8 | 45 | 3 missing PRD sections; hero all same image; wrong Commitment design |
| shop.html | ❌ FAIL | 5 | 33 | Filter overlay broken; all products same name; no pagination |
| product.html | ❌ FAIL | 4 | 29 | Gallery not sticky; missing asset; reviews section HTML absent |
| checkout.html | ❌ FAIL | 4 | 28 | Wrong header; missing delivery method; mobile form untappable |
| contact.html | ❌ FAIL | 1 | 27 | **Entire page is wrong — this is a copy of your-story.html** |
| our-story.html | ❌ FAIL | 3 | 25 | **Entire page is wrong — duplicate of your-story.html** |
| your-story.html | ❌ FAIL | 2 | 20 | `.font-sans` class not defined; split section overflows on mobile |
| cart.html | ❌ FAIL | 2 | 18 | Cart table has zero responsive CSS; completely broken at 375px |

---

## Top 10 Most Impactful Bugs

| # | Bug | Scope | Impact |
|---|---|---|---|
| 1 | `contact.html` and `our-story.html` are copies of `your-story.html` | 2 pages | Brand story and contact pages don't exist |
| 2 | 3 PRD homepage sections entirely absent (Rituals, Sensory Science, Newsletter block) | index.html | ~30% of required content missing |
| 3 | `.font-sans` CSS class not defined anywhere | All pages | Every heading using this class renders in wrong font |
| 4 | Header/mega-menu/search overlay all use pure `#ffffff` | All pages | Brand "no pure white" rule violated sitewide |
| 5 | Mega menu references `product-2.png` instead of `mega-menu-image.png` | All pages | Wrong image in nav on every page |
| 6 | Cart table has no responsive CSS | cart.html | Completely unusable on mobile |
| 7 | Checkout `.form-row` not collapsing on mobile | checkout.html | Form inputs ~116px wide at 375px — untappable |
| 8 | All 3 hero slides use same image | index.html | Slider navigation is purely cosmetic |
| 9 | Footer has no mobile single-column collapse | All pages | Two cramped columns on every page at 375px |
| 10 | Product gallery not sticky + missing `aspect-ratio: 3/4` | product.html | Core PDP layout pattern broken |

---

## Systemic Brand Compliance Issues

### Colour Violations
- **Pure white `#ffffff`** used on header, search overlay, and mega menu across all pages — must all be changed to `var(--bg-primary)` (`#F9F6F2`)
- **`checkout.css`** has `border-radius: 4px` on `.payment-box` and `.summary-img-wrap` — brand mandates `0px`
- **Shop swatches** use `border-radius: 50%` — brand mandates `0px`
- **Filter overlay** uses pure `#fff` background

### Typography Violations
- `.font-sans` utility class entirely missing from all stylesheets — headings that should be sans-serif render in RL Limo serif
- Multiple inline `font-size` overrides prevent responsive token scaling (product H1, cart H1, shop hero, your-story hero)
- Testimonial author names all-caps — reference shows sentence case with dash prefix

### Layout Violations
- Mega menu wrong image on all 8 pages
- Slider dots `border-radius: 50%` across all pages
- Numerous undefined CSS utility classes used across pages (`.w-full`, `.font-weight-normal`, `.mt-12`, `.mb-12`, `.tracking-widest`, etc.)

### Responsive Violations
- Footer has no single-column collapse at 375px — affects all 8 pages
- Announcement bar is not sticky — breaks combined 132px header height spec
- Split-belief section has no mobile stack rule — causes horizontal overflow on your-story, our-story, and contact
- Inline grid styles on form rows override responsive CSS collapse rules

---

## What Is Working Well

- ✅ Design token system (`design-tokens.css`) is well-structured and largely used correctly
- ✅ Typography scale and font loading (RL Limo via Typekit, Suisse Int'l local) is architecturally correct
- ✅ Warm neutral colour palette applied correctly in body/section backgrounds
- ✅ `border-radius: 0px` enforced correctly on rectangular UI elements (buttons, cards, inputs) — only violation is circular swatches and dots
- ✅ Container/gutter/content-max system (`1920px` max, `100px` gutters, `1720px` content max) is consistent
- ✅ JavaScript product interactions (accordion, thumbnail swap, qty stepper, swatch label update) are implemented and functional
- ✅ Hero slider dot navigation functional
- ✅ Sticky header scroll hide/show logic in `main.js` is correct in principle
- ✅ Footer structure consistent across all pages
- ✅ Mobile hamburger menu overlay implemented

---

## Asset Gaps

| Asset | Status | Used By |
|---|---|---|
| `our-commitment-left.png` | ❌ Missing (404) | product.html line 335 |
| `mega-menu-image.png` | ✅ Exists but unused | Should replace `product-2.png` on all pages |
| `hero-bg-2.png`, `hero-bg-3.png` | ❌ Missing | Needed for hero slider slides 2 and 3 |
| Scent editorial photography (vanilla, lavender) | ❌ Missing | product.html scents section |
| Lifestyle/community photography for story cards | ❌ Missing | your-story.html, our-story.html |
| `our-commitment.png` | ✅ Exists | Used in index.html (but section design needs rework) |

---

## PRD Coverage Analysis (Homepage)

| PRD Section | Status |
|---|---|
| 1. Announcement bar | ✅ Present |
| 2. Header/Nav + Mega Menu | ⚠️ Present but wrong image, wrong nav item labels |
| 3. Hero slider (3 slides, 2 CTAs) | ⚠️ Present — 1 CTA only; all 3 slides same image |
| 4. Bestsellers strip | ⚠️ Present — wrong button label "SHOP NOW" vs "ADD TO BASKET" |
| 5. Brand Story / Founder split | ⚠️ Present — image may not match reference version |
| 6. Collections overview | ⚠️ Present — only 2 of 3 collections; missing heading |
| 7. Rituals & Wellbeing teaser | ❌ Entirely absent |
| 8. Sensory Science section | ❌ Entirely absent |
| 9. Testimonials slider | ⚠️ Present — formatting issues; missing subtitle |
| 10. Newsletter / Community block | ❌ Missing as standalone — only inside footer |
| 11. Footer | ⚠️ Present — column ratio off; no mobile collapse |

---

## Estimated Fix Effort

| Phase | Work | Estimated Scope |
|---|---|---|
| P0 — Structural | Build `contact.html` + `our-story.html` from scratch | Large (2 new pages) |
| P1 — Global CSS | Fix global CSS (white backgrounds, `.font-sans`, utility classes, footer mobile) | Small (1–2 CSS files) |
| P2 — Critical per-page | Hero images, gallery sticky, reviews HTML, cart table responsive, checkout form mobile | Medium (per-page edits) |
| P3 — Missing PRD sections | Add Rituals & Wellbeing, Sensory Science, Newsletter block to index.html | Medium (new HTML sections) |
| P4 — Major polish | Product names, swatch labels, CTA text, wrong image assets, border-radius violations | Small (scattered fixes) |
| P5 — Minor/responsive | Announcement bar sticky, all mobile responsive overrides, utility classes | Medium (CSS additions) |

---

*Full bug details in `docs/review/bug.md`*
*Per-page task lists in `docs/review/tasks-{page}.md`*
*Fix plan in `docs/review/fix-plan.md`*

