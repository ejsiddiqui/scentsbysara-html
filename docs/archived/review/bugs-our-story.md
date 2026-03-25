<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# Bugs — our-story.html (Our Story / "Your Story" Community Page)

**Audit Date:** 2026-03-01
**Auditor:** QA Visual Review
**File audited:** `our-story.html`
**Live URL:** `file:///D:/Ejaz/Epyc%20Digital/Repositories/Scentsbysara/scentsbysara-v3/our-story.html`
**Reference Screenshots:** `screenshots/your-story.jpeg`, `screenshots/your-story.png`, `screenshots/your-voice-matter.png`

---

## Critical

### [BUG-OST-001] File is named `our-story.html` but contains "Your Story" community page content

**Severity:** Critical — Routing / Page Identity Mismatch
**Description:** The file `our-story.html` has its `<title>` set to "Your Story | Scents by Sara" and the entire page content (hero, community story cards, submit form) belongs to the "YOUR STORY" community page — not the brand "OUR STORY" page. A completely separate `our-story.html` page with the brand founder narrative content (seen in `screenshots/our-story-section.png`) does not appear to exist as a standalone page. The nav link "OUR STORY" (`href="our-story.html"`) currently routes to what is actually the "Your Story" community page.
**Evidence:** `<title>Your Story | Scents by Sara</title>`, hero `<h1>YOUR STORY</h1>`, presence of community story submission form. Nav link "YOUR STORY" (`href="your-story.html"`) points to a separate `your-story.html` which appears to be a duplicate of this same file.
**Expected:** `our-story.html` should be the brand founder/brand story page (OUR STORY) with the "Grounded in Ritual. Embodied in Confidence." split layout, brand values, founder narrative — matching `screenshots/our-story-section.png`. The community submission page should be `your-story.html` exclusively.
**Impact:** SEO, internal navigation confusion, brand story page is effectively missing.

---

### [BUG-OST-002] `your-story.html` and `our-story.html` appear to be identical duplicate files

**Severity:** Critical — Duplicate Content / Missing Brand Page
**Description:** Both `our-story.html` and `your-story.html` have the same `<title>`, same CSS includes (`assets/css/your-story.css`), same hero heading ("YOUR STORY"), same content sections, and same structure. The brand "OUR STORY" page (with the founder narrative) is absent from the entire site.
**Evidence:** Both files use `assets/css/your-story.css`, both have `<title>Your Story | Scents by Sara</title>`, both have class `story-hero` with hero text "YOUR STORY".
**Expected:** `our-story.html` must be a distinct page with brand story content — founder background, brand values, editorial split layouts. This was referenced in the `our-story-section.png` screenshot.

---

### [BUG-OST-003] Announcement bar is not sticky — scrolls away from view

**Severity:** Critical — Layout / UX
**Description:** The `.announcement-bar` has `position: relative` (not `position: sticky` or `position: fixed`). Once the user scrolls, the announcement bar disappears, which is inconsistent with ecommerce convention and the brand's launch messaging.
**Evidence:** `window.getComputedStyle(document.querySelector(".announcement-bar")).position` returns `"relative"`.
**Expected:** The announcement bar should be either sticky (scrolls with page) or at minimum the header should be offset to account for the announcement bar height when sticky. Currently only the `.site-header` is `position: sticky`, so the announcement scrolls away while the header sticks.
**Impact:** Launch messaging disappears immediately on scroll.

---

## Major

### [BUG-OST-004] Active nav link "OUR STORY" has no visual active/current-page indicator

**Severity:** Major — Navigation UX
**Description:** The navigation link for "OUR STORY" (`href="our-story.html"`) has no active state styling (no underline, no color change, no bold weight, no border-bottom) to indicate the user is on the current page.
**Evidence:** Nav link audit shows no `.active` class or `aria-current` attribute applied to any link. No inline style or CSS class marks the current page.
**Expected:** Current page nav link should have a visual indicator (underline or color shift). In `your-story.jpeg` reference, "YOUR STORY" nav item appears to have an underline decoration.

---

### [BUG-OST-005] Hero `<h1>` uses `font-sans` (Suisse Int'l) instead of the expected serif font for page headings

**Severity:** Major — Typography Brand Deviation
**Description:** The story hero `<h1>YOUR STORY</h1>` has class `font-sans mb-4` and the computed font-family is `"Suisse Int'l", sans-serif`. Per brand guidelines, editorial/page headings of this weight should use the serif typeface (RL Limo). Comparing against the `your-story.jpeg` reference screenshot, the hero title appears in a different typographic treatment.
**Evidence:** `heroH1Class: "font-sans mb-4"`, computed font is `"Suisse Int'l", sans-serif`.
**Expected:** Hero `<h1>` should use `font-serif` (RL Limo / `var(--font-serif)`) for the editorial headline, consistent with brand guidelines stating "Headlines: RL Limo Regular (serif) — Used for hero titles, section headings".

