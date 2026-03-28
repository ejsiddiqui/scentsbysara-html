# Visual QA Task List
> Generated: 2026-03-28 | Source: Screenshot comparison of live store vs `figma-exports/figma-<page>.png`
> Live store: https://scentsbysara-dev.myshopify.com?preview_theme_id=147874775176
> Status values: `pending` | `in-progress` | `done` | `pending (admin)`

---

## Legend
- 🔴 CRITICAL — Blocking; users can't access or use the feature
- 🟠 HIGH — Significant visual/functional deviation from Figma
- 🟡 MEDIUM — Noticeable but non-blocking difference
- 🔵 LOW — Minor polish issue

---

## Homepage (`/`)
> Reference: `figma-exports/figma-homepage.png`

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| HP-01 | 🟠 HIGH | **Hero slide order wrong.** First slide shows "SCAR COLLECTION" macro texture; Figma shows "THE FEMALE FORM, AS IT IS" with two body candle figurines as the opening slide. | pending (admin) |
| HP-02 | 🟠 HIGH | **Featured products section has filter/sort controls.** The "Best Sellers" section on the homepage renders as a mini-collection embed with a FILTER button and SORT BY dropdown. Figma shows a clean product grid with no filter controls. | pending |
| HP-03 | 🟠 HIGH | **Logo renders as text fallback instead of wordmark image.** Live shows "SCENTS BY SARA" as plain text. Logo image is likely not uploaded in theme settings. | pending (admin) |
| HP-04 | 🟠 HIGH | **Hero slide indicators missing.** Figma shows three dot/line pagination indicators centred below the hero text. Live shows no visible slide indicators against the image. | done |
| HP-05 | 🟠 HIGH | **Product card variant selectors visible on homepage cards.** Live shows "BODY SHAPE: SLIM" dropdowns on each product card in the homepage bestsellers grid. Figma shows clean product cards with no variant select UI. | done |
| HP-06 | 🟠 HIGH | **Product names faint on homepage cards.** Figma shows bold, spaced uppercase product names below each card image. Live renders them lighter/smaller in weight, appearing faint. | pending |
| HP-07 | 🟡 MEDIUM | **Announcement bar text mismatch.** Live: "Launching April 2026 — join the waiting list for early access". Figma: "LAUNCHING MARCH 2026 — JOIN THE WAIT LIST FOR EARLY ACCESS". Date and phrasing differ. | pending (admin) |
| HP-08 | 🟡 MEDIUM | **Hero CTA button too close to subheading.** Figma shows clear breathing room between the subheading and "SHOP NOW" button. Live button appears with minimal gap. | pending |
| HP-09 | 🟡 MEDIUM | **Currency selector (USD $) visible in announcement bar.** Figma does not show this element. Needs to be hidden or repositioned. | done |
| HP-10 | 🟡 MEDIUM | **Collections section — tile label treatment differs.** Figma SCAR/SCULPTED tiles show the collection name as an overlaid label at the bottom of the image. Live appears to show it as text below the image. | pending |

---

## Mega Menu
> Reference: `figma-exports/figma-mega-menu.png`

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| MM-01 | 🔴 CRITICAL | **Mega menu not implemented.** Clicking "Shop" navigates directly to `/collections/all`. Figma shows a 4-column dropdown: POPULAR (Shop All, Best Sellers), BODY CANDLES (7 product links), SHOP BY SIZE (Slim, Curvy, Plus Size), SHOP BY COLLECTION (Scar, Sculpted), plus an editorial image panel on the right. | pending (admin) |
| MM-02 | 🟠 HIGH | **"Shop" nav item has no child links configured** in Shopify navigation settings. The `mega-menu.liquid` snippet exists but is never triggered because the menu item has no children. | pending (admin) |
| MM-03 | 🟠 HIGH | **Featured editorial image column not configured.** Figma shows a product close-up image (~320px wide) on the right side of the mega menu. Requires `mega_menu_featured_image` and `mega_menu_featured_link` to be set in theme customiser. | pending (admin) |
| MM-04 | 🟠 HIGH | **"BESTSELLERS" link missing from POPULAR column.** Figma shows "Best Sellers" as a sub-link under POPULAR. No bestsellers collection exists yet (see BS-01). | pending (admin) |
| MM-05 | 🟡 MEDIUM | **Column heading style unverified.** Figma shows POPULAR, BODY CANDLES, SHOP BY SIZE, SHOP BY COLLECTION as small-caps eyebrow labels with a bottom border. Cannot be verified until MM-01 is resolved. | pending (admin) |
| MM-06 | 🟡 MEDIUM | **No hover/active underline on "Shop" nav item** when menu is open. Figma shows active state styling. | pending |

