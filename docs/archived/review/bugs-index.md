<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# Bugs — index.html (Homepage)
**Audit Date:** 2026-03-01
**Auditor:** QA Review (Claude Code)
**Page:** `index.html` — Homepage
**References:** `screenshots/v3-hero.png`, `screenshots/v2-header-hero.png`, `screenshots/v2-best-sellers.png`, `screenshots/v2-collections.png`, `screenshots/v2-our-story.png`, `screenshots/v2-testimonials.png`, `screenshots/v2-footer.png`, `screenshots/home-page.png`, `screenshots/footer-fix.png`, `screenshots/mobile-full.png`, `screenshots/mobile-header.png`

---

## Critical

- **[BUG-IDX-001] Hero slider uses same image for all 3 slides**
  - **Location:** `<section class="home-hero">`, `.hero-slide` elements (lines 164–173)
  - **Expected:** Three distinct full-bleed hero images showing different body candle compositions, as seen in `v2-header-hero.png` and `v3-hero.png`
  - **Actual:** All three `<div class="hero-slide">` elements reference the same image: `assets/images/hero-bg.png`. The slider navigates but shows identical content on every slide, making the slider UX meaningless.
  - **Fix:** Provide `hero-bg-2.png` and `hero-bg-3.png` (or use existing `Hero-slide-bg.png` / `bg2.png`) and assign each slide a unique image.

- **[BUG-IDX-002] Header uses pure white (`#ffffff`) background — violates brand standard**
  - **Location:** `css/components.css` line 178: `background-color: #ffffff;`
  - **Expected:** Header background should be `#F9F6F2` (sand) per brand guidelines. Reference screenshots (`v3-hero.png`, `v2-header-hero.png`) show the header rendered in the warm sand/ivory tone.
  - **Actual:** Header `background-color` is hard-coded to `#ffffff` (pure white), which breaks the "no pure black or white" brand rule and creates a visible mismatch against the hero image.
  - **Fix:** Change `background-color: #ffffff` to `background-color: var(--bg-primary)` (`#F9F6F2`).

- **[BUG-IDX-003] Search overlay uses pure white (`#ffffff`) background — violates brand standard**
  - **Location:** `css/components.css` line 149: `background-color: #ffffff;`
  - **Expected:** Search overlay background should be `var(--bg-primary)` (`#F9F6F2`)
  - **Actual:** Hard-coded `#ffffff` (pure white)
  - **Fix:** Replace with `var(--bg-primary)`.

- **[BUG-IDX-004] Mega menu uses pure white (`#ffffff`) background — violates brand standard**
  - **Location:** `css/components.css` line 268: `background-color: #ffffff;`
  - **Expected:** Per `mega-menu.png` reference, the dropdown uses the warm ivory/sand background, not pure white.
  - **Actual:** Hard-coded `#ffffff` on `.mega-menu` rule
  - **Fix:** Replace with `var(--bg-primary)`.

- **[BUG-IDX-005] Commitment section design completely differs from references — OUR COMMITMENT section has wrong layout**
  - **Location:** `<section class="section-block commitment-section">` (lines 258–297)
  - **Expected per v2-commitment.png / v4-commitment-full.png / v5-commitment-full.png:** The "Our Commitment" section in the reference uses a dark mocha (`#3F3229`) full-width background with a centered heading at the top, left-side icons (eco-friendly leaf, handmade hands, cruelty-free icons), body text for each item, and a right-aligned image block (grayscale/editorial hands image).
  - **Actual:** The implementation uses a two-column grid (`grid-cols-2`) on a sand background (`var(--bg-primary)`), with the `our-commitment-left.png` image on the left and commitment text on the right, using an eyebrow label, serif headline in taupe, and 4 commitment items. The heading "OUR COMMITMENT" is right-aligned in the text column, not centered above the section.
  - **Impact:** Section is visually unrecognizable compared to references. Background should be dark mocha, layout should be different.

