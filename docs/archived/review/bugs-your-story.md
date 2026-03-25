<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# Bugs — your-story.html (Your Story Page)

**Audit Date:** 2026-03-01
**Viewports Tested:** 1440px | 1024px | 375px
**Reference Files:** `screenshots/your-story.png`, `screenshots/your-story.jpeg`, `screenshots/your-voice-matter.png`

---

## Critical

### [BUG-YST-001] `.font-sans` utility class is undefined — all sans-serif headings render in serif font
- **Element:** H1 (hero), all H2 and H3 elements with class `font-sans`, split-belief H2
- **Expected:** Elements marked `.font-sans` should render in `"Suisse Int'l", sans-serif`
- **Actual:** Computed font resolves to `rl-limo, serif` — the base `h1, h2, h3, .font-serif` rule in `layout.css` (line 64–71) applies to all heading tags globally, and since no `.font-sans` rule exists anywhere in the CSS to override it, all headings including those marked `.font-sans` inherit the serif font
- **Affected Elements:** `.story-hero-content h1`, `.intro-quote h2`, `.community-stories h2`, all `.ys-card h3`, `.split-belief h2`
- **Scope:** Sitewide missing utility — not defined in `css/layout.css`, `css/components.css`, `css/responsive.css`, or `assets/css/your-story.css`
- **Impact:** Critical typography regression — the entire page's heading hierarchy renders in the wrong typeface

### [BUG-YST-002] Hero H1 uses `font-sans` class but should match reference — serif font-family mismatch compounds BUG-YST-001
- **Reference (`your-story.jpeg`):** "YOUR STORY" headline appears in a clean sans-serif uppercase face in the hero
- **Actual:** Rendered in `rl-limo` serif (RL Limo), giving the hero headline the wrong character weight and letterform
- **HTML Line:** Line 164 — `<h1 class="font-sans mb-4">`
- **Fix dependency:** Resolving BUG-YST-001 will fix this

---

## Major

### [BUG-YST-003] `.font-weight-normal` utility class is undefined — font-weight override has no effect
- **Elements affected:** `.intro-quote h2`, all `.ys-card h3`, `.split-belief h2`, `.community-stories h2`
- **Expected:** `font-weight: 400` applied via `.font-weight-normal`
- **Actual:** Class has no CSS definition anywhere in the stylesheet chain — the property has no effect (though headings default to `font-weight: 400` via the base heading rule, making this a silent failure)
- **HTML Line:** Line 178, 186, 205, 223, 242, 262, 293

### [BUG-YST-004] `.text-md` utility class is undefined — font-size relies on browser fallback
- **Elements affected:** `.intro-quote h2`, `.community-stories h2` (class `text-md`)
- **Actual Computed Value:** Resolves to `24px` (browser default for H2), not a defined token
- **Expected:** Should map to a design token (likely `--text-h2: 32px` based on the scale)
- **HTML Lines:** Line 178, 186

### [BUG-YST-005] `.split-belief` section has no responsive rule — horizontal flex layout overflows at tablet and mobile
- **Section:** "EVERY SCENT HAS A STORY WAITING TO BE TOLD." split banner (line 286–307)
- **CSS:** `.split-belief .container` uses `display: flex; flex-wrap: nowrap; gap: 60px` with `split-left max-width: 400px` + `split-right max-width: 360px` = minimum 820px needed
- **At 1024px:** Container width is `1024px - 2×48px = 928px` — layout fits but is extremely tight
- **At 375px:** Container width is `375px - 2×16px = 343px` — layout is 820px minimum, causing severe horizontal overflow and horizontal scroll
- **No responsive breakpoint exists** for this section in `css/responsive.css` or `assets/css/your-story.css`
- **Reference (`your-voice-matter.png`):** Section shows a clean stacked layout at narrow sizes

