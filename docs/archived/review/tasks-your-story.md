<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# QA Tasks — your-story.html (Your Story Page)

## Status: REVIEWED
## Audit Date: 2026-03-01
## Viewport Tested: 1440px | 1024px | 375px
## Reference Files: `screenshots/your-story.png`, `screenshots/your-story.jpeg`, `screenshots/your-voice-matter.png`

---

## Section Checklist

| Section | Status | Notes |
|---|---|---|
| Announcement Bar | FAIL | Position is `relative`, not `sticky` — bar scrolls away (BUG-YST-007) |
| Header / Nav | PASS | Logo renders correctly, desktop nav shows at 1440px, hamburger hides; icons present and interactive |
| Mega Menu | MINOR FAIL | Uses `product-2.png` instead of lifestyle image; `mega-menu-image.png` asset exists but unused (BUG-YST-009) |
| Hero Section | FAIL | H1 font resolves to serif (rl-limo) instead of sans (Suisse Int'l) due to missing `.font-sans` class (BUG-YST-001, BUG-YST-002); hero image `sara.png` loads correctly |
| Intro Quote / Eyebrow | MINOR FAIL | H2 renders in serif via `font-sans` class failure; `text-md` utility undefined (BUG-YST-003, BUG-YST-004); quote mark is straight `"` not typographic `"` (BUG-YST-017) |
| "YOUR STORIES" Section Header | MINOR FAIL | `pb-16` and `gap-8` utilities undefined (BUG-YST-011, BUG-YST-012); section-header has no bottom padding |
| Story Cards Grid | FAIL | Card images are bare product shots, not lifestyle photography per reference (BUG-YST-010); badge text contains raw whitespace newlines (BUG-YST-018); card background colors use off-brand hex values not tokens (BUG-YST-015); card H3s render in serif due to BUG-YST-001 |
| Split-Belief Banner | FAIL | No responsive CSS — causes severe horizontal overflow at 375px (BUG-YST-005, BUG-YST-R04); divider height hardcoded (BUG-YST-016) |
| Story Submission Form | FAIL | Two-column grid is hardcoded via inline style, overrides responsive collapse (BUG-YST-006, BUG-YST-R05); `mb-12` class undefined but saved by inline style fallback (BUG-YST-014) |
| Footer Newsletter | PASS | Input, subscribe button, and social icons all render correctly; social SVG icons present (not image-based, so no broken images) |
| Footer Link Columns | MINOR FAIL | "GIFTING" column links "Your Story" to current page (self-referential, misclassified — BUG-YST-019) |
| Footer Bottom Row | PASS | BYSARA logo renders in serif font correctly; payment icons image loads; copyright text correct |
| Mobile Menu Overlay | PASS | Mobile overlay structure present; close button, nav links, and SHOP NOW CTA all present |
| Search Overlay | MINOR FAIL | Background is pure white `#ffffff`, not warm neutral (BUG-YST-008) |

---

## Priority Task List

### P0 — Critical (Fix before any review handoff)

- [ ] **TASK-YST-001** — Add `.font-sans` CSS utility class to `css/layout.css`
  - Add: `.font-sans { font-family: var(--font-sans); }`
  - This resolves BUG-YST-001, BUG-YST-002 and cascades to fix all heading font family issues sitewide
  - File: `css/layout.css`
  - Reference bug: BUG-YST-001, BUG-YST-002

- [ ] **TASK-YST-002** — Add responsive rules for `.split-belief` section to prevent mobile overflow
  - Add `flex-wrap: wrap` and `flex-direction: column` at `max-width: 768px` for `.split-belief .container`
  - Set `split-left` and `split-right` to `max-width: 100%` on mobile
  - File: `assets/css/your-story.css`
  - Reference bug: BUG-YST-005, BUG-YST-R04

- [ ] **TASK-YST-003** — Fix story submission form to be responsive on mobile
  - Remove or override inline `grid-template-columns: 1fr 1fr` for the name/email row at `max-width: 768px`
  - Add media query in `assets/css/your-story.css`: at ≤768px, `.ys-form .grid-cols-2 { grid-template-columns: 1fr; }`
  - Reference bug: BUG-YST-006, BUG-YST-R05

### P1 — Major (Fix before stakeholder/client review)

- [ ] **TASK-YST-004** — Add `.font-weight-normal` utility class to `css/layout.css`
  - Add: `.font-weight-normal { font-weight: 400; }`
  - Reference bug: BUG-YST-003

- [ ] **TASK-YST-005** — Add `.text-md` utility class to `css/layout.css`
  - Add: `.text-md { font-size: var(--text-h2); }` (32px) or define a specific midpoint token
  - Reference bug: BUG-YST-004

- [ ] **TASK-YST-006** — Make announcement bar sticky with the header
  - Option A: Wrap announcement bar + site-header in a sticky `<div class="sticky-header-wrap">` container
  - Option B: Change `.announcement-bar { position: sticky; top: 0; z-index: 1002; }` and adjust header `top` offset
  - Reference bug: BUG-YST-007

- [ ] **TASK-YST-007** — Replace mega menu image with the correct lifestyle asset
  - Change `src="assets/images/product-2.png"` to `src="assets/images/mega-menu-image.png"` on line 132
  - File: `your-story.html`
  - Reference bug: BUG-YST-009

- [ ] **TASK-YST-008** — Replace story card product images with lifestyle photography
  - Source or create 4 lifestyle/UGC-style images for the community story cards
  - Current placeholders: `product-1.png` through `product-4.png`
  - Suggested naming: `story-amara.jpg`, `story-claire.jpg`, `story-nadia.jpg`, `story-priya.jpg`
  - Reference bug: BUG-YST-010

- [ ] **TASK-YST-009** — Add hero responsive padding override for mobile
  - Add: `@media (max-width: 768px) { .story-hero-content { padding: 24px 20px; } }`
  - Reference bug: BUG-YST-R07

### P2 — Minor (Fix before public launch)

- [ ] **TASK-YST-010** — Add missing utility classes to `css/layout.css`
  - `.pb-16 { padding-bottom: 64px; }` (fixes BUG-YST-011)
  - `.gap-8 { gap: 32px; }` (fixes BUG-YST-012)
  - `.tracking-widest { letter-spacing: 0.2em; }` (fixes BUG-YST-013)
  - `.mt-0 { margin-top: 0; }` (fixes BUG-YST-020)
  - `.mb-12 { margin-bottom: 48px; }` (fixes BUG-YST-014, removes need for inline style fallback)

- [ ] **TASK-YST-011** — Fix story card background colors to use design tokens
  - Cards 1 & 3 (`#E8E6E1`): Change to `background: var(--color-stone)` (`#E7E3DC`)
  - Cards 2 & 4 (`#F6F4EF`): Change to `background: var(--bg-primary)` (`#F9F6F2`)
  - Also align the `.split-belief` inline style to use `var(--bg-secondary)` instead of hardcoded `#EBE8E3`
  - Reference bug: BUG-YST-015

- [ ] **TASK-YST-012** — Fix search overlay background color to warm neutral
  - Change `css/components.css` line 149: `background-color: #ffffff` → `background-color: var(--color-sand)`
  - Reference bug: BUG-YST-008

- [ ] **TASK-YST-013** — Fix `.ys-badge` HTML whitespace — remove line breaks inside badge text
  - Lines 199–200, 220–221, 244–245, 265–266 — collapse multi-line badge text to single line
  - Example: Change `SHE\n                                IS GRACE` to `SHE IS GRACE`
  - Reference bug: BUG-YST-018

- [ ] **TASK-YST-014** — Fix typographic quote mark in intro section
  - Line 177: Change `"` to `&#8220;` (left double quotation mark)
  - Reference bug: BUG-YST-017

- [ ] **TASK-YST-015** — Fix footer "GIFTING" column link misclassification
  - Line 426: Replace `<li><a href="your-story.html">Your Story</a></li>` with a proper gifting-related link (e.g., gift guide, gift sets page, or custom gifting page) once those pages exist
  - Reference bug: BUG-YST-019

- [ ] **TASK-YST-016** — Replace hardcoded vertical divider height in split-belief with flexible CSS
  - Change inline `height: 100px` to `align-self: stretch` + `height: auto` with `min-height: 60px`
  - Or control height via CSS class `.split-divider { width: 1px; align-self: stretch; background-color: rgba(163, 147, 130, 0.4); }`
  - Reference bug: BUG-YST-016

- [ ] **TASK-YST-017** — Clean up triple padding conflict on `.intro-quote` section
  - The section has `.container` class (gutter padding), inline `padding: 60px 24px` (overrides gutter), and inline `max-width: 800px`
  - Recommended: Remove `.container` class and use a dedicated `.container-editorial` class or a standalone class; define padding in `assets/css/your-story.css`
  - Reference bug: BUG-YST-R09

---

## Assets to Create / Source

| Asset | Purpose | Priority |
|---|---|---|
| `assets/images/story-amara.jpg` | Lifestyle image for "A Moment of Grace" card | P1 |
| `assets/images/story-claire.jpg` | Lifestyle image for "Reclaiming My Body" card | P1 |
| `assets/images/story-nadia.jpg` | Lifestyle image for "The Gift That Said Everything" card | P1 |
| `assets/images/story-priya.jpg` | Lifestyle image for "Strength in Stillness" card | P1 |
| Confirm `assets/images/mega-menu-image.png` | Verify this is the correct mega menu lifestyle asset | P1 |

---

## Summary

**Total bugs found: 20** (2 critical, 7 major, 11 minor)

| Category | Count |
|---|---|
| Critical | 2 |
| Major | 7 |
| Minor | 11 |
| Responsive — 1024px (Tablet) | 3 |
| Responsive — 375px (Mobile) | 6 |

**Most impactful single fix:** TASK-YST-001 — defining the `.font-sans` CSS class will instantly correct the typography on every heading element across the page and resolves 2 critical bugs in one change.

**Highest mobile risk:** BUG-YST-R04 (split-belief section horizontal overflow at 375px) causes visible page breakage and horizontal scroll — this is the most severe responsive regression.