- **[BUG-IDX-006] "Our Commitment" image asset (`our-commitment-left.png`) may not match design intent**
  - **Location:** `<img src="assets/images/our-commitment-left.png">` (line 261)
  - **Expected:** Reference screenshots (`v2-commitment.png`) show a close-up editorial grayscale image of hands/skin on the right side of the dark section.
  - **Actual:** The file `our-commitment-left.png` exists but is positioned on the left in a sand-background two-column layout. The image file `our-commitment.png` (which is the correct editorial hands photo) exists in assets but is not used.

- **[BUG-IDX-007] Collections section shows only 2 collections — reference shows 3**
  - **Location:** `<section class="section-block collections-section">` (lines 300–332)
  - **Expected per v2-collections.png / v2-collections-full.png / v5-commitment-full.png:** Collections grid shows 3 cards — "Custom Collections", "Gold Collections", and "Plus Size Collections" — in a 3-column layout with overlaid text labels.
  - **Actual:** Only 2 collection cards are present ("The Lived-In Body Collection" using `custom-collections.png` and "The Sculpted Collection" using `gold-collections.png`). The Plus Size collection card is missing. Layout is 2-column (`grid-cols-2`) with text content blocks below each image rather than overlaid labels.

- **[BUG-IDX-008] Hero slider has no previous/next arrow controls**
  - **Location:** `<section class="home-hero">` (lines 162–185)
  - **Expected:** Reference screenshots show previous/next arrow navigation on the hero slider in addition to dots.
  - **Actual:** Only dot navigation is present. No left/right arrow buttons exist in the HTML. The `main.js` slider logic also has no arrow button hookup.

---

## Major