### [BUG-YST-006] Story submission form uses hardcoded `grid-template-columns: 1fr 1fr` inline style — not responsive at mobile
- **HTML Line:** Line 320–321 — `style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;"`
- **At 375px:** The two-column form layout (Name / Email) remains two columns, making each input only ~155px wide — inputs are too narrow and placeholder text is clipped
- **Fix:** The inline style overrides the grid class. The `.grid-cols-2` class in `css/responsive.css` line 64–67 collapses to `grid-template-columns: 1fr` at 1024px, but the inline style always wins over the class
- **Reference (`your-story.jpeg`):** Form shows single-column layout on mobile

### [BUG-YST-007] Announcement bar is not sticky — it scrolls away before the header
- **Element:** `.announcement-bar` — computed `position: relative`
- **Expected:** Announcement bar should stick to the top with the header (or at minimum the header should include the announcement height in its sticky positioning)
- **Actual:** Bar scrolls out of view; header is `position: sticky` but 38px shorter than intended combined height
- **Brand spec:** `--header-height: 132px` = 38px announcement + 94px nav, suggesting both should stay visible
- **Reference:** Reference screenshots show the announcement bar visible at top throughout scroll

### [BUG-YST-008] Search overlay background is pure white — violates brand warm neutral rule
- **Element:** `.search-overlay` in `css/components.css` line 149 — `background-color: #ffffff`
- **Brand standard:** No pure white or black — all warm neutral tones
- **Expected:** Background should be `var(--color-sand): #F9F6F2` or similar warm neutral
- **Impact:** Minor brand violation but breaks the visual system consistency

### [BUG-YST-009] Mega menu image uses `product-2.png` (product photo) instead of a lifestyle/editorial image
- **Element:** `<img src="assets/images/product-2.png" alt="Featured Body Candles">` (line 132)
- **Reference screenshots (mega-menu.png):** Shows a lifestyle/editorial image in the mega menu image column
- **Actual:** Displays the same terracotta product sculpture used in the story cards — not a contextually correct editorial/lifestyle image
- **A dedicated mega menu lifestyle image asset (`mega-menu-image.png`) exists in `assets/images/` but is not used**

### [BUG-YST-010] Community stories card images use generic product shots — reference shows lifestyle photography
- **Cards:** All 4 `.ys-card` elements use `product-1.png`, `product-2.png`, `product-3.png`, `product-4.png`
- **Reference (`your-story.jpeg`):** Story cards in the reference show lifestyle/contextual photography (person handling candle, candle on surface, etc.) — not bare product shots
- **Impact:** Significant visual fidelity gap vs. reference; story cards feel like a product grid rather than a community UGC section

---

## Minor

### [BUG-YST-011] `.pb-16` utility class is undefined — community stories section bottom padding resolves to `0px`
- **Element:** `.community-stories.pb-16` (line 184)
- **Actual:** `padding-bottom: 0px` — class not defined in any CSS file
- **Expected:** Should be `64px` (16 × 4px base unit, following the 8pt spacing scale)
- **Impact:** Stories grid sits flush against the split-belief banner with no breathing room

### [BUG-YST-012] `.gap-8` utility class is undefined — stories section header spacing relies on fallback
- **Element:** `.section-header.gap-8` (line 185) and `.masonry-grid.gap-8` (line 192)
- **Actual:** Gap resolves through `.grid-cols-2` default gap of `64px` (from `var(--space-xl)`) on the masonry grid — the `.gap-8` class has no effect
- **Layout.css defines:** `.gap-2` (8px), `.gap-3` (12px), `.gap-4` (16px) but not `.gap-8`

### [BUG-YST-013] `.tracking-widest` and `.align-end` utility classes are undefined
- **Elements:**
  - `.ys-author.tracking-widest` (lines 211, 232, 257, 278) — letter-spacing resolves to inherited value only
  - `.section-header.align-end` (line 185) — `align-items` resolves through `.flex-between` rule which already sets `align-items: flex-end`, making this redundant but still undefined
- **Impact:** Low — fallback values are close to intended, but the missing class is a fragility

