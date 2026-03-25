# PROJECT MASTER — Scents by Sara (V2)

This document serves as the absolute source of truth and architectural brain for the Scents by Sara clean frontend rebuild (V2).

## Superseding Directive Notice
The layout and breakpoint directives in this file are superseded by the `1920px` desktop contract below. If any older guidance conflicts, follow this contract.

## 1. Project Architecture Overview
The frontend is structured as a static HTML/CSS/JS application, strictly built to emulate a premium, luxury editorial ecommerce experience. No heavy frontend frameworks (React/Vue) are permitted to maintain raw load speed and exact DOM control, reflecting high-end Shopify theme standards.

## 2. Folder Structure Explanation
The `v2/` directory is isolated to guarantee a clean build state:
- `/v2/screenshots/` — The unyielding source of visual truth.
- `/v2/docs/` — Core reference files (PRD, this master document).
- `/v2/skills/` — The 10 strict Standard Operating Procedure (SOP) rulebooks.
- `/v2/styles/` — Modular CSS architecture (tokens, typography, layout, components, pages).
- `/v2/scripts/` — Vanilla JS modules (header observer, mega menu logic, cart state).
- `/v2/tests/` — Testing scripts to ensure zero regression.

## 3. Design System Enforcement Summary
Everything scales from the `brand-guideline.png` palette:
- **Brand Colors:** Strict usage of `#F9F6F2`, `#E7E3DC`, `#CEC5B8`, `#A39382`, `#3F3229`, `#2D2B27` mapping to CSS Variables. No pure blacks/whites.
- **Typography:** `RL Limo` (Primary/Display) and `Suisse Int'l` (Body/UI).
- **Layout Contract (Superseding):**
  - Desktop reference breakpoint is `1920px`.
  - Layout is section-based (row model).
  - Section baseline width is `1920px` while sections still support `width: 100%`.
  - Default `.container` width is `1800px` (equivalent to `60px` left/right spacing within a 1920 section).
  - `container-full` is `100%` width with no side margins.
  - For viewports above `1920px`, layout remains boxed and centered.
- **Micro-Aesthetics:** `0px` border-radius globally.

## 4. Page-by-Page Execution Plan
Implementation strictly follows this chronological path:
1. `index.html` (Home Page)
2. `shop.html` (Shop Page)
3. `product.html` (Product Page)
4. `checkout.html` (Checkout Page)
5. `your-story.html` (Your Story Page)

## 5. Screenshot Comparison Workflow
- Implementation shall not be deemed "done" by code completion alone.
- A visual overlay test masking the local build at `50%` opacity over the reference `.png` is mandatory.
- Code adapts to the image, the image does not adapt to the code.

## 6. QA 2–3 Pass Review Rule
No page advances without clearing:
- **Pass 1:** Literal Screenshot Audit (1920px desktop overlay against `references/sections`).
- **Pass 2:** Responsive Integrity (Mobile/Tablet stacking check without reference assets if missing, utilizing system logic).
- **Pass 3:** Code Disciplinary (Review CSS tokens, remove magic variables, verify font weight rendering).

## 7. Screenshot Validation Rule
Developers must declare **"Page Completed — Pixel Perfect Matched"** and include visual proof/artifacts before advancing to the next file in the execution plan. 

## 8. Responsive Testing Breakpoints
- **1920px:** Primary desktop design target (authoritative reference).
- **1440px:** Secondary desktop/laptop adaptation derived from 1920 baseline.
- **1024px:** Tablet Landscape (Nav collapses to hamburger).
- **768px:** Tablet Portrait (Grids fracture to fewer columns).
- **375px:** Minimum Mobile Target (Touch constraints, 1-col strict stacking).
- **>1920px:** Boxed centered layout behavior.

## 9. Header Scroll Logic Rule
The header must hide immediately on any downward scroll distance (`translateY(-100%)`) to favor content visibility, and reappear instantly pinned to the top on any upward scroll vector. Maximum height is `130px`.

## 10. Mega Menu Hover Enforcement
Desktop mega navigation must trigger via CSS `:hover` states with a `0.3s` opacity-fade in, avoiding instant flashes. It spans the full container width and provides structural product links.

## 11. Deployment Testing Checklist
- [ ] Are console errors `0`?
- [ ] Do images lazily load correctly without reflow layout shifts?
- [ ] Are CSS files minified or structured properly?
- [ ] Have all magic numbers (`23px`, `19px`) been purged?
- [ ] Is horizontal scroll eradicated on `375px` views?

## 12. Superseding Notes (2026-03-01)
- Shared layout contract implemented in `css/design-tokens.css`, `css/layout.css`, `css/components.css`, and `css/responsive.css` with section-row baseline (`1920`) and default container (`1800`).
- Route templates are now distinct: `your-story.html`, `our-story.html`, and `contact.html` no longer share byte-identical content.
- Commerce state is unified through `assets/js/cart-state.js`, with page behavior in `assets/js/cart.js`, `assets/js/checkout.js`, `assets/js/product.js`, and `assets/js/shop.js`.
- Form validation now runs through `assets/js/forms.js` for story/contact experiences.