---

### [BUG-OST-006] Split Belief section background color mismatch vs CSS class definition

**Severity:** Major — Visual Brand Consistency
**Description:** The `.split-belief` section has an inline `style="background-color: #EBE8E3"` which overrides the CSS class rule in `your-story.css` that sets `background-color: #F6F4F0`. The inline value `#EBE8E3` is also not a defined brand token. Both values are close but neither matches a named brand token.
**Evidence:** `splitBeliefInlineStyle: "background-color: #EBE8E3; padding: 120px 0;"`, CSS class uses `#F6F4F0`. Both differ.
**Expected:** Should use a defined brand token (e.g., `var(--color-stone): #E7E3DC` or `var(--bg-secondary)`). Inline style should be removed and the CSS class corrected to a brand token.

---

### [BUG-OST-007] Story cards (masonry grid) use product placeholder images, not real community/story imagery

**Severity:** Major — Content Authenticity
**Description:** All four `.ys-card` story cards use product images (`product-1.png`, `product-2.png`, `product-3.png`, `product-4.png`) as the story illustration photos. These are product photography images (body candles against marble/linen) that have no visual relationship to the community stories being told (e.g., "A Moment of Grace", "Reclaiming My Body").
**Evidence:** Card images: `product-2.png` (Grace), `product-1.png` (Reclaiming), `product-4.png` (Gift), `product-3.png` (Strength). All naturalWidth = 429px — product images confirmed loading.
**Expected:** Story cards should use editorial lifestyle photography showing the product in use, intimate personal moments, or community-submitted images — not product-only cut-out photography. Real story photography assets are needed.

---

### [BUG-OST-008] Mega menu image references `product-2.png` (a plain product cut-out) instead of editorial mega menu imagery

**Severity:** Major — Navigation Visual
**Description:** The mega menu `<div class="mega-image-col">` uses `<img src="assets/images/product-2.png">`. This is a plain product cut-out photo, but `assets/images/mega-menu-image.png` exists and appears to be the correct styled editorial image designed for the mega menu.
**Evidence:** `megaMenuImgSrc: "assets/images/product-2.png"`, `mega-menu-image.png` exists in assets/images/.
**Expected:** Mega menu image should use `assets/images/mega-menu-image.png` as built for this purpose.

---

### [BUG-OST-009] `ys-form .grid-cols-2` name/email field row collapses to single column at 1024px but has no responsive override for the form specifically

**Severity:** Major — Responsive Layout
**Description:** At 1024px and below, the global `.grid-cols-2` rule in `responsive.css` collapses to single column (`grid-template-columns: 1fr`). This means the "YOUR NAME" and "EMAIL ADDRESS" side-by-side form fields will stack vertically at tablet, which is expected for content grids but may be undesirable for the compact form layout (matches the reference at mobile, but may cause excessive vertical height at 1024px with large input padding of 16px each).
**Evidence:** `responsive.css` line 64: `.grid-cols-2 { grid-template-columns: 1fr; gap: var(--space-lg); }` at `max-width: 1024px`. The form row uses `.grid-cols-2`.
**Expected:** At 1024px the form fields stacking is acceptable, but should be verified — the reference `your-story.jpeg` shows them side-by-side. A `.ys-form .grid-cols-2` override may be needed to keep side-by-side down to a narrower breakpoint.

---

## Minor

### [BUG-OST-010] Page `<title>` should reference the actual page in context — "Our Story" if this is `our-story.html`

**Severity:** Minor — SEO / Meta
**Description:** The `<title>` tag reads "Your Story | Scents by Sara". Since the file is `our-story.html` and is linked from the "OUR STORY" nav item, either the title is wrong, or the file is misnamed. This creates SEO confusion and incorrect browser tab labeling.
**Evidence:** `titleText: "Your Story | Scents by Sara"`.
**Expected:** Title should match the page identity: either "Our Story | Scents by Sara" (if this is the brand story page) or the file should be renamed to `your-story.html` and the nav updated.

---

### [BUG-OST-011] `GIFTS` nav link incorrectly routes to `shop.html` instead of a dedicated gifts page

