# Color System Enforcement

This document enforces color fidelity and programmatic extraction of hex values. All hex values must derive from the provided `brand-guideline.md` and no other external references.

## 1. The Scents by Sara Master Palette

### Light Mode UI / Neutrals

- **SBS White Sand:** `#F9F6F2`
  - *Usage:* Primary page backgrounds (`.page-wrapper`). Bright but slightly warm.
- **SBS Neutral Stone:** `#E7E3DC`
  - *Usage:* Card backgrounds (`.site-footer`, `.bc-feature`). Creates soft separation from White Sand without needing drop shadows.
- **SBS Soft Clay:** `#CEC5B8`
  - *Usage:* Deepest light-mode neutral. Used for footer blocks or bold UI structural bounding logic.

### Muted Elements & Text

- **SBS Nude Taupe:** `#A39382`
  - *Usage:* Muted text (`.text-muted`), input placeholders, inactive states, secondary pricing descriptors.

### High Contrast & Dominant Elements

- **SBS Warm Mocha:** `#3F3229`
  - *Usage:* Main body font color (`--text-primary`). This is the default text color if nothing is mentioned. Primary solid button backgrounds (`.btn-solid`)
- **SBS Black Slate:** `#2D2B27`
  - *Usage:* The primary dark text color (`--text-primary-dark`). Usually used in text-color to have high emphasis.

## 2. CSS Variable Construction

Never use raw hex codes directly in CSS logic. Build a token map.

```css
:root {
  --color-sand: #F9F6F2;
  --color-stone: #E7E3DC;
  --color-clay: #CEC5B8;
  --color-taupe: #A39382;
  --color-mocha: #3F3229;
  --color-slate: #2D2B27;

  /* Semantic Aliases */
  --bg-primary: var(--color-sand);
  --bg-secondary: var(--color-stone);
  --bg-tertiary: var(--color-clay);
  --text-primary: var(--color-mocha);
  --text-primary-dark: var(--color-slate);
  --text-muted: var(--color-taupe);
  --border-primary: var(--color-clay);
  --btn-bg-primary: var(--color-mocha);
  --btn-bg-secondary: var(--color-taupe)
}
```

## 3. Strict Prohibitions

- **Do not** introduce "pure black" `#000000` or "pure white" `#FFFFFF`. The brand depends entirely on its soft, earthy off-tones.
- **Do not** use raw RGB/HSL transparency layers (like `rgba(0,0,0,0.5)`) over the entire site unless strictly doing a hero-background text legibility gradient (`linear-gradient(rgba(45, 43, 39, 0.4), ...)`, referencing `SBS Black Slate` logic).
