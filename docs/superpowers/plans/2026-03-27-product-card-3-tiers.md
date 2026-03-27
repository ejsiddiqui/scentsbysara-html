# Product Card 3-Tier System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `compact` third layout tier to product cards, update all card typography to use design tokens, and make the card layout selectable per-section in Shopify Admin.

**Architecture:** All product card CSS lives in a single `{% stylesheet %}` block in `featured-collection.liquid` — this is where all visual changes land. The `product-card.liquid` snippet handles layout branching via `card_layout` parameter. A new `--text-body-small` token is added to `design-tokens.liquid` to fill the 14px gap in the type scale.

**Tech Stack:** Shopify Liquid, CSS custom properties (design tokens), vanilla JS (Web Component pattern)

**Spec:** `docs/superpowers/specs/2026-03-27-product-card-3-tiers-design.md`

---

## File Map

| File | Action | What changes |
|---|---|---|
| `theme/snippets/design-tokens.liquid` | Modify | Add `--text-body-small: 14px` token |
| `theme/snippets/product-card.liquid` | Modify | Add `compact` layout branch; add shape `<select>` + variant JSON to `shop` branch |
| `theme/assets/product-card.js` | Modify | Add `change` handler for shape select; parse variant JSON for navigation |
| `theme/sections/featured-collection.liquid` | Modify | CSS: typography tokens, swatch override, compact styles, shape select styles, mobile rules. Schema: add `compact` to `card_layout` options |
| `theme/sections/main-collection.liquid` | Modify | Schema: add `card_layout` select. Liquid: use `section.settings.card_layout` |
| `theme/sections/product-recommendations.liquid` | Modify | Schema: add `card_layout` select. Liquid: use `section.settings.card_layout` |

---

## Task 1: Add `--text-body-small` design token

**Files:**
- Modify: `theme/snippets/design-tokens.liquid` (line 80–81)

- [ ] **Step 1: Add the token**

In `theme/snippets/design-tokens.liquid`, find the type scale block and add `--text-body-small` between `--text-body` and `--text-small`:

```liquid
  --text-body: {{ settings.body_font_size | default: 16 }}px;
  --text-body-small: 14px;
  --text-small: 13px;
```

- [ ] **Step 2: Verify the token resolves**

In browser DevTools on any page with `shopify theme dev` running, run:

```js
getComputedStyle(document.documentElement).getPropertyValue('--text-body-small').trim()
// Expected: "14px"
```

- [ ] **Step 3: Commit**

```bash
git add theme/snippets/design-tokens.liquid
git commit -m "feat: add --text-body-small 14px design token"
```

---

## Task 2: Add CSS — typography, swatches, compact layout, shape select, mobile

**Files:**
- Modify: `theme/sections/featured-collection.liquid` (inside `{% stylesheet %}` block, before `{% endstylesheet %}`)

- [ ] **Step 1: Add all new CSS rules**

Inside the `{% stylesheet %}` block in `featured-collection.liquid`, add the following before the closing `{% endstylesheet %}` tag (currently at line 349):

```css
  /* ── Product card: typography ────────────────────────── */
  .product-card__title,
  .product-card__title a {
    font-size: var(--text-body);
    font-weight: 400;
    line-height: 1.15;
  }

  .product-card__subtitle {
    font-size: var(--text-body-small);
    font-weight: 300;
    color: var(--color-muted);
  }

  .product-card .price__current {
    font-size: var(--text-body);
    font-weight: 400;
  }

  .product-card__button {
    font-size: var(--text-body-small);
    font-weight: 300;
    letter-spacing: 0.1em;
  }

  /* ── Product card: swatch size override ──────────────── */
  .product-card {
    --swatch-size: 30px;
  }

  /* ── Compact layout (Tier 3) ─────────────────────────── */
  .product-card--compact .product-card__body {
    align-items: flex-start;
    justify-content: space-between;
  }

  .product-card--compact .product-price {
    align-items: flex-end;
    flex: 0 0 auto;
    text-align: right;
  }

  /* ── Shape select (Tier 2 shop layout) ───────────────── */
  .product-card__option-select {
    appearance: none;
    border: 1px solid var(--color-border);
    background: transparent;
    padding: var(--space-xs) calc(var(--space-md) + var(--space-sm)) var(--space-xs) var(--space-sm);
    font-family: var(--font-sans);
    font-size: var(--text-small);
    font-weight: 300;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    cursor: pointer;
    background-image:
      linear-gradient(45deg, transparent 50%, currentColor 50%),
      linear-gradient(135deg, currentColor 50%, transparent 50%);
    background-position:
      calc(100% - 10px) calc(50% - 1px),
      calc(100% - 6px) calc(50% - 1px);
    background-size: 4px 4px, 4px 4px;
    background-repeat: no-repeat;
  }

  /* ── Mobile (≤480px) ─────────────────────────────────── */
  @media (max-width: 480px) {
    .product-card__button {
      display: none;
    }

    .product-card--stacked .product-card__body {
      text-align: left;
    }

    .product-card--stacked .product-price {
      align-items: flex-start;
      text-align: left;
    }
  }
```

