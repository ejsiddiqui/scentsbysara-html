<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# Bugs — contact.html (Contact Page)

> Audited: 2026-03-01
> Viewport breakpoints tested: 1440px | 1024px | 375px
> Note: This file is named `contact.html` but serves content belonging to the "Your Story" page. See BUG-CNT-001.

---

## Critical

### [BUG-CNT-001] Wrong page content — contact.html renders the "Your Story" page
- **Severity:** Critical
- **Element:** `<main>`, `<title>`, entire page body
- **Detail:** `contact.html` contains the complete "Your Story" community stories page — a hero with Sara's photo, story submission form, 4 community story cards, and a "SUBMIT YOUR STORY" form. There is no Contact Us page content (no contact form with Name / Email / Subject / Order Number fields, no business hours, no direct email address). The `<title>` tag reads `"Your Story | Scents by Sara"` confirming this is copy-paste duplication of `your-story.html`. This page must be replaced or rebuilt from scratch as a dedicated contact page.
- **Impact:** Entire page is wrong. Any customer navigating to "Contact Us" from the nav reaches the Your Story page instead.

---

## Major

### [BUG-CNT-002] Page `<title>` tag is wrong
- **Severity:** Major
- **Element:** `<head> > <title>`
- **Detail:** Title is `"Your Story | Scents by Sara"`. Should be `"Contact Us | Scents by Sara"` or equivalent.
- **Code:** `<title>Your Story | Scents by Sara</title>`

### [BUG-CNT-003] Hero section heading reads "YOUR STORY" — not a contact-appropriate heading
- **Severity:** Major
- **Element:** `.story-hero-content > h1`
- **Detail:** The hero h1 renders "YOUR STORY" in 48px uppercase sans-serif. A contact page should have a heading such as "Contact Us", "Get in Touch", or "Reach Us" styled in RL Limo serif per brand standards for page headers.
- **Code:** `<h1 class="font-sans mb-4" style="font-size: 48px; ...">YOUR STORY</h1>`

### [BUG-CNT-004] Hero image is `sara.png` (Your Story background) — wrong asset for contact page
- **Severity:** Major
- **Element:** `.story-hero` background-image in `assets/css/your-story.css`
- **Detail:** Hero background is set to `url('../images/sara.png')` via `.story-hero` class defined in `your-story.css`. This is correct for your-story.html but is wrong branding context for a contact page. A contact page should use a neutral brand image or a minimal text-only hero.

### [BUG-CNT-005] Contact form is missing — only a story submission form present
- **Severity:** Major
- **Element:** `<form class="ys-form">`
- **Detail:** The form on the page has fields: "YOUR NAME", "EMAIL ADDRESS", and "YOUR NARRATIVE" (textarea). This is a story submission form, not a contact/enquiry form. A contact page requires: Name, Email, Subject/Order Number, Message textarea, and a "Send Message" CTA. None of the expected contact-specific fields exist.

### [BUG-CNT-006] No contact information present — email, phone, business hours all missing
- **Severity:** Major
- **Element:** `<main>`
- **Detail:** Brand standard for a contact page expects direct contact info: email address, social links for support, and business hours. None of these are present. The entire contact info section is absent.

### [BUG-CNT-007] stylesheet `assets/css/your-story.css` is linked — wrong page-specific CSS
- **Severity:** Major
- **Element:** `<head> > <link rel="stylesheet" href="assets/css/your-story.css">`
- **Detail:** The contact page imports `your-story.css` which defines `.story-hero`, `.ys-card`, `.ys-form`, `.ys-input`, `.ys-textarea`, `.split-belief`, etc. — all scoped to the Your Story page. A contact page should use its own `contact.css` or a neutral page-level stylesheet.

---

## Minor

### [BUG-CNT-008] Hero heading uses `font-sans` class — should use `font-serif` for page titles
- **Severity:** Minor
- **Element:** `.story-hero-content > h1`
- **Detail:** The hero h1 carries `class="font-sans"` and inline `font-weight: 400`. Per brand standards, page-level headings should use the RL Limo serif (`font-serif` class / `--font-serif` token). The heading font class is incorrect.
- **Code:** `<h1 class="font-sans mb-4" style="font-size: 48px; ...">`

