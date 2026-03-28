# Mobile 480px Visual QA — Issue Tracker

Reference: `html/index.html` + `html/css/responsive.css`
Date: 2026-03-28

---

## Issues

| # | Section | Issue | Status |
|---|---------|-------|--------|
| 1 | Hero | Heading too large at 480px (text-h1 = 47px) | ✅ Done — section-hero.css already had 480px rule (text-h3) |
| 2 | Collections Grid | Stacked layout instead of horizontal carousel | ✅ Done — added 480px carousel CSS to collections-grid.liquid |
| 3 | Collections Grid | `overflow: clip` blocked horizontal scroll | ✅ Done — overridden on section + container |
| 4 | Collections Grid | DISCOVER NOW button visible on mobile (should be hidden) | ✅ Done — `display: none` on button at 480px |
| 5 | Collections Grid | Collection card title used serif font (should be sans) | ✅ Done — `font-family: var(--font-sans)` at 480px |
| 6 | Bestsellers | Product card width too narrow (78vw ≈ 374px; should be calc(100% - 44px)) | ✅ Done — added 480px override to featured-collection.liquid |
| 7 | Bestsellers | Section title too large (24px serif; should be ~13px sans) | ✅ Done — added font-size/family override to featured-collection.liquid |
| 8 | Commitment | No background colour (transparent instead of --color-stone) | ✅ Done — added `background-color: var(--color-stone)` at 480px |
| 9 | Commitment | Section padding not removed (padding-block should be 0) | ✅ Done — `padding-block: 0` at 480px |
| 10 | Commitment | Content side padding too wide (`0 80px` inner-gutter; should be ~20px) | ✅ Done — overridden to `var(--space-lg) var(--gutter)` at 480px |
| 11 | Commitment | Heading too large (47px; should be ~text-h4 = 25px) | ✅ Done — overridden to `var(--text-h4)` at 480px |
| 12 | Testimonials | Heading too large (47px text-h1; should be text-small = 13px) | ✅ Done — added {% style %} block to testimonials.liquid |
| 13 | Testimonials | Testimonial quote text too large (should be text-body) | ✅ Done — added to testimonials.liquid 480px style |

| 14 | Mobile Menu | Footer (login/newsletter/social) not pushed to viewport bottom | ✅ Done — changed panels to flex column, panel to flex:1 |
| 15 | Mobile Menu | Nav items had border-bottom separators; mockup uses gap only | ✅ Done — removed border-bottom, padding set to 0 |
| 16 | Mobile Menu | Nav item gap too small (1rem vs 32px in mockup) | ✅ Done — changed to var(--space-lg) |

---

## All issues resolved ✅
