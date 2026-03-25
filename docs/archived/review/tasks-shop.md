<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# QA Tasks — shop.html (Shop Page)

## Status: REVIEWED
## Audit Date: 2026-03-01
## Viewport Tested: 1440px | 1024px | 375px
## Audit Method: Static HTML + CSS code analysis with reference screenshot comparison

---

## Section Checklist

- [FAIL] **Announcement Bar**
  - Text renders correctly: PASS (correct copy, correct styling)
  - Background color `#3F3229` (mocha): PASS
  - Text color `#F9F6F2` (sand): PASS
  - Height 38px: PASS (token `--announcement-height: 38px` applied)
  - Font: Suisse Int'l, 10px, uppercase, letter-spacing 0.1em: PASS
  - Fixed/sticky position: PASS (renders above sticky header)
  - FAIL NOTE: Announcement bar sits outside `.site-header`; when the scroll-hide behavior fires (main.js), the announcement bar becomes orphaned above a hidden header, creating a layout gap. See BUG-SHP-014.

- [FAIL] **Header / Navigation**
  - Three-column layout (search | logo | icons): PASS
  - Logo "SCENTS BY SARA" centered (desktop): PASS
  - Logo "BYSARA" shown on mobile: PASS (display toggled at 768px)
  - Header height 94px nav area: PASS (`.site-header` height: 94px)
  - Total header + announcement = 132px: PASS (38 + 94)
  - Sticky header: PASS (`position: sticky; top: 0`)
  - Header background warm neutral: FAIL — uses `#ffffff` pure white (BUG-SHP-004)
  - Nav links visible at 1440px: PASS
  - Nav links hidden at 1024px / hamburger shown: PASS
  - Active page indicator in nav: FAIL — no `.active` class or `aria-current` on "SHOP" link
  - Border-radius on all interactive elements: PARTIAL FAIL — buttons use `border-radius: var(--radius-max)` (0px) but swatch dots use `border-radius: 50%` (BUG-SHP-008)

- [FAIL] **Mega Menu (SHOP dropdown)**
  - Four-column link grid: PASS (POPULAR, BODY CANDLES, SHOP BY SIZE, SHOP BY COLLECTION)
  - Image column renders: PASS (image file exists)
  - Image asset correct: FAIL — uses `product-2.png` instead of `mega-menu-image.png` (BUG-SHP-005)
  - Hover reveal animation: PASS (opacity/visibility/transform transition)
  - Hover bridge gap: PARTIAL FAIL — `margin-bottom: -30px` hack is fragile (BUG-SHP-019)
  - White background on mega menu: FAIL — same pure white `#ffffff` issue as header (BUG-SHP-004 related)
  - All links resolve to `shop.html`: PASS (intentional for prototype)

- [FAIL] **Page Title / Collection Header (Shop Hero)**
  - "SHOP ALL" heading visible: PASS
  - Heading font: RL Limo (font-serif): PASS (`font-family: var(--font-serif)`)
  - Heading size 48px: PASS (defined in `.shop-hero .text-h1`)
  - Heading color `#3F3229` (mocha): PASS
  - Subtext paragraph color `#A39382` (taupe): PASS
  - Left-aligned: PASS
  - Max-width on paragraph: FAIL — `max-width: 800px` commented out (BUG-SHP-015)
  - Typo "meaning detail": FAIL — should be "meaningful detail" (BUG-SHP-017)
  - Hero heading responsive (375px): FAIL — `font-size: 48px` hardcoded, overrides CSS token at 375px (BUG-SHP-M02)

- [FAIL] **Filter / Sort Controls**
  - Filter button visible with icon: PASS
  - Filter button border `1px solid var(--color-clay)`: PASS
  - Sort dropdown visible: PASS
  - Sort label "SORT BY:": PASS
  - Default sort value "PRICE (LOW TO HIGH)": PASS
  - Sort caret icon: PASS
  - Toolbar top/bottom border: PASS
  - Filter overlay background: FAIL — pure white `#ffffff` (BUG-SHP-002)
  - Filter grid class `grid-cols-3` undefined: FAIL (BUG-SHP-011)
  - Filter overlay in DOM: FAIL — JS-injected into body (BUG-SHP-010)
  - Sort dropdown accessibility (ARIA): FAIL — no `role="listbox"`, no keyboard nav (BUG-SHP-013)
  - Filter toolbar responsive at 375px: FAIL — sort-dropdown `min-width: 280px` overflows (BUG-SHP-M03)