### [BUG-YST-014] `.mb-12` utility class is undefined — submit form description paragraph margin relies on inline fallback
- **Element:** Form description `<p class="text-sm text-muted mb-12">` (line 316) also has `style="margin-bottom: 48px"` as inline override
- **Actual:** Inline style wins; mb-12 has no effect — inline style provides the correct `48px` value
- **Risk:** If inline style is ever removed, the element will use an undefined class with no effect

### [BUG-YST-015] Story cards background color inconsistency — two cards use `#E8E6E1`, two use `#F6F4EF`
- **Cards 1 & 3 (left column):** `background: #E8E6E1` (slightly warm gray)
- **Cards 2 & 4 (right column):** `background: #F6F4EF` (slightly warmer off-white)
- **Reference (`your-story.jpeg`):** Cards appear to use the same unified stone/clay background
- **Brand tokens:** Neither `#E8E6E1` nor `#F6F4EF` are defined design tokens — should use `var(--color-stone): #E7E3DC` for cards on the darker column and `var(--bg-primary): #F9F6F2` or `var(--bg-secondary)` for the lighter
- **Note:** `assets/css/your-story.css` line 60 defines `.split-belief { background-color: #F6F4F0 }` but the section inline style overrides it with `#EBE8E3` — further token drift

### [BUG-YST-016] Split-belief divider uses hardcoded `height: 100px` — may not scale with content height
- **Element:** `<div style="width: 1px; height: 100px; background-color: rgba(163, 147, 130, 0.4);">` (line 298)
- **Issue:** Vertical divider is fixed at 100px but the surrounding text blocks may grow taller on smaller screens, leaving the divider visually truncated
- **Reference (`your-voice-matter.png`):** Divider appears proportional to text height

### [BUG-YST-017] Quote icon (`"`) uses `.font-sans` class but renders in serif — and is not using the correct curly quote character
- **Element:** `<span class="quote-icon" style="color: #A39382; font-size: 35px;">"`</span>` (line 177)
- **Actual font:** `"Suisse Int'l", sans-serif` (eyebrow's computed font) — the quote icon spans uses a CSS fallback OK here but the `"` character is a straight double-quote, not a typographic left-double-quote (`"`)
- **Expected:** Should use `&#8220;` or `"` for correct typographic rendering

### [BUG-YST-018] `.ys-badge` text contains raw newlines and extra whitespace in the DOM
- **Elements:** All `.ys-badge` elements (lines 199, 220, 244, 265)
- **Actual DOM text:** `"SHE\n                                IS GRACE"` — badge renders "SHE" on one line and "IS GRACE" on another due to HTML whitespace
- **Expected:** Badge should read "SHE IS GRACE" as a single line
- **Fix:** Write badge text without line breaks: `<span class="ys-badge">SHE IS GRACE</span>`

### [BUG-YST-019] Footer "GIFTING" column mislinks — `Your Story` links to `your-story.html` (self-referential, not a gifting page)
- **HTML Line:** Line 426 — `<li><a href="your-story.html">Your Story</a></li>` under "GIFTING" footer column
- **Issue:** "Your Story" is a community/UGC page, not a gifting resource — this link is misclassified and self-referential when on the your-story page
- **Expected:** Gifting column should link to a gift guide or gifting-specific page

### [BUG-YST-020] `mt-0` class used on `.story-hero` but class is undefined
- **HTML Line:** Line 161 — `<section class="story-hero mt-0">`
- **Actual:** `mt-0` is not defined in any CSS file — `margin-top` defaults to `0` on section elements anyway, so there is no visible bug, but it represents an undefined class usage

---

## Responsive Issues

### 1024px (Tablet)