- **[BUG-IDX-009] Hero nav items mismatch reference — "GIFTS" replaces "COLLECTIONS" and "RITUALS"**
  - **Location:** `<nav class="nav-links">` (lines 82–140)
  - **Expected per v3-hero.png / mega-menu.png:** Navigation shows: SHOP | COLLECTIONS | OUR STORY | CONTACT (or SHOP | GIFTS | OUR STORY | YOUR STORY | CONTACT US as variations)
  - **Actual:** Navigation items are: SHOP (with mega menu) | GIFTS | OUR STORY | YOUR STORY | CONTACT US. The "COLLECTIONS" link mentioned in the PRD expected sections (#2) is absent. There is no dedicated Collections nav link; instead, collections appear only in the SHOP mega menu.
  - **Note:** The mega-menu reference shows "SHOP | COLLECTIONS | OUR STORY | CONTACT" at top level.

- **[BUG-IDX-010] Hero CTA uses only one button — reference shows two CTAs**
  - **Location:** `<div class="hero-content container">` (lines 174–178)
  - **Expected per v3-hero.png / v2-header-hero.png:** Hero section shows two CTA buttons (e.g., "EXPLORE COLLECTIONS" and a secondary CTA)
  - **Actual:** Only one CTA button is present: `<a href="shop.html" class="btn-solid">SHOP NOW</a>`. The button uses the `.btn-solid` class rather than `.btn-hero`. The reference shows "EXPLORE COLLECTIONS" as the CTA text.

- **[BUG-IDX-011] Hero headline text mismatch from reference**
  - **Location:** `<h1 class="font-serif text-hero">` (line 175)
  - **Expected per v2-header-hero.png:** Headline reads "Hand Made Bespoke Candles" (mixed case, serif)
  - **Actual:** Headline reads "HAND MADE BESPOKE CANDLES" (full uppercase). The CSS class `.text-hero` applies `text-transform: uppercase`, which matches, but the reference screenshot clearly shows mixed-case rendering ("Hand Made / Bespoke / Ca..." with natural case). Additionally, the hero content has `padding-left: var(--gutter)` which may left-align text away from center even on tablet (the tablet responsive override sets `padding-left: 0` and centers the text).

- **[BUG-IDX-012] "OUR STORY" section — image asset missing; `sara.png` referenced but design called for lifestyle/window-blind photo**
  - **Location:** `<div class="story-img-block"><img src="assets/images/sara.png">` (line 351)
  - **Expected per v2-our-story.png / v3-our-story-final.png:** The right column shows a lifestyle window-blind ambient photo (the blurred bokeh candle/window photo). The text block is on the left with a dark mocha or secondary background.
  - **Actual:** `sara.png` is referenced (founder portrait), and the text block background is `bg-secondary` (stone). The references show two distinct Our Story design versions — the v3 final shows the window-blind ambient photo with text overlay as a full-bleed split, with a dark overlay quote block on the right. The current implementation with `sara.png` may be intentional (founder photo) but the cited reference `v2-our-story.png` shows a different image.

- **[BUG-IDX-013] Best sellers product cards missing "ADD TO BASKET" button — reference shows this label**
  - **Location:** `.product-btn` (lines 206, 221, 236, 251)
  - **Expected per v2-best-sellers.png / v2-commitment.png:** Product cards display an "ADD TO BASKET" button below the price.
  - **Actual:** All four product cards use `SHOP NOW` as the button text. The reference screenshots (`v2-commitment.png`, `v4-commitment.png`) clearly show "ADD TO BASKET" on the product cards.

- **[BUG-IDX-014] Testimonials section missing subtitle/descriptor text visible in reference**
  - **Location:** `<section class="section-block testimonials-section">` (lines 357–411)
  - **Expected per home-page.png:** Below "CUSTOMER TESTIMONIALS" heading there is a subtitle line: *"What our customers are saying?"* in italics.
  - **Actual:** No subtitle text element exists in the HTML. The section jumps directly from the `h2` to `.stars`.

- **[BUG-IDX-015] Testimonial author name formatting differs — no dash prefix in reference**
  - **Location:** `<p class="testimonial-author">EUNICE YUMBA</p>` (line 375)
  - **Expected per home-page.png:** Author shown as `- Eunice Yumba` with a dash prefix in sentence case.
  - **Actual:** Current HTML renders `EUNICE YUMBA` (all caps, no dash). CSS `.testimonial-author` applies `text-transform: uppercase` and `letter-spacing: 0.2em`. Reference uses sentence case with a leading dash.

- **[BUG-IDX-016] Quote marks positioned using `position: absolute` with `top: 50%` — causes overlap with multi-line quotes**
  - **Location:** `css/components.css` lines 622–639, `.quote-mark` styles
  - **Expected:** Opening and closing quote marks should flank the testimonial text visually without overlapping the body text.
  - **Actual:** Both `.quote-mark.left` and `.quote-mark.right` are `position: absolute; top: 50%; transform: translateY(-50%)` — this centers them vertically relative to `.testimonial-content`, not relative to the text. For multi-line quotes this will place the marks mid-way through paragraphs, overlapping text.

- **[BUG-IDX-017] Collections section missing "OUR COLLECTIONS" heading**
  - **Location:** `<section class="section-block collections-section">` (lines 300–332)
  - **Expected per v2-collections-full.png / v5-commitment-full.png:** A large centered "OUR COLLECTIONS" heading appears above the collection image grid.
  - **Actual:** No heading exists in the collections section HTML. The section goes directly from the container to the two collection cards.

- **[BUG-IDX-018] `container-editorial` inside `.story-text-block` adds extra gutter padding on top of existing block padding**
  - **Location:** `<div class="container-editorial">` (line 340) inside `.story-text-block` which already has `padding: var(--space-4xl) var(--gutter)`
  - **Expected:** Editorial text container should constrain max-width of text for readability without double-applying gutter.
  - **Actual:** `.container-editorial` applies `padding-left: var(--gutter)` and `padding-right: var(--gutter)` (100px each at max width), adding those on top of `.story-text-block`'s own `padding: var(--space-4xl) var(--gutter)`. This effectively doubles the horizontal padding, creating an excessively narrow text column.

- **[BUG-IDX-019] Footer social icons use large SVG inline paths (32px) rather than icon image assets**
  - **Location:** Footer social icons (lines 427–451)
  - **Expected per footer-fix.png:** Social icons rendered at a smaller, uniform size with consistent visual weight, using the icon image files (`icon-instagram.png`, `icon-tiktok.png`, `icon-pinterest.png`) that exist in the assets folder.
  - **Actual:** Large inline SVG paths at `width="32" height="32"` are used. The `footer-social-group img` CSS rule applies a filter to image elements, but these are SVG elements, not `<img>` tags, so the filter rule does not apply. Additionally, there is no Facebook icon in the reference footer (only Instagram, TikTok, Pinterest are shown in `footer-fix.png`), but Facebook is included in the HTML.

- **[BUG-IDX-020] QA overlay script (`qa-overlay.js`) left in production HTML**
  - **Location:** `<script src="assets/js/qa-overlay.js"></script>` (line 539)
  - **Expected:** Dev/QA tooling scripts must be removed before production. The script injects a red "Toggle QA Overlay" button fixed to the bottom-right of every page viewport.
  - **Actual:** The `qa-overlay.js` script is included in `index.html` with an inline comment noting "QA Tooling (Remove before prod)" — the reminder exists but the file is still referenced.

---

## Minor

- **[BUG-IDX-021] Mega menu image references `product-2.png` — not a dedicated mega menu image**
  - **Location:** `<img src="assets/images/product-2.png" alt="Featured Body Candles">` (line 131)
  - **Expected:** `mega-menu.png` reference and the `assets/images/mega-menu-image.png` file exist specifically for this slot.
  - **Actual:** Product card image reused. File `assets/images/mega-menu-image.png` exists in the assets but is not used.

- **[BUG-IDX-022] `logo-text` renders "SCENTS BY SARA" but reference shows "BYSARA" in most screens**
  - **Location:** `<a href="index.html" class="logo-text font-serif">SCENTS BY SARA</a>` (line 38)
  - **Expected per v3-hero.png / v2-header-hero.png / mega-menu.png:** The desktop header shows "BYSARA" as the logo wordmark, not "SCENTS BY SARA". The full name appears in the footer as the brand wordmark.
  - **Actual:** The desktop `.logo-text` shows "SCENTS BY SARA" (32px serif). The mobile `.logo-mobile` shows "BYSARA". The reference consistently shows "BYSARA" in the header center — even on desktop. The `logo.svg` and `logo-long.svg` assets exist but are not used; a text-based logo is used instead.

- **[BUG-IDX-023] Announcement bar text wraps or overflows on narrow viewports due to no truncation/marquee**
  - **Location:** `<div class="announcement-bar">` (line 18)
  - **Text:** "LAUNCHING MARCH 2026 - JOIN THE WAIT LIST FOR EARLY ACCESS"
  - **Expected per mobile-header.png:** On mobile, the announcement bar wraps to two lines ("LAUNCHING MARCH 2026 — JOIN THE WAITLIST FOR / EARLY ACCESS"), which increases header height beyond the `38px` announcement height variable and pushes the nav down.
  - **Actual:** The `.announcement-bar` is fixed at `height: var(--announcement-height)` (38px) with no `overflow: hidden` or multi-line allowance. On narrow viewports (375px) where gutter is 16px, the text will overflow or clip rather than wrap gracefully.
  - **Note:** Mobile screenshot `mobile-header.png` appears to show the two-line version fitting, suggesting height may expand — but the `38px` token would need to be `min-height` not `height`.

- **[BUG-IDX-024] Slider dots use `border-radius: 50%` (circular) — violates brand's `0px` border-radius standard**
  - **Location:** `css/components.css` lines 468, 675 — `.dot { border-radius: 50%; }` and `.testimonials-section .dot { border-radius: 50%; }`
  - **Expected:** Brand standard mandates `--radius-max: 0px` (sharp corners everywhere). Slider dots are visually an exception in the references (they appear circular in screenshots), but the strict brand rule should be noted as a deviation.
  - **Actual:** Dots use `border-radius: 50%`. This is a design discretionary element, but it is a technical deviation from the `--radius-max: 0px` token.

- **[BUG-IDX-025] `.hero-content` has redundant `max-width: var(--container-max)` and `padding-left: var(--gutter)` when it already has class `container` which applies those values**
  - **Location:** `css/components.css` lines 426–431
  - **Expected:** Container class should handle max-width and padding uniformly.
  - **Actual:** `.hero-content` has both the `container` class in HTML (which applies `max-width: 1920px; padding: 0 100px`) AND additional CSS rules setting `max-width: var(--container-max)` and `padding-left: var(--gutter)` with no `padding-right`, effectively nullifying the right padding from `.container`. This means hero text will bleed to the right edge at wide viewports.

- **[BUG-IDX-026] `font-family` path mismatch — `design-tokens.css` declares `SuisseIntl-Regular.woff2` but fonts are in `/assets/fonts/` while CSS path is `../assets/fonts/`**
  - **Location:** `css/design-tokens.css` lines 77, 84, 91, 97 — `src: url('../assets/fonts/...')`
  - **Expected:** Font paths must resolve correctly relative to the CSS file location (`css/` directory, so `../assets/fonts/` = correct).
  - **Actual:** The path `../assets/fonts/` from `css/design-tokens.css` resolves to `assets/fonts/` at the root — which is correct since `css/` is one level deep. However, this should be verified as working since the Suisse Intl font family is critical for brand accuracy.

- **[BUG-IDX-027] `has-mega-menu` uses `position: static` but parent `.nav-links` is inside `.header-bottom` which may not be `position: relative`**
  - **Location:** `css/components.css` line 257 — `.has-mega-menu { position: static; }`
  - **Expected:** Mega menu dropdown uses `position: absolute; top: 100%` relative to the `.site-header`.
  - **Actual:** `.site-header` is `position: sticky` (line 179), so absolute children of a static-positioned nav item will position relative to the sticky header, which is correct. However, the `top: 100%` on `.mega-menu` references its nearest positioned ancestor. Without explicit `position: relative` on the header, the mega menu may miscalculate its top position.

- **[BUG-IDX-028] `footer-main-grid` has mismatched column template with reference**
  - **Location:** `css/components.css` line 892: `grid-template-columns: 3.5fr 1fr 1fr 1fr 1.5fr`
  - **Expected per footer-fix.png:** Newsletter column is visually wider than other columns but not 3.5x wider. The reference shows approximately a 2:1:1:1:1.5 ratio.
  - **Actual:** `3.5fr` makes the newsletter column extremely wide relative to the link columns, which may cause the link columns to appear cramped at standard viewport widths.

- **[BUG-IDX-029] No `<section>` heading for the Rituals & Wellbeing section — section entirely absent from HTML**
  - **Location:** Between Collections section and Our Story section in `index.html`
  - **Expected per PRD (Section 7):** "Rituals & Wellbeing content teaser" section is listed as a required homepage section.
  - **Actual:** No Rituals & Wellbeing section exists in the current `index.html`. The page goes from Collections directly to Our Story.

- **[BUG-IDX-030] No Sensory Science / Scent Story section — section entirely absent from HTML**
  - **Location:** Between Our Story and Testimonials in `index.html`
  - **Expected per PRD (Section 8):** "Sensory Science / Scent Story section (3–4 icon points)" is a required homepage section.
  - **Actual:** No such section exists. The page goes from Our Story split directly to Testimonials.

- **[BUG-IDX-031] Newsletter/Community block absent as standalone section — rolled into footer only**
  - **Location:** No standalone section between Testimonials and Footer
  - **Expected per PRD (Section 10):** A dedicated "Newsletter / Community block" above the footer.
  - **Actual:** Newsletter form only exists inside the footer. No standalone newsletter banner/community block with visual treatment exists on the page.

- **[BUG-IDX-032] `commitment-text` has `padding-left: var(--gutter)` creating asymmetric double-gutter with container**
  - **Location:** `css/components.css` line 702: `.commitment-text { padding-left: var(--gutter); }`
  - **Expected:** Text column should use natural grid gap for spacing from the image column.
  - **Actual:** The `.commitment-section .container` already has `padding-left: var(--gutter)` from the `.container` class. The `.commitment-text` adds another `var(--gutter)` on top, creating `200px` of left offset on the text block at desktop widths. This is excessive and misaligns with the reference design.

- **[BUG-IDX-033] `story-split` section adds `margin-top: var(--space-section)` (80px) on top of `section-block` padding — double-spacing**
  - **Location:** `css/components.css` line 814: `.story-split { margin-top: var(--space-section); }`
  - **Expected:** Consistent 80px section separation.
  - **Actual:** The collections section above uses `.section-block` with `padding-bottom: var(--space-section)` (80px), then `.story-split` adds `margin-top: 80px`, creating 160px of whitespace between collections and Our Story, significantly more than other section gaps.

---

## Responsive Issues

### 1440px (Laptop/Desktop)

- **[BUG-IDX-034] Gutter reduces to 80px at 1440px but hero content `padding-left` is not overridden**
  - **Location:** `css/responsive.css` line 9: `--gutter: 80px` at max 1440px
  - **Actual:** The `.hero-content` CSS applies `padding-left: var(--gutter)` so it will reduce to 80px correctly via the CSS variable. However, `.hero-content` inside `.container` also inherits `.container`'s `padding-left`. The two padding sources compound.

- **[BUG-IDX-035] `footer-main-grid` column proportions create cramped link columns at 1440px**
  - **Location:** `css/components.css` line 892
  - **Actual:** At 1440px viewport with 80px gutters, the available content width is approximately 1280px. The `3.5fr` newsletter column consumes ~530px, leaving ~750px for four link columns (~188px each). At 100px gutters the proportions are even more extreme.

### 1024px (Tablet)

- **[BUG-IDX-036] Nav collapses but hamburger icon does not visually confirm open state**
  - **Location:** `assets/js/main.js` — hamburger toggle logic; `aria-expanded` attribute used for state.
  - **Expected:** Hamburger icon changes to an X or otherwise signals open state.
  - **Actual:** The JS toggles `aria-expanded` attribute and adds `.active` to the mobile menu overlay, but the hamburger SVG icon remains the three-line hamburger icon — it does not animate or change to an X icon when open.

- **[BUG-IDX-037] `grid-cols-2` collapses to single column at 1024px — collections show stacked vertically**
  - **Location:** `css/responsive.css` lines 64–67: `.grid-cols-2 { grid-template-columns: 1fr; gap: var(--space-lg); }`
  - **Expected:** Collections section should still show 2 columns at tablet landscape (1024px) — this is standard for product-focused layouts.
  - **Actual:** Both commitment and collections two-column grids collapse to single column at 1024px, which may be intentional for commitment but causes the collections section to show images stacked vertically with excessive height.

- **[BUG-IDX-038] `product-grid` shows 2-column at 1024px — 4 cards may have different visual weight distribution**
  - **Location:** `css/responsive.css` line 25: `grid-template-columns: repeat(2, 1fr)` at 1024px
  - **Expected:** 2-column product grid is appropriate for tablet.
  - **Actual:** Correct breakpoint handling. However, combined with the container gutter reduction to 48px, card widths may be sufficient. This is acceptable — flagged for visual verification.

- **[BUG-IDX-039] `header-bottom` (nav) is hidden at 1024px but hamburger is shown — desktop nav links partially cut off between 1024px and 1280px**
  - **Location:** `css/responsive.css` line 35: `.header-bottom { display: none; }` at max 1024px
  - **Actual:** The breakpoint hides the full nav at exactly 1024px. Viewports between 1025px and ~1280px would show the desktop nav but the nav items may be crowded with `gap: 64px` and 5 items. No intermediate breakpoint exists in this range.

### 375px (Mobile)

- **[BUG-IDX-040] Announcement bar fixed `height: 38px` clips two-line text at 375px**
  - **Location:** `css/components.css` line 129: `height: var(--announcement-height)` (38px)
  - **Expected per mobile-header.png:** Two-line announcement bar text visible.
  - **Actual:** Fixed `height: 38px` will clip the second line of text. The mobile reference shows the full announcement wrapping to two lines. The fix is to use `min-height` instead of `height`.

- **[BUG-IDX-041] Hero headline font size reduces to 32px at 375px but subtext remains 18px (`text-body-large`) — imbalanced ratio**
  - **Location:** `css/responsive.css` line 169: hero `.text-hero` becomes 32px; `css/components.css` line 441: `.hero-subtext { font-size: var(--text-body-large); }` (18px)
  - **Expected:** Subtext should scale down proportionally (max 16px) when headline is 32px.
  - **Actual:** At 375px, `--text-body-large` is not overridden in the 375px media query (only the hero and h1/h2 tokens are overridden). The subtext at 18px is relatively oversized compared to the 32px headline.

- **[BUG-IDX-042] Product grid collapses to 1-column at 480px (not 375px) — creates overly tall product list**
  - **Location:** `css/responsive.css` lines 154–157: `grid-template-columns: repeat(1, 1fr)` at max 480px
  - **Actual:** At 375px, only one product card is visible at a time. With `aspect-ratio: 4/5` on the image wrap, each card at 375px width (~343px content) becomes approximately 430px tall. Four stacked cards = ~1720px scroll depth for bestsellers alone. Consider a 2-column grid down to 375px for better density.

- **[BUG-IDX-043] Mobile menu has no visual link to account/wishlist/cart icons — these remain in the header but mobile menu has no equivalent**
  - **Location:** `<div class="mobile-menu-overlay">` (lines 513–534)
  - **Expected:** Account and wishlist links should be accessible from mobile nav menu.
  - **Actual:** Mobile menu only shows nav page links. The account, wishlist, and cart icon buttons in the desktop header remain visible on mobile (they are in `.header-right` which is not hidden on mobile), but they are not replicated in the mobile overlay.

- **[BUG-IDX-044] `testimonial-content` has `padding: 0 100px` — at 375px this leaves only 175px (343px - 200px) for testimonial text**
  - **Location:** `css/components.css` line 619: `.testimonial-content { padding: 0 100px; }`
  - **Expected:** Testimonial text should have reasonable reading width on mobile.
  - **Actual:** No responsive override exists for `.testimonial-content` padding. At 375px with 16px gutter and 100px side padding on the content div, testimonial text will be extremely narrow, causing excessive line-wrapping or horizontal overflow. The quote marks will also visually intrude into minimal space.

- **[BUG-IDX-045] Footer collapses to 2-column grid at 1024px but no single-column override at 375px**
  - **Location:** `css/components.css` lines 1031–1040 — footer 2-column at max-1024px
  - **Expected:** Footer link columns should stack to single column on mobile (375px).
  - **Actual:** The footer responsive override only targets `max-width: 1024px`, switching to `1fr 1fr` (2-column). No further override at 768px or 375px exists. At 375px with 16px gutter, two columns of footer links (newsletter spanning full width, then 4 link cols in pairs of 2) will be very tight.