### [BUG-CNT-009] Search overlay uses pure white background — violates brand palette
- **Severity:** Minor
- **Element:** `.search-overlay` in `components.css` line 149
- **Detail:** `background-color: #ffffff` is pure white. Brand requires warm neutrals. Should use `var(--color-sand)` (`#F9F6F2`) or `var(--color-stone)` (`#E7E3DC`).
- **Code (components.css:149):** `background-color: #ffffff;`

### [BUG-CNT-010] Site header also uses pure white background
- **Severity:** Minor
- **Element:** `.site-header` in `components.css` line 178
- **Detail:** `background-color: #ffffff` is pure white. Should be `var(--color-sand)` to stay fully in the warm neutral palette.
- **Code (components.css:178):** `background-color: #ffffff;`

### [BUG-CNT-011] Mega menu background also uses pure white
- **Severity:** Minor
- **Element:** `.mega-menu` in `components.css` line 268
- **Detail:** `background-color: #ffffff`. Should use `var(--color-sand)` per brand standards (no pure white or black).

### [BUG-CNT-012] Community story cards use product images (product-1 through product-4) as testimonial photos
- **Severity:** Minor (acceptable as placeholder, but will need real community photos)
- **Element:** `.ys-card .ys-img-wrap > img` (four instances)
- **Detail:** All four story cards reference `assets/images/product-1.png` through `product-4.png`. These are product shots used across the site and are not community story/testimonial photos. Will require content replacement.

### [BUG-CNT-013] Mega menu image references `assets/images/product-2.png` — not a dedicated mega menu image
- **Severity:** Minor
- **Element:** `.mega-image-col > img`
- **Detail:** Mega menu references `product-2.png`. The repository contains `mega-menu-image.png` which should be used instead.
- **Code:** `<img src="assets/images/product-2.png" alt="Featured Body Candles">`

### [BUG-CNT-014] `.font-weight-normal` utility class used but not defined in any CSS file
- **Severity:** Minor
- **Element:** Multiple headings use `class="... font-weight-normal"`
- **Detail:** Class `.font-weight-normal` appears on `.intro-quote h2`, story section `h2`, `.split-left h2`, and the form `h2`. This class is not declared in `layout.css`, `components.css`, or `design-tokens.css`. The heading weight would fall back to whatever the element default is (usually `bold` for `h2`). Should be added as `font-weight: 400` to the layout system.

### [BUG-CNT-015] `.mb-12` utility class is used but not defined
- **Severity:** Minor
- **Element:** `.story-submit-section p.text-sm`
- **Detail:** `class="text-sm text-muted mb-12"` — `mb-12` (48px) is not in the spacing utilities defined in `layout.css`. Inline `style="margin-bottom: 48px"` is also present which does the same job but the class is dead weight and creates confusion.

### [BUG-CNT-016] `.pt-24` and `.pb-24` utility classes used but not defined
- **Severity:** Minor
- **Element:** `.story-submit-section`
- **Detail:** `class="... pt-24 pb-24"` — these classes do not exist in the layout utilities. The section also has `style="padding: 120px 24px"` inline, making the classes redundant no-ops.

### [BUG-CNT-017] `.tracking-widest` utility class is used but not defined
- **Severity:** Minor
- **Element:** `.eyebrow` spans and `.ys-author` spans
- **Detail:** Class `tracking-widest` appears on eyebrow labels. Not defined in any CSS file. The letter-spacing is always set via inline style or the `.eyebrow` base class, so no visual regression, but the dead class adds clutter.

### [BUG-CNT-018] `.align-end` utility class used but not defined in layout.css
- **Severity:** Minor
- **Element:** `.section-header.flex-between.align-end`
- **Detail:** `align-end` is not declared in `layout.css`. `flex-between` sets `align-items: flex-end` already, making this redundant, but the missing utility class could cause issues if `flex-between` is changed later.

### [BUG-CNT-019] Character counter shows static "0 characters" — no JavaScript connected
- **Severity:** Minor
- **Element:** `<div style="text-align: right; font-size: 10px; ...">0 characters</div>`
- **Detail:** A character counter div is rendered below the textarea but it always displays "0 characters". There is no JavaScript in `main.js` wiring up an input listener to update this counter dynamically. Either the counter should be removed or the JS should be implemented.

