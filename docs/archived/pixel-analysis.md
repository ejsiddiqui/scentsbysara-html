# Pixel Analysis & Design Architecture Report

## Superseding Directive Notice
The layout directives below supersede any older conflicting values in prior docs.

## 1. Global Viewport & Layout
- **Reference Baseline:** `references/sections/` screenshots are authored at `1920px` desktop and are the primary source of truth.
- **Viewport Assumption:** 1920px (Primary Desktop), 1440px (Desktop/Laptop adaptation), 1024px (Tablet), 768px (Mobile), 375px (Small Mobile).
- **Section Model:** Section-based rows.
- **Section Width Contract:** Each section supports `width: 100%` with a `1920px` design baseline.
- **Default Container Width:** `1800px` content area.
- **Section Side Margins at 1920:** `60px` left and `60px` right.
- **Boxed Layout Rule:** Viewports above `1920px` remain centered and boxed.
- **Container Full Variant:** `.container-full` is `100%` width with no side margins.
- **Vertical Rhythm:** Maintained via strict 8pt modular scale.

## 2. Header Dimensions
- **Announcement Bar:** 38px
- **Main Navigation:** 94px
- **Total Max Height:** 132px precisely.

## 3. Typography Scale & Fonts
- **Font Families:**
  - Serif (Headings/Display): `RL Limo`
  - Sans-Serif (Body/UI/Sub: `Suisse Int'l`
- **Typographic Hierarchy:**
  - Hero Text: 56px (max), line-height 1.1
  - H1 Text: 48px, line-height 1.2
  - H2 Text: 32px, line-height 1.3
  - Body Text: 16px & 18px (Editorial), line-height 1.6
  - UI Labels / Micro Text: 11px, letter-spacing 0.1em, Uppercase.

## 4. Brand Color Palette (Hex Values)
- **Primary Background (Sand):** `#F9F6F2`
- **Secondary Background (Stone):** `#E7E3DC`
- **Tertiary Border (Clay):** `#CEC5B8`
- **Muted Text (Taupe):** `#A39382`
- **Accent/Hover (Warm Mocha):** `#3F3229`
- **Primary Text (Slate):** `#2D2B27`

## 5. Component Restrictions & Styling
- **Border Radius:** Maximum 2px strictly enforced.
- **Buttons:** 
  - Primary (Solid): Background `#3F3229`, Text `#F9F6F2`, border 1px solid `#3F3229`. Hover state inverts to transparent with `#3F3229` text.
  - Text: `SHOP NOW`
- **Product Cards:**
  - No gray outer wrapper/border around image.
  - Image aspect ratio: ~4:5 (Tall crop). Full-width spanning.

## 6. Structural Implementation Plan
As requested, the CSS architecture will be modularized into the exact requested structure:
- `/v2/css/design-tokens.css` (Variables, Colors, Fonts, Roots)
- `/v2/css/layout.css` (Containers, Grids, Header/Footer wrappers)
- `/v2/css/components.css` (Hero, Cards, Buttons, Inputs, Sliders)
- `/v2/css/responsive.css` (Media queries anchored from 1920 baseline: 1920, 1440, 1024, 768, 375)

*Assumptions:* The existing `assets/css` directory will be deprecated in favor of this new `/css/` root as mandated inside the `/v2/` directory to satisfy Phase 2 architectural constraints. We will refactor HTML files to respect these modular links.

## 7. Superseding Notes (2026-03-01)
- Implemented baseline section-row behavior using `--section-max: 1920px`, `--container-max: 1800px`, and `--gutter: 60px`.
- Added explicit boxed verification assets for widths above `1920` in `docs/qa/final/*-2200.png`.
- Responsive verification evidence for `1920`, `1440`, `1024`, `768`, `390`, and `375` is now captured in `docs/qa/final/`.