- [ ] **Step 2: Verify CSS is applied**

With `shopify theme dev` running, open a page with product cards. In DevTools:
- Inspect `.product-card__title` → computed `font-size` should be `16px`, `font-weight` `400`
- Inspect `.product-card__subtitle` → computed `font-size` should be `14px`, `font-weight` `300`
- Inspect `.variant-swatches__swatch` inside a `.product-card` → `width` and `height` should be `30px`

- [ ] **Step 3: Commit**

```bash
git add theme/sections/featured-collection.liquid
git commit -m "feat: update product card CSS — typography tokens, 30px swatches, compact layout, mobile rules"
```

---

## Task 3: Add `compact` option to featured-collection schema

**Files:**
- Modify: `theme/sections/featured-collection.liquid` (schema block, `card_layout` setting)

- [ ] **Step 1: Update the schema**

Find the `card_layout` select in the `{% schema %}` block (around line 409) and replace it:

```json
{
  "type": "select",
  "id": "card_layout",
  "label": "Card layout",
  "default": "stacked",
  "options": [
    {
      "value": "stacked",
      "label": "Full / Stacked"
    },
    {
      "value": "shop",
      "label": "Shop / Collection"
    },
    {
      "value": "compact",
      "label": "Compact / Carousel"
    }
  ]
},
```

- [ ] **Step 2: Verify in Shopify Admin**

Open the theme editor → click any **Featured collection** section → confirm the **Card layout** dropdown shows three options: "Full / Stacked", "Shop / Collection", "Compact / Carousel".

- [ ] **Step 3: Commit**

```bash
git add theme/sections/featured-collection.liquid
git commit -m "feat: add compact option to featured-collection card_layout schema"
```

---

## Task 4: Add compact layout + shape select to product-card.liquid

**Files:**
- Modify: `theme/snippets/product-card.liquid`

- [ ] **Step 1: Add variant JSON capture for shop layout**

After the closing `-%}` of the liquid block (after line 44), add a variant JSON capture scoped to the `shop` layout:

```liquid
{%- if card_layout == 'shop' -%}
  {%- capture card_variants_json -%}
    [{%- for v in card_product.variants -%}
      {"id":{{ v.id }},"url":"{{ card_product.url }}?variant={{ v.id }}","options":{{ v.options | json }}}
      {%- unless forloop.last -%},{%- endunless -%}
    {%- endfor -%}]
  {%- endcapture -%}
{%- endif -%}
```

- [ ] **Step 2: Add `data-variants` attribute to the `<product-card>` element**

The `<product-card>` opening tag (lines 47–54) currently ends at `data-card-image-ratio`. Add one conditional attribute:

```liquid
{%- if card_product != blank -%}
  <product-card
    class="product-card product-card--{{ card_layout }}{% if card_product.available == false %} is-sold-out{% endif %}"
    data-product-card
    data-product-card-id="{{ card_product.id }}"
    data-product-url="{{ card_product.url }}"
    data-card-layout="{{ card_layout }}"
    data-card-image-ratio="{{ image_ratio }}"
    {%- if card_layout == 'shop' -%}data-variants='{{ card_variants_json | strip }}'{%- endif -%}
  >
```

- [ ] **Step 3: Replace the shop/stacked if-else with a three-branch if/elsif/else**

Replace lines 99–139 (the `{%- if card_layout == 'shop' -%} … {%- endif -%}` block) with:

