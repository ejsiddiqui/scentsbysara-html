# Layout System Architecture

This file governs the strict CSS Grid and layout constraints for Scents by Sara Phase V2.

## 1. Global Width Enforcements

Modern layouts fluidly scale, but must respect hard ceilings to maintain premium editorial readability.

- **Section Max Width (`1920px`)**
  - All `<section>` wrappers or `<div>` backgrounds that stretch full-screen must max out here.
  - If a screen is `2560px` wide, the `1920px` wrapper must center itself using `margin: 0 auto;`.
- **Content Max Width (`1720px`)**
  - Inside a section, content grids and wrapping text max out at `1720px`. The inner container acts as the bounding box.
- **Side Spacing (`100px`)**
  - Left and right gutters must be strictly enforced at `100px` for all desktop resolutions `>= 1024px`.
  - Token reference: `padding: 0 var(--gutter-desk, 100px);`

## 2. CSS Architecture & Structure

Layout logic is heavily reliant on CSS Grid to avoid complex nested Flexbox math.

### The Standard Grid Setup
```css
.container {
  max-width: 1720px;
  margin: 0 auto;
  padding: 0 var(--gutter-desk, 100px);
}

/* 4-Column Product Grids */
.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-md, 16px);
}

/* 50/50 Split Editorial Sections */
.split-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center; /* Adjust based on reference top/middle alignment */
}
```

## 3. Do's and Don'ts
- **Do:** Enforce layout at the parent `container` level. Components inside should take `100%` of their allocated grid cell.
- **Don't:** Apply left/right margin to individual cards or buttons to create layout structures.
- **Do:** Use `gap` for internal spacing between sibling items in a grid or flex flex layout.
- **Don't:** Rely on pseudo-selectors or nested float clear hacks for layout control.

## 4. Header & Overflow Controls
- **Header Max Height:** `130px`. The site content below the header must account for this fixed real-estate when anchored or sticky.
- **Horizontal Overflow:** `overflow-x: hidden` must be permanently applied to the global `body` or `.site-wrapper` to prevent mobile grid blow-outs from causing side scrolling.
