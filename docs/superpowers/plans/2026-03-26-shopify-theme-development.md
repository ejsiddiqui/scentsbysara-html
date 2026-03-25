# Scents by Sara - Shopify Theme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a production-ready Shopify Online Store 2.0 theme for Scents by Sara, translating the existing HTML mockup (`/html` directory) into a fully admin-editable Shopify theme.

**Architecture:** Skeleton theme as base, cherry-picking patterns from Horizon (Web Components, Section Rendering API, import maps). Vanilla ES modules, no build step. All CSS generated from Liquid-powered design tokens. JSON templates with sections/blocks for full theme customizer support.

**Tech Stack:** Liquid, vanilla JavaScript (ES modules, Custom Elements), CSS custom properties, Shopify Storefront APIs (Cart, Section Rendering, Storefront Filtering), Shopify CLI for local development.

**Reference:** HTML mockup lives in `/html` directory. All visual decisions come from there. Design tokens in `/html/css/design-tokens.css`.

---

## Pre-requisites

Before starting any phase:
1. Shopify CLI installed (`npm install -g @shopify/cli`)
2. Shopify Partner account with a development store created
3. Node.js 18+ installed
4. HTML mockup moved to `/html` directory
5. Git repository clean with a fresh branch for theme work

---

## File Structure

```
scentsbysara-v3/
  html/                          # Existing HTML mockup (moved here)
  theme/                         # Shopify theme root
    assets/
      base.css                   # Global styles (reset, utilities, components)
      section-hero.css           # Hero slideshow styles
      section-product.css        # Product page styles
      section-collection.css     # Collection/shop page styles
      section-cart.css           # Cart page + drawer styles
      section-split-view.css     # Split-view section styles
      section-testimonials.css   # Testimonials carousel styles
      component.js               # Base Web Component class
      slideshow.js               # <slideshow-component> carousel/slider
      variant-picker.js          # <variant-picker> color/shape/scent selection
      product-card.js            # <product-card> hover image, swatches
      cart-drawer.js             # <cart-drawer> slide-out cart
      cart.js                    # <cart-items> cart page management
      header.js                  # <header-component> sticky, scroll, mega menu
      mobile-menu.js             # <mobile-menu> drawer with nested panels
      accordion.js               # <accordion-component> expandable content
      facets.js                  # <facet-filters> collection filtering/sorting
      quantity-selector.js       # <quantity-selector> +/- input
      dialog.js                  # <dialog-component> base for drawers/modals
      predictive-search.js       # <predictive-search> search overlay
    blocks/                      # (Optional, Horizon-style. Evaluate during Phase 2)
    config/
      settings_schema.json       # Theme settings definition
      settings_data.json         # Default settings values
    layout/
      theme.liquid               # Main layout wrapper
      password.liquid             # Password page layout
    locales/
      en.default.json            # English translations
      en.default.schema.json     # Schema translations for theme editor
    sections/
      header-group.json          # Header section group ordering
      footer-group.json          # Footer section group ordering
      announcement-bar.liquid    # Announcement bar section
      header.liquid              # Header section (logo, nav, icons)
      footer.liquid              # Footer section (newsletter, menus, social)
      hero-slideshow.liquid      # Homepage hero carousel
      featured-collection.liquid # Bestsellers / product carousel
      commitment.liquid          # Our Commitment section (values grid)
      collections-grid.liquid    # Homepage collection cards
      split-view.liquid          # Reusable split-view (image + content)
      testimonials.liquid        # Customer testimonials carousel
      main-product.liquid        # Product detail page
      main-collection.liquid     # Collection page (grid + filters)
      main-cart.liquid           # Cart page
      main-page.liquid           # Generic page content
      story-form.liquid          # Your Story submission form
      story-grid.liquid          # Your Story metaobject display grid
      contact-form.liquid        # Contact page form
      main-search.liquid         # Search results
      main-list-collections.liquid # All collections page
      main-404.liquid            # 404 page
    snippets/
      product-card.liquid        # Reusable product card
      price.liquid               # Price with sale/compare-at logic
      variant-swatches.liquid    # Color swatches for cards
      image.liquid               # Responsive <picture> element
      icon.liquid                # SVG icon renderer
      button.liquid              # Styled button component
      breadcrumbs.liquid         # Breadcrumb navigation
      accordion.liquid           # Accordion item
      slideshow-controls.liquid  # Dots + arrows for carousels
      cart-drawer.liquid         # Cart drawer markup
      search-modal.liquid        # Predictive search overlay
      mega-menu.liquid           # Mega menu dropdown
      color-schemes.liquid       # CSS variables for color schemes
      design-tokens.liquid       # All CSS custom properties from settings
      scripts.liquid             # Import map + script tags
      meta-tags.liquid           # SEO meta tags
      localization-form.liquid   # Currency/market selector
      pagination.liquid          # Collection pagination
    templates/
      index.json                 # Homepage
      product.json               # Product detail page
      collection.json            # Collection page
      cart.json                  # Cart page
      page.json                  # Generic page
      page.our-story.json        # Our Story page
      page.your-story.json       # Your Story (UGC) page
      page.contact.json          # Contact page
      search.json                # Search results
      404.json                   # 404 page
      gift_card.liquid           # Gift card (required by Shopify)
      password.json              # Password page
      blog.json                  # Blog listing (placeholder)
      article.json               # Blog article (placeholder)
      list-collections.json      # All collections page
```

---

## Phase 1: Foundation

**Goal:** Skeleton theme cloned, design tokens ported, layout working, base CSS in place.
**Dependencies:** Pre-requisites complete.
**Can run in parallel:** Tasks 1.1 and 1.2 are independent. Tasks 1.3-1.7 are sequential.

### Task 1.1: Move HTML Mockup to `/html` Directory

**Files:**
- Move: all root-level `.html` files, `css/`, `assets/`, `partials/` into `/html/`

- [ ] **Step 1: Create `/html` directory and move mockup files**

```bash
mkdir -p html
git mv index.html product.html shop.html cart.html checkout.html body-candles.html gifts.html scar-collection.html sculpted-collection.html contact.html our-story.html your-story.html html/
git mv css html/
git mv assets html/
git mv partials html/
```

- [ ] **Step 2: Verify HTML mockup still works from new location**

Open `html/index.html` in browser. Verify all pages load with correct styles and images.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: move HTML mockup to /html directory for reference"
```

### Task 1.2: Clone Skeleton Theme and Set Up Directory

**Files:**
- Create: `theme/` directory with Skeleton theme contents

- [ ] **Step 1: Scaffold theme directory**

Note: Shopify's skeleton-theme repo may be archived. Use `shopify theme init` if available, or manually scaffold:

```bash
# Option A: Try shopify theme init
shopify theme init theme

# Option B: If skeleton-theme is available
git clone https://github.com/Shopify/skeleton-theme.git theme-temp
cp -r theme-temp/* theme/
rm -rf theme-temp

# Option C: Manual scaffold (fallback)
mkdir -p theme/{assets,blocks,config,layout,locales,sections,snippets,templates}
```

- [ ] **Step 2: Verify theme directory structure exists**

```bash
ls theme/layout/ theme/sections/ theme/templates/ theme/config/ theme/assets/ theme/snippets/ theme/locales/
```

Expected: all directories exist (with starter files if using Option A/B, empty if Option C).

- [ ] **Step 3: Connect to Shopify dev store**

```bash
cd theme
shopify theme dev --store=your-dev-store.myshopify.com
```

Expected: Theme preview opens in browser with Skeleton's bare-bones output.

- [ ] **Step 4: Commit**

```bash
git add theme/
git commit -m "chore: add Skeleton theme as base for Shopify development"
```

### Task 1.3: Port Design Tokens to `settings_schema.json`

**Files:**
- Create: `theme/config/settings_schema.json`
- Reference: `html/css/design-tokens.css`

- [ ] **Step 1: Create `settings_schema.json` with all theme settings**

Map every design token to a Shopify theme setting. The schema should include these groups:

1. **theme_info** - Name: "Scents by Sara", author: "Epyc Digital"
2. **Logo & Favicon** - `logo` (image), `logo_inverse` (image for dark bg), `logo_mobile` (symbol), `logo_height` (range: 20-80, default: 40), `favicon` (image)
3. **Colors** - `color_scheme_group` with two schemes:
   - **Sand (default):** bg `#F9F6F2`, text `#3F3229`, muted `#A39382`, border `#CEC5B8`, secondary_bg `#E7E3DC`, accent `#3F3229`
   - **Mocha (dark):** bg `#3F3229`, text `#F9F6F2`, muted `#CEC5B8`, border `#A39382`, secondary_bg `#2D2B27`, accent `#F9F6F2`
   - Status colors: success `#2d6a4f`, error `#8b2e2e`
10. **Social Media** - `social_instagram` (url), `social_facebook` (url), `social_tiktok` (url), `social_pinterest` (url) — global settings reused in footer, mobile menu, etc.
4. **Typography** - `type_heading_font` (font_picker, default: rl-limo serif), `type_body_font` (font_picker, default: Suisse Int'l sans-serif), heading sizes H1-H6 (range inputs matching token values), body size (16px default)
5. **Layout** - `page_width` (select: 1920/1440/1200), `section_spacing` (range: 40-120, default: 80), `container_gutter` (range: 20-80, default: 60)
6. **Buttons** - `button_border_radius` (range: 0-20, default: 0), `button_border_width` (range: 0-3, default: 1)
7. **Cart** - `cart_type` (select: drawer/page, default: drawer), `cart_note_enabled` (checkbox), `cart_auto_open` (checkbox, default: true)
8. **Product Cards** - `card_image_ratio` (select: portrait/square/auto), `card_show_secondary_image` (checkbox, default: true), `card_show_swatches` (checkbox, default: true), `card_show_quick_add` (checkbox, default: true)
9. **Swatches** - `swatch_shape` (select: circle/square, default: circle), `swatch_size` (range: 20-48, default: 32)

- [ ] **Step 2: Create `settings_data.json` with defaults**

```json
{
  "current": {
    "sections": {},
    "content_for_index": [],
    "color_scheme_sand": {
      "background": "#F9F6F2",
      "foreground": "#3F3229"
    }
  }
}
```

- [ ] **Step 3: Verify settings load in theme editor**

```bash
cd theme && shopify theme dev
```

Open theme customizer. Verify all setting groups appear with correct defaults.

- [ ] **Step 4: Commit**

```bash
git add theme/config/
git commit -m "feat: add theme settings schema with design tokens"
```

### Task 1.4: Create Design Token Snippets

**Files:**
- Create: `theme/snippets/design-tokens.liquid`
- Create: `theme/snippets/color-schemes.liquid`
- Reference: `html/css/design-tokens.css`

- [ ] **Step 1: Create `design-tokens.liquid`**

This snippet generates CSS custom properties from theme settings. It should output a `<style>` tag inside `<head>` containing:

```liquid
{% comment %}
  Generates CSS custom properties from theme settings.
  Included in layout/theme.liquid <head>.
  Uses the first (default) color scheme for :root variables.
{% endcomment %}

{% style %}
:root {
  /* Brand Colors - derived from default color scheme */
  {%- assign default_scheme = settings.color_schemes | first -%}
  --color-background: {{ default_scheme[1].settings.background }};
  --color-foreground: {{ default_scheme[1].settings.foreground }};
  --color-muted: {{ default_scheme[1].settings.muted }};
  --color-border: {{ default_scheme[1].settings.border }};
  --color-secondary-bg: {{ default_scheme[1].settings.secondary_bg }};
  /* ... map all color scheme values ... */

  /* Spacing Scale (8pt system) */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 32px;
  --space-xl: 64px;
  --space-xxl: {{ settings.section_spacing }}px;
  --space-section: {{ settings.section_spacing }}px;

  /* Layout */
  --container-max: {{ settings.page_width }}px;
  --container-editorial: 800px;
  --gutter: {{ settings.container_gutter }}px;
  --inner-gutter: 80px;

  /* Typography - from font pickers */
  --font-serif: {{ settings.type_heading_font.family }}, {{ settings.type_heading_font.fallback_families }};
  --font-sans: {{ settings.type_body_font.family }}, {{ settings.type_body_font.fallback_families }};
  --text-hero: {{ settings.heading_size_h1 | plus: 2 }}px;
  --text-h1: {{ settings.heading_size_h1 }}px;
  /* ... all heading sizes ... */
  --text-body: {{ settings.body_font_size }}px;

  /* Buttons */
  --radius-max: {{ settings.button_border_radius }}px;

  /* Z-Index */
  --z-base: 1;
  --z-elevated: 10;
  --z-header: 1000;
  --z-overlay: 2000;

  /* Header - computed */
  --announcement-height: 38px;
  --header-height: 132px;
}
{% endstyle %}
```

- [ ] **Step 2: Create `color-schemes.liquid`**

Generate per-scheme CSS classes:

```liquid
{% for scheme in settings.color_schemes %}
  .color-{{ scheme.id }} {
    --color-background: {{ scheme.settings.background }};
    --color-foreground: {{ scheme.settings.foreground }};
    --color-muted: {{ scheme.settings.muted }};
    --color-border: {{ scheme.settings.border }};
    --color-secondary-bg: {{ scheme.settings.secondary_bg }};
    --color-accent: {{ scheme.settings.accent }};
  }
{% endfor %}
```

- [ ] **Step 3: Commit**

```bash
git add theme/snippets/design-tokens.liquid theme/snippets/color-schemes.liquid
git commit -m "feat: add design token and color scheme Liquid snippets"
```

### Task 1.5: Create Base CSS

**Files:**
- Create: `theme/assets/base.css`
- Reference: `html/css/layout.css`, `html/css/components.css`, `html/css/responsive.css`

- [ ] **Step 1: Port reset, base typography, and utility classes from HTML mockup**

Combine `layout.css`, `components.css` into `base.css`. Replace all hardcoded color/font/spacing values with `var(--token)` references. Remove any mockup-specific JS-dependent styles. Keep:
- CSS reset / normalize
- Base typography (body, headings, links)
- Utility classes (.container, .flex-between, .items-center, .text-center, .grid-cols-2, .grid-cols-4, .font-serif, .text-muted, .eyebrow, .text-hero through .text-micro)
- Button styles (.btn-solid, .btn-outline, .icon-btn)
- Form inputs (.form-input, .form-label, .form-group)
- Responsive container and grid

- [ ] **Step 2: Verify base styles render correctly**

```bash
cd theme && shopify theme dev
```

Open preview. Body text, headings, and colors should match the mockup's look and feel.

- [ ] **Step 3: Commit**

```bash
git add theme/assets/base.css
git commit -m "feat: add base CSS ported from HTML mockup design tokens"
```

### Task 1.6: Create `theme.liquid` Layout

**Files:**
- Modify: `theme/layout/theme.liquid`
- Create: `theme/snippets/scripts.liquid`
- Create: `theme/snippets/meta-tags.liquid`

- [ ] **Step 1: Write `theme.liquid`**

```liquid
<!doctype html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ page_title }}{% unless page_title contains shop.name %} | {{ shop.name }}{% endunless %}</title>

  {% render 'meta-tags' %}

  {%- comment -%} Font declarations and preloads {%- endcomment -%}
  {{ settings.type_heading_font | font_face: font_display: 'swap' }}
  {{ settings.type_body_font | font_face: font_display: 'swap' }}
  <link rel="preload" href="{{ settings.type_heading_font | font_url }}" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{{ settings.type_body_font | font_url }}" as="font" type="font/woff2" crossorigin>

  {%- comment -%} Design tokens & color schemes {%- endcomment -%}
  {% render 'design-tokens' %}
  {% render 'color-schemes' %}

  {%- comment -%} Stylesheets {%- endcomment -%}
  {{ 'base.css' | asset_url | stylesheet_tag }}

  {%- comment -%} Scripts {%- endcomment -%}
  {% render 'scripts' %}

  {{ content_for_header }}