---

## Responsive Issues

### 1024px (Tablet)

#### [BUG-CNT-020] Two-column story form grid collapses to single-column at 1024px — acceptable, but gutter breaks
- **Severity:** Minor — Responsive
- **Element:** `.story-submit-section form .grid-cols-2`
- **Detail:** The responsive rule in `responsive.css` collapses `.grid-cols-2` to `1fr` at 1024px. The name/email two-column form row stacks vertically. This is acceptable stacking behaviour but the inline `gap: 16px` on the grid itself conflicts with the system gap var `--space-xl: 64px` from `.grid-cols-2`. The form grid overrides with inline style `gap: 16px` which is correct, but the class collision means any global grid changes would silently break the form.

#### [BUG-CNT-021] Stories masonry grid collapses to single column at 1024px — left column stacks first, breaking visual rhythm
- **Severity:** Minor — Responsive
- **Element:** `.masonry-grid.grid-cols-2`
- **Detail:** At 1024px, `.grid-cols-2` collapses to a single column. The masonry columns stack sequentially (col-1 then col-2), producing: Card 1 > Card 3 > Card 2 > Card 4. This breaks the intended alternating editorial sequence. Cards should be reordered in DOM to read naturally when stacked.

#### [BUG-CNT-022] Belief banner split layout overflows or wraps awkwardly at 1024px
- **Severity:** Minor — Responsive
- **Element:** `.split-belief .container` inner flex row
- **Detail:** The split-belief section uses a hardcoded flex row with `gap: 60px`, `max-width: 400px` and `max-width: 360px` on each side plus a separator. At 1024px with `--gutter: 48px`, the total minimum width of the three elements (~820px) is tight against the 1024px container. No flex-wrap or stack breakpoint is defined for this section, risking content squeeze or overflow.

### 375px (Mobile)

#### [BUG-CNT-023] Belief banner split section does not stack on mobile — horizontal layout persists and text overflows
- **Severity:** Major — Responsive
- **Element:** `.split-belief .container`
- **Detail:** The split-belief section uses `display: flex` with fixed `max-width: 400px` and `max-width: 360px` per column and `gap: 60px`. No media query changes this to `flex-direction: column` on mobile. At 375px this causes severe horizontal overflow and text truncation. The section is completely broken on mobile.

#### [BUG-CNT-024] Hero h1 "YOUR STORY" (48px) does not scale down on mobile — oversized text
- **Severity:** Minor — Responsive
- **Element:** `.story-hero-content > h1`
- **Detail:** The h1 has a hard-coded inline `font-size: 48px`. The responsive tokens in `responsive.css` at 375px set `--text-h1: 32px`, but this only affects elements using the CSS variable. The inline style overrides all responsive token scaling. At 375px viewport, 48px heading becomes visually dominant and may break line wrapping.

#### [BUG-CNT-025] Form section `max-width: 800px` with `padding: 120px 24px` inline — excessive top/bottom padding on mobile
- **Severity:** Minor — Responsive
- **Element:** `.story-submit-section`
- **Detail:** The section is set with `padding: 120px 24px` via inline style. This is not overridden at mobile breakpoints, resulting in 120px top and bottom padding on a 375px screen — disproportionate spacing. Vertical rhythm collapses. Padding should reduce to ~40–60px on mobile.

#### [BUG-CNT-026] Intro quote section padding not responsive — `padding: 60px 24px` at all sizes
- **Severity:** Minor — Responsive
- **Element:** `.intro-quote` with inline `padding: 60px 24px`
- **Detail:** Section uses inline style padding with no mobile override. At 375px 60px vertical padding is excessive relative to content height. Should reduce to ~32px on mobile.

#### [BUG-CNT-027] Footer main grid collapse at mobile is not defined for 375px
- **Severity:** Minor — Responsive
- **Element:** `.footer-main-grid`
- **Detail:** `components.css` defines a 1024px breakpoint for the footer grid (`1fr 1fr`), but no 375px/mobile breakpoint collapses it to a single column. The 2-column footer grid persists on mobile, causing cramped link columns.