**Severity:** Minor — Navigation
**Description:** The `<a href="shop.html">GIFTS</a>` nav link points to `shop.html`. GIFTS is listed as a separate nav item and should route to a dedicated gifting page or a filtered collection.
**Evidence:** `navLinks` audit: `{text: "GIFTS", href: "shop.html"}`.
**Expected:** GIFTS should link to a `gifts.html` or a filtered `shop.html?collection=gifts` URL.

---

### [BUG-OST-012] Story card badge text has excessive internal whitespace due to multiline HTML formatting

**Severity:** Minor — Content Cleanliness
**Description:** The `.ys-badge` elements contain significant internal whitespace from multi-line HTML formatting, resulting in rendered text like "SHE\n                                IS GRACE". While browsers collapse whitespace in normal rendering, this is sloppy HTML authoring that could cause issues in certain contexts.
**Evidence:** `badgeText: "SHE\n                                IS GRACE"` from DOM inspection.
**Expected:** Badge text should be written on a single line or use `<br>` intentionally: `SHE IS GRACE`.

---

### [BUG-OST-013] Search overlay uses `background-color: #ffffff` — pure white — violating brand standard of "no pure white"

**Severity:** Minor — Brand Compliance
**Description:** The `.search-overlay` in `components.css` is styled with `background-color: #ffffff`, which explicitly contradicts the brand guideline: "No pure black or white — all warm neutral tones".
**Evidence:** CSS rule: `.search-overlay { background-color: #ffffff; }`.
**Expected:** Search overlay background should use `var(--color-sand)` (`#F9F6F2`) or `var(--bg-primary)` for brand compliance.

---

### [BUG-OST-014] Site header background is pure white (`#ffffff`) — violates "no pure white" brand standard

**Severity:** Minor — Brand Compliance
**Description:** The `.site-header` CSS rule sets `background-color: #ffffff` explicitly. Per brand standards, no elements should use pure white; all surfaces should use warm neutral tones.
**Evidence:** CSS: `.site-header { background-color: #ffffff; }`, computed: `headerBg: "rgb(255, 255, 255)"`.
**Expected:** Header background should be `var(--color-sand)` (`#F9F6F2`) or another warm neutral brand token.

---

### [BUG-OST-015] Character counter on textarea defaults to "0 characters" but is non-functional (no JS listener attached)

**Severity:** Minor — Interactive Feature
**Description:** A "0 characters" counter is displayed below the `.ys-textarea` form field, implying a live character count. However, `main.js` does not implement a `keyup` or `input` event listener for this element, so the count never updates.
**Evidence:** HTML: `<div style="text-align: right; font-size: 10px; color: #a39382; padding-top: 4px; letter-spacing: 0;">0 characters</div>`. No corresponding JS was found.
**Expected:** Either implement a working character counter via JS, or remove the non-functional UI element.

---

### [BUG-OST-016] `.ys-form .text-left` class set to `text-align: left` but parent `.story-submit-section` forces `text-align: center`, creating style conflict

**Severity:** Minor — CSS Conflict
**Description:** The form has `class="ys-form text-left"` intending labels and inputs to be left-aligned, but `ysFormTextAlign` is computed as `"center"` — meaning the `text-center` class on the parent section is cascading into the form incorrectly. Form labels and placeholder text should be left-aligned per the reference.
**Evidence:** `ysFormTextAlign: "center"`, parent has `class="story-submit-section section-block container text-center"`.
**Expected:** The `.ys-form` should have an explicit `text-align: left` CSS rule in `your-story.css` to override the parent container's `text-center` directive.

---

### [BUG-OST-017] `dot` slider indicators use `border-radius: 50%` (circular) — violates sharp-corner brand standard

**Severity:** Minor — Brand Compliance
**Description:** The `.dot` class in `components.css` has `border-radius: 50%`, making the slider indicator dots circular. The brand standard mandates `border-radius: 0px` for all elements (sharp corners everywhere). The slider dots appear in the testimonials section and hero dot indicators.
**Evidence:** CSS: `.dot { border-radius: 50%; }`, brand standard: "All border-radius must be 0px (sharp corners everywhere)".
**Expected:** Slider dots should use square/rectangular indicators consistent with the 0px border-radius brand rule, or a line/dash indicator style.

---

## Responsive Issues

### 1024px (Tablet)

#### [BUG-OST-018] At 1024px the `.grid-cols-2` masonry stories grid collapses to single column — all 4 story cards stack in one vertical column

