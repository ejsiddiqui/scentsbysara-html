<!-- superseding-layout-contract-2026-03 -->
> **Superseding Layout Contract (March 2026):** This review document is historical. If any layout or breakpoint guidance here conflicts with current standards, follow the authoritative contract in `prd.md`, `docs/project-master.md`, and `docs/pixel-analysis.md`:
> - `references/sections/` is the 1920px baseline.
> - `1920px` is the primary wide-desktop breakpoint.
> - Viewports above `1920px` must use boxed centered layout.
> - The site uses section-row layout structure.
> - Each section has a 1920px baseline while still supporting `width: 100%`.
> - Default container width is `1800px` (`60px` side spacing each side within 1920).
> - `.container-full` is full width with no side margins.
# QA Tasks — contact.html (Contact Page)

## Status: REVIEWED
## Audited: 2026-03-01
## Viewport Tested: 1440px | 1024px | 375px
## Reference: No dedicated contact screenshot — audited against brand standards and structural integrity
## Auditor note: contact.html is a direct copy of your-story.html with no contact-specific content. The page must be rebuilt.

---

## Section Checklist

| # | Section | Status | Notes |
|---|---------|--------|-------|
| 1 | Announcement bar | PASS | Correct mocha bg (#3F3229), sand text, uppercase tracking. Displays "LAUNCHING MARCH 2026 - JOIN THE WAIT LIST FOR EARLY ACCESS". |
| 2 | Header / Nav | PASS | Sticky header renders correctly at 1440px. Logo "SCENTS BY SARA" centred, icons right-aligned, nav links visible. `background-color: #ffffff` deviates from brand (should be sand). See BUG-CNT-010. |
| 3 | Mobile hamburger | PASS | Hamburger hidden at 1440px via `display: none !important`. Visible correctly at tablet/mobile via responsive override. |
| 4 | Mega menu | PASS (structural) | Hover-reveal mega menu structure correct with 4 columns + image. Wrong image asset used (product-2.png vs mega-menu-image.png). See BUG-CNT-013. |
| 5 | Page hero | FAIL | Hero heading reads "YOUR STORY" using `font-sans` class. Should read "Contact Us" or "Get in Touch" using `font-serif` (RL Limo). Background image is sara.png — wrong context. See BUG-CNT-001, BUG-CNT-003, BUG-CNT-004, BUG-CNT-008. |
| 6 | Page `<title>` | FAIL | Reads "Your Story | Scents by Sara". Should be "Contact Us | Scents by Sara". See BUG-CNT-002. |
| 7 | Intro quote block | FAIL | Renders a "Your Story" brand quote about community stories. Not appropriate for a contact page. Should be removed or replaced with contact-relevant copy. |
| 8 | Community stories grid | FAIL | Four community story cards (A Moment of Grace, Reclaiming My Body, The Gift That Said Everything, Strength in Stillness) should not exist on a contact page. This is Your Story content. See BUG-CNT-001. |
| 9 | Belief banner split | FAIL | "EVERY SCENT HAS A STORY WAITING TO BE TOLD." — entirely wrong copy for contact. Also broken on mobile (no flex-wrap). See BUG-CNT-023. |
| 10 | Contact form (Name, Email, Subject, Message) | FAIL | Not present. Only a "Submit Your Story" form exists with Name, Email, and Narrative fields. A true contact form with Subject/Order Number field and "Send Message" CTA is absent. See BUG-CNT-005. |
| 11 | Form field styling (sharp borders, warm tones) | PARTIAL | Form inputs use `border: 1px solid var(--border-heavy)` and `background: transparent` which aligns with brand. Focus state properly removes outline and darkens border. However, the form is for the wrong purpose. |
| 12 | Submit CTA button | PARTIAL | "SHARE WITH US" button uses `.btn-hero` class, `var(--color-mocha)` background, `border-radius: 0` (from reset). Correct styling pattern. Wrong label and purpose. Should be "SEND MESSAGE" on a contact page. |
| 13 | Contact info block (email, hours, social) | FAIL | Not present anywhere on the page. Required brand section for a contact page. |
| 14 | Character counter | FAIL | Static "0 characters" displayed with no JS wired up. Dead UI element. See BUG-CNT-019. |
| 15 | Footer | PASS (structural) | Footer renders with newsletter col, 4 link columns, social icons (SVG inline), divider, BYSARA logo, copyright. Payment icons image present. Footer collapses to 2-col at 1024px. No single-col breakpoint for 375px. See BUG-CNT-027. |
| 16 | Font: RL Limo serif loaded | PASS | Adobe Typekit link `https://use.typekit.net/abn0bto.css` present in `<head>`. |
| 17 | Font: Suisse Int'l loaded | PASS | All Suisse Int'l woff2 files present in `assets/fonts/`. `@font-face` declarations correct in `design-tokens.css`. |
| 18 | Border-radius enforcement | PASS | CSS reset `border-radius: var(--radius-max)` on buttons/inputs, and `--radius-max: 0px` in tokens. All elements should be sharp-cornered. |
| 19 | Color palette compliance | PARTIAL | Warm neutrals used throughout. However, `.site-header`, `.search-overlay`, and `.mega-menu` use `#ffffff` (pure white) which violates the brand rule of no pure white. See BUG-CNT-009, BUG-CNT-010, BUG-CNT-011. |
| 20 | Container max-width / gutter | PASS | `.container` uses `var(--container-max): 1920px` and `var(--gutter): 100px` at desktop. Responsive gutter compression correct (80px at 1440px, 48px at 1024px, 20px at 768px, 16px at 375px). |
| 21 | Responsive: 1024px tablet | PARTIAL | Nav collapses correctly (`.header-bottom: display:none`). Stories grid collapses to 1-col. Form rows stack. Belief banner begins to squeeze. No critical overflow except belief banner. See BUG-CNT-020, BUG-CNT-021, BUG-CNT-022. |
| 22 | Responsive: 375px mobile | FAIL | Belief banner severely overflows (no flex-wrap/stack). Hero h1 stays at 48px (not scaled). Form section has 120px vertical padding (disproportionate). Footer remains 2-col. See BUG-CNT-023, BUG-CNT-024, BUG-CNT-025, BUG-CNT-026, BUG-CNT-027. |
| 23 | Missing utility classes | FAIL | `.font-weight-normal`, `.mb-12`, `.pt-24`, `.pb-24`, `.tracking-widest`, `.align-end` — all used in markup but undefined in any CSS file. See BUG-CNT-014 through BUG-CNT-018. |
| 24 | Assets: images referenced | PARTIAL | `product-1.png` through `product-4.png` exist. `sara.png` exists. `payment-icons.png` exists. `mega-menu-image.png` exists but not used (wrong asset referenced). `product-2.png` used in mega menu instead. |

---

## Priority Action Plan

### P0 — Must fix before any review of this page is meaningful

1. **Rebuild contact.html from scratch** as a dedicated contact page with:
   - Page hero: "Contact Us" / "Get in Touch" heading in `font-serif` (RL Limo)
   - Contact form: Name, Email, Subject (or Order #), Message fields with sharp borders and warm-toned styling
   - Submit CTA: "SEND MESSAGE" using `.btn-hero` or `.btn-solid` in mocha
   - Contact info block: brand email address, social links for support, business hours
   - Remove all "Your Story" content (story cards, belief banner, story submission form, intro quote)
2. **Update `<title>`** to `"Contact Us | Scents by Sara"`
3. **Replace `your-story.css` stylesheet link** with a dedicated `contact.css`

### P1 — Fix before production deployment

4. Fix belief banner mobile layout — add `flex-direction: column` and `align-items: center` at 768px breakpoint
5. Fix hero heading font class — use `font-serif` not `font-sans` for any page-level h1
6. Replace `#ffffff` backgrounds on `.site-header`, `.search-overlay`, `.mega-menu` with `var(--color-sand)`
7. Add missing utility classes to `layout.css`: `.font-weight-normal`, `.mb-12`, `.pt-24`, `.pb-24`, `.tracking-widest`, `.align-end`
8. Fix hero h1 inline `font-size: 48px` — use CSS token `var(--text-h1)` so responsive scaling applies
9. Add mobile breakpoint for footer grid (`.footer-main-grid` → single column at 480px or 375px)

### P2 — Polish / pre-launch

10. Implement or remove character counter JS on textarea
11. Reduce section vertical padding via responsive overrides at 375px (story submit section, intro quote)
12. Replace `assets/images/product-2.png` in mega menu with `assets/images/mega-menu-image.png`
13. Review masonry card DOM order for logical mobile reading sequence

---

## Summary

**27 bugs found**

| Severity | Count |
|----------|-------|
| Critical | 1 |
| Major | 6 (+ 2 responsive) |
| Minor | 18 (+ 5 responsive) |

**Root cause:** `contact.html` is an unmodified copy of `your-story.html`. The page has never been built as a contact page. The entire content layer must be replaced. The structural shell (header, footer, CSS system) is broadly correct and can be reused.