</head>
<body class="template-{{ template.name }}{% if template.suffix %} template-{{ template.name }}-{{ template.suffix }}{% endif %}">
  <a href="#MainContent" class="skip-to-content">{{ 'accessibility.skip_to_content' | t }}</a>

  {% sections 'header-group' %}

  <main id="MainContent" class="page-wrapper">
    {{ content_for_layout }}
  </main>

  {% sections 'footer-group' %}

  {%- comment -%} Cart drawer (rendered globally) {%- endcomment -%}
  {% if settings.cart_type == 'drawer' %}
    {% render 'cart-drawer' %}
  {% endif %}
</body>
</html>
```

- [ ] **Step 2: Create `scripts.liquid` with import map**

```liquid
<script type="importmap">
{
  "imports": {
    "@theme/component": "{{ 'component.js' | asset_url }}",
    "@theme/slideshow": "{{ 'slideshow.js' | asset_url }}",
    "@theme/variant-picker": "{{ 'variant-picker.js' | asset_url }}",
    "@theme/product-card": "{{ 'product-card.js' | asset_url }}",
    "@theme/cart-drawer": "{{ 'cart-drawer.js' | asset_url }}",
    "@theme/cart": "{{ 'cart.js' | asset_url }}",
    "@theme/header": "{{ 'header.js' | asset_url }}",
    "@theme/mobile-menu": "{{ 'mobile-menu.js' | asset_url }}",
    "@theme/accordion": "{{ 'accordion.js' | asset_url }}",
    "@theme/facets": "{{ 'facets.js' | asset_url }}",
    "@theme/quantity-selector": "{{ 'quantity-selector.js' | asset_url }}",
    "@theme/dialog": "{{ 'dialog.js' | asset_url }}",
    "@theme/predictive-search": "{{ 'predictive-search.js' | asset_url }}"
  }
}
</script>
```

- [ ] **Step 3: Create `meta-tags.liquid`**

Standard Shopify SEO meta tags snippet (title, description, og tags, canonical URL).

- [ ] **Step 4: Verify layout renders**

```bash
cd theme && shopify theme dev
```

Page should render with correct `<head>`, empty `<main>`, no console errors.

- [ ] **Step 5: Commit**

```bash
git add theme/layout/theme.liquid theme/snippets/scripts.liquid theme/snippets/meta-tags.liquid
git commit -m "feat: create theme.liquid layout with design tokens and import map"
```

### Task 1.7: Create Base Component JS Class

**Files:**
- Create: `theme/assets/component.js`

- [ ] **Step 1: Write base `Component` class**

Simplified version of Horizon's Component pattern:

```javascript
/**
 * Base class for all custom elements in the theme.
 * Provides:
 * - refs system (child elements with ref="name" auto-collected)
 * - connectedCallback / disconnectedCallback lifecycle
 */
export class Component extends HTMLElement {
  constructor() {
    super();
    this._refs = {};
  }

  connectedCallback() {
    this._collectRefs();
    this.onConnect?.();
  }

  disconnectedCallback() {
    this.onDisconnect?.();
  }

  _collectRefs() {
    this.querySelectorAll('[ref]').forEach(el => {
      const name = el.getAttribute('ref');
      if (name.endsWith('[]')) {
        const key = name.slice(0, -2);
        this._refs[key] = this._refs[key] || [];
        this._refs[key].push(el);
      } else {
        this._refs[name] = el;
      }
    });
  }

