# Visual QA Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement all 80 visual QA issues from `docs/visual-qa-tasks.md` — creating missing page/collection templates, fixing CSS/Liquid issues, and documenting Shopify-admin-only tasks for the user.

**Architecture:** Work in the `theme/` directory only. Templates = JSON files in `theme/templates/`. Sections = `.liquid` files in `theme/sections/`. CSS = `theme/assets/*.css`. After each task group, commit and deploy via `shopify theme push`.

**Tech Stack:** Shopify Liquid, CSS, JSON template files, `shopify theme push` CLI.

**Admin-only tasks (user must do these — code cannot fix them):**
- Upload logo image in Shopify Admin → Online Store → Theme Settings
- Configure mega menu: add child links to "Shop" nav item in Admin → Navigation
- Fix footer menu links: update menus in Admin → Navigation (Our Story, Your Story, Sustainability, etc.)
- Fix "Gifts" header nav link: change to `/pages/gifts` in Admin → Navigation
- Create missing collections: Bestsellers, Curvy/Shop-by-Curvy in Admin → Products → Collections
- Enable Body Shape + Body Colour filters: Admin → Apps → Search & Discovery → Filters
- Install Judge.me reviews app: Admin → Apps

---

## Task 1: Create Sustainability Page Template

**Files:**
- Create: `theme/templates/page.our-sustainability.json`

> User action after: Create a new page in Shopify Admin, set handle to `our-sustainability`, assign template `page.our-sustainability`.

- [ ] **Step 1: Create the template**

```json
{
  "sections": {
    "hero": {
      "type": "split-view",
      "settings": {
        "color_scheme": "scheme-2",
        "full_width": true,
        "eyebrow": "OUR SUSTAINABILITY",
        "heading": "CRAFTED WITH CONSIDERATION.",
        "body": "<p>At Scents by Sara, sustainability is not a feature — it is a foundation. Every material, process, and decision is made with environmental responsibility and long-term impact in mind.</p>",
        "image_position": "right",
        "content_background": "secondary",
        "cta_text": "SHOP NOW",
        "cta_link": "shopify://collections/all",
        "button_style": "btn-solid"
      }
    },
    "quote": {
      "type": "quote-highlight",
      "settings": {
        "quote": "The story begins before the candle is lit.",
        "attribution": "Sara",
        "color_scheme": "scheme-1",
        "text_alignment": "center"
      }
    },
    "materials": {
      "type": "split-view",
      "settings": {
        "color_scheme": "scheme-1",
        "full_width": false,
        "eyebrow": "OUR MATERIALS",
        "heading": "INTENTIONAL FROM THE INSIDE OUT.",
        "body": "<p>Every candle is hand-poured using a plant-based wax blend, free from paraffin, parabens, and phthalates. Our wicks are cotton-core and lead-free. Fragrances are IFRA-certified and sourced from responsible suppliers.</p>",
        "image_position": "left",
        "content_background": "primary",
        "cta_text": "",
        "button_style": "btn-outline"
      }
    },
    "packaging": {
      "type": "split-view",
      "settings": {
        "color_scheme": "scheme-1",
        "full_width": false,
        "eyebrow": "PACKAGING",
        "heading": "DESIGNED TO BE KEPT, NOT DISCARDED.",
        "body": "<p>Our packaging is printed on FSC-certified kraft card using water-based inks. Every element is recyclable. We use minimal void fill and never use plastic wrapping in our shipments.</p>",
        "image_position": "right",
        "content_background": "secondary",
        "cta_text": "SHOP NOW",
        "cta_link": "shopify://collections/all",
        "button_style": "btn-outline"
      }
    }
  },
  "order": [
    "hero",
    "quote",
    "materials",
    "packaging"
  ]
}
```

Save to `theme/templates/page.our-sustainability.json`.

- [ ] **Step 2: Commit and deploy**

```bash
cd theme
git add templates/page.our-sustainability.json
git commit -m "feat(templates): add Our Sustainability page template"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only templates/page.our-sustainability.json --allow-live
```

- [ ] **Step 3: Update task list**

In `docs/visual-qa-tasks.md`, change `SUS-01` status to `done`.

---

## Task 2: Create SCAR Collection Template