**Severity:** Major (Tablet)
**Description:** `responsive.css` overrides `.grid-cols-2` to `grid-template-columns: 1fr` at max-width 1024px. This collapses the two-column masonry layout into a single vertical stack, dramatically increasing page height and making the masonry presentation meaningless.
**Evidence:** CSS: `@media (max-width: 1024px) { .grid-cols-2 { grid-template-columns: 1fr; } }`.
**Expected:** At 1024px the 2-column stories grid should remain 2-column (it fits comfortably) or collapse gracefully to a single card per row only at mobile (768px or below). A `.masonry-grid` override is needed.

#### [BUG-OST-019] At 1024px the hamburger menu icon is visible but the nav bar (`header-bottom`) is hidden — hamburger has no toggle functionality

**Severity:** Major (Tablet)
**Description:** The responsive CSS hides `.header-bottom` and shows `.hamburger-btn` at 1024px. The hamburger triggers the mobile overlay menu. However, based on DOM snapshot, the hamburger button at 1024px only activates the mobile slide-out menu which is designed for very small screens. At 1024px, a visible nav would be preferable, or the mobile menu should scale better for tablet viewport.
**Evidence:** `responsive.css`: `.header-bottom { display: none }` at 1024px, `.hamburger-btn { display: flex !important }`.

#### [BUG-OST-020] Split belief section flex row layout may overflow or become cramped at 1024px — no tablet-specific override

**Severity:** Minor (Tablet)
**Description:** The `.split-belief .container` uses `display: flex; gap: 60px` with `max-width: 400px` on the left column and `max-width: 360px` on the right. At 1024px with 48px gutters, the available content width narrows significantly, potentially cramping the two columns and the divider line. No responsive override exists for this section.
**Evidence:** No CSS `@media (max-width: 1024px)` rules target `.split-belief`, `.split-left`, or `.split-right`.
**Expected:** At 1024px, consider switching to `flex-direction: column` for the split belief section or reducing `max-width` constraints.

### 375px (Mobile)

#### [BUG-OST-021] Hero section `padding: 64px` on `.story-hero-content` is not overridden for mobile — causes heavy horizontal padding on 375px

**Severity:** Major (Mobile)
**Description:** `.story-hero-content` has `padding: 64px` with no mobile breakpoint override. At 375px viewport width, 64px padding on each side leaves only 247px for content — extremely narrow. The hero headline and body text will be severely constrained.
**Evidence:** `heroContentPadding: "64px"`, `--gutter: 16px` at 375px. No mobile override for `.story-hero-content` in `responsive.css` or `your-story.css`.
**Expected:** On mobile, `.story-hero-content` should reduce to `padding: 24px 20px` or use the gutter variable.

#### [BUG-OST-022] Form grid at 375px: name/email fields collapse to single column correctly, but the 2-column inline form style attribute overrides the responsive CSS

**Severity:** Minor (Mobile)
**Description:** The form name/email row has inline `style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;"`. This inline style will override the `responsive.css` `.grid-cols-2` collapse at mobile, keeping two narrow input fields side-by-side at 375px where single column is required.
**Evidence:** HTML inline style: `style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;"` on the form grid row.
**Expected:** Inline grid style should be removed and the `.grid-cols-2` class should control the collapse. Or add `style="... grid-template-columns: 1fr;"` within a media query override.

#### [BUG-OST-023] Footer main grid collapses to 2 columns at 1024px but has no further collapse to 1 column for mobile (375px)

**Severity:** Major (Mobile)
**Description:** Footer responsive override in `components.css` only defines `grid-template-columns: 1fr 1fr` at max-width 1024px. There is no 768px or 375px override to collapse to single column. At 375px, a 2-column footer grid with content will be very cramped.
**Evidence:** CSS: `@media (max-width: 1024px) { .footer-main-grid { grid-template-columns: 1fr 1fr; } }`. No 768px or 375px override for `.footer-main-grid`.
**Expected:** At 768px or 375px, footer should collapse to a single column layout.

#### [BUG-OST-024] Split belief section does not collapse to column layout on mobile — left/right text will overflow or wrap badly on 375px

**Severity:** Major (Mobile)
**Description:** At 375px, the `.split-belief .container` maintains `flex-direction: row` with 60px gap and max-widths of 400px + 360px. This will severely overflow the 375px viewport. The section has no responsive breakpoint adjustments.
**Evidence:** No `@media` rules for `.split-belief` or `.split-left`/`.split-right` in any CSS file.
**Expected:** At 768px or below, `.split-belief .container` should switch to `flex-direction: column`, reduce padding, and drop the vertical divider line.

---

## Summary

| Severity | Count |
|----------|-------|
| Critical | 3 |
| Major | 6 |
| Minor | 9 |
| Responsive (Tablet 1024px) | 3 |
| Responsive (Mobile 375px) | 4 |
| **Total** | **25** |

