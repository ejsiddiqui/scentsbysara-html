# Product Card 3-Tier System

**Date:** 2026-03-27
**Status:** Approved

## Overview

Introduce three named card layout tiers for the Shopify theme's `product-card` snippet. Each tier targets a specific placement context and is selectable via Shopify Admin section settings. Typography, swatch sizing, and responsive behaviour are standardised across all tiers.

---

## Layout Tiers

| Value | Tier | Admin Label | Used In |
|---|---|---|---|
| `stacked` | Tier 1 | Full / Stacked | Body Candle Homepage, Shop by Size |
| `shop` | Tier 2 | Shop / Collection | Collection & Shop All pages |
| `compact` | Tier 3 | Compact / Carousel | Bestsellers Carousel, You May Also Like |

### Tier 1 — `stacked`
- **Structure:** image → swatches row → centered body (title · subtitle · price) → SHOP NOW button
- **Swatches:** colour swatches only, no shape/size selector
- **Mobile (≤480px):** body left-aligned; SHOP NOW button hidden

### Tier 2 — `shop`
- **Structure:** [shape select + swatches] row → body (title left · price right; subtitle below title) → SHOP NOW button
- **Shape selector:** native `<select>` rendered for the first non-colour product option (e.g. Shape). Hidden if no such option exists.
- **Variant data:** all variant IDs and their option values embedded as `data-variants` JSON on `<product-card>`. On `change`, JS finds the best-matching variant (matching shape + current active colour, falls back to first available with that shape) and navigates to its URL.
- **Mobile (≤480px):** SHOP NOW button hidden

### Tier 3 — `compact`
- **Structure:** [swatches only] row → body (title left · price right; subtitle below title) → SHOP NOW button
- **No shape selector** — colour swatches only, even if the product has non-colour options
- **Mobile (≤480px):** SHOP NOW button hidden

---

## Typography

All values use Suisse Int'l (already loaded as `var(--font-sans)`).

| Element | Font Size | Weight | Letter Spacing |
|---|---|---|---|
| Product title (`.product-card__title`) | 16px | 400 (Regular) | — |
| Price (`.product-card .price__current`) | 16px | 400 (Regular) | — |
| Short description (`.product-card__subtitle`) | 14px | 300 (Light) | — |
| SHOP NOW button (`.product-card__button`) | 14px | 300 (Light) | 0.1em (10%) |

---

## Swatches

- Size: **30×30px** (width and height)
- Applied as a CSS override scoped to `.product-card` so it does not affect global swatch settings
- Border included within the 30px dimension (existing `border: 1px solid var(--color-border)` unchanged)

---

## Responsive Behaviour (≤480px)

| Rule | Effect |
|---|---|
| `.product-card__button { display: none }` | SHOP NOW button hidden on all tiers |
| `.product-card--stacked .product-card__body { text-align: left }` | Tier 1 body left-aligned (desktop is centered) |
| `.product-card--stacked .product-price { align-items: flex-start; text-align: left }` | Tier 1 price left-aligned |

---

## Files Changed

### 1. `theme/snippets/product-card.liquid`
- Add `compact` layout block (mirrors `shop` body structure, omits shape select)
- Add shape `<select>` in `shop` layout block, conditional on product having non-colour options
- Embed variant JSON as `data-variants` on `<product-card>` for `shop` layout: `[{ id, url, options: [string] }]` per variant

### 2. `theme/assets/product-card.js`
- Add `change` event listener for `.product-card__option-select`
- On change: parse `data-variants` JSON, find best-matching variant, navigate to its URL and update active swatch state

### 3. `theme/sections/featured-collection.liquid`
- **Schema:** add `compact` option to `card_layout` select
- **CSS `{% stylesheet %}`:** add typography rules, 30px swatch override, responsive rules, `compact` layout CSS

### 4. `theme/sections/main-collection.liquid`
- **Schema:** add `card_layout` select setting (options: stacked / shop / compact; default: `shop`)
- **Liquid:** replace hardcoded `card_layout: 'shop'` with `card_layout: section.settings.card_layout`