**Files:**
- Create: `theme/templates/collection.scar-collection.json`

> The `scar-collection` collection already exists with handle `scar-collection`. This template will be picked up automatically.

- [ ] **Step 1: Create the template**

```json
{
  "sections": {
    "main": {
      "type": "main-collection",
      "settings": {
        "products_per_page": 16,
        "columns_desktop": 4,
        "enable_filtering": true,
        "enable_sorting": true,
        "color_scheme": "scheme-1"
      }
    },
    "sustainable": {
      "type": "commitment",
      "blocks": {
        "value_1": {
          "type": "value",
          "settings": {
            "title": "Plant-Based Wax",
            "description": "Each candle is hand-poured using a clean, plant-based wax blend — free from paraffin, parabens, and phthalates."
          }
        },
        "value_2": {
          "type": "value",
          "settings": {
            "title": "IFRA-Certified Fragrance",
            "description": "All fragrances meet IFRA standards and are sourced from responsible suppliers who share our commitment to clean ingredients."
          }
        },
        "value_3": {
          "type": "value",
          "settings": {
            "title": "Recyclable Packaging",
            "description": "Our kraft packaging is FSC-certified and printed with water-based inks. Minimal, considered, and completely recyclable."
          }
        },
        "value_4": {
          "type": "value",
          "settings": {
            "title": "Hand-Poured in Small Batches",
            "description": "Small-batch production reduces waste and ensures every piece receives the care and attention it deserves."
          }
        }
      },
      "block_order": [
        "value_1",
        "value_2",
        "value_3",
        "value_4"
      ],
      "settings": {
        "full_width": true,
        "color_scheme": "scheme-1",
        "eyebrow": "OUR SUSTAINABLE PRACTICE",
        "heading": "CRAFTED WITH CONSIDERATION.",
        "description": "Every material used by Scents by Sara is chosen for performance, longevity, and environmental consideration.",
        "image": "shopify://shop_images/our-commitment.png",
        "image_alt": "Sustainable craftsmanship",
        "image_position": "left",
        "button_label": "READ MORE",
        "button_link": "/pages/our-sustainability"
      }
    }
  },
  "order": [
    "main",
    "sustainable"
  ]
}
```

Save to `theme/templates/collection.scar-collection.json`.

- [ ] **Step 2: Commit and deploy**

```bash
cd theme
git add templates/collection.scar-collection.json
git commit -m "feat(templates): add SCAR collection template with sustainable practice section"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only templates/collection.scar-collection.json --allow-live
```

- [ ] **Step 3: Update task list**

Mark `SC-04` as `done`.

---

## Task 3: Create Sculpted Collection Template

**Files:**
- Create: `theme/templates/collection.sculpted-collection.json`

- [ ] **Step 1: Create the template**

```json
{
  "sections": {
    "main": {
      "type": "main-collection",
      "settings": {
        "products_per_page": 16,
        "columns_desktop": 4,
        "enable_filtering": true,
        "enable_sorting": true,
        "color_scheme": "scheme-1"
      }
    },
    "scar_crossell": {
      "type": "split-view",
      "settings": {
        "color_scheme": "scheme-2",
        "full_width": true,
        "eyebrow": "ALSO FROM SCENTS BY SARA",
        "heading": "SCAR COLLECTION",
        "body": "<p>The Scar Collection celebrates the body as a holder of memory, healing, and confidence. Gold leaf is applied by hand to mark scars — not as decoration but as recognition.</p>",
        "image": "shopify://shop_images/scar-collection-half-left.png",
        "image_alt": "SCAR Collection",
        "image_position": "left",
        "content_background": "secondary",
        "cta_text": "DISCOVER SCAR COLLECTION",
        "cta_link": "/collections/scar-collection",
        "button_style": "btn-solid"
      }
    }
  },
  "order": [
    "main",
    "scar_crossell"
  ]
}
```

Save to `theme/templates/collection.sculpted-collection.json`.

- [ ] **Step 2: Commit and deploy**

```bash
cd theme
git add templates/collection.sculpted-collection.json
git commit -m "feat(templates): add Sculpted collection template with SCAR cross-sell section"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only templates/collection.sculpted-collection.json --allow-live
```

- [ ] **Step 3: Update task list**

