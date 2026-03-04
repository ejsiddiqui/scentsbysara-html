# Responsive System Rulebook

This file dictates precisely how layout matrices transform under pressure across varied device sizes.

## 1. Base Breakpoints Setup

- **Large Desktop (`>= 1440px`)**: The default target. All split layouts (`1fr 1fr`) exist here perfectly. The `100px` gutter rules supreme.
- **Tablet Landscape (`1024px`)**: The critical pivoting threshold. Here, the desktop header (`nav-links`) collapses into the Mobile Hamburger Menu structure. Gutters compress slightly (`48px`).
- **Tablet Portrait (`768px`)**: Complex grids shatter. 4-column product displays collapse to 2 columns.
- **Mobile (`<= 767px`)**: Structural realignment. Gutters compress to `20px`. The 1440px split hero reorganizes to stack vertically (Text top, image bottom).

### Writing Media Queries
Use desktop-down Max-Width parameters.
```css
/* Standard Desktop Logic Base */
.product-grid { grid-template-columns: repeat(4, 1fr); }

/* Tablet Pivot */
@media (max-width: 1024px) {
  .product-grid { grid-template-columns: repeat(3, 1fr); }
  .header-nav { display: none; } /* Switch to hamburger */
}

/* Base Mobile Structure */
@media (max-width: 768px) {
  .product-grid { grid-template-columns: repeat(2, 1fr); }
  .split-hero { grid-template-columns: 1fr; }
}
```

## 2. Touch Target Enforcement (Mobile)
Mobile elements require spatial confidence.
- Every button, hamburger menu icon, cart icon, or clickable UI facet must maintain a minimum physical touch target bound of `44px by 44px`.
- E.g.: `.nav-icons .btn { width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; }`

## 3. Horizontal Scroll Prohibition
The mobile web must never break its horizontal container.
Apply `max-width: 100vw; overflow-x: hidden;` to the outermost page wrapper shell, ensuring runaway grid elements or absolute positioning doesn't shatter the viewport bound.

## 4. Typography Shifting
Body copy (`16px`) stays intact, but Hero / H1 headers must gracefully shrink.
Ensure `clamp()` formulas bottom out no lower than `32px` for H1 scaling, so `.ys-hero-title` doesn't become illegible on mobile devices.