```liquid
    {%- if card_layout == 'shop' -%}
      <div class="product-options product-card__options">
        {%- for option in card_product.options_with_values -%}
          {%- assign opt_down = option.name | downcase -%}
          {%- unless opt_down contains 'colour' or opt_down contains 'color' -%}
            <select
              class="product-card__option-select"
              data-product-card-option="{{ option.name | downcase }}"
            >
              {%- for value in option.values -%}
                <option
                  value="{{ value | escape }}"
                  {%- if current_variant.options[forloop.parentloop.index0] == value %} selected{%- endif -%}
                >{{ option.name | upcase }}: {{ value | upcase }}</option>
              {%- endfor -%}
            </select>
          {%- endunless -%}
        {%- endfor -%}
        {%- if show_swatches -%}
          {% render 'variant-swatches', product: card_product, variant: current_variant %}
        {%- endif -%}
      </div>

      <div class="product-info-shop product-card__body">
        <div class="product-card__copy">
          <span class="product-name product-card__title">
            <a href="{{ card_product.url }}">{{ card_product.title | escape }}</a>
          </span>

          {%- if subtitle != blank -%}
            <span class="product-desc product-card__subtitle">{{ subtitle | escape }}</span>
          {%- endif -%}
        </div>

        {% render 'price', product: card_product, variant: current_variant %}
      </div>

    {%- elsif card_layout == 'compact' -%}
      {%- if show_swatches -%}
        <div class="product-options product-card__options">
          {% render 'variant-swatches', product: card_product, variant: current_variant %}
        </div>
      {%- endif -%}

      <div class="product-info-shop product-card__body">
        <div class="product-card__copy">
          <span class="product-name product-card__title">
            <a href="{{ card_product.url }}">{{ card_product.title | escape }}</a>
          </span>

          {%- if subtitle != blank -%}
            <span class="product-desc product-card__subtitle">{{ subtitle | escape }}</span>
          {%- endif -%}
        </div>

        {% render 'price', product: card_product, variant: current_variant %}
      </div>

    {%- else -%}
      <div class="product-info-stacked product-card__body">
        <div class="product-card__copy">
          <span class="product-name product-card__title">
            <a href="{{ card_product.url }}">{{ card_product.title | escape }}</a>
          </span>

          {%- if subtitle != blank -%}
            <span class="product-desc product-card__subtitle">{{ subtitle | escape }}</span>
          {%- endif -%}
        </div>

        {% render 'price', product: card_product, variant: current_variant %}
      </div>

      {%- if show_swatches -%}
        <div class="product-options product-card__options">
          {% render 'variant-swatches', product: card_product, variant: current_variant %}
        </div>
      {%- endif -%}
    {%- endif -%}
```

- [ ] **Step 4: Verify the three layouts render correctly**

With `shopify theme dev` running:
- **Tier 1 (`stacked`):** Visit a page using the featured-collection set to "Full / Stacked". Confirm: swatches below image, body centered, SHOP NOW button visible.
- **Tier 2 (`shop`):** Set a section to "Shop / Collection". On a product with a Shape option, confirm the shape `<select>` appears above swatches. On a product with only colour options, confirm no `<select>` appears.
- **Tier 3 (`compact`):** Set a section to "Compact / Carousel". Confirm only colour swatches appear (no shape select) and the body layout matches Tier 2 (inline title/price).

- [ ] **Step 5: Commit**

```bash
git add theme/snippets/product-card.liquid
git commit -m "feat: add compact layout and shop shape selector to product-card snippet"
```

---

## Task 5: Add shape select JS handler to product-card.js

**Files:**
- Modify: `theme/assets/product-card.js`

- [ ] **Step 1: Add variant parsing and option select handler in `onConnect()`**

Add the following lines at the end of `onConnect()`, after the existing `this.addEventListener('click', this.handleClick)` line:

```js
    // Shape / option select handler (shop layout only)
    this.variants = [];
    try {
      this.variants = JSON.parse(this.dataset.variants || '[]');
    } catch (_) {
      this.variants = [];
    }

    this.handleOptionChange = (event) => {
      const select = event.target.closest('[data-product-card-option]');
      if (!select || !this.contains(select)) return;

      const selectedValue = select.value.toLowerCase();
      const activeSwatchValue = this.querySelector('.variant-swatches__swatch.is-active')
        ?.dataset.swatchValue?.toLowerCase();

      // Prefer variant matching both shape and current colour; fall back to first with matching shape
      const match =
        this.variants.find((v) => {
          const opts = v.options.map((o) => o.toLowerCase());
          return opts.includes(selectedValue) && (activeSwatchValue ? opts.includes(activeSwatchValue) : true);
        }) ||
        this.variants.find((v) =>
          v.options.map((o) => o.toLowerCase()).includes(selectedValue)
        );

      if (match?.url) window.location.assign(match.url);
    };

    this.addEventListener('change', this.handleOptionChange);
```