Mark `SLC-02` as `done`.

---

## Task 4: Fix PDP Gallery Layout — Thumbnails to Left Sidebar

**Files:**
- Modify: `theme/assets/section-product.css` (gallery grid)

The current `.product-gallery` uses `flex-direction: column` which stacks thumbnails below the main image. Figma shows thumbnails as a left vertical column with the main image to the right.

- [ ] **Step 1: Read current gallery CSS**

Read `theme/assets/section-product.css` lines 38–200 to find `.product-gallery`, `.product-gallery__thumbnails`, `.thumbnails`.

- [ ] **Step 2: Change gallery to row layout**

In `theme/assets/section-product.css`, find:
```css
.product-gallery {
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: sticky;
  top: 140px;
}
```

Replace with:
```css
.product-gallery {
  display: grid;
  grid-template-columns: 96px 1fr;
  grid-template-rows: auto;
  gap: 12px;
  position: sticky;
  top: 140px;
}
```

- [ ] **Step 3: Move thumbnails to first column**

Find `.product-gallery__thumbnails` (or `.thumbnails`) and add:
```css
.product-gallery__thumbnails,
.thumbnails {
  grid-column: 1;
  grid-row: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
```

Find `.product-gallery__stage` (or `.main-image-wrap`) and add:
```css
.main-image-wrap,
.product-gallery__stage {
  grid-column: 2;
  grid-row: 1;
}
```

- [ ] **Step 4: Fix thumbnail track for vertical scrolling**

Find `.product-gallery__thumb-viewport`:
```css
.product-gallery__thumb-viewport {
  overflow: hidden;
  width: 96px;
}
.product-gallery__thumb-track {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
```

- [ ] **Step 5: Mobile — revert to column on small screens**

```css
@media (max-width: 749px) {
  .product-gallery {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .product-gallery__thumbnails,
  .thumbnails {
    order: 1;
  }
  .main-image-wrap,
  .product-gallery__stage {
    order: 0;
  }
}
```

- [ ] **Step 6: Commit and deploy**

```bash
cd theme
git add assets/section-product.css
git commit -m "fix(pdp): move gallery thumbnails to left sidebar layout"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only assets/section-product.css --allow-live
```

- [ ] **Step 7: Update task list**

Mark `PDP-02` as `done`.

---

## Task 5: Fix PDP — Add to Bag Button Width + Title Size + Accordion Borders

**Files:**
- Modify: `theme/assets/section-product.css`

- [ ] **Step 1: Fix Add to Bag button width**

Find the CSS rule for `.product-details .btn-solid, .add-to-cart-btn, [data-add-to-cart]` or whatever class the add-to-cart button uses.

Read `theme/sections/main-product.liquid` lines 198–300 to find the button class name.

Then in `theme/assets/section-product.css`, add:
```css
.product-form__submit,
.btn-add-to-cart,
[data-add-to-cart] {
  width: 100%;
}
```

(Adjust selector after reading the actual class.)

- [ ] **Step 2: Fix product title font size**

In `theme/assets/section-product.css`, find `.product-details__title` or `.product-title`:
```css
.product-details__title {
  font-size: var(--text-h1); /* should be 47px */
}
```

If the rule uses a different size, change it to `var(--text-h1)`.

- [ ] **Step 3: Fix accordion item borders**

In `theme/assets/section-product.css`, find the accordion CSS. Add:
```css
.product-details .accordion-item,
.product-details [data-accordion-item] {
  border-top: 1px solid var(--color-taupe);
}
.product-details .accordion-item:last-child,
.product-details [data-accordion-item]:last-child {
  border-bottom: 1px solid var(--color-taupe);
}
```

- [ ] **Step 4: Fix breadcrumb separator spacing**

In `theme/snippets/breadcrumbs.liquid` (or `theme/assets/section-product.css`), find the separator character. Change `.breadcrumbs` gap or find the separator `/` and add spaces:

In `theme/snippets/breadcrumbs.liquid`, find the separator output and change:
```liquid
{%- unless forloop.last -%}
  <span class="breadcrumb-sep" aria-hidden="true"> / </span>
{%- endunless -%}
```
(Add space before and after the slash if they're missing.)

- [ ] **Step 5: Fix commitment section copy error on PDP**

In `theme/templates/product.json`, find the commitment section's `heading` setting:
```
"heading": "INTENTIONAL DESIGN IN SCENT AND DESIGN."
```
Change to:
```
"heading": "INTENTIONAL DESIGN IN SCENT AND FORM."
```

- [ ] **Step 6: Commit and deploy**

```bash
cd theme
git add assets/section-product.css snippets/breadcrumbs.liquid templates/product.json
git commit -m "fix(pdp): button full-width, title size, accordion borders, breadcrumb spacing, copy fix"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only "assets/section-product.css" "snippets/breadcrumbs.liquid" "templates/product.json" --allow-live
```

- [ ] **Step 7: Update task list**

Mark `PDP-03`, `PDP-07`, `PDP-10`, `PDP-14`, `PDP-15` as `done`.

---

## Task 6: Fix PDP — Wishlist Icon (Outline → Filled)

**Files:**
- Modify: `theme/snippets/icon.liquid`
- Modify: `theme/assets/base.css` (or `section-product.css`)

- [ ] **Step 1: Check current wishlist icon**

Read `theme/snippets/icon.liquid` and find the `wishlist` icon case. It likely renders a `<svg>` with `fill="none"` stroke-based heart. Change to a filled heart:

Find in `icon.liquid`:
```liquid
{%- when 'wishlist' -%}
  <svg ...>
    <path ... fill="none" stroke="currentColor" .../>
  </svg>
```

Change `fill="none"` to `fill="currentColor"` and remove `stroke="currentColor"` (or set stroke to match fill).

- [ ] **Step 2: Set wishlist icon color to taupe**

In `theme/assets/section-product.css`, add:
```css
.product-gallery__wishlist,
.product-card__wishlist {
  color: var(--color-taupe);
}
```

- [ ] **Step 3: Commit and deploy**

```bash
cd theme
git add snippets/icon.liquid assets/section-product.css
git commit -m "fix(pdp): use filled taupe heart for wishlist icon"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only snippets/icon.liquid assets/section-product.css --allow-live
```

- [ ] **Step 4: Update task list**

Mark `PDP-16` as `done`.

---

## Task 7: Fix Homepage — Hero Slide Indicators Visibility

**Files:**
- Modify: `theme/sections/hero-slideshow.liquid` (schema) or `theme/assets/base.css`

- [ ] **Step 1: Check current indicator CSS**

Read `theme/sections/hero-slideshow.liquid` and search for `.slideshow-dots`, `.slideshow-indicator`, `[role="tab"]` or similar. Find if indicators are hidden by `display: none` or `opacity: 0`.

- [ ] **Step 2: Fix indicator visibility**

If indicators are hidden when `show_arrows: false`, they need to always show. Add CSS or update the conditional:

In `hero-slideshow.liquid` or the slideshow CSS:
```css
.slideshow__indicators,
.hero-slideshow__dots {
  display: flex !important;
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  gap: 8px;
  z-index: 2;
}
```

- [ ] **Step 3: Update index.json to show slide controls**

In `theme/templates/index.json`, find the `hero` section settings and consider enabling navigation or keeping arrows off but dots on. If there's a `show_dots` or `show_indicators` setting, enable it.

- [ ] **Step 4: Commit and deploy**

```bash
cd theme
git add sections/hero-slideshow.liquid templates/index.json
git commit -m "fix(homepage): ensure hero slide indicators are visible"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only sections/hero-slideshow.liquid templates/index.json --allow-live
```

- [ ] **Step 5: Update task list**

Mark `HP-04` as `done`.

---

## Task 8: Fix Homepage — Product Cards Show Variant Selectors

**Files:**
- Modify: `theme/templates/index.json`
- Modify: `theme/snippets/product-card.liquid` (if needed)

- [ ] **Step 1: Check why variant selectors show on homepage**

The `featured-collection` section in `index.json` has `card_layout: "shop"`. In `product-card.liquid`, the `shop` layout renders body-shape option selects (lines 169–188).

- [ ] **Step 2: Change card_layout to hide selectors**

Option A — change `card_layout` to `stacked` or `compact` for the homepage featured section (cleaner cards, no select dropdowns).

Option B — add a `show_options` parameter to `product-card.liquid` and set it to `false` for the featured collection.

Simpler: in `index.json`, change the bestsellers section:
```json
"card_layout": "compact"
```

Or keep `shop` but hide the option selects via CSS for the featured-collection context:
```css
.featured-collection .product-card__options {
  display: none;
}
```

Add the CSS to `theme/assets/base.css` or the featured-collection stylesheet.

- [ ] **Step 3: Commit and deploy**

```bash
cd theme
git add templates/index.json assets/base.css
git commit -m "fix(homepage): hide variant selectors on featured collection product cards"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only templates/index.json assets/base.css --allow-live
```

- [ ] **Step 4: Update task list**

Mark `HP-05` as `done`.

---

## Task 9: Fix Contact Us Page — Hero, Heading, Form

**Files:**
- Modify: `theme/templates/page.contact.json`
- Modify: `theme/sections/contact-form.liquid`

- [ ] **Step 1: Read current contact template**

Read `theme/templates/page.contact.json` — check what sections it has. Currently it likely has a page-hero section + contact-form section.

- [ ] **Step 2: Fix section headings**

In `page.contact.json`, find the contact-form section settings and change:
- `heading` or `eyebrow` from "LET US SUPPORT YOUR RITUAL" to "GET IN TOUCH"
- Remove or hide WhatsApp / Studio hours if they don't appear in Figma

Read `theme/sections/contact-form.liquid` to find the settings that control heading and extra content fields.

- [ ] **Step 3: Update form fields**

In `contact-form.liquid`, check if First Name / Last Name are separate fields or combined. Figma shows two separate side-by-side fields. If the section uses a single "Full Name" field, update the liquid to output two fields:
```liquid
<div class="contact-form__name-row">
  <input type="text" name="contact[first_name]" placeholder="FIRST NAME" required>
  <input type="text" name="contact[last_name]" placeholder="LAST NAME" required>
</div>
```

- [ ] **Step 4: Fix Topic field type**

If `contact-form.liquid` uses `<select>` for Topic, change to `<input type="text">`:
```liquid
<input type="text" name="contact[topic]" placeholder="TOPIC" class="contact-form__input">
```

- [ ] **Step 5: Remove character counter from Message field**

If the message textarea has a `maxlength` counter JS, remove it or hide via CSS:
```css
.contact-form__message-count {
  display: none;
}
```

- [ ] **Step 6: Commit and deploy**

```bash
cd theme
git add templates/page.contact.json sections/contact-form.liquid
git commit -m "fix(contact): heading, form field layout, remove topic dropdown"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only templates/page.contact.json sections/contact-form.liquid --allow-live
```

- [ ] **Step 7: Update task list**

Mark `CU-03`, `CU-05`, `CU-06`, `CU-07` as `done`.

---

## Task 10: Fix Your Story — Page Redirect + Hero Section

**Files:**
- Modify: `theme/templates/page.your-story.json`
- Modify: `theme/sections/story-form.liquid` (if hero is missing)

- [ ] **Step 1: Diagnose the redirect**

The page redirects to `/collections/all` after loading. Check `page.your-story.json` for any redirect-causing JS or a section that auto-navigates. Also check `story-form.liquid` and `story-grid.liquid` for any JavaScript that redirects.

Run:
```bash
grep -n "location\|redirect\|navigate" theme/sections/story-form.liquid theme/sections/story-grid.liquid
```

- [ ] **Step 2: Add hero section to Your Story template**

The Figma shows a two-column hero. Update `theme/templates/page.your-story.json` to add a `split-view` section as the first section:

```json
{
  "sections": {
    "hero": {
      "type": "split-view",
      "settings": {
        "color_scheme": "scheme-1",
        "full_width": false,
        "eyebrow": "YOUR STORY",
        "heading": "THE PLEASURE OF A LIFETIME.",
        "body": "<p>Scents by Sara was built on the stories of real women. Every candle holds a memory. We invite you to share yours.</p>",
        "image_position": "left",
        "content_background": "primary",
        "cta_text": "",
        "button_style": "btn-outline"
      }
    },
    "grid": {
      "type": "story-grid",
      "settings": {
        "color_scheme": "scheme-1",
        "heading": "YOUR STORIES",
        "eyebrow": "AS TOLD BY OUR COMMUNITY",
        "description": "Every candle tells a story. These are yours."
      }
    },
    "form": {
      "type": "story-form",
      "settings": {
        "color_scheme": "scheme-1",
        "eyebrow": "SHARE WITH US",
        "heading": "SUBMIT YOUR STORY",
        "description": "Tell us about your moment. We may feature your story.",
        "disclaimer": "By submitting, you agree that Scents by Sara may publish your story."
      }
    }
  },
  "order": ["hero", "grid", "form"]
}
```

- [ ] **Step 3: Commit and deploy**

```bash
cd theme
git add templates/page.your-story.json
git commit -m "fix(your-story): add hero section, reorder sections to match Figma"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only templates/page.your-story.json --allow-live
```

- [ ] **Step 4: Update task list**

Mark `YS-03` as `done`. Investigate `YS-02` redirect separately if it persists.

---

## Task 11: Fix Collection Sort Default + Toolbar Margin

**Files:**
- Modify: `theme/templates/collection.json`
- Modify: `theme/assets/section-collection.css`

- [ ] **Step 1: Fix default sort in collection template**

In `theme/templates/collection.json`, the `main-collection` section settings do not control `default_sort_by` (that's a Shopify collection-level setting). However, the sort dropdown order can be influenced. For the `collection.json` template, no code change needed — the user must set **Default sort order** to "Featured" for each collection in Shopify Admin → Products → Collections → [Collection] → Sort.

Document this as an admin task for SA-02.

- [ ] **Step 2: Fix toolbar bottom margin**

In `theme/assets/section-collection.css`, find:
```css
.collection-toolbar {
  ...
  margin-bottom: var(--gutter);
  ...
}
```

Change to:
```css
.collection-toolbar {
  ...
  margin-bottom: 40px;
  ...
}
```

- [ ] **Step 3: Commit and deploy**

```bash
cd theme
git add assets/section-collection.css
git commit -m "fix(collection): reduce toolbar bottom margin to 40px"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only assets/section-collection.css --allow-live
```

- [ ] **Step 4: Update task list**

Mark `SA-03` as `done`.

---

## Task 12: Fix Product Card — SHOP NOW Button Visibility on Collection Pages

**Files:**
- Modify: `theme/assets/base.css`

- [ ] **Step 1: Verify if SHOP NOW is hidden**

The `product-card.liquid` already has the SHOP NOW button at the bottom (unconditional). Check if CSS is hiding it.

In `theme/assets/base.css`, search for `.product-btn` or `.product-card__button`:
```bash
grep -n "product-btn\|product-card__button" theme/assets/base.css
```

- [ ] **Step 2: Ensure SHOP NOW is visible on collection cards**

If `.product-card__button` has `display: none` or is hidden inside the stacked/shop layouts, override:

```css
.product-card .product-card__button,
.product-card .product-btn {
  display: block;
  width: 100%;
  text-align: center;
  padding: 12px 24px;
  margin-top: 12px;
  border: 1px solid var(--color-foreground);
  font-family: var(--font-sans);
  font-size: var(--text-small);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  text-decoration: none;
  color: var(--color-foreground);
  background: transparent;
}
.product-card .product-card__button:hover,
.product-card .product-btn:hover {
  background: var(--color-foreground);
  color: var(--color-secondary-bg);
}
```

- [ ] **Step 3: Commit and deploy**

```bash
cd theme
git add assets/base.css
git commit -m "fix(product-card): ensure SHOP NOW button visible on all collection cards"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only assets/base.css --allow-live
```

- [ ] **Step 4: Update task list**

Mark `GL-03`, `SC-03`, `SLC-03` as `done`.

---

## Task 13: Mega Menu — Configure Navigation (Admin Task Documentation)

**Files:** None (Shopify Admin configuration)

- [ ] **Step 1: Verify mega-menu.liquid has correct structure**

Read `theme/snippets/mega-menu.liquid` to confirm it renders the 4-column layout when child links exist.

- [ ] **Step 2: Document admin steps for the user**

The user needs to:
1. Go to Shopify Admin → Online Store → Navigation → Main Menu
2. Click "Add menu item" under "Shop" to create child links:
   - Under "POPULAR" group: "Shop All" → `/collections/all`, "Bestsellers" → `/collections/bestsellers`
   - Under "BODY CANDLES" group: "All Body Candles" → `/collections/body-candles`, plus individual products
   - Under "SHOP BY SIZE" group: "Slim" → `/collections/body-candles/Slim`, "Curvy" → `/collections/body-candles/Curvy`
   - Under "SHOP BY COLLECTION" group: "Scar Collection" → `/collections/scar-collection`, "Sculpted" → `/collections/sculpted-collection`
3. In Theme Editor → Header section → set `mega_menu_featured_image` and `mega_menu_featured_link`

Mark `MM-01`, `MM-02`, `MM-03` as pending/admin-task in the task list.

---

## Task 14: Announcement Bar Text Fix

**Files:**
- Modify: `theme/sections/announcement-bar.liquid` schema/settings OR `theme/config/settings_data.json`

- [ ] **Step 1: Read current announcement bar text**

Read `theme/sections/announcement-bar.liquid` to find where the text is stored (either hardcoded or via section settings).

- [ ] **Step 2: Update announcement bar text**

If text is in `settings_data.json` or the section schema defaults, update to match Figma:
- Text: "LAUNCHING APRIL 2026 — JOIN THE WAITING LIST FOR EARLY ACCESS"

(Keep "April" per current live text — this reflects the actual launch date. Flag to user to update once launch date is confirmed.)

If it's in the announcement section settings in the theme JSON, update accordingly.

- [ ] **Step 3: Remove/hide currency selector from announcement bar**

In `theme/sections/header.liquid` or `theme/snippets/localization-form.liquid`, find the currency/market selector that appears near the announcement bar and either hide it with CSS or move it:

```css
.announcement-bar__market,
.header-top__market,
.localization-form--header {
  display: none;
}
```

Or check if it's a header setting `show_currency_selector` that can be disabled.

- [ ] **Step 4: Commit and deploy**

```bash
cd theme
git add sections/announcement-bar.liquid assets/base.css
git commit -m "fix(header): hide currency selector from header bar (HP-09)"
git pull origin main --no-rebase --strategy-option=ours
git push origin main
shopify theme push --theme 147874775176 --only sections/announcement-bar.liquid assets/base.css --allow-live
```

- [ ] **Step 5: Update task list**

Mark `HP-07`, `HP-09` as `done`.

---

## Task 15: Fix Gifts Page Navigation Link

**Files:** Shopify Admin (Navigation) — no code changes

- [ ] **Step 1: Document admin steps for the user**

The "Gifts" nav link points to `/collections`. The user needs to:
1. Go to Shopify Admin → Online Store → Navigation → Main Menu
2. Find the "Gifts" menu item and change its link to `/pages/gifts`

Also check that the `page.gifts.json` template exists (it does) and that a page with handle `gifts` exists in Admin → Pages.

Mark `GF-01` as admin-task/pending until user completes.

---

## Task 16: Final — Update All Remaining Task Statuses

**Files:**
- Modify: `docs/visual-qa-tasks.md`

- [ ] **Step 1: Mark admin-only tasks clearly**

For all tasks that require Shopify Admin action, add a note in the status column:
- `MM-01`, `MM-02`, `MM-03`, `MM-04` → `pending (admin: add nav child links)`
- `GL-01`, `GL-02` → `pending (admin: update navigation menus)`
- `GF-01` → `pending (admin: fix nav link to /pages/gifts)`
- `BS-01` → `pending (admin: create bestsellers collection)`
- `CRV-01` → `pending (admin: create curvy collection)`
- `SCF-01`, `GL-05` → `pending (admin: Search & Discovery filters)`
- `PDP-01` → `pending (admin: install Judge.me)`
- `HP-03` → `pending (admin: upload logo)`
- `OS-02`, `YS-01` → `pending (admin: fix nav links in Navigation menu)`
- `SUS-02` → `pending (admin: fix footer Sustainability link)`
- `SA-02` → `pending (admin: set collection default sort to Featured)`

- [ ] **Step 2: Final commit of task list**

```bash
cd ..
git add docs/visual-qa-tasks.md
git commit -m "docs(qa): mark admin-only tasks and completed code fixes"
git push origin shopify-theme
```