### 5. `theme/sections/product-recommendations.liquid`
- **Schema:** add `card_layout` select setting (options: stacked / shop / compact; default: `stacked`)
- **Liquid:** replace hardcoded `card_layout: 'stacked'` with `card_layout: section.settings.card_layout`

---

## CSS Changes (detail)

Added to `featured-collection.liquid` `{% stylesheet %}`:

```css
/* Typography */
.product-card__title,
.product-card__title a {
  font-size: 16px;
  font-weight: 400;
}

.product-card__subtitle {
  font-size: 14px;
  font-weight: 300;
}

.product-card .price__current {
  font-size: 16px;
  font-weight: 400;
}

.product-card__button {
  font-size: 14px;
  font-weight: 300;
  letter-spacing: 0.1em;
}

/* Swatch size override (scoped to card) */
.product-card .variant-swatches__swatch {
  width: 30px;
  height: 30px;
}

/* Compact layout body (same as shop) */
.product-card--compact .product-card__body {
  align-items: flex-start;
  justify-content: space-between;
}

.product-card--compact .product-price {
  align-items: flex-end;
  text-align: right;
}

/* Shape select styling */
.product-card__option-select {
  appearance: none;
  border: 1px solid var(--color-border);
  background: transparent;
  padding: 6px 24px 6px 8px;
  font-family: var(--font-sans);
  font-size: 13px;
  font-weight: 300;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  cursor: pointer;
  background-image: linear-gradient(45deg, transparent 50%, currentColor 50%),
    linear-gradient(135deg, currentColor 50%, transparent 50%);
  background-position: calc(100% - 10px) calc(50% - 1px), calc(100% - 6px) calc(50% - 1px);
  background-size: 4px 4px, 4px 4px;
  background-repeat: no-repeat;
}

/* Mobile */
@media (max-width: 480px) {
  .product-card__button { display: none; }
  .product-card--stacked .product-card__body { text-align: left; }
  .product-card--stacked .product-price { align-items: flex-start; text-align: left; }
}
```

---

## Shape Select — Liquid Structure (Tier 2)

```liquid
{%- for option in card_product.options_with_values -%}
  {%- assign opt_down = option.name | downcase -%}
  {%- unless opt_down contains 'colour' or opt_down contains 'color' -%}
    <select class="product-card__option-select" data-product-card-option="{{ option.name | downcase }}">
      {%- for value in option.values -%}
        <option
          value="{{ value | escape }}"
          {% if current_variant.options[forloop.parentloop.index0] == value %}selected{% endif %}
        >{{ option.name | upcase }}: {{ value | upcase }}</option>
      {%- endfor -%}
    </select>
  {%- endunless -%}
{%- endfor -%}
```

## Shape Select — JS Logic

```js
// In ProductCard.onConnect():
this.optionSelects = Array.from(this.querySelectorAll('[data-product-card-option]'));
this.variants = JSON.parse(this.dataset.variants || '[]');

this.handleOptionChange = (event) => {
  const select = event.target.closest('[data-product-card-option]');
  if (!select) return;
  const optionName = select.dataset.productCardOption;
  const selectedValue = select.value;
  const activeSwatchValue = this.querySelector('.variant-swatches__swatch.is-active')
    ?.dataset.swatchValue?.toLowerCase();

  // Find best variant: matching shape + current colour, or first with shape
  const match = this.variants.find((v) => {
    const options = v.options.map((o) => o.toLowerCase());
    const hasShape = options.includes(selectedValue.toLowerCase());
    const hasColour = activeSwatchValue ? options.includes(activeSwatchValue) : true;
    return hasShape && hasColour;
  }) || this.variants.find((v) =>
    v.options.map((o) => o.toLowerCase()).includes(selectedValue.toLowerCase())
  );

  if (match?.url) window.location.assign(match.url);
};

this.addEventListener('change', this.handleOptionChange);
```

---

## Out of Scope

- No changes to swatch global settings_schema default (30px applied via CSS override only)
- No changes to `variant-swatches.liquid` or `variant-picker.liquid`
- No new CSS files — all product card CSS remains in `featured-collection.liquid` stylesheet block