- [ ] **Step 2: Remove the listener in `onDisconnect()`**

Add to `onDisconnect()` after the existing `removeEventListener` calls:

```js
    this.removeEventListener('change', this.handleOptionChange);
```

- [ ] **Step 3: Verify shape select navigation**

With `shopify theme dev` running, open a collection page (Tier 2 / shop layout) on a product that has a Shape option (e.g. "She Is Strength" with Plus Size / Regular shapes). Change the shape select — the page should navigate to the matching variant URL.

Inspect the `<product-card>` element in DevTools — `data-variants` should contain a valid JSON array of `{ id, url, options }` objects.

- [ ] **Step 4: Commit**

```bash
git add theme/assets/product-card.js
git commit -m "feat: add shape select variant navigation to product-card component"
```

---

## Task 6: Make card layout configurable in main-collection

**Files:**
- Modify: `theme/sections/main-collection.liquid`

- [ ] **Step 1: Add `card_layout` setting to schema**

In the `{% schema %}` block (after line 263), add the `card_layout` setting after the `columns_desktop` range setting:

```json
    {
      "type": "select",
      "id": "card_layout",
      "label": "Card layout",
      "default": "shop",
      "options": [
        {
          "value": "stacked",
          "label": "Full / Stacked"
        },
        {
          "value": "shop",
          "label": "Shop / Collection"
        },
        {
          "value": "compact",
          "label": "Compact / Carousel"
        }
      ]
    },
```

- [ ] **Step 2: Use the setting in the product-card render call**

At line 196–202, replace the hardcoded `card_layout: 'shop'`:

```liquid
            {% render 'product-card',
              product: product,
              card_layout: section.settings.card_layout,
              show_secondary_image: true,
              show_swatches: true,
              show_quick_add: false
            %}
```

- [ ] **Step 3: Verify in Shopify Admin**

Open the theme editor → click the **Main collection** section → confirm a **Card layout** dropdown appears with three options, defaulting to "Shop / Collection".

- [ ] **Step 4: Commit**

```bash
git add theme/sections/main-collection.liquid
git commit -m "feat: make card layout configurable in main-collection section"
```

---

## Task 7: Make card layout configurable in product-recommendations

**Files:**
- Modify: `theme/sections/product-recommendations.liquid`

- [ ] **Step 1: Add `card_layout` setting to schema**

In the `{% schema %}` block (around line 107), add after the `products_to_show` range setting:

```json
    {
      "type": "select",
      "id": "card_layout",
      "label": "Card layout",
      "default": "stacked",
      "options": [
        {
          "value": "stacked",
          "label": "Full / Stacked"
        },
        {
          "value": "shop",
          "label": "Shop / Collection"
        },
        {
          "value": "compact",
          "label": "Compact / Carousel"
        }
      ]
    },
```

- [ ] **Step 2: Use the setting in the product-card render call**

At line 22–28, replace the hardcoded `card_layout: 'stacked'`:

```liquid
          {% render 'product-card',
            product: product,
            card_layout: section.settings.card_layout,
            show_secondary_image: true,
            show_swatches: true,
            show_quick_add: false
          %}
```

- [ ] **Step 3: Verify in Shopify Admin**

Open the theme editor on a product page → click the **Product recommendations** section → confirm a **Card layout** dropdown appears defaulting to "Full / Stacked".

- [ ] **Step 4: Commit**

```bash
git add theme/sections/product-recommendations.liquid
git commit -m "feat: make card layout configurable in product-recommendations section"
```

---

## Self-Review Checklist (run before handing off)

- [ ] All 3 layout tiers render without errors (stacked, shop, compact)
- [ ] `--text-body-small` resolves to `14px` in DevTools
- [ ] Product card `--swatch-size` overrides to `30px` (swatches measure 30×30px in DevTools box model)
- [ ] Shape select appears in `shop` layout only on products with non-colour options; absent on colour-only products
- [ ] Changing shape select navigates to correct variant URL
- [ ] `compact` layout shows colour swatches only — no shape select
- [ ] SHOP NOW button hidden at ≤480px viewport on all three tiers
- [ ] Tier 1 body is left-aligned at ≤480px
- [ ] `card_layout` dropdown present in Shopify Admin for: featured-collection, main-collection, product-recommendations