---

## Product Detail Page (PDP)
> Reference: `figma-exports/figma-PDP.png`

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| PDP-01 | 🔴 CRITICAL | **Reviews section empty.** Live shows Judge.me placeholder "Reviews will appear here once the app is installed." Figma shows a full reviews block with star ratings, reviewer names, and review text. Judge.me app not installed/connected. | pending (admin) |
| PDP-02 | 🟠 HIGH | **Gallery layout wrong.** Live shows thumbnails horizontally below the main image. Figma shows thumbnails stacked vertically on the left side of the main image (sidebar layout). | done |
| PDP-03 | 🟠 HIGH | **Add to Bag button not full width.** Live: ~452px. Figma shows CTA stretching to the full width of the right column (`width: 100%`). | pending |
| PDP-04 | 🟠 HIGH | **Button label includes price.** Live: "ADD TO BAG — $27.11". Figma: "ADD TO CART" (no price). Confirm if intentional. | pending |
| PDP-05 | 🟠 HIGH | **"SHOP NOW" button missing from product recommendation cards.** "You May Also Like" cards show title + price only. Figma shows a "SHOP NOW" button per card. | done |
| PDP-06 | 🟠 HIGH | **Scents section has no background imagery.** Figma shows two image-backed scent cards (warm amber for VANILLA, cool green for LAVENDER). Live renders text-only styled cards — scent images not uploaded/connected in Shopify admin. | pending (admin) |
| PDP-07 | 🟡 MEDIUM | **Product title font size undersized.** Live renders `h1` at ~32px. Figma and the `--text-h1` token suggest ~47px. The token may not be resolving correctly. | done |
| PDP-08 | 🟡 MEDIUM | **Gallery column ratio not applying.** CSS sets `1.12fr / 0.88fr` split. Computed styles return equal `564px / 564px` columns — the asymmetric ratio is not taking effect at the measured viewport. | pending |
| PDP-09 | 🟡 MEDIUM | **Color swatch label format mismatch.** Live: `COLOR : IVORY` (colon + selected value inline). Figma: label "COLOR" on its own line, selected value not duplicated inline. | pending |
| PDP-10 | 🟡 MEDIUM | **Accordion items have no visible divider borders.** Live: `border-top: 0px`. Figma shows clear horizontal lines between accordion rows. | done |
| PDP-11 | 🟡 MEDIUM | **Quantity selector and CTA layout.** Live stacks quantity selector and button vertically. Figma shows them closer together or side-by-side. | pending |
| PDP-12 | 🟡 MEDIUM | **Recommendation card subtitle missing.** Cards in "You May Also Like" show title + price. Figma also shows a subtitle line (e.g., "Stretch Mark Body Candle"). | pending |
| PDP-13 | 🟡 MEDIUM | **Scents section heading placement.** Live shows "SCENTS" as a standalone heading above the 2-column grid. Figma shows the scent name ("VANILLA") as a large overlay inside the right-side card. | pending |
| PDP-14 | 🔵 LOW | **Commitment section copy error.** Live: "INTENTIONAL DESIGN IN SCENT AND DESIGN." (repeated word). Figma: "INTENTIONAL DESIGN IN SCENT AND FORM." | done |
| PDP-15 | 🔵 LOW | **Breadcrumb separator lacks spaces.** Live: `SHOP/ BODY CANDLES/ SHE IS YOU`. Figma: `SHOP / BODY CANDLES / SHE IS YOU`. | done |
| PDP-16 | 🔵 LOW | **Wishlist icon is outline style instead of filled.** Figma shows a filled heart in `--color-taupe` (#A39382). Live renders an outline heart via `icon.liquid`. | done |
| PDP-17 | 🔵 LOW | **Gallery main image may be cropped.** Live: ~564×620px. Figma shows a taller, more portrait crop with the full candle body visible. | pending |

---

## SCAR Collection (`/collections/scar-collection`)
> Reference: `figma-exports/figma-scar-collection.png`
> Note: Live handle is `/collections/scar-collection` (not `/collections/scar`)

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| SC-01 | 🟠 HIGH | **Collection handle mismatch.** Live URL is `/collections/scar-collection`. Any deeplinks, nav items, or footer links using `/collections/scar` will 404. All references need to point to the correct handle. | pending (admin) |
| SC-02 | 🟠 HIGH | **Hero description text not shown.** Figma shows a multi-line description paragraph beneath "SCAR COLLECTION" overlaid on the hero image. Live shows only the title — no description. Collection description is not set in Shopify admin. | pending (admin) |
| SC-03 | 🟠 HIGH | **"SHOP NOW" CTA button missing on product cards.** Figma shows a "SHOP NOW" button at the bottom of each collection card. Live collection cards have no CTA button (`show_quick_add: false` and no card CTA rendered). | done |
| SC-04 | 🟠 HIGH | **"OUR SUSTAINABLE PRACTICE" editorial section missing.** Figma shows a full-width editorial section below the product grid (matchsticks/craft image, heading, body text, CTA). Live page goes directly from products to newsletter/footer. | done |
| SC-05 | 🟡 MEDIUM | **Default sort shows "BEST SELLING" instead of "FEATURED".** Figma shows "SORT BY: FEATURED". Collection `default_sort_by` is not set to `manual`. | pending (admin) |
| SC-06 | 🟡 MEDIUM | **Collection hero height feels shorter than Figma.** Figma hero occupies ~50vh in a prominent crop. Live uses `clamp(280px, 35vw, 480px)` which may feel less dominant at desktop widths. | pending |

---

## SCAR Collection — Filter Panel
> Reference: `figma-exports/figma-scar-collection-filter.png`

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| SCF-01 | 🔴 CRITICAL | **Filter groups show wrong facets.** Figma shows BODY SHAPE (Slim, Curvy, Plus Size) and BODY COLOUR (Ivory, Caramel, Mocha) checkboxes. Live shows AVAILABILITY (In stock/Out of stock) and PRICE (Min/Max). Product variant metafields are not enabled as storefront filters in the Shopify "Search & Discovery" app. | pending (admin) |
| SCF-02 | 🟡 MEDIUM | **Filter panel width may be narrower than Figma.** Live uses `width: min(24rem, 100%)` (~384px max). Figma panel appears wider and more prominent (~30–35% of viewport). | pending |
| SCF-03 | 🟡 MEDIUM | **Background scrim darker than Figma.** CSS uses `rgba(63, 50, 41, 0.18)` which appears darker in the live render than the subtle overlay shown in Figma. | pending |

---

## Sculpted Collection (`/collections/sculpted-collection`)
> Reference: `figma-exports/figma-sculpted-collection.png`
> Note: Live handle is `/collections/sculpted-collection` (not `/collections/sculpted`)

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| SLC-01 | 🟠 HIGH | **Collection handle mismatch.** Live URL is `/collections/sculpted-collection`. Links using `/collections/sculpted` will 404. All references need updating. | pending (admin) |
| SLC-02 | 🟠 HIGH | **"SCAR COLLECTION" cross-sell section missing.** Figma shows a full editorial section below the product grid: dark brown image left, "SCAR COLLECTION" heading + description + "DISCOVER SCAR COLLECTION" CTA button right. Not present on the live page. | done |
| SLC-03 | 🟠 HIGH | **"SHOP NOW" CTA button missing on product cards.** Same issue as SC-03 — Figma shows a button per card; live renders none. | done |
| SLC-04 | 🟠 HIGH | **Hero description text missing.** Figma shows a description paragraph below "SCULPTED COLLECTION" in the hero. Live shows only the title. Collection description not set in Shopify admin. | pending (admin) |
| SLC-05 | 🟠 HIGH | **Navigation missing "BESTSELLERS" item.** Figma header shows: SHOP ALL | BESTSELLERS | GIFTS | OUR STORY | YOUR STORY | CONTACT US. Live nav shows: SHOP | GIFTS | OUR STORY | YOUR STORY | CONTACT US. "BESTSELLERS" is absent. | pending (admin) |
| SLC-06 | 🟡 MEDIUM | **Product count may be one short.** Figma suggests ~3 products in grid; live shows 2. Either one product is unpublished or the Figma anticipates a future addition. | pending (admin) |

---

## Shop All (`/collections/all`)
> Reference: `figma-exports/figma-shop-all.png`

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| SA-01 | 🔴 CRITICAL | **JavaScript auto-redirect on `/collections/all`.** Page loads then redirects away (~300ms) to homepage or another page. Users cannot browse Shop All. Root cause: JS navigation script in the theme needs diagnosis. | pending |
| SA-02 | 🟠 HIGH | **Default sort is "Alphabetically, A–Z" instead of "Featured".** Figma shows "SORT BY: FEATURED". Collection `default_sort_by` needs to be set to `manual`. | pending (admin) |
| SA-03 | 🟡 MEDIUM | **Toolbar bottom margin too large.** Live shows ~80px gap between toolbar and first product row. Figma shows ~40–48px gap. | done |
| SA-04 | 🟡 MEDIUM | **Product card body-shape dropdown visible.** Live shows "BODY SHAPE: SLIM" on each collection card. Figma shows only colour swatches (no shape dropdown visible on the card). | pending |

---

## Bestsellers
> Reference: `figma-exports/figma-bestsellers.png`

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| BS-01 | 🔴 CRITICAL | **Collection does not exist.** `/collections/bestsellers` returns 404. Figma shows a full "BESTSELLERS" page with hero, 4-column product grid (6 products), and filter/sort toolbar. Collection needs to be created in Shopify admin and populated. | pending (admin) |

---

## Shop by Curvy
> Reference: `figma-exports/figma-shop-by-curvy.png`

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| CRV-01 | 🔴 CRITICAL | **No dedicated curvy collection.** `/collections/shop-by-curvy`, `/collections/curvy`, `/collections/curvy-body-candles` all return 404. Figma shows a "CURVY BODY CANDLES" page. Note: `/collections/body-candles/Curvy` exists as a tag-filtered view but may not match the Figma page design. | pending (admin) |
| CRV-02 | 🟠 HIGH | **"Curvy Body Candles" footer link broken.** Footer link points to `/collections` (generic) instead of the curvy sub-collection. | pending (admin) |

---

## Gifts Page (`/pages/gifts`)
> Reference: `figma-exports/figma-gifts-page.png`

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| GF-01 | 🔴 CRITICAL | **"Gifts" header nav link points to `/collections` instead of `/pages/gifts`.** Users clicking Gifts in the nav never reach the gifts landing page. | pending (admin) |
| GF-02 | 🟠 HIGH | **Hero section missing.** Figma shows a full-width dark mocha hero banner with "PERSONALISED GIFTS" headline and lifestyle fragrance photo. Live page starts with plain text on a cream background with no hero image. | pending |
| GF-03 | 🟠 HIGH | **Hero right-panel image missing.** Figma shows a second large lifestyle photo in the right half of the hero. Live shows only the notebook/journal image on the left side. | pending |
| GF-04 | 🟡 MEDIUM | **"She Is Also" editorial section layout mismatch.** Figma shows a proper two-column split (image right, text + CTA left). Live layout proportions differ. | pending |
| GF-05 | 🟡 MEDIUM | **SCAR/SCULPTED editorial sections less prominent.** Heading treatment and text hierarchy appear smaller and less visually impactful than Figma. | pending |
| GF-06 | 🟡 MEDIUM | **"YOU MAY ALSO LIKE" product row more compressed** than Figma's spaced-out 4-card row. | pending |
| GF-07 | 🔵 LOW | **Footer sub-links under Gifts (Customisation, Corporate Gifting) point to `/#`.** | pending (admin) |

---

## Our Story (`/pages/our-story`)
> Reference: `figma-exports/figma-our-story-page.png`

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| OS-01 | 🔴 CRITICAL | **Page does not exist.** `/pages/our-story` returns 404. Template exists (`page.our-story.json`) — create the page in Shopify Admin → Pages, set handle to `our-story`, assign template `page.our-story`. | pending (admin) |
| OS-02 | 🔴 CRITICAL | **Header and footer "Our Story" nav links broken.** Both point to `/#`. Update in Admin → Online Store → Navigation. | pending (admin) |

---

## Our Sustainability (`/pages/our-sustainability`)
> Reference: `figma-exports/figma-our-sustainability-page.png`

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| SUS-01 | 🔴 CRITICAL | **Page does not exist.** Template created (`page.our-sustainability.json`) — create the page in Shopify Admin → Pages, set handle to `our-sustainability`, assign template `page.our-sustainability`. | pending (admin) |
| SUS-02 | 🔴 CRITICAL | **Footer "Sustainability" link broken.** Points to `/#`. Update in Admin → Online Store → Navigation. | pending (admin) |

---

## Your Story (`/pages/your-story`)
> Reference: `figma-exports/figma-your-story-page.png`

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| YS-01 | 🔴 CRITICAL | **Header "Your Story" nav link broken.** Points to `/#`. Update in Admin → Online Store → Navigation. | pending (admin) |
| YS-02 | 🟠 HIGH | **Page redirects away.** `/pages/your-story` briefly loads then redirects to `/collections/all`. No redirect code found in sections — verify page handle and template assignment in Admin → Pages. | pending (admin) |
| YS-03 | 🟠 HIGH | **Hero section missing.** Figma shows a two-column hero: lifestyle candle image (left), intro text + headline "The Pleasure of a Lifetime…" (right). Added split-view hero to `page.your-story.json`. | done |
| YS-04 | 🟠 HIGH | **UGC stories grid wrong layout.** Figma shows 3-column × 2 rows = 6+ story cards. Live shows 2-column with only 4 cards. | pending |
| YS-05 | 🟡 MEDIUM | **Story submission form layout unstyled.** Figma shows a designed two-column layout (decorative text/image left, form fields right). Live shows the form without the surrounding layout. | pending |
| YS-06 | 🟡 MEDIUM | **Bottom editorial CTA section missing.** Figma shows a closing full-width image with text overlay. Not present on live. | pending |
| YS-07 | 🔵 LOW | **No filter/category tabs above stories grid.** Figma shows navigation tabs; live shows none. | pending |

---

## Contact Us (`/pages/contact`)
> Reference: `figma-exports/figma-contact-us-page.png`

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| CU-01 | 🟠 HIGH | **Hero image missing.** Figma shows a large full-width hero (woman at a mood board) directly below the nav. Live opens with a sage/olive green banner containing only "CONTACT US" text. | pending |
| CU-02 | 🟠 HIGH | **Sage green title banner not in Figma.** This coloured banner design element does not exist in the Figma. | pending |
| CU-03 | 🟠 HIGH | **Left column heading mismatch.** Live: "LET US SUPPORT YOUR RITUAL". Figma: "GET IN TOUCH". | done |
| CU-04 | 🟠 HIGH | **Left column has extra content not in Figma.** Live shows WhatsApp contact and Studio hours. Figma shows only heading, description, email address, and social icons. | pending |
| CU-05 | 🟡 MEDIUM | **Form fields differ.** Live: single "Full Name" field. Figma: "First Name" + "Last Name" as two separate side-by-side fields. | done |
| CU-06 | 🟡 MEDIUM | **Topic field is a `<select>` dropdown.** Figma shows a plain text input for Topic. | done |
| CU-07 | 🔵 LOW | **Character counter on Message field** ("0 / 500"). Not visible in Figma. | pending |
| CU-08 | 🔵 LOW | **URL slug: live is `/pages/contact`, Figma references `/pages/contact-us`.** May need a redirect. | pending |

---

## Global / Cross-page Issues

| ID | Priority | Issue | Status |
|----|----------|-------|--------|
| GL-01 | 🔴 CRITICAL | **Multiple footer links point to `/#`.** Affected: Our Story, Your Story, Sustainability, Candle Care, Customisation, Corporate Gifting, Shipping & Returns, FAQs, Terms & Conditions. All are dead links with no target page. Update in Admin → Online Store → Navigation. | pending (admin) |
| GL-02 | 🟠 HIGH | **"BESTSELLERS" missing as a primary nav item.** Figma for Sculpted Collection and Mega Menu shows BESTSELLERS as a top-level nav link. Live nav only has SHOP, GIFTS, OUR STORY, YOUR STORY, CONTACT US. | pending (admin) |
| GL-03 | 🟠 HIGH | **Product card "SHOP NOW" button absent on all collection pages.** Figma consistently shows a "SHOP NOW" button on each product card across all collection pages. Live collection cards have no CTA button. Needs to be enabled in `product-card.liquid` for collection contexts. | done |
| GL-04 | 🟠 HIGH | **Collection hero descriptions not populated.** Figma shows description text below the collection title in the hero on SCAR and Sculpted pages. No collection descriptions are set in Shopify admin. | pending (admin) |
| GL-05 | 🟠 HIGH | **Body Shape and Body Colour filters not enabled.** Figma filter panel shows BODY SHAPE and BODY COLOUR facets. Live shows generic AVAILABILITY and PRICE. Requires enabling product metafield-based filters in the Shopify "Search & Discovery" app. | pending (admin) |
| GL-06 | 🟡 MEDIUM | **Announcement bar text references March 2026 in Figma; live shows April 2026.** Content needs to align with actual go-live date. Also: "WAIT LIST" vs "WAITING LIST" phrasing should be standardised. | pending (admin) |
| GL-07 | 🟡 MEDIUM | **"Plus Size Body Candles" footer link points to `/collections` instead of a size-filtered collection.** | pending (admin) |

---

## Summary

| Priority | Count | Done | Pending (Admin) | Remaining |
|----------|-------|------|-----------------|-----------|
| 🔴 CRITICAL | 15 | 1 | 11 | 3 |
| 🟠 HIGH | 32 | 11 | 10 | 11 |
| 🟡 MEDIUM | 24 | 4 | 3 | 17 |
| 🔵 LOW | 9 | 3 | 0 | 6 |
| **Total** | **80** | **19** | **24** | **37** |

### Admin Tasks Checklist
Items requiring action in Shopify Admin (no code changes needed):

- [ ] **HP-01** — Reorder hero slides: set "THE FEMALE FORM" slide as first in Theme Editor
- [ ] **HP-03** — Upload logo image: Admin → Online Store → Theme Settings → Logo
- [ ] **HP-07/GL-06** — Update announcement bar text to match go-live date
- [ ] **MM-01/MM-02** — Add child links to "Shop" nav item in Admin → Navigation → Main Menu
- [ ] **MM-03** — Set `mega_menu_featured_image` + `mega_menu_featured_link` in Theme Editor → Header
- [ ] **MM-04/GL-02/SLC-05** — Add "BESTSELLERS" nav item after creating the collection (BS-01)
- [ ] **PDP-01** — Install Judge.me app: Admin → Apps
- [ ] **PDP-06** — Upload scent card images for VANILLA and LAVENDER in Theme Editor → PDP → Scents section
- [ ] **SC-01/SLC-01** — Fix nav/footer links pointing to old collection handles (`/collections/scar`, `/collections/sculpted`)
- [ ] **SC-02/GL-04** — Add collection descriptions in Admin → Products → Collections → [Collection] → Description
- [ ] **SC-05/SA-02** — Set default sort to "Featured" for each collection: Admin → Products → Collections → [Collection] → Sort
- [ ] **SCF-01/GL-05** — Enable Body Shape + Body Colour filters: Admin → Apps → Search & Discovery → Filters
- [ ] **BS-01** — Create "Bestsellers" collection with handle `bestsellers` and populate with products
- [ ] **CRV-01** — Create "Curvy Body Candles" collection or confirm tag-filtered URL strategy
- [ ] **CRV-02/GL-07** — Fix Curvy and Plus Size footer links in Admin → Navigation
- [ ] **GF-01** — Fix Gifts nav link: change from `/collections` to `/pages/gifts` in Admin → Navigation → Main Menu
- [ ] **OS-01** — Create "Our Story" page in Admin → Pages, set handle `our-story`, assign template `page.our-story`
- [ ] **OS-02** — Fix "Our Story" nav + footer links in Admin → Navigation
- [ ] **SUS-01** — Create "Our Sustainability" page in Admin → Pages, set handle `our-sustainability`, assign template `page.our-sustainability`
- [ ] **SUS-02** — Fix footer "Sustainability" link in Admin → Navigation
- [ ] **YS-01** — Fix "Your Story" nav link in Admin → Navigation
- [ ] **YS-02** — Verify `/pages/your-story` page handle and template assignment in Admin → Pages
- [ ] **SA-02** — Set default sort to "Featured" on the all-products collection
- [ ] **GL-01** — Fix all broken `/#` footer links in Admin → Navigation