#### [BUG-YST-R01] Navigation bar hides but hamburger is visible — layout renders identically to 1440px
- **Observation:** At 1024px, the `.header-bottom` (desktop nav) hides per `css/responsive.css` line 35–37, and the hamburger becomes visible. Layout otherwise matches 1440px which is correct behavior.
- **Issue:** Stories grid collapses from 2-column masonry to 1-column per `.grid-cols-2` override in `responsive.css` line 64–67, but the masonry columns (`masonry-col`) become single stacked full-width columns with no gap between cards — visual result is four cards stacked without the intended 2-column reference layout
- **Reference (`your-story.jpeg`):** At narrower widths, cards still appear in 2-column layout

#### [BUG-YST-R02] Split-belief section starts to become cramped at 1024px
- **At 1024px:** Container width = `1024 - 2×48 = 928px`. Split-left (400px) + gap (60px) + split-right (360px) = 820px. Fits within 928px but leaves only 108px margin — content is tightly packed with no flex breathing room
- **The `flex-wrap: nowrap` with `justify-content: center` prevents wrapping** — if text in either panel grows, overflow will occur

#### [BUG-YST-R03] Form two-column inputs remain at tablet size
- Per BUG-YST-006 — the inline `grid-template-columns: 1fr 1fr` persists at 1024px, overriding the `.grid-cols-2` responsive collapse rule

### 375px (Mobile)

#### [BUG-YST-R04] Split-belief section causes horizontal scroll at 375px (Critical mobile regression)
- **Details:** See BUG-YST-005. At 375px, `split-left (max-width:400px) + gap(60px) + split-right(max-width:360px)` = 820px minimum within a 343px container — content overflows by ~477px
- **Visual result:** "EVERY SCENT HAS A STORY..." headline is cut off; the right-side description paragraph is invisible off-screen; horizontal scrolling appears on the page

#### [BUG-YST-R05] Form grid remains two-column at 375px — inputs are too narrow
- **Details:** See BUG-YST-006. Each input is approximately `(375 - 32 - 16) / 2 = 163px` wide — placeholder text "First & Last Name" and "your@email.com" are both clipped

#### [BUG-YST-R06] Footer grid has no 375px breakpoint — 5-column layout persists beyond 768px breakpoint
- **CSS:** `css/responsive.css` only has a `max-width: 1024px` rule for footer (1fr 1fr grid). No `max-width: 480px` or `max-width: 375px` rule exists for footer
- **At 375px:** Footer collapses to 2-column at 768px breakpoint — this is handled — but the newsletter column and link columns become very narrow
- **Specific issue:** Footer link columns may squeeze below readable width; the "CUSTOMER SERVICE" column title wraps awkwardly

#### [BUG-YST-R07] Hero section content is not centered/padded properly on mobile — text may overflow hero overlay
- **Hero content has `padding: 64px`** on `.story-hero-content` but no responsive override reducing this padding at mobile
- **At 375px:** `64px * 2 = 128px` of horizontal padding inside a 375px container leaves only `375 - 128 = 247px` for the "YOUR STORY" headline at `font-size: 48px` — headline will wrap unexpectedly

#### [BUG-YST-R08] `logo-mobile` / `logo-text` swap breakpoint is at 768px, not 375px — "SCENTS BY SARA" logo text visible at 375px until 768px applies
- **CSS `responsive.css` lines 91–97:** `.logo-text { display: none }` and `.logo-mobile { display: inline-block }` only apply at `max-width: 768px`
- **At 375px:** The full "SCENTS BY SARA" text renders (as 375px < 768px, the rule does apply) — this is technically correct, but the full logo text at `font-size: 32px` in a 375px header is extremely large and may overflow the header

#### [BUG-YST-R09] Intro quote section uses `.container` + inline `max-width: 800px` + inline `padding: 60px 24px` — triple padding conflict
- **At 375px:** `.container` applies `--gutter: 16px` padding on each side. The inline `padding: 60px 24px` overrides the container padding, setting it to 24px each side. The `max-width: 800px` is larger than the 375px screen, so it has no effect — the section works but the `container` class and inline padding are contradictory and may cause issues if the container class changes