  get refs() {
    return this._refs;
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add theme/assets/component.js
git commit -m "feat: add base Component web component class"
```

### Task 1.8: Create Locale Files

**Files:**
- Create: `theme/locales/en.default.json`
- Create: `theme/locales/en.default.schema.json`

- [ ] **Step 1: Create `en.default.json` with all translation keys**

Populate with all strings used via `| t` filter across the theme:

```json
{
  "accessibility": {
    "skip_to_content": "Skip to content",
    "close": "Close",
    "previous_slide": "Previous slide",
    "next_slide": "Next slide"
  },
  "general": {
    "continue_shopping": "Continue Shopping",
    "search": "Search",
    "cart": "Cart",
    "account": "Account"
  },
  "products": {
    "add_to_cart": "Add to Bag",
    "sold_out": "Sold Out",
    "quantity": "Quantity",
    "shop_now": "Shop Now"
  },
  "cart": {
    "title": "Your Bag",
    "empty": "Your bag is empty",
    "subtotal": "Subtotal",
    "shipping": "Shipping",
    "tax": "Tax (VAT)",
    "total": "Total",
    "checkout": "Checkout",
    "view_bag": "View Bag"
  },
  "collections": {
    "filter": "Filter",
    "sort": "Sort by",
    "items_count": "{{ count }} items"
  },
  "contact": {
    "success": "Thank you for your message. We'll get back to you soon."
  },
  "newsletter": {
    "success": "Thank you for subscribing!"
  }
}
```

- [ ] **Step 2: Create `en.default.schema.json` with setting/section labels**

Populate with all schema labels used in section and setting definitions (section names, setting labels, block names, etc.). This ensures the theme editor displays proper labels.

- [ ] **Step 3: Commit**

```bash
git add theme/locales/
git commit -m "feat: add locale files with translation keys"
```

### Phase 1 QA Checkpoint

- [ ] **QA: Verify Phase 1 deliverables**

Run `shopify theme dev` and verify:
1. Theme preview loads without console errors
2. CSS custom properties are present in `:root` (inspect with DevTools)
3. Color scheme classes generate correctly
4. Font families load (check Network tab)
5. Import map is present in page source
6. Theme customizer shows all setting groups with correct defaults
7. HTML mockup in `/html` still works independently
8. Translation strings resolve correctly (not showing raw keys)

Fix any issues found, re-test, then commit fixes.

---

## Phase 2: Global Sections (Header + Footer + Announcement Bar)

**Goal:** Full header (announcement bar, logo, mega menu, mobile menu, sticky behavior) and footer (newsletter, link columns, social, payment icons) working across all pages.
**Dependencies:** Phase 1 complete.
**Can run in parallel:** Tasks 2.1 (Announcement Bar) and 2.5 (Footer) are independent. Tasks 2.2-2.4 (Header, Mega Menu, Mobile Menu) are sequential.

### Task 2.1: Announcement Bar Section

**Files:**
- Create: `theme/sections/announcement-bar.liquid`
- Reference: `html/partials/site-header.html` (lines 1-14)

- [ ] **Step 1: Create announcement bar section with schema**

The section should render:
- Announcement text (editable, supports multiple rotating messages via blocks)
- Currency/market selector (Shopify localization form)

Schema settings:
- `color_scheme` (color_scheme selector)
- `text_style` (select: static / marquee)
- Blocks type `announcement` with: `text` (text field), `link` (url field)

- [ ] **Step 2: Create `localization-form.liquid` snippet**

Renders Shopify's native market/currency selector using `localization.available_countries`:

```liquid
{%- form 'localization', id: 'currency-form' -%}
  <select name="country_code" onchange="this.form.submit()">
    {%- for country in localization.available_countries -%}
      <option value="{{ country.iso_code }}"
        {% if country.iso_code == localization.country.iso_code %}selected{% endif %}>
        {{ country.currency.iso_code }} {{ country.currency.symbol }}
      </option>
    {%- endfor -%}
  </select>
{%- endform -%}
```

- [ ] **Step 3: Verify announcement bar renders with currency selector**

- [ ] **Step 4: Commit**

```bash
git add theme/sections/announcement-bar.liquid theme/snippets/localization-form.liquid
git commit -m "feat: add announcement bar section with currency selector"
```

### Task 2.2: Header Section

**Files:**
- Create: `theme/sections/header.liquid`
- Create: `theme/assets/header.js`
- Create: `theme/snippets/icon.liquid`
- Create: `theme/sections/header-group.json`
- Reference: `html/partials/site-header.html` (lines 16-end)

- [ ] **Step 1: Create `icon.liquid` snippet**

SVG icon renderer supporting all icons used in the mockup: search, cart (handbag), account (user), wishlist (heart), hamburger, close, chevron-left, chevron-right, plus, minus, instagram, facebook, tiktok, pinterest.

```liquid
{%- comment -%}
  Renders an SVG icon by name.
  Usage: {% render 'icon', name: 'search' %}
{%- endcomment -%}
{%- case name -%}
  {%- when 'search' -%}
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">...</svg>
  {%- when 'cart' -%}
    <!-- handbag icon from mockup -->
  {%- when 'account' -%}
    <!-- user icon from mockup -->
  {%- comment -%} ... all other icons ... {%- endcomment -%}
{%- endcase -%}
```

- [ ] **Step 2: Create `header.liquid` section**

Structure matching mockup:
- `.header-top.container` with 3 columns:
  - Left: search icon (desktop), search + cart (mobile)
  - Center: logo (long version desktop, symbol mobile)
  - Right: account, wishlist, cart icons + hamburger (mobile only)
- `.header-bottom` (desktop only): navigation from Shopify menu

Schema settings:
- `logo` (image_picker)
- `logo_mobile` (image_picker)
- `menu` (link_list, default: "main-menu")
- `sticky_header` (select: none/always/scroll-up, default: always)
- `enable_transparent` (checkbox, for homepage hero overlap)

- [ ] **Step 3: Create `header.js` custom element**

`<header-component>` with:
- Sticky header behavior (based on setting: always visible, show on scroll-up)
- CSS variable `--header-height` updated via ResizeObserver
- Search overlay toggle
- Cart drawer trigger (dispatches event)

- [ ] **Step 4: Create `header-group.json`**

```json
{
  "type": "header",
  "name": "Header Group",
  "sections": {
    "announcement-bar": { "type": "announcement-bar" },
    "header": { "type": "header" }
  },
  "order": ["announcement-bar", "header"]
}
```

- [ ] **Step 5: Verify header renders with logo, navigation, icons**

- [ ] **Step 6: Commit**

```bash
git add theme/sections/header.liquid theme/sections/header-group.json theme/assets/header.js theme/snippets/icon.liquid
git commit -m "feat: add header section with sticky behavior and navigation"
```

### Task 2.3: Mega Menu

**Files:**
- Create: `theme/snippets/mega-menu.liquid`
- Modify: `theme/sections/header.liquid` (add mega menu rendering)
- Modify: `theme/assets/header.js` (add mega menu activation)
- Reference: `html/partials/site-header.html` mega menu markup

- [ ] **Step 1: Create `mega-menu.liquid` snippet**

Renders a multi-column dropdown for menu items that have children. Structure:
- Columns auto-calculated from child link groups
- Optional featured image (via header section settings: `mega_menu_featured_image`)
- Columns: link group title + child links

The mega menu reads from Shopify's native menu structure:
- Top-level link "Shop" has child links (Popular, Body Candles, etc.)
- Each child link can have its own children (sub-items)

```liquid
{%- comment -%}
  Renders mega menu for a top-level nav link.
  Usage: {% render 'mega-menu', link: link, featured_image: section.settings.mega_menu_image %}
{%- endcomment -%}
<div class="mega-menu" data-mega-menu>
  <div class="mega-menu-inner container">
    <div class="mega-menu-columns">
      {%- for child_link in link.links -%}
        <div class="mega-menu-col">
          <span class="mega-menu-col-title eyebrow text-micro">{{ child_link.title }}</span>
          {%- if child_link.links.size > 0 -%}
            <ul class="mega-menu-links">
              {%- for grandchild in child_link.links -%}
                <li><a href="{{ grandchild.url }}">{{ grandchild.title }}</a></li>
              {%- endfor -%}
            </ul>
          {%- endif -%}
        </div>
      {%- endfor -%}
    </div>
    {%- if featured_image -%}
      <div class="mega-menu-featured">
        <img src="{{ featured_image | image_url: width: 400 }}" alt="" loading="lazy">
      </div>
    {%- endif -%}
  </div>
</div>
```

- [ ] **Step 2: Add mega menu hover/focus activation to `header.js`**

On desktop: pointer enter on nav link with children shows mega menu. Pointer leave hides. Focus support for keyboard nav.

- [ ] **Step 3: Add header section settings for mega menu**

Add to header schema:
- `mega_menu_featured_image` (image_picker)
- `mega_menu_featured_link` (url)

- [ ] **Step 4: Verify mega menu shows on hover with correct column layout**

- [ ] **Step 5: Commit**

```bash
git add theme/snippets/mega-menu.liquid theme/sections/header.liquid theme/assets/header.js
git commit -m "feat: add mega menu with Shopify native navigation"
```

### Task 2.4: Mobile Menu

**Files:**
- Create: `theme/assets/mobile-menu.js`
- Create: `theme/assets/dialog.js`
- Modify: `theme/sections/header.liquid` (add mobile menu markup)
- Reference: `html/partials/site-header.html` (mobile menu section)

- [ ] **Step 1: Create `dialog.js` base class**

```javascript
import { Component } from '@theme/component';

export class DialogComponent extends Component {
  onConnect() {
    this._dialog = this.querySelector('dialog');
  }

  open() {
    this._dialog?.showModal();
    document.body.style.overflow = 'hidden';
  }

  close() {
    document.body.style.overflow = '';
    this._dialog?.close();
  }
}

customElements.define('dialog-component', DialogComponent);
```

- [ ] **Step 2: Create `mobile-menu.js`**

`<mobile-menu>` extends `DialogComponent`:
- 2-panel system: main nav panel + submenu panel
- Hamburger button triggers open
- Back button in submenu returns to main panel
- Renders same Shopify menu as desktop nav
- Social links + currency selector at bottom

- [ ] **Step 3: Add mobile menu markup to `header.liquid`**

Inside `header.liquid`, render the mobile menu `<dialog>` element with:
- Panel 1: main navigation links, CTA buttons, social icons, currency selector
- Panel 2: shop submenu (nested links from menu)

- [ ] **Step 4: Verify mobile menu opens/closes, submenu navigation works**

Test at mobile viewport (< 768px). Hamburger opens drawer, "Shop" shows submenu panel, back button returns.

- [ ] **Step 5: Commit**

```bash
git add theme/assets/dialog.js theme/assets/mobile-menu.js theme/sections/header.liquid
git commit -m "feat: add mobile menu drawer with nested navigation panels"
```

### Task 2.5: Predictive Search

**Files:**
- Create: `theme/assets/predictive-search.js`
- Create: `theme/snippets/search-modal.liquid`
- Modify: `theme/sections/header.liquid` (add search overlay markup)

- [ ] **Step 1: Create `search-modal.liquid` snippet**

Search overlay triggered by the search icon in the header. Renders:
- Full-width search input with close button
- Results area showing product cards, collection links, page suggestions

```liquid
<predictive-search class="search-modal" role="search">
  <dialog ref="dialog" class="search-dialog">
    <div class="search-inner container">
      <form action="{{ routes.search_url }}" method="get" role="search">
        <input type="search" name="q" placeholder="SEARCH" autocomplete="off"
          ref="input" aria-label="Search" class="search-input">
        <button type="button" ref="close" class="icon-btn" aria-label="Close search">
          {% render 'icon', name: 'close' %}
        </button>
      </form>
      <div ref="results" class="search-results" hidden></div>
    </div>
  </dialog>
</predictive-search>
```

- [ ] **Step 2: Create `predictive-search.js`**

`<predictive-search>` extends `DialogComponent`:
- Search icon click opens dialog, focuses input
- On input (debounced 300ms), fetch from `/search/suggest.json?q={query}&resources[type]=product,collection,page&resources[limit]=4`
- Render results as product cards + collection/page links
- Enter key or form submit navigates to full search results page
- Close on Escape / click outside / close button

- [ ] **Step 3: Wire search icon in header to open search overlay**

- [ ] **Step 4: Verify search opens, predictive results load, navigation works**

- [ ] **Step 5: Commit**

```bash
git add theme/assets/predictive-search.js theme/snippets/search-modal.liquid theme/sections/header.liquid
git commit -m "feat: add predictive search overlay with Shopify Search API"
```

### Task 2.6: Footer Section

**Files:**
- Create: `theme/sections/footer.liquid`
- Create: `theme/sections/footer-group.json`
- Reference: `html/partials/site-footer.html`

- [ ] **Step 1: Create `footer.liquid` section**

Structure matching mockup:
- 5-column grid (newsletter + 4 link columns)
- Newsletter column: heading, email form (Shopify `customer` form), social links (from global `settings.social_*` URLs)
- Link columns: each reads from a Shopify menu (accordion on mobile)
- Footer bottom: logo + copyright + payment icons

Schema settings:
- `color_scheme` (color_scheme, default: stone/secondary)
- `newsletter_heading` (text, default: "JOIN OUR NEWSLETTER")
- `menu_1` through `menu_4` (link_list pickers)
- `show_payment_icons` (checkbox, default: true)
- Note: Social link URLs come from global theme settings (`settings.social_instagram`, etc.) defined in Task 1.3, NOT section-level settings. This allows reuse in mobile menu and other sections.

- [ ] **Step 2: Create `footer-group.json`**

```json
{
  "type": "footer",
  "name": "Footer Group",
  "sections": {
    "footer": { "type": "footer" }
  },
  "order": ["footer"]
}
```

- [ ] **Step 3: Add footer accordion JS for mobile**

On mobile, footer link columns collapse into accordions. Add to `accordion.js` or inline in footer section.

- [ ] **Step 4: Verify footer renders with newsletter form, 4 menu columns, social links, payment icons**

- [ ] **Step 5: Commit**

```bash
git add theme/sections/footer.liquid theme/sections/footer-group.json
git commit -m "feat: add footer section with newsletter, menus, and social links"
```

### Phase 2 QA Checkpoint

- [ ] **QA: Verify Phase 2 deliverables**

1. Announcement bar shows text + currency selector (test switching currencies)
2. Header: logo displays (long on desktop, symbol on mobile)
3. Navigation links render from Shopify menu
4. Mega menu appears on hover with correct column layout + featured image
5. Sticky header works (scroll down, header stays/reappears based on setting)
6. Mobile: hamburger opens drawer, navigation works with submenu panels
7. Footer: newsletter form submits, all 4 menu columns show correct links
8. Footer: social icons link correctly, payment icons display
9. Footer: accordion behavior on mobile (columns collapse/expand)
10. All pages: header + footer render consistently
11. No console errors
12. Responsive: test at 375px, 768px, 1024px, 1440px, 1920px

Fix any issues, re-test, commit.

---

## Phase 3: Homepage

**Goal:** Complete homepage matching the HTML mockup.
**Dependencies:** Phase 2 complete (header/footer working).
**Can run in parallel:** Tasks 3.1, 3.3, 3.4, 3.5, 3.6 can be built independently. Task 3.2 depends on `product-card.liquid` snippet which is needed in later phases too.

### Task 3.1: Hero Slideshow Section

**Files:**
- Create: `theme/sections/hero-slideshow.liquid`
- Create: `theme/assets/slideshow.js`
- Create: `theme/assets/section-hero.css`
- Create: `theme/snippets/slideshow-controls.liquid`
- Reference: `html/index.html` (lines 22-100 approx)

- [ ] **Step 1: Create `slideshow-controls.liquid` snippet**

Renders dot indicators and optional prev/next arrows for any carousel:

```liquid
{%- comment -%}
  Usage: {% render 'slideshow-controls', total: 3, id: 'hero' %}
{%- endcomment -%}
<div class="slideshow-controls">
  <div class="slideshow-dots" role="tablist">
    {%- for i in (1..total) -%}
      <button class="slideshow-dot{% if forloop.first %} is-active{% endif %}"
        type="button" role="tab"
        aria-label="Slide {{ i }}" aria-selected="{{ forloop.first }}"
        data-slide-index="{{ forloop.index0 }}">
      </button>
    {%- endfor -%}
  </div>
</div>
```

- [ ] **Step 2: Create `hero-slideshow.liquid` section**

Each slide is a block with: heading, subheading, CTA text, CTA link, desktop image, mobile image, text alignment.

```liquid
<slideshow-component class="home-hero" data-autoplay="{{ section.settings.autoplay }}" data-interval="{{ section.settings.interval }}">
  <div class="hero-slider">
    {%- for block in section.blocks -%}
      <div class="hero-slide{% if forloop.first %} is-active{% endif %}" {{ block.shopify_attributes }}>
        <picture>
          {%- if block.settings.image_mobile -%}
            <source media="(max-width: 749px)" srcset="{{ block.settings.image_mobile | image_url: width: 750 }}">
          {%- endif -%}
          <img src="{{ block.settings.image_desktop | image_url: width: 1920 }}"
            alt="{{ block.settings.heading | escape }}" loading="{% if forloop.first %}eager{% else %}lazy{% endif %}">
        </picture>
        <div class="hero-content container" style="text-align: {{ block.settings.text_alignment }}">
          <h1 class="font-serif text-hero">{{ block.settings.heading }}</h1>
          {%- if block.settings.subheading != blank -%}
            <p class="hero-subtext text-body">{{ block.settings.subheading }}</p>
          {%- endif -%}
          {%- if block.settings.cta_text != blank -%}
            <a href="{{ block.settings.cta_link }}" class="btn-solid">{{ block.settings.cta_text }}</a>
          {%- endif -%}
        </div>
      </div>
    {%- endfor -%}
  </div>
  {% render 'slideshow-controls', total: section.blocks.size, id: section.id %}
</slideshow-component>
```

Schema: section settings for `autoplay` (checkbox, default: true), `interval` (range 3-10, default: 5). Block type `slide` with all fields above. Presets with 3 default slides matching mockup.

- [ ] **Step 3: Create `slideshow.js`**

`<slideshow-component>` extends `Component`:
- Auto-advances slides on timer (if autoplay enabled)
- Dot click navigates to slide
- Touch/swipe support on mobile
- Pause on hover/focus
- CSS transition for slide change (fade or slide)

- [ ] **Step 4: Create `section-hero.css`**

Port hero styles from `html/assets/css/index.css`. Use CSS custom properties for all values.

- [ ] **Step 5: Add hero section to `index.json` template**

- [ ] **Step 6: Verify hero slider works: auto-advance, dot navigation, touch swipe, responsive images**

- [ ] **Step 7: Commit**

```bash
git add theme/sections/hero-slideshow.liquid theme/assets/slideshow.js theme/assets/section-hero.css theme/snippets/slideshow-controls.liquid theme/templates/index.json
git commit -m "feat: add hero slideshow section with autoplay and swipe"
```

### Task 3.2: Product Card Snippet + Featured Collection Section

**Files:**
- Create: `theme/snippets/product-card.liquid`
- Create: `theme/snippets/price.liquid`
- Create: `theme/snippets/variant-swatches.liquid`
- Create: `theme/assets/product-card.js`
- Create: `theme/sections/featured-collection.liquid`
- Reference: `html/index.html` (bestsellers section), `html/shop.html` (product cards)

- [ ] **Step 1: Create `price.liquid` snippet**

```liquid
{%- comment -%}
  Renders product price with sale/compare-at logic.
  Usage: {% render 'price', product: product %}
{%- endcomment -%}
<span class="price font-sans" data-price>
  {%- if product.compare_at_price > product.price -%}
    <s class="price-compare text-muted">{{ product.compare_at_price | money }}</s>
    <span class="price-sale">{{ product.price | money }}</span>
  {%- else -%}
    {{ product.price | money }}
  {%- endif -%}
</span>
```

- [ ] **Step 2: Create `variant-swatches.liquid` snippet**

Renders color swatches on product cards. Reads from product option "Colour" and maps to swatch colors via variant metafields or option value swatches.

```liquid
{%- comment -%}
  Usage: {% render 'variant-swatches', product: product, option_name: 'Colour' %}
{%- endcomment -%}
{%- assign color_option = nil -%}
{%- for option in product.options_with_values -%}
  {%- if option.name == option_name -%}
    {%- assign color_option = option -%}
  {%- endif -%}
{%- endfor -%}

{%- if color_option -%}
  <div class="card-swatches">
    {%- for value in color_option.values -%}
      <button class="swatch{% if forloop.first %} is-active{% endif %}"
        type="button"
        aria-label="{{ value }}"
        data-option-value="{{ value }}"
        style="background-color: {{ value | handle | replace: 'ivory', '#EAE5DE' | replace: 'caramel', '#C99B6A' | replace: 'mocha', '#6A4232' }}">
      </button>
    {%- endfor -%}
  </div>
{%- endif -%}
```

Note: In production, swatch colors should come from variant `option_value.swatch` or metafields. The above is a starter; refine once products are set up in Shopify admin.

- [ ] **Step 3: Create `product-card.liquid` snippet**

Matches mockup card structure:
- Product image + hover second image
- Variant swatches (color)
- Product title + description
- Price (with sale logic)
- "SHOP NOW" link

```liquid
{%- comment -%}
  Usage: {% render 'product-card', product: product, show_swatches: true %}
{%- endcomment -%}
<product-card class="product-card">
  <a href="{{ product.url }}" class="product-card-link">
    <div class="product-card-media">
      <img src="{{ product.featured_image | image_url: width: 600 }}"
        alt="{{ product.featured_image.alt | escape }}" loading="lazy" class="card-image-primary">
      {%- if product.images.size > 1 and settings.card_show_secondary_image -%}
        <img src="{{ product.images[1] | image_url: width: 600 }}"
          alt="{{ product.images[1].alt | escape }}" loading="lazy" class="card-image-hover">
      {%- endif -%}
    </div>
  </a>
  <div class="product-card-info">
    {%- if show_swatches and settings.card_show_swatches -%}
      {% render 'variant-swatches', product: product, option_name: 'Colour' %}
    {%- endif -%}
    <a href="{{ product.url }}" class="product-card-title font-serif">{{ product.title }}</a>
    {%- if product.metafields.custom.subtitle -%}
      <p class="product-card-subtitle text-micro text-muted">{{ product.metafields.custom.subtitle }}</p>
    {%- endif -%}
    {% render 'price', product: product %}
    <a href="{{ product.url }}" class="btn-outline product-card-cta">SHOP NOW</a>
  </div>
</product-card>
```

- [ ] **Step 4: Create `product-card.js`**

`<product-card>` extends `Component`:
- Hover image swap (show secondary image on mouse enter, revert on leave)
- Swatch click changes card image to the variant's featured image (via data attributes)
- Optional: prefetch product URL on hover

- [ ] **Step 5: Create `featured-collection.liquid` section**

Renders a product carousel from a selected collection. Structure:
- Section heading (editable, default: "BESTSELLERS")
- Back/Next navigation arrows
- Product card grid (scrollable horizontal on mobile, 4-col on desktop)

Schema settings:
- `heading` (text, default: "BESTSELLERS")
- `collection` (collection picker)
- `products_to_show` (range: 4-12, default: 4)
- `show_navigation` (checkbox, default: true)
- `color_scheme` (color_scheme)

Uses `slideshow-component` or a simpler horizontal scroll pattern.

- [ ] **Step 6: Add to `index.json` and verify bestsellers carousel renders**

- [ ] **Step 7: Commit**

```bash
git add theme/snippets/product-card.liquid theme/snippets/price.liquid theme/snippets/variant-swatches.liquid theme/assets/product-card.js theme/sections/featured-collection.liquid theme/templates/index.json
git commit -m "feat: add product card snippet and featured collection section"
```

### Task 3.3: Our Commitment Section

**Files:**
- Create: `theme/sections/commitment.liquid`
- Reference: `html/index.html` (Our Commitment section)

- [ ] **Step 1: Create `commitment.liquid` section**

2-column layout: image left, content right (or reversed via setting).
- Image block (image_picker)
- Heading (text)
- Repeatable value blocks: icon (image_picker), title (text), description (text)
- Optional CTA link

Schema settings:
- `image` (image_picker)
- `heading` (text, default: "OUR COMMITMENT")
- `image_position` (select: left/right, default: left)
- `color_scheme` (color_scheme)
- `cta_text` (text), `cta_link` (url)
- Block type `value`: `icon` (image_picker), `title` (text), `description` (textarea)

- [ ] **Step 2: Add to `index.json` and verify**

- [ ] **Step 3: Commit**

```bash
git add theme/sections/commitment.liquid theme/templates/index.json
git commit -m "feat: add Our Commitment section with values grid"
```

### Task 3.4: Collections Grid Section

**Files:**
- Create: `theme/sections/collections-grid.liquid`
- Reference: `html/index.html` (collections section - Scar Collection + Sculpted Collection cards)

- [ ] **Step 1: Create `collections-grid.liquid` section**

Renders collection cards in a 2-column grid (or configurable columns).
- Each block is a collection card: image (from collection or override), heading (from collection or override), CTA link

Schema:
- `heading` (text, optional section heading)
- `columns` (range: 1-4, default: 2)
- `color_scheme` (color_scheme)
- Block type `collection_card`: `collection` (collection picker), `image_override` (image_picker), `heading_override` (text), `cta_text` (text, default: "DISCOVER NOW")

- [ ] **Step 2: Add to `index.json` and verify**

- [ ] **Step 3: Commit**

```bash
git add theme/sections/collections-grid.liquid theme/templates/index.json
git commit -m "feat: add collections grid section for homepage"
```

### Task 3.5: Split-View Section (Reusable)

**Files:**
- Create: `theme/sections/split-view.liquid`
- Create: `theme/assets/section-split-view.css`
- Reference: `html/index.html` (Our Story split section)

- [ ] **Step 1: Create `split-view.liquid` section**

Reusable 2-column section with image + content. Used on homepage (Our Story) and Our Story page (multiple instances).

Schema settings:
- `image` (image_picker)
- `image_position` (select: left/right, default: left)
- `color_scheme` (color_scheme)
- `eyebrow` (text, optional, e.g., "OUR STORY")
- `heading` (text)
- `body` (richtext)
- `cta_text` (text), `cta_link` (url)

- [ ] **Step 2: Port split-view CSS from mockup**

- [ ] **Step 3: Add to `index.json` and verify**

- [ ] **Step 4: Commit**

```bash
git add theme/sections/split-view.liquid theme/assets/section-split-view.css theme/templates/index.json
git commit -m "feat: add reusable split-view section"
```

### Task 3.6: Testimonials Section

**Files:**
- Create: `theme/sections/testimonials.liquid`
- Create: `theme/assets/section-testimonials.css`
- Reference: `html/index.html` (testimonials carousel)

- [ ] **Step 1: Create `testimonials.liquid` section**

Uses `<slideshow-component>` for carousel. Each testimonial is a block.

Schema settings:
- `heading` (text, default: "CUSTOMER TESTIMONIALS")
- `show_stars` (checkbox, default: true)
- `star_count` (range: 1-5, default: 5)
- `color_scheme` (color_scheme)
- Block type `testimonial`: `quote` (textarea), `author` (text), `rating` (range: 1-5, default: 5)

Reuses `slideshow.js` and `slideshow-controls.liquid` from Task 3.1.

- [ ] **Step 2: Port testimonial styles from mockup**

- [ ] **Step 3: Add to `index.json` and verify carousel works**

- [ ] **Step 4: Commit**

```bash
git add theme/sections/testimonials.liquid theme/assets/section-testimonials.css theme/templates/index.json
git commit -m "feat: add testimonials carousel section"
```

### Task 3.7: Compose `index.json` Template

**Files:**
- Modify: `theme/templates/index.json`

- [ ] **Step 1: Finalize `index.json` with all homepage sections in correct order**

```json
{
  "sections": {
    "hero": { "type": "hero-slideshow", "blocks": { ... }, "settings": { ... } },
    "bestsellers": { "type": "featured-collection", "settings": { "heading": "BESTSELLERS", ... } },
    "commitment": { "type": "commitment", "settings": { ... } },
    "collections": { "type": "collections-grid", "settings": { ... } },
    "our-story": { "type": "split-view", "settings": { ... } },
    "testimonials": { "type": "testimonials", "settings": { ... } }
  },
  "order": ["hero", "bestsellers", "commitment", "collections", "our-story", "testimonials"]
}
```

- [ ] **Step 2: Verify full homepage matches mockup layout**

- [ ] **Step 3: Commit**

```bash
git add theme/templates/index.json
git commit -m "feat: compose homepage template with all sections"
```

### Phase 3 QA Checkpoint

- [ ] **QA: Verify Phase 3 deliverables**

1. Hero: slides auto-advance, dots work, swipe works on mobile, responsive images load correctly
2. Bestsellers: 4 products display from selected collection, carousel navigation works
3. Product cards: hover reveals second image, swatches display, price renders correctly
4. Commitment: 2-column layout with image + values grid, responsive stacking on mobile
5. Collections: 2 cards display with images, headings, CTA links
6. Split-view: image + content renders, image position toggle works
7. Testimonials: carousel works with dots, quotes display correctly
8. Full homepage: section ordering matches mockup, spacing is consistent
9. Theme customizer: all sections editable, blocks can be added/removed/reordered
10. Responsive: test at 375px, 768px, 1024px, 1440px, 1920px
11. No console errors

Fix any issues, re-test, commit.

---

## Phase 4: Product Detail Page

**Goal:** Complete product template with gallery, variant picker, accordions, related sections.
**Dependencies:** Phase 3 complete (product-card.liquid available, base components working).
**Can run in parallel:** Tasks 4.1-4.3 are sequential (gallery → variant picker → accordions build on each other). Tasks 4.4, 4.5 are independent of each other but depend on 4.1-4.3.

### Task 4.1: Product Media Gallery

**Files:**
- Create: `theme/sections/main-product.liquid` (start with gallery portion)
- Create: `theme/assets/section-product.css`
- Reference: `html/product.html` (lines 38-87)

- [ ] **Step 1: Create `main-product.liquid` section — gallery portion**

2-column layout: left = gallery, right = product details.

Gallery structure:
- Main image viewport with slide track
- Previous/next arrows
- Thumbnail strip below
- Wishlist button (placeholder — deferred feature)

The gallery should update when variants change (via Section Rendering API later in Task 4.2).

- [ ] **Step 2: Port product gallery CSS from `html/assets/css/product.css`**

- [ ] **Step 3: Add gallery interactivity**

Add to `main-product.liquid` inline `<script type="module">` or create a dedicated `product-gallery.js`:
- Thumbnail click → update main image
- Arrow navigation
- Touch swipe on mobile
- Active thumbnail state tracking

- [ ] **Step 4: Create `product.json` template with `main-product` section**

- [ ] **Step 5: Verify gallery renders with product images, thumbnails, navigation**

- [ ] **Step 6: Commit**

```bash
git add theme/sections/main-product.liquid theme/assets/section-product.css theme/templates/product.json
git commit -m "feat: add product page with media gallery"
```

### Task 4.2: Variant Picker (Color + Shape + Scent)

**Files:**
- Create: `theme/assets/variant-picker.js`
- Create: `theme/snippets/variant-picker.liquid` (full product page version)
- Modify: `theme/sections/main-product.liquid` (add variant picker to details column)
- Reference: `html/product.html` (lines 99-150 approx)

- [ ] **Step 1: Create `variant-picker.liquid` snippet**

Renders variant options based on product option type:
- **Colour** → large swatches (circles with background colors)
- **Body Shape** → pill buttons (Slim, Curvy, Plus-Size)
- **Scent** → pill buttons (Vanilla, Lavender)

Each option is a `<fieldset>` with hidden radio inputs:

```liquid
{%- for option in product.options_with_values -%}
  <fieldset class="variant-option" data-option-position="{{ option.position }}">
    <legend class="selector-label text-sm">
      {{ option.name | upcase }} : <span data-selected-value>{{ option.selected_value }}</span>
    </legend>
    <div class="variant-option-values{% if option.name == 'Colour' %} swatch-group{% else %} pill-group{% endif %}">
      {%- for value in option.values -%}
        <label class="{% if option.name == 'Colour' %}swatch-label{% else %}pill-label{% endif %}">
          <input type="radio" name="{{ option.name }}"
            value="{{ value }}"
            {% if value == option.selected_value %}checked{% endif %}
            data-option-value-id="{{ value.id }}"
            {% unless value.available %}disabled{% endunless %}>
          {%- if option.name == 'Colour' -%}
            <span class="swatch swatch-large"
              style="background-color: {{ value | handle | replace: 'ivory', '#EAE5DE' | replace: 'caramel', '#C99B6A' | replace: 'mocha', '#6A4232' }}"
              aria-label="{{ value }}"></span>
          {%- else -%}
            <span class="pill">{{ value }}</span>
          {%- endif -%}
        </label>
      {%- endfor -%}
    </div>
  </fieldset>
{%- endfor -%}
```

- [ ] **Step 2: Create `variant-picker.js`**

`<variant-picker>` extends `Component`:
- Listens for `change` events on radio inputs
- On change: updates selected value label, updates URL with variant ID
- Fetches updated section HTML via Section Rendering API (`?section_id=...&variant=...`)
- Updates: gallery images, price, add-to-cart button state (available/sold out)
- Uses DOM diffing or targeted element swaps

- [ ] **Step 3: Add variant picker + quantity selector + add-to-cart to product details column**

Complete the right column of `main-product.liquid`:
- Product title + subtitle (from metafield)
- Price
- Variant picker (wrapped in `<variant-picker>`)
- Quantity selector
- Add to cart button (Shopify product form)

```liquid
{%- form 'product', product, id: 'product-form', data-product-form: '' -%}
  <input type="hidden" name="id" value="{{ product.selected_or_first_available_variant.id }}">
  <variant-picker data-section="{{ section.id }}" data-product-url="{{ product.url }}">
    {% render 'variant-picker', product: product %}
  </variant-picker>
  <quantity-selector class="quantity-selector">
    <button type="button" data-action="decrease" aria-label="Decrease quantity">-</button>
    <input type="number" name="quantity" value="1" min="1" aria-label="Quantity">
    <button type="button" data-action="increase" aria-label="Increase quantity">+</button>
  </quantity-selector>
  <button type="submit" class="btn-solid add-to-cart"
    {% unless product.selected_or_first_available_variant.available %}disabled{% endunless %}>
    {%- if product.selected_or_first_available_variant.available -%}
      ADD TO BAG — {{ product.selected_or_first_available_variant.price | money }}
    {%- else -%}
      SOLD OUT
    {%- endif -%}
  </button>
{%- endform -%}
```

- [ ] **Step 4: Create `quantity-selector.js`**

`<quantity-selector>` extends `Component`:
- +/- buttons increment/decrement input value
- Min value = 1, prevents going below

- [ ] **Step 5: Verify variant selection updates gallery, price, and add-to-cart**

- [ ] **Step 6: Commit**

```bash
git add theme/assets/variant-picker.js theme/assets/quantity-selector.js theme/snippets/variant-picker.liquid theme/sections/main-product.liquid
git commit -m "feat: add variant picker with Section Rendering API and quantity selector"
```

### Task 4.3: Product Accordions

**Files:**
- Create: `theme/assets/accordion.js`
- Create: `theme/snippets/accordion.liquid`
- Modify: `theme/sections/main-product.liquid` (add accordion blocks)
- Reference: `html/product.html` (accordion section)

- [ ] **Step 1: Create `accordion.js`**

`<accordion-component>` extends `Component`:
- Click header toggles body visibility
- Supports exclusive mode (only one open at a time) or independent
- Manages `aria-expanded` state
- Smooth height animation via CSS transition

- [ ] **Step 2: Create `accordion.liquid` snippet**

```liquid
{%- comment -%}
  Usage: {% render 'accordion', title: 'Description', content: product.description, open: true %}
{%- endcomment -%}
<details class="accordion"{% if open %} open{% endif %}>
  <summary class="accordion-header">
    <span>{{ title }}</span>
    {% render 'icon', name: 'plus' %}
  </summary>
  <div class="accordion-body">
    {{ content }}
  </div>
</details>
```

- [ ] **Step 3: Add accordion blocks to `main-product.liquid` schema**

Block type `accordion` with: `title` (text), `content` (richtext), `open_by_default` (checkbox).

Default blocks:
1. "Description" (maps to `product.description`, open by default)
2. "Craft & Intention" (richtext from metafield `custom.craft_intention`)
3. "How to Use" (richtext from metafield `custom.how_to_use`)
4. "Dimensions & Ingredients" (richtext from metafield `custom.dimensions_ingredients`)

- [ ] **Step 4: Verify accordions open/close, first is open by default**

- [ ] **Step 5: Commit**

```bash
git add theme/assets/accordion.js theme/snippets/accordion.liquid theme/sections/main-product.liquid
git commit -m "feat: add product accordion blocks for description, craft, how-to-use"
```

### Task 4.4: Product Page — Scents Section + Commitment Reuse

**Files:**
- Create: `theme/sections/scents-section.liquid` (or reuse as a generic content section)
- Modify: `theme/templates/product.json` (add scents + commitment sections)
- Reference: `html/product.html` (scents section, commitment section)

- [ ] **Step 1: Create scents section**

Displays scent options for the product. Each scent is a block with: image, name, description.

Schema:
- `heading` (text, default: "SCENTS")
- Block type `scent`: `image` (image_picker), `name` (text), `description` (textarea)

- [ ] **Step 2: Add scents section + commitment section (reuse from Phase 3) to `product.json`**

- [ ] **Step 3: Verify both sections render on product page below the main product**

- [ ] **Step 4: Commit**

```bash
git add theme/sections/scents-section.liquid theme/templates/product.json
git commit -m "feat: add scents section and commitment reuse to product page"
```

### Task 4.5: Product Recommendations + Reviews Placeholder

**Files:**
- Create: `theme/sections/product-recommendations.liquid`
- Create: `theme/sections/reviews-placeholder.liquid`
- Modify: `theme/templates/product.json`
- Reference: `html/product.html` (You May Also Like, Reviews sections)

- [ ] **Step 1: Create `product-recommendations.liquid` section**

Uses Shopify's Product Recommendations API:

```liquid
<section class="section-block product-recommendations" data-url="{{ routes.product_recommendations_url }}?product_id={{ product.id }}&limit=4&section_id={{ section.id }}">
  {%- if recommendations.performed? and recommendations.products_count > 0 -%}
    <div class="container">
      <h2 class="font-serif text-h3">{{ section.settings.heading }}</h2>
      <div class="product-grid grid-cols-4">
        {%- for product in recommendations.products -%}
          {% render 'product-card', product: product, show_swatches: true %}
        {%- endfor -%}
      </div>
    </div>
  {%- endif -%}
</section>
```

Schema: `heading` (text, default: "YOU MAY ALSO LIKE"), `products_to_show` (range: 2-8, default: 4)

- [ ] **Step 2: Create `reviews-placeholder.liquid` section**

Placeholder section for Judge.me app integration. Renders:
- Section heading "WHAT OUR CUSTOMERS ARE SAYING"
- An app block placeholder: `{% content_for 'blocks' %}` or simply a `<div id="judgeme-reviews">` that Judge.me's script will populate

Schema: `heading` (text, default: "WHAT OUR CUSTOMERS ARE SAYING")

- [ ] **Step 3: Add both sections to `product.json`**

- [ ] **Step 4: Verify recommendations load, reviews placeholder renders**

- [ ] **Step 5: Commit**

```bash
git add theme/sections/product-recommendations.liquid theme/sections/reviews-placeholder.liquid theme/templates/product.json
git commit -m "feat: add product recommendations and Judge.me reviews placeholder"
```

### Task 4.6: Breadcrumbs

**Files:**
- Create: `theme/snippets/breadcrumbs.liquid`
- Modify: `theme/sections/main-product.liquid` (add breadcrumbs at top)
- Reference: `html/product.html` (line 25-28)

- [ ] **Step 1: Create `breadcrumbs.liquid` snippet**

Auto-generates breadcrumb trail from product's collection hierarchy:

```liquid
<nav class="breadcrumbs text-micro text-muted" aria-label="Breadcrumb">
  <a href="{{ routes.collections_url }}" class="text-muted">SHOP</a>
  {%- if product.collections.size > 0 -%}
    {% assign collection = product.collections.first %}
    / <a href="{{ collection.url }}" class="text-muted">{{ collection.title | upcase }}</a>
  {%- endif -%}
  / <span class="text-primary breadcrumb-current">{{ product.title | upcase }}</span>
</nav>
```

- [ ] **Step 2: Add breadcrumbs to main-product section**

- [ ] **Step 3: Commit**

```bash
git add theme/snippets/breadcrumbs.liquid theme/sections/main-product.liquid
git commit -m "feat: add breadcrumb navigation to product page"
```

### Phase 4 QA Checkpoint

- [ ] **QA: Verify Phase 4 deliverables**

1. Product gallery: images display, thumbnails work, arrows navigate, swipe on mobile
2. Variant picker: colour swatches change gallery image, shape/scent pills update selection
3. Section Rendering: variant change updates price, add-to-cart text, availability
4. Add to cart: form submits, cart count updates, drawer opens (if enabled)
5. Quantity selector: +/- works, min value = 1
6. Accordions: open/close, first open by default, smooth animation
7. Breadcrumbs: correct hierarchy displayed
8. Scents section: renders correctly below product
9. Commitment section: reused from homepage, renders on product page
10. Recommendations: loads 4 related products from Shopify API
11. Reviews placeholder: Judge.me can hook into the placeholder
12. Mobile: full page works at mobile viewport, gallery swipe, stacked layout
13. Theme customizer: all product sections/blocks editable
14. No console errors

Fix, re-test, commit.

---

## Phase 5: Collection Pages

**Goal:** Shop All, Body Candles, Scar Collection, Sculpted Collection, Gifts — all use the same collection template with native filtering and sorting.
**Dependencies:** Phase 3 complete (product-card.liquid available).
**Can run in parallel with Phase 4.** Tasks 5.1-5.3 are sequential.

### Task 5.1: Main Collection Section with Product Grid

**Files:**
- Create: `theme/sections/main-collection.liquid`
- Create: `theme/snippets/product-grid.liquid` (optional, or inline in section)
- Create: `theme/assets/section-collection.css`
- Create: `theme/templates/collection.json`
- Reference: `html/shop.html`

- [ ] **Step 1: Create `main-collection.liquid` section**

Structure:
- Collection hero: title + description (auto from collection)
- Filter toolbar: filter button + sort dropdown
- Product grid: 4-column layout using `product-card.liquid`
- Pagination

```liquid
{%- paginate collection.products by section.settings.products_per_page -%}
<section class="collection-page">
  <div class="container">
    {%- comment -%} Collection Hero {%- endcomment -%}
    <div class="collection-hero">
      <h1 class="font-serif text-h1">{{ collection.title | upcase }}</h1>
      {%- if collection.description != blank -%}
        <div class="collection-description text-body">{{ collection.description }}</div>
      {%- endif -%}
    </div>

    {%- comment -%} Toolbar {%- endcomment -%}
    <facet-filters class="collection-toolbar" data-section="{{ section.id }}">
      <button class="btn-outline filter-toggle" type="button" aria-controls="filter-drawer">
        {% render 'icon', name: 'filter' %} FILTER
      </button>
      <div class="sort-wrapper">
        <label for="sort-select" class="visually-hidden">Sort by</label>
        <select id="sort-select" name="sort_by" data-sort-select>
          {%- for option in collection.sort_options -%}
            <option value="{{ option.value }}"{% if collection.sort_by == option.value %} selected{% endif %}>
              {{ option.name }}
            </option>
          {%- endfor -%}
        </select>
      </div>
      <span class="product-count text-micro text-muted">{{ collection.products_count }} ITEMS</span>
    </facet-filters>

    {%- comment -%} Filter Drawer {%- endcomment -%}
    <div id="filter-drawer" class="filter-panel" hidden>
      {%- for filter in collection.filters -%}
        <details class="filter-group" open>
          <summary>{{ filter.label }}</summary>
          <ul>
            {%- for value in filter.values -%}
              <li>
                <label>
                  <input type="checkbox" name="{{ value.param_name }}" value="{{ value.value }}"
                    {% if value.active %}checked{% endif %}>
                  {{ value.label }} ({{ value.count }})
                </label>
              </li>
            {%- endfor -%}
          </ul>
        </details>
      {%- endfor -%}
    </div>

    {%- comment -%} Product Grid {%- endcomment -%}
    <div class="product-grid grid-cols-4" id="product-grid">
      {%- for product in collection.products -%}
        {% render 'product-card', product: product, show_swatches: true %}
      {%- endfor -%}
    </div>

    {%- comment -%} Pagination {%- endcomment -%}
    {%- if paginate.pages > 1 -%}
      {% render 'pagination', paginate: paginate %}
    {%- endif -%}
  </div>
</section>
{%- endpaginate -%}
```

Schema settings:
- `products_per_page` (range: 8-48, default: 16)
- `columns_desktop` (range: 2-5, default: 4)
- `enable_filtering` (checkbox, default: true)
- `enable_sorting` (checkbox, default: true)
- `color_scheme` (color_scheme)

- [ ] **Step 2: Port collection page CSS from mockup**

- [ ] **Step 3: Create `collection.json` template**

```json
{
  "sections": {
    "main": { "type": "main-collection", "settings": {} }
  },
  "order": ["main"]
}
```

- [ ] **Step 4: Verify collection page renders with products from Shopify admin**

- [ ] **Step 5: Commit**

```bash
git add theme/sections/main-collection.liquid theme/assets/section-collection.css theme/templates/collection.json
git commit -m "feat: add collection page with product grid and pagination"
```

### Task 5.2: Filtering & Sorting (AJAX)

**Files:**
- Create: `theme/assets/facets.js`
- Create: `theme/snippets/pagination.liquid`
- Modify: `theme/sections/main-collection.liquid`

- [ ] **Step 1: Create `facets.js`**

`<facet-filters>` extends `Component`:
- Filter checkbox changes and sort select changes trigger AJAX fetch
- Fetches collection page with updated params (e.g., `?filter.v.option.colour=Ivory&sort_by=price-ascending`)
- Extracts updated product grid + filter state from response HTML
- Replaces `#product-grid` and filter panel content without full page reload
- Updates browser URL via `history.replaceState`
- Updates product count

- [ ] **Step 2: Create `pagination.liquid` snippet**

Numbered pagination with prev/next:

```liquid
{%- if paginate.pages > 1 -%}
<nav class="pagination" aria-label="Pagination">
  {%- if paginate.previous -%}
    <a href="{{ paginate.previous.url }}" class="pagination-prev" aria-label="Previous page">&larr;</a>
  {%- endif -%}
  {%- for part in paginate.parts -%}
    {%- if part.is_link -%}
      <a href="{{ part.url }}" class="pagination-page">{{ part.title }}</a>
    {%- elsif part.title == paginate.current_page -%}
      <span class="pagination-page is-current" aria-current="page">{{ part.title }}</span>
    {%- else -%}
      <span class="pagination-page">{{ part.title }}</span>
    {%- endif -%}
  {%- endfor -%}
  {%- if paginate.next -%}
    <a href="{{ paginate.next.url }}" class="pagination-next" aria-label="Next page">&rarr;</a>
  {%- endif -%}
</nav>
{%- endif -%}
```

- [ ] **Step 3: Verify filtering and sorting work without page reload**

Test: select a filter → products update, URL updates, filter shows as checked. Sort → products reorder. Pagination → next page loads.

- [ ] **Step 4: Commit**

```bash
git add theme/assets/facets.js theme/snippets/pagination.liquid theme/sections/main-collection.liquid
git commit -m "feat: add AJAX filtering, sorting, and pagination for collections"
```

### Task 5.3: Gifts Collection Template (Alternate Layout)

**Files:**
- Create: `theme/templates/collection.gifts.json` (if gifts page needs a different layout)

- [ ] **Step 1: Evaluate whether Gifts, Body Candles, Scar, or Sculpted pages need custom templates**

If any collection page has a unique hero or layout different from the standard collection template, create alternate templates (e.g., `collection.gifts.json`, `collection.body-candles.json`). These can add a hero image section or split-view section above the standard product grid.

If they're visually identical to the standard collection (just different title/description/products), skip custom templates — the founder configures them via collection admin (title, description, products) and the standard `collection.json` handles the rest.

- [ ] **Step 2: Create alternate template if needed**

- [ ] **Step 3: Commit (if applicable)**

```bash
git add theme/templates/collection.gifts.json
git commit -m "feat: add gifts collection template with custom hero"
```

### Phase 5 QA Checkpoint

- [ ] **QA: Verify Phase 5 deliverables**

1. Collection page renders product grid (4 columns desktop, 2 mobile)
2. Collection hero shows title + description from Shopify admin
3. Filtering: checkboxes filter products via AJAX, URL updates, filter state persists
4. Sorting: dropdown reorders products, URL updates
5. Product count updates after filtering
6. Pagination works (numbered pages, prev/next)
7. Product cards: images, swatches, price, hover effect all work
8. Different collections (Shop All, Body Candles, Scar, Sculpted, Gifts) all use the template
9. Responsive: grid collapses to 2 columns on tablet, 1-2 on mobile
10. No console errors

Fix, re-test, commit.

---

## Phase 6: Cart (Drawer + Page)

**Goal:** Cart drawer (slide-out) and full cart page, integrated with Shopify Cart API.
**Dependencies:** Phase 4 Task 4.2 complete (add-to-cart form working).
**Can run in parallel with Phase 5.** Tasks 6.1-6.2 are sequential.

### Task 6.1: Cart Drawer

**Files:**
- Create: `theme/snippets/cart-drawer.liquid`
- Create: `theme/assets/cart-drawer.js`
- Create: `theme/assets/section-cart.css`
- Reference: Horizon theme's cart drawer pattern

- [ ] **Step 1: Create `cart-drawer.liquid` snippet**

Renders inside `theme.liquid` when `settings.cart_type == 'drawer'`:

```liquid
<cart-drawer class="cart-drawer" {% if settings.cart_auto_open %}data-auto-open{% endif %}>
  <dialog ref="dialog" class="cart-drawer-dialog">
    <div class="cart-drawer-header">
      <h2 class="font-serif">YOUR BAG</h2>
      <button type="button" ref="close" aria-label="Close cart" class="icon-btn">
        {% render 'icon', name: 'close' %}
      </button>
    </div>
    <div class="cart-drawer-body" ref="body">
      {%- if cart.item_count > 0 -%}
        {%- for item in cart.items -%}
          <div class="cart-drawer-item" data-line="{{ forloop.index }}">
            <img src="{{ item.image | image_url: width: 120 }}" alt="{{ item.title }}">
            <div class="cart-drawer-item-info">
              <a href="{{ item.url }}" class="cart-item-title">{{ item.product.title }}</a>
              <p class="text-micro text-muted">{{ item.variant.title }}</p>
              <quantity-selector data-line="{{ forloop.index }}" data-cart-quantity>
                <button type="button" data-action="decrease">-</button>
                <input type="number" value="{{ item.quantity }}" min="0">
                <button type="button" data-action="increase">+</button>
              </quantity-selector>
            </div>
            <div class="cart-drawer-item-price">
              {%- comment -%} Cart line_item uses final_line_price, not product.price {%- endcomment -%}
              {%- if item.original_line_price > item.final_line_price -%}
                <s class="price-compare text-muted">{{ item.original_line_price | money }}</s>
              {%- endif -%}
              <span class="price">{{ item.final_line_price | money }}</span>
            </div>
          </div>
        {%- endfor -%}
      {%- else -%}
        <p class="cart-empty-message text-muted">Your bag is empty</p>
        <a href="{{ routes.collections_url }}" class="btn-outline">CONTINUE SHOPPING</a>
      {%- endif -%}
    </div>
    <div class="cart-drawer-footer" ref="footer">
      <div class="cart-subtotal flex-between">
        <span>SUBTOTAL</span>
        <span>{{ cart.total_price | money }}</span>
      </div>
      <a href="{{ routes.cart_url }}" class="btn-outline">VIEW BAG</a>
      <button type="submit" form="cart-drawer-form" class="btn-solid" name="checkout">CHECKOUT</button>
      <form id="cart-drawer-form" action="{{ routes.cart_url }}" method="post"></form>
    </div>
  </dialog>
</cart-drawer>
```

- [ ] **Step 2: Create `cart-drawer.js`**

`<cart-drawer>` extends `DialogComponent`:
- Opens on `cart:add` custom event (if `data-auto-open` present)
- Cart icon click opens drawer
- Close button / click outside / Escape closes
- Quantity changes in drawer call Cart API (`/cart/change.js`) and re-render drawer via Section Rendering API
- Remove item (quantity = 0)
- Updates cart count badge in header

- [ ] **Step 3: Port cart drawer styles**

- [ ] **Step 4: Wire add-to-cart form to dispatch `cart:add` event**

In `main-product.liquid`, intercept form submit:
- Prevent default
- POST to `/cart/add.js`
- On success: dispatch `CartAddEvent`, update cart count, open drawer

- [ ] **Step 5: Verify drawer opens on add-to-cart, shows items, quantity works, checkout redirects**

- [ ] **Step 6: Commit**

```bash
git add theme/snippets/cart-drawer.liquid theme/assets/cart-drawer.js theme/assets/section-cart.css
git commit -m "feat: add cart drawer with Cart API integration"
```

### Task 6.2: Cart Page

**Files:**
- Create: `theme/sections/main-cart.liquid`
- Create: `theme/assets/cart.js`
- Create: `theme/templates/cart.json`
- Reference: `html/cart.html`

- [ ] **Step 1: Create `main-cart.liquid` section**

Structure matching mockup:
- Breadcrumb tracker (BAG → INFORMATION → SHIPPING → PAYMENT) — first step active
- 2-column layout:
  - Left: cart items table (image, product info, price, quantity, total, remove)
  - Right: order summary (subtotal, shipping, tax, total, checkout button)

Uses Shopify's `cart` object. Quantity changes via Cart API + Section Rendering.

- [ ] **Step 2: Create `cart.js`**

`<cart-items>` extends `Component`:
- Quantity change → Cart API `POST /cart/change.js` → re-render section
- Remove item → quantity = 0
- Update totals in summary
- Sync cart drawer if open

- [ ] **Step 3: Create `cart.json` template**

- [ ] **Step 4: Verify full cart page: items display, quantity change, remove, totals update, checkout redirects to Shopify checkout**

- [ ] **Step 5: Commit**

```bash
git add theme/sections/main-cart.liquid theme/assets/cart.js theme/templates/cart.json
git commit -m "feat: add cart page with quantity management and order summary"
```

### Phase 6 QA Checkpoint

- [ ] **QA: Verify Phase 6 deliverables**

1. Add to cart from product page → drawer opens with correct item
2. Cart drawer: quantity +/- updates price, remove works
3. Cart drawer: "VIEW BAG" goes to cart page, "CHECKOUT" goes to Shopify checkout
4. Cart page: items display with image, title, variant, price, quantity
5. Cart page: quantity change updates totals via AJAX
6. Cart page: remove item works
7. Cart page: order summary shows subtotal, shipping info, tax, total
8. Cart page: checkout button redirects to Shopify checkout
9. Cart count badge in header updates across all pages
10. Empty cart: shows message + continue shopping link
11. Responsive: cart drawer works on mobile, cart page stacks on mobile
12. No console errors

Fix, re-test, commit.

---

## Phase 7: Static Pages

**Goal:** Our Story, Your Story (UGC), Contact pages.
**Dependencies:** Phase 2 complete (header/footer). Phase 3 Task 3.5 complete (split-view section).
**Can run in parallel:** All 3 tasks are independent.

### Task 7.1: Our Story Page

**Files:**
- Create: `theme/templates/page.our-story.json`
- Reuse: `theme/sections/hero-slideshow.liquid` (or a simpler hero variant)
- Reuse: `theme/sections/split-view.liquid`
- Create: `theme/sections/quote-highlight.liquid`
- Reference: `html/our-story.html`

- [ ] **Step 1: Create `quote-highlight.liquid` section**

Large quote text with optional attribution. Styled with accent background.

Schema:
- `quote` (textarea)
- `attribution` (text, optional)
- `color_scheme` (color_scheme)
- `text_alignment` (select: left/center, default: center)

- [ ] **Step 2: Create `page.our-story.json` template**

Compose using reusable sections:
```json
{
  "sections": {
    "hero": { "type": "split-view", "settings": { "eyebrow": "OUR STORY", ... } },
    "story-1": { "type": "split-view", "settings": { "image_position": "left", ... } },
    "quote-1": { "type": "quote-highlight", "settings": { ... } },
    "story-2": { "type": "split-view", "settings": { "image_position": "right", ... } }
  },
  "order": ["hero", "story-1", "quote-1", "story-2"]
}
```

The founder can add/remove/reorder split-view and quote sections via theme customizer.

- [ ] **Step 3: Create a "Our Story" page in Shopify admin, assign template**

- [ ] **Step 4: Verify page renders with correct sections, all content editable**

- [ ] **Step 5: Commit**

```bash
git add theme/sections/quote-highlight.liquid theme/templates/page.our-story.json
git commit -m "feat: add Our Story page template with split-view and quote sections"
```

### Task 7.2: Your Story (UGC) Page

**Files:**
- Create: `theme/sections/story-form.liquid`
- Create: `theme/sections/story-grid.liquid`
- Create: `theme/templates/page.your-story.json`
- Reference: `html/your-story.html`

- [ ] **Step 1: Create `story-form.liquid` section**

Custom form that submits to the founder's email. Uses Shopify's contact form as the transport:

```liquid
<section class="story-form-section">
  <div class="container">
    <h2 class="font-serif text-h2">{{ section.settings.heading }}</h2>
    <p class="text-body text-muted">{{ section.settings.description }}</p>

    {%- form 'contact', id: 'story-submission' -%}
      {%- if form.posted_successfully? -%}
        <p class="form-success">Thank you for sharing your story! We'll review it soon.</p>
      {%- endif -%}
      {%- if form.errors -%}
        <div class="form-errors" role="alert">
          {{ form.errors | default_errors }}
        </div>
      {%- endif -%}

      <input type="hidden" name="contact[tags]" value="story-submission">
      <div class="form-group">
        <label for="story-name" class="form-label">YOUR NAME</label>
        <input type="text" id="story-name" name="contact[name]" class="form-input" required>
      </div>
      <div class="form-group">
        <label for="story-email" class="form-label">YOUR EMAIL</label>
        <input type="email" id="story-email" name="contact[email]" class="form-input" required>
      </div>
      <div class="form-group">
        <label for="story-text" class="form-label">YOUR STORY</label>
        <textarea id="story-text" name="contact[body]" class="form-input" rows="6" required></textarea>
      </div>
      <button type="submit" class="btn-solid">SUBMIT YOUR STORY</button>
    {%- endform -%}
  </div>
</section>
```

Schema: `heading` (text), `description` (textarea)

- [ ] **Step 2: Create `story-grid.liquid` section**

Displays approved stories from metaobjects. Each story card opens in a modal on click.

Prerequisites: Create a metaobject definition "Customer Story" in Shopify admin with fields:
- `name` (single_line_text)
- `story` (multi_line_text)
- `image` (file_reference)
- `product` (product_reference, optional)

```liquid
<section class="story-grid-section">
  <div class="container">
    <h2 class="font-serif text-h2">{{ section.settings.heading }}</h2>
    <div class="story-grid grid-cols-3">
      {%- assign stories = section.settings.stories.value -%}
      {%- for story in stories -%}
        <button class="story-card" type="button" data-story-modal="{{ forloop.index }}">
          {%- if story.image -%}
            <img src="{{ story.image | image_url: width: 400 }}" alt="{{ story.name }}" loading="lazy">
          {%- endif -%}
          <div class="story-card-info">
            <h3 class="story-card-name font-serif">{{ story.name }}</h3>
            <p class="story-card-excerpt text-small text-muted">{{ story.story | truncate: 120 }}</p>
          </div>
        </button>
      {%- endfor -%}
    </div>

    {%- comment -%} Modals for each story {%- endcomment -%}
    {%- for story in stories -%}
      <dialog-component>
        <dialog class="story-modal" id="story-modal-{{ forloop.index }}">
          <div class="story-modal-content">
            <button type="button" class="icon-btn story-modal-close" aria-label="Close">
              {% render 'icon', name: 'close' %}
            </button>
            {%- if story.image -%}
              <img src="{{ story.image | image_url: width: 800 }}" alt="{{ story.name }}">
            {%- endif -%}
            <h3 class="font-serif text-h3">{{ story.name }}</h3>
            <div class="story-modal-body text-body">{{ story.story }}</div>
          </div>
        </dialog>
      </dialog-component>
    {%- endfor -%}
  </div>
</section>
```

Schema: `heading` (text, default: "YOUR STORIES"), `stories` (list.metaobject_reference, metaobject type: customer_story)

Note: The metaobject list reference allows the founder to curate which approved stories appear.

- [ ] **Step 3: Add JS for story card click → modal open**

Inline script or extend `dialog.js` to handle `data-story-modal` click.

- [ ] **Step 4: Create `page.your-story.json` template**

```json
{
  "sections": {
    "form": { "type": "story-form" },
    "grid": { "type": "story-grid" }
  },
  "order": ["form", "grid"]
}
```

- [ ] **Step 5: Create page in Shopify admin, assign template, create test metaobjects**

- [ ] **Step 6: Verify form submits, story grid displays, modal opens on click**

- [ ] **Step 7: Commit**

```bash
git add theme/sections/story-form.liquid theme/sections/story-grid.liquid theme/templates/page.your-story.json
git commit -m "feat: add Your Story UGC page with submission form and metaobject grid"
```

### Task 7.3: Contact Page

**Files:**
- Create: `theme/templates/page.contact.json`
- Create: `theme/sections/contact-form.liquid`
- Reference: `html/contact.html`

- [ ] **Step 1: Create `contact-form.liquid` section**

Uses Shopify's built-in contact form:

```liquid
<section class="contact-section">
  <div class="container">
    <h1 class="font-serif text-h1">{{ section.settings.heading }}</h1>

    {%- form 'contact', id: 'contact-form' -%}
      {%- if form.posted_successfully? -%}
        <p class="form-success">Thank you for your message. We'll get back to you soon.</p>
      {%- endif -%}
      {%- if form.errors -%}
        <div class="form-errors" role="alert">
          {{ form.errors | default_errors }}
        </div>
      {%- endif -%}

      <div class="form-grid grid-cols-2">
        <div class="form-group">
          <label for="contact-name" class="form-label">NAME</label>
          <input type="text" id="contact-name" name="contact[name]" class="form-input" required>
        </div>
        <div class="form-group">
          <label for="contact-email" class="form-label">EMAIL</label>
          <input type="email" id="contact-email" name="contact[email]" class="form-input" required>
        </div>
      </div>
      <div class="form-group">
        <label for="contact-subject" class="form-label">SUBJECT</label>
        <input type="text" id="contact-subject" name="contact[subject]" class="form-input">
      </div>
      <div class="form-group">
        <label for="contact-message" class="form-label">MESSAGE</label>
        <textarea id="contact-message" name="contact[body]" class="form-input" rows="6" required></textarea>
      </div>
      <button type="submit" class="btn-solid">SEND MESSAGE</button>
    {%- endform -%}
  </div>
</section>
```

Schema: `heading` (text, default: "CONTACT US"), `description` (richtext, optional)

Blocks for contact info: `info_block` with `icon` (image_picker), `title` (text), `content` (richtext) — for address, email, phone.

- [ ] **Step 2: Create `page.contact.json`**

- [ ] **Step 3: Verify form submits, confirmation shows, contact info blocks editable**

- [ ] **Step 4: Commit**

```bash
git add theme/sections/contact-form.liquid theme/templates/page.contact.json
git commit -m "feat: add contact page with form and info blocks"
```

### Phase 7 QA Checkpoint

- [ ] **QA: Verify Phase 7 deliverables**

1. Our Story: hero section renders, split-view sections display with correct image positioning
2. Our Story: quote highlight section renders, all content editable in customizer
3. Our Story: founder can add/remove/reorder sections
4. Your Story: form submits successfully (check email/Shopify admin for submission)
5. Your Story: story grid displays metaobject entries
6. Your Story: clicking a story card opens modal with full content
7. Your Story: modal closes on X / click outside / Escape
8. Contact: form submits, success message shows
9. Contact: info blocks render with contact details
10. All pages: header/footer consistent, responsive layout works
11. No console errors

Fix, re-test, commit.

---

## Phase 8: Polish & Production Readiness

**Goal:** Responsive QA, accessibility, SEO, performance, final testing.
**Dependencies:** All previous phases complete.
**Can run in parallel:** Tasks 8.1-8.4 are largely independent.

### Task 8.1: Responsive QA Across All Pages

**Files:**
- Modify: Various CSS files as needed
- Modify: `theme/assets/base.css` (responsive adjustments)
- Reference: `html/css/responsive.css`

- [ ] **Step 1: Test every page at 5 breakpoints**

Test each page at: 375px (iPhone SE), 390px (iPhone 14), 768px (iPad), 1024px (iPad landscape), 1440px (laptop), 1920px (desktop).

Pages to test:
- Homepage
- Product page
- Collection page (Shop All)
- Cart page + drawer
- Our Story
- Your Story
- Contact

Document all layout issues.

- [ ] **Step 2: Fix responsive issues**

Port remaining responsive styles from `html/css/responsive.css`. Ensure:
- Mobile: single column layouts, stacked grids, hamburger menu
- Tablet: 2-column grids, reduced padding
- Desktop: full 4-column grids, mega menu, all desktop features

- [ ] **Step 3: Re-test all breakpoints after fixes**

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "fix: responsive layout adjustments across all pages"
```

### Task 8.2: Accessibility Audit

- [ ] **Step 1: Run automated accessibility checks**

Use Lighthouse or axe DevTools on every page. Target: 90+ accessibility score.

Key areas:
- All images have alt text
- All form inputs have labels
- Color contrast meets WCAG AA (4.5:1 for text)
- Focus indicators visible on all interactive elements
- Skip-to-content link works
- Keyboard navigation: mega menu, cart drawer, modals, accordions
- ARIA attributes correct on: dialogs, tabs (slideshow dots), expanded/collapsed (accordions)
- Screen reader: product variant selection announces changes

- [ ] **Step 2: Fix accessibility issues**

- [ ] **Step 3: Re-run audit, verify 90+ score**

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "fix: accessibility improvements for WCAG AA compliance"
```

### Task 8.3: SEO & Meta Tags

**Files:**
- Modify: `theme/snippets/meta-tags.liquid`
- Add: structured data (JSON-LD) for products and organization

- [ ] **Step 1: Ensure meta tags are complete**

- Title tags: unique per page, include shop name
- Meta descriptions: product description, collection description, page content
- Open Graph tags: og:title, og:description, og:image, og:url, og:type
- Twitter cards: twitter:card, twitter:title, twitter:description, twitter:image
- Canonical URLs

- [ ] **Step 2: Add JSON-LD structured data**

Product page:
```liquid
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": {{ product.title | json }},
  "image": {{ product.featured_image | image_url: width: 1200 | json }},
  "description": {{ product.description | strip_html | truncate: 200 | json }},
  "brand": { "@type": "Brand", "name": "Scents by Sara" },
  "offers": {
    "@type": "Offer",
    "price": {{ product.price | money_without_currency | json }},
    "priceCurrency": {{ cart.currency.iso_code | json }},
    "availability": "{% if product.available %}https://schema.org/InStock{% else %}https://schema.org/OutOfStock{% endif %}"
  }
}
</script>
```

- [ ] **Step 3: Verify with Google Rich Results Test**

- [ ] **Step 4: Commit**

```bash
git add theme/snippets/meta-tags.liquid
git commit -m "feat: add SEO meta tags and JSON-LD structured data"
```

### Task 8.4: Performance Optimization

- [ ] **Step 1: Audit with Lighthouse Performance**

Target: 80+ performance score on mobile.

Key optimizations:
- Lazy load all below-fold images (`loading="lazy"`)
- Eager load hero image and above-fold content
- Preload critical fonts (already in theme.liquid)
- Minimize render-blocking CSS (inline critical styles if needed)
- All JS loaded as `type="module"` (non-blocking by default)
- Image sizing: use Shopify's `image_url` with appropriate widths, `srcset` for responsive
- Avoid layout shift: set `aspect-ratio` on image containers

- [ ] **Step 2: Implement optimizations**

- [ ] **Step 3: Re-audit, verify 80+ mobile score**

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "perf: optimize images, fonts, and rendering performance"
```

### Task 8.5: Remaining Templates

**Files:**
- Create: `theme/templates/search.json` + `theme/sections/main-search.liquid`
- Create: `theme/templates/404.json` + `theme/sections/main-404.liquid`
- Create: `theme/templates/password.json` + `theme/layout/password.liquid`
- Create: `theme/templates/gift_card.liquid`
- Create: `theme/templates/page.json` + `theme/sections/main-page.liquid`
- Create: `theme/templates/blog.json` + `theme/templates/article.json` (placeholder)
- Create: `theme/templates/list-collections.json`

- [ ] **Step 1: Create search results template**

Simple grid of product cards matching collection layout. Uses `search.results` object.

- [ ] **Step 2: Create 404 page**

Branded 404 with message + "CONTINUE SHOPPING" CTA.

- [ ] **Step 3: Create password page**

Coming soon / password page with email signup and brand styling.

- [ ] **Step 4: Create gift card template**

Required by Shopify. Simple branded gift card display.

- [ ] **Step 5: Create generic page template**

For any pages the founder creates that don't have a custom template.

- [ ] **Step 6: Create blog/article templates (placeholder)**

Minimal templates for future use.

- [ ] **Step 7: Create list-collections template**

Grid of all collections.

- [ ] **Step 8: Commit**

```bash
git add theme/templates/ theme/sections/main-search.liquid theme/sections/main-404.liquid theme/sections/main-page.liquid theme/layout/password.liquid
git commit -m "feat: add remaining templates (search, 404, password, gift card, blog)"
```

### Task 8.6: Checkout Branding

> **Note:** `html/checkout.html` from the mockup is for visual reference only. On Shopify Basic plan, checkout is fully managed by Shopify — no custom Liquid templates. Customization is limited to branding (logo, colors, fonts) via admin settings. The multi-step progress bar (BAG → INFORMATION → SHIPPING → PAYMENT) exists natively in Shopify checkout.

- [ ] **Step 1: Configure checkout appearance in Shopify admin**

Go to Settings → Checkout → Customize checkout:
- Upload logo
- Set primary color to `#3F3229` (mocha)
- Set background color to `#F9F6F2` (sand)
- Set font to match brand (closest available)
- Add accent color `#A39382` (taupe)

- [ ] **Step 2: Screenshot and compare with brand guidelines**

### Task 8.7: Shopify Markets Configuration

- [ ] **Step 1: Configure 3 markets in Shopify admin**

Go to Settings → Markets:
- **Primary market: United Kingdom (GBP)**
- **International market 1: United Arab Emirates (AED)**
- **International market 2: United States (USD)**

- [ ] **Step 2: Verify currency selector in announcement bar works with all 3 markets**

- [ ] **Step 3: Verify prices display in correct currency per market**

### Phase 8 QA Checkpoint (Final)

- [ ] **QA: Final production readiness check**

1. All pages render correctly at all breakpoints (375px through 1920px)
2. Lighthouse accessibility: 90+ on all pages
3. Lighthouse performance: 80+ mobile on all pages
4. All forms submit correctly (contact, newsletter, story submission)
5. Cart flow: add to cart → drawer → cart page → checkout works end-to-end
6. Variant selection: all combinations work, out-of-stock handled gracefully
7. Filtering/sorting: works on all collection pages
8. Navigation: mega menu, mobile menu, search all work
9. Currency: GBP, USD, AED all display correctly
10. SEO: meta tags present, structured data validates
11. Theme customizer: founder can edit all content, images, colors, fonts
12. No console errors on any page
13. All Shopify-required templates present (gift_card, 404, password, search)
14. Checkout: branded with logo, colors, fonts

---

## Dependency Graph

```
Phase 1 (Foundation)
  ├── Task 1.1 (Move HTML) ──┐
  └── Task 1.2 (Clone Skeleton) ──┤
                                   ├── Task 1.3 (Settings Schema) → Task 1.4 (Token Snippets) → Task 1.5 (Base CSS) → Task 1.6 (Layout) → Task 1.7 (Component JS)
                                   │
Phase 2 (Global Sections) ────────┘
  ├── Task 2.1 (Announcement Bar) ─────────────────────────────────────────┐
  ├── Task 2.2 (Header) → Task 2.3 (Mega Menu) → Task 2.4 (Mobile Menu) → Task 2.5 (Search) ──┤
  └── Task 2.6 (Footer) ──────────────────────────────────────────────────┤
                                                                           │
Phase 3 (Homepage) ←───────────────────────────────────────────────────────┘
  ├── Task 3.1 (Hero Slideshow) ──────┐
  ├── Task 3.2 (Product Card + Featured Collection) ──┤  (all can run in parallel)
  ├── Task 3.3 (Commitment) ──────────┤
  ├── Task 3.4 (Collections Grid) ────┤
  ├── Task 3.5 (Split-View) ──────────┤
  └── Task 3.6 (Testimonials) ────────┤
                                       └── Task 3.7 (Compose index.json)

Phase 4 (Product) ←── Phase 3 (product-card.liquid needed)
  ├── Task 4.1 (Gallery) → Task 4.2 (Variant Picker) → Task 4.3 (Accordions)
  ├── Task 4.4 (Scents + Commitment) ──┤  (independent after 4.1-4.3)
  ├── Task 4.5 (Recommendations + Reviews) ──┤
  └── Task 4.6 (Breadcrumbs) ──────────┤

Phase 5 (Collections) ←── Phase 3 (product-card.liquid needed) [CAN RUN PARALLEL WITH PHASE 4]
  ├── Task 5.1 (Main Collection) → Task 5.2 (Filtering/Sorting)
  └── Task 5.3 (Gifts Template)

Phase 6 (Cart) ←── Phase 4 Task 4.2 (add-to-cart form) [CAN RUN PARALLEL WITH PHASE 5]
  └── Task 6.1 (Cart Drawer) → Task 6.2 (Cart Page)

Phase 7 (Static Pages) ←── Phase 2 (header/footer), Phase 3 Task 3.5 (split-view)
  ├── Task 7.1 (Our Story) ──┐
  ├── Task 7.2 (Your Story) ──┤  (all can run in parallel)
  └── Task 7.3 (Contact) ─────┘

Phase 8 (Polish) ←── All phases complete
  ├── Task 8.1 (Responsive QA) ──┐
  ├── Task 8.2 (Accessibility) ──┤  (all can run in parallel)
  ├── Task 8.3 (SEO) ────────────┤
  ├── Task 8.4 (Performance) ────┤
  ├── Task 8.5 (Remaining Templates) ──┤
  └── Task 8.6 (Checkout) + Task 8.7 (Markets) ──── Final QA
```

## Parallel Execution Summary

| Slot | Agent A | Agent B | Agent C |
|------|---------|---------|---------|
| 1 | Phase 1: Task 1.1 (Move HTML) | Phase 1: Task 1.2 (Clone Skeleton) | - |
| 2 | Phase 1: Tasks 1.3-1.8 (sequential) | - | - |
| 3 | Phase 2: Tasks 2.2-2.5 (Header chain + Search) | Phase 2: Task 2.1 (Announcement) | Phase 2: Task 2.6 (Footer) |
| 4 | Phase 3: Task 3.1 (Hero) | Phase 3: Task 3.2 (Product Card) | Phase 3: Tasks 3.3-3.6 (other sections) |
| 5 | Phase 4: Tasks 4.1-4.3 (Product core) | Phase 5: Tasks 5.1-5.2 (Collections) | Phase 7: Tasks 7.1-7.3 (Static Pages) |
| 6 | Phase 4: Tasks 4.4-4.6 (Product extras) | Phase 5: Task 5.3 (Gifts/sub-collections) | - |
| 7 | Phase 6: Tasks 6.1-6.2 (Cart) | - | - |
| 8 | Phase 8: Tasks 8.1-8.7 (Polish — split across agents) | | |

## QA Process (Applied at Every Phase)

```
Test → Verify → Fix → Re-Test → Commit
```

1. **Test**: Run through the QA checklist for the phase
2. **Verify**: Cross-reference with HTML mockup in `/html` — visual match?
3. **Fix**: Address all issues found
4. **Re-Test**: Run the full QA checklist again
5. **Commit**: Only commit when all checks pass

## Commit Strategy

- Commit after every completed task (not just phases)
- Commit message format: `type: description` (feat/fix/chore/perf)
- Phase completion commits include QA fixes
- Never commit broken code — always verify theme loads without errors first