- [FAIL] **Product Grid**
  - 4-column grid at 1440px: PASS (`grid-cols-4` = `repeat(4, 1fr)`)
  - 3-column grid at 1024px: PASS (responsive override applied)
  - 1-column grid at 375px/480px: PASS (collapses correctly at 480px breakpoint)
  - Product image aspect ratio 4/5: PASS (`.product-image-wrap`)
  - Image hover scale effect: PASS (transform scale 1.03)
  - Size dropdown per card: PASS
  - Color swatches (3 per card): PASS
  - Active swatch highlight: PASS (border + scale)
  - Swatch border-radius 50% (circular): FAIL — violates 0px brand standard (BUG-SHP-008)
  - Swatch white color `#FFFFFF`: FAIL — violates brand standard (BUG-SHP-007)
  - Product name styling: PASS (Suisse Int'l, 11px, bold, uppercase, mocha)
  - Product description styling: PASS (Suisse Int'l, 10px, taupe)
  - Price styling: PASS (11px, bold, mocha)
  - "SHOP NOW" button full-width: PASS
  - "SHOP NOW" button border color `--color-clay`: FAIL — inconsistent with global `.product-btn` which uses `--color-slate` (BUG-SHP-012)
  - All 6 cards have unique product names: FAIL — all show "SHE IS TIMELESS" (BUG-SHP-006)
  - Product images: PASS — all 4 product images (product-1 through product-4) exist in assets
  - Product images reused (cards 5+6 repeat images 1 and 2): NOTE — acceptable for prototype
  - Pagination / load-more control: FAIL — completely absent (BUG-SHP-001)

- [FAIL] **Footer**
  - 5-column layout (newsletter + 4 link columns): PASS
  - Newsletter heading "JOIN OUR NEWSLETTER": PASS (RL Limo serif)
  - Email input with placeholder "YOUR EMAIL": PASS
  - Subscribe button dark fill: PASS
  - Social icons (Instagram, Facebook, TikTok, Pinterest): PASS (inline SVG icons)
  - "SHOP ALL" column with correct links: PASS
  - "ABOUT US" column: PASS
  - "GIFTING" column: PASS
  - "CUSTOMER SERVICE" column: PASS
  - Footer column title border-bottom underline: PASS
  - Footer divider rule: PASS
  - "BYSARA" large serif logo: PASS
  - Copyright text: PASS (2026)
  - Payment icons image: PASS (file exists)
  - Footer background `#E7E3DC` (stone): PASS (`bg-secondary`)
  - Footer responsive 2-column at 1024px: PASS
  - Footer bottom row stacked at 1024px — no gap/margin between brand and payment blocks: FAIL (BUG-SHP-M04)
  - Reference footer (footer-fix.png) column structure: PASS — HTML matches reference column layout

- [FAIL] **Mobile Navigation Overlay**
  - Mobile menu overlay exists: PASS
  - Close button: PASS
  - Nav links (SHOP ALL, BEST SELLERS, GIFTS, OUR STORY, YOUR STORY, CONTACT US): PASS
  - Mobile nav font (RL Limo serif, 32px): PASS
  - Active page indicator (`aria-current`): FAIL — no active state on "SHOP ALL" link
  - CTA button style `.btn-outline`: FAIL — should be `.btn-solid` for primary CTA (BUG-SHP-M05)
  - Menu slides in from right: PASS (CSS transition `right: -100%` to `right: 0`)

- [PASS] **JavaScript Functionality**
  - Swatch click selects active state: PASS
  - Size dropdown cycles through sizes: PASS
  - Sort toggles ASC/DESC and re-orders DOM: PASS
  - Filter overlay toggle (open/close): PASS
  - Apply/Clear filter logic: PASS
  - "SHOP NOW" add-to-basket feedback animation: PASS
  - Scroll header hide/show: PASS
  - Hamburger menu toggle: PASS
  - Search overlay toggle: PASS

- [FAIL] **Brand Standards Compliance**
  - Colors — no pure black: PASS
  - Colors — no pure white: FAIL (header, search overlay, filter overlay, mega menu use `#ffffff`) — BUG-SHP-002, BUG-SHP-003, BUG-SHP-004
  - Border-radius 0px everywhere: FAIL (swatches use 50%, slider dots use 50%) — BUG-SHP-008, BUG-SHP-009
  - Container max 1920px: PASS
  - Content max 1720px (implicit via gutter system): PASS
  - Gutter 100px at desktop: PASS (token `--gutter: 100px`, reduced at breakpoints)
  - Fonts RL Limo for headings: PASS (Adobe Typekit loaded)
  - Fonts Suisse Int'l for body: PASS (local woff2 files loaded)

- [FAIL] **SEO / Accessibility**
  - `<title>` tag: PARTIAL FAIL — exists but inconsistent brand casing (BUG-SHP-018)
  - `<meta name="description">`: FAIL — missing entirely (BUG-SHP-020)
  - `<link rel="canonical">`: FAIL — missing (BUG-SHP-022)
  - `alt` attributes on product images: PASS (set, though all say "SHE IS TIMELESS" — linked to BUG-SHP-006)
  - `alt` on payment-icons image: PASS ("Payment Methods")
  - ARIA labels on icon buttons: PASS (search, account, wishlist, cart, hamburger all have `aria-label`)
  - `aria-expanded` on hamburger: PASS (toggled by JS)
  - `aria-current="page"` on active nav link: FAIL — not present on any nav item
  - Form labels on newsletter input: FAIL — no `<label>` for email input (only `placeholder`)
  - Sort dropdown ARIA: FAIL (BUG-SHP-013)

---

## Summary

**29 bugs / issues found total**

| Severity | Count | Bug IDs |
|---|---|---|
| Critical | 5 | BUG-SHP-001 through BUG-SHP-005 |
| Major | 10 | BUG-SHP-006 through BUG-SHP-015 |
| Minor | 8 | BUG-SHP-016 through BUG-SHP-023 (excl. BUG-SHP-024 as non-issue) |
| Responsive (1024px Tablet) | 4 | BUG-SHP-T01 through BUG-SHP-T04 |
| Responsive (375px Mobile) | 6 | BUG-SHP-M01 through BUG-SHP-M06 |

---

## Priority Fix Order

1. **[CRITICAL — Immediate]** Fix all pure `#ffffff` backgrounds to warm neutrals (BUG-SHP-002, BUG-SHP-003, BUG-SHP-004)
2. **[CRITICAL — Immediate]** Add pagination or "Load More" control to product grid (BUG-SHP-001)
3. **[CRITICAL — Immediate]** Move filter overlay HTML into markup, remove JS DOM injection (BUG-SHP-010)
4. **[MAJOR — Before Launch]** Fix all border-radius violations — swatches and dots to 0px (BUG-SHP-008, BUG-SHP-009)
5. **[MAJOR — Before Launch]** Differentiate product names across cards (BUG-SHP-006)
6. **[MAJOR — Before Launch]** Uncomment `max-width` on shop hero paragraph (BUG-SHP-015)
7. **[MAJOR — Before Launch]** Fix filter grid class `grid-cols-3` (BUG-SHP-011)
8. **[MAJOR — Before Launch]** Fix filter toolbar overflow at 375px — remove `min-width: 280px` on sort-dropdown at mobile (BUG-SHP-M03)
9. **[MAJOR — Before Launch]** Fix shop hero h1 to use CSS variable `var(--text-h1)` instead of hardcoded `48px` so 375px token override works (BUG-SHP-M02)
10. **[MINOR — Pre-QA Sign-Off]** Fix typo "meaning detail" → "meaningful detail" (BUG-SHP-017)
11. **[MINOR — Pre-QA Sign-Off]** Add meta description and canonical link (BUG-SHP-020, BUG-SHP-022)
12. **[MINOR — Pre-QA Sign-Off]** Fix swatch white color to warm neutral (BUG-SHP-007)
13. **[MINOR — Pre-QA Sign-Off]** Add `aria-current="page"` to active nav and mobile menu links
14. **[MINOR — Pre-QA Sign-Off]** Add newsletter input `<label>` for accessibility
15. **[MINOR — Nice to Have]** Change mobile menu CTA from `.btn-outline` to `.btn-solid` (BUG-SHP-M05)

