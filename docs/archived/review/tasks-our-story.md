<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# QA Tasks — our-story.html (Our Story / Your Story Community Page)

## Status: REVIEWED
## Audit Date: 2026-03-01
## Viewports Tested: 1440px | 1024px | 375px
## Reference: `screenshots/your-story.jpeg`, `screenshots/your-story.png`, `screenshots/your-voice-matter.png`, `screenshots/our-story-section.png`
## Bugs File: `docs/review/bugs-our-story.md`

---

## Section Checklist

| # | Section | Status | Notes |
|---|---------|--------|-------|
| 1 | Announcement Bar | FAIL | Not sticky — scrolls away. Pure mocha bg color is correct. Text and font are correct. |
| 2 | Site Header / Nav | FAIL | Header background is pure `#ffffff` (violates "no pure white"). No active nav state on current page link. GIFTS nav links to wrong page. |
| 3 | Hero / Page Header | FAIL | H1 uses `font-sans` instead of `font-serif` (RL Limo). Hero padding 64px not reduced for mobile. Background image (`sara.png`) loads correctly. Overlay rgba(63,50,41,0.4) correct. Min-height 640px correct. |
| 4 | Intro Quote Section | PASS | Quote icon, heading text, and dividing line present. Max-width 800px, centered layout correct. Padding 60px 24px applied. |
| 5 | Community Stories Grid | FAIL | 2-column masonry layout correct at 1440px. Story card images use product cut-outs (not lifestyle/editorial community photos). Grid collapses too early at 1024px. Card border-radius is 0px (correct). Card content backgrounds use off-token colours (#E8E6E1 / #F6F4EF). |
| 6 | Split Belief Banner | FAIL | Background uses non-token inline hex `#EBE8E3` overriding CSS class. No responsive collapse for tablet/mobile. Text content correct. Vertical divider line correct. |
| 7 | Submit Your Story Form | FAIL | Character counter is non-functional (no JS). Name/email row has hardcoded inline grid style overriding responsive collapse on mobile. Form text-align is center (cascading from parent, overriding intended left-align). Submit button bg and styling correct. |
| 8 | Footer | FAIL | No single-column collapse at mobile (375px). Social icons use inline SVG correctly. Newsletter form styling correct. Payment icon image loads. BYSARA logo correct. Copyright text correct. |
| 9 | Mobile Overlay Menu | PASS | Menu slides in from right. Close button present. Nav links correct. "SHOP NOW" CTA button present. |
| 10 | Mega Menu | FAIL | Mega menu uses `product-2.png` instead of dedicated `mega-menu-image.png` asset. Menu structure and hover animation correct. |

---

## Critical Tasks (Must Fix Before Launch)

- [ ] **TASK-OST-001** — [BUG-OST-001 / BUG-OST-002] **Create a proper `our-story.html` brand story page.** The current `our-story.html` is a duplicate of `your-story.html` and contains the "Your Story" community content. A new `our-story.html` must be built with the brand founder narrative — matching the layout seen in `screenshots/our-story-section.png` (founder split layout with "GROUNDED IN RITUAL. EMBODIED IN CONFIDENCE." heading, OUR STORY eyebrow, descriptive brand text, and "READ MORE" CTA). Update nav links accordingly.

- [ ] **TASK-OST-002** — [BUG-OST-003] **Make announcement bar sticky.** Add `position: sticky; top: 0; z-index: 1001;` to `.announcement-bar` so the launch messaging persists on scroll. Verify header `top` offset accounts for announcement bar height (38px). Alternatively, wrap announcement + header in a sticky parent container.

- [ ] **TASK-OST-003** — [BUG-OST-001/010] **Fix page `<title>` tag.** If `our-story.html` is repurposed to be the brand story page, title should be `"Our Story | Scents by Sara"`. If kept as the community page, title stays `"Your Story | Scents by Sara"` but the file must be renamed.

---

## Major Tasks

- [ ] **TASK-OST-004** — [BUG-OST-004] **Add active/current-page state to nav.** Apply `aria-current="page"` attribute and a CSS `.nav-links a[aria-current="page"]` style rule (e.g., `border-bottom: 1px solid var(--color-slate)`) on the appropriate nav link per page. The "YOUR STORY" link should be underlined/indicated on `our-story.html` (or the equivalent active page).

- [ ] **TASK-OST-005** — [BUG-OST-005] **Change hero `<h1>` from `font-sans` to `font-serif`.** In `our-story.html` line 164, change `class="font-sans mb-4"` to `class="font-serif mb-4"` so the hero headline renders in RL Limo as per brand typography standards for editorial hero headings.

- [ ] **TASK-OST-006** — [BUG-OST-006] **Replace non-token background colors with brand tokens.** In the `.split-belief` section:
  - Remove inline `style="background-color: #EBE8E3"` from the section element.
  - Update `your-story.css` `.split-belief` rule to use `background-color: var(--color-stone)` (`#E7E3DC`) or `var(--bg-secondary)`.
  - Audit all other inline hex colors on `.ys-content` elements (`#E8E6E1`, `#F6F4EF`) and replace with brand tokens.

- [ ] **TASK-OST-007** — [BUG-OST-007] **Replace product cut-out images in story cards with editorial/lifestyle photography.** Source or create 4 story card images that depict personal/intimate moments (candles in home environments, people, ritual use). If production photography is not yet available, use warm lifestyle placeholder images — not product cut-outs.

- [ ] **TASK-OST-008** — [BUG-OST-008] **Fix mega menu image.** Change `<img src="assets/images/product-2.png">` in the mega menu `mega-image-col` to `<img src="assets/images/mega-menu-image.png" alt="Featured Body Candles">`.

- [ ] **TASK-OST-009** — [BUG-OST-009 / BUG-OST-018] **Prevent masonry grid collapsing at 1024px.** Add a CSS override in `your-story.css`:
  ```css
  @media (max-width: 1024px) {
    .masonry-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  ```
  This prevents the story cards from collapsing to a single column at tablet where 2-column is perfectly readable.

- [ ] **TASK-OST-010** — [BUG-OST-011] **Fix GIFTS nav link.** Change `<a href="shop.html">GIFTS</a>` in the nav to point to the correct gifts page (once created) or to a filtered collection URL.

---

## Minor Tasks

- [ ] **TASK-OST-011** — [BUG-OST-013] **Fix search overlay white background.** In `components.css`, change `.search-overlay { background-color: #ffffff; }` to `background-color: var(--bg-primary);`.

- [ ] **TASK-OST-012** — [BUG-OST-014] **Fix site header white background.** In `components.css`, change `.site-header { background-color: #ffffff; }` to `background-color: var(--bg-primary);`.

- [ ] **TASK-OST-013** — [BUG-OST-015] **Implement or remove the character counter.** Either:
  - Add a JS event listener in `main.js` to count characters on the textarea and update the counter div.
  - Or remove the "0 characters" div entirely if a character limit feature is out of scope for v3.

- [ ] **TASK-OST-014** — [BUG-OST-016] **Fix form text-align cascade.** In `your-story.css`, add:
  ```css
  .ys-form {
    text-align: left;
  }
  ```
  This ensures form labels, inputs and placeholder text align left despite the parent section having `text-center`.

- [ ] **TASK-OST-015** — [BUG-OST-017] **Replace circular slider dots with square indicators.** In `components.css`, remove `border-radius: 50%` from `.dot` and `.testimonials-section .dot` rules (or replace `50%` with `0`). Consider using a short wide rectangle (e.g., `width: 24px; height: 3px`) as a brand-appropriate progress indicator.

- [ ] **TASK-OST-016** — [BUG-OST-012] **Clean up badge text whitespace.** Collapse the multiline `<span class="ys-badge">` content to single lines. Example: change `SHE\n                                IS GRACE` to `SHE IS GRACE`.

---

## Responsive Tasks

### Tablet (1024px)

- [ ] **TASK-OST-017** — [BUG-OST-019] Review hamburger/nav behavior at 1024px. Consider keeping the nav bar visible at 1024px (hiding only below 768px) or testing the mobile overlay menu at tablet size. Update `responsive.css` breakpoint for `.header-bottom { display: none }` to `max-width: 768px` if desired.

- [ ] **TASK-OST-018** — [BUG-OST-020] Add responsive override for the split belief section at 1024px in `your-story.css`:
  ```css
  @media (max-width: 1024px) {
    .split-belief .container {
      flex-direction: column;
      align-items: flex-start;
      gap: 40px;
    }
    .split-belief .container > div:nth-child(2) {
      display: none; /* hide vertical divider */
    }
  }
  ```

### Mobile (375px)

- [ ] **TASK-OST-019** — [BUG-OST-021] Add mobile padding override for `.story-hero-content` in `your-story.css`:
  ```css
  @media (max-width: 768px) {
    .story-hero-content {
      padding: 32px 20px;
    }
  }
  ```

- [ ] **TASK-OST-020** — [BUG-OST-022] Remove hardcoded inline grid style from the form name/email row. Replace:
  ```html
  <div class="grid-cols-2 gap-4 mb-4" style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
  ```
  With:
  ```html
  <div class="grid-cols-2 gap-4 mb-4">
  ```
  The global `.grid-cols-2` responsive rule in `responsive.css` will then correctly collapse this to 1fr at mobile.

- [ ] **TASK-OST-021** — [BUG-OST-023] Add mobile footer collapse to `components.css`:
  ```css
  @media (max-width: 768px) {
    .footer-main-grid {
      grid-template-columns: 1fr;
      gap: 40px;
    }
    .footer-newsletter-col {
      grid-column: span 1;
    }
  }
  ```

- [ ] **TASK-OST-022** — [BUG-OST-024] Add full mobile override for split belief section in `your-story.css`:
  ```css
  @media (max-width: 768px) {
    .split-belief {
      padding: 80px 0;
    }
    .split-belief .container {
      flex-direction: column;
      gap: 32px;
    }
    .split-left,
    .split-right {
      max-width: 100%;
    }
    .split-belief .container > div:nth-child(2) {
      display: none;
    }
  }
  ```

---

## Summary

**Total bugs found: 25**
- Critical: 3
- Major: 6
- Minor: 9
- Responsive (1024px tablet): 3
- Responsive (375px mobile): 4

**Total tasks: 22**
- Critical tasks: 3
- Major tasks: 7
- Minor tasks: 6
- Responsive tasks: 6

**Overall verdict: FAIL — Page requires significant work before production launch.**

The most urgent issue is the missing brand "Our Story" page (the founder narrative page is entirely absent and `our-story.html` is a duplicate of `your-story.html`). Responsive layout for mobile is broken in multiple sections. Typography deviations and brand token usage inconsistencies must also be resolved.

