# Brand Guidelines & Design System

## 1. Brand Overview

**Aesthetic:** Quiet Luxury, Artisanal, Minimalist, Sensory.
**Core Vibe:** Clean lines, generous negative space, editorial typography, and earth-toned natural palettes.
**Reference Style:** Similar to Aesop, Jo Malone, Melyon.

---

## 2. Asset Directory

**Logo:**

* **File Path:** `/images/logo.svg`
* **Placement:** Centered in Navbar (Desktop), or Top-Left (Mobile).

**Iconography:**

* **SVG Icons** Use provided svg icons
* **Lucide Icons** If svg icon is not available, use Lucide icons
* **Library:** [Lucide Icons](https://lucide.dev/)
* **Settings:** Stroke width `1px`, Size `24px`.
* **Color:** Inherits text color (`#3F3229`).

---

## 3. Typography

The type system relies on a contrast between an editorial Serif (RL Limo) and a utilitarian Sans-Serif (Suisse Int'l).

### Primary Typeface (Headings)

**Font Name:** `RL Limo`
**Source:** Adobe Typekit
**Import Tag:**

```html
<link rel="stylesheet" href="[https://use.typekit.net/ife0byt.css](https://use.typekit.net/ife0byt.css)">

```

**CSS Usage:**

```css
h1, h2, h3, .serif-display {
  font-family: rl-limo, sans-serif;
  font-weight: 400;
  font-style: normal;
}

```

### Secondary Typeface (Body/UI)

**Font Name:** `Suisse Int'l`
**Source:** Local Files
**File Path:** `/assets/fonts/SuisseIntl-Regular.woff2`

**CSS Usage:**

```css
@font-face {
  font-family: "Suisse Intl";
  src: url("/assets/fonts/SuisseIntl-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
}

body, button, input, .sans-ui {
  font-family: "Suisse Intl", sans-serif;
  font-weight: 400;
}

```

### Type Scale (Desktop)

* **H1 (Hero):** 4rem (64px) / Line-height: 1.1 / Font: `rl-limo`
* **H2 (Section):** 2.5rem (40px) / Line-height: 1.2 / Font: `rl-limo`
* **H3 (Product Title):** 1.5rem (24px) / Line-height: 1.3 / Font: `rl-limo`
* **Body (Base):** 1rem (16px) / Line-height: 1.6 / Font: `Suisse Intl`
* **Label/Button:** 0.875rem (14px) / Uppercase / Tracking: 0.05em / Font: `Suisse Intl`

---

## 4. Colour Palette & Theme

### Primitive Hex Codes

* **Cream Light:** `#F9F6F2` (Main Background)
* **Cream Medium:** `#E8E4DD` (Cards / Secondary Background)
* **Beige Warm:** `#CFC6B9` (Buttons / Borders)
* **Taupe:** `#A49483` (Muted Text)
* **Brown Dark:** `#3F3229` (Primary Text / Hover Backgrounds)
* **Charcoal:** `#2D2B27` (Strong Accents / Footer)

### CSS Variables (Root)

```css
:root {
  /* Backgrounds */
  --bg-surface: #F9F6F2;
  --bg-secondary: #E8E4DD;
  
  /* Text */
  --text-primary: #3F3229;
  --text-secondary: #A49483;
  --text-inverse: #F9F6F2;

  /* UI Elements */
  --border-color: #CFC6B9;
  --btn-bg-default: #CFC6B9;
  --btn-text-default: #3F3229;
  --btn-bg-hover: #3F3229;
  --btn-text-hover: #F9F6F2;
}

```

---

## 5. UI Components

### A. Buttons (Primary CTA)

**Shape:** Sharp rectangular corners (`border-radius: 0px`) or Micro-radius (`2px`).
**Typography:** Uppercase, 14px, Wide tracking (`0.05em`).

**States:**

| State      | Background             | Text Color              |
| ---------- | ---------------------- | ----------------------- |
| **Normal** | `#CFC6B9` (Beige Warm) | `#3F3229` (Brown Dark)  |
| **Hover**  | `#3F3229` (Brown Dark) | `#F9F6F2` (Cream Light) |

**CSS Reference:**

```css
.btn-primary {
  background-color: var(--btn-bg-default);
  color: var(--btn-text-default);
  padding: 12px 24px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 14px;
  border: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: var(--btn-bg-hover);
  color: var(--btn-text-hover);
}

```

### B. Layout & Spacing

* **Grid:** 12-column grid system.
* **Max Width:** `1440px`.
* **Section Spacing:** Generous whitespace. `py-20` (approx 80px-100px) between sections.
* **Element Spacing:** `24px` gap is standard for cards and grids.

### C. Product Cards

* **Aspect Ratio:** Images should be 4:5 or 1:1.
* **Style:** Clean, minimal. Image takes precedence.
* **Text Align:** Left aligned or Centered.
* **Background:** Transparent or `#F9F6F2`.
* **Details:** Title (Serif) + Scent/Variant (Sans-serif Muted) + Price (Sans-serif).

### D. Navigation

* **Position:** Fixed/Sticky or Static.
* **Background:** Transparent on Hero, `#F9F6F2` on scroll.
* **Links:** Uppercase, `Suisse Intl`, 12-13px.

---

## 6. Imagery Style Guide

* **Lighting:** Natural, soft shadows, warm undertones.
* **Props:** Organic materials (wood, stone, linen, dried flora).
* **Composition:** Minimalist. Single object focus.
* **Avoid:** Harsh neon colors, clutter, pure white (`#FFFFFF`) backgrounds (use `#F9F6F2` instead).
