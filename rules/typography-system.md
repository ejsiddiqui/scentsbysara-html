# Typography System Architecture

This document enforces the strict font usage for the Scents by Sara UI.

## 1. Typeface Enforcement
There are exactly two approved typefaces for this project.

- **Primary Typeface:** `RL Limo` (Regular). 
  - Usage: H1, H2, H3, Hero Headings, pull quotes, `.mega-menu` primary titles.
  - Fallback: `Georgia, serif` (if font fails to load).
  
- **Secondary Typeface:** `Suisse Int'l` (Regular).
  - Usage: Body copy (`<p>`), tiny navigation links, buttons, meta-data (pricing), functional inputs.
  - Fallback: `Helvetica, Arial, sans-serif`.

### Crucial Prohibition
Do not use italic variations of `RL Limo` or `Suisse Int'l` unless explicitly present in the design screenshot. Almost all text is set to `font-style: normal`. Use tracking (letter-spacing) in buttons, not italics.

## 2. Typographic Scale Strategy
The system must be fluidly responsive across breakpoints. Do not hardcode `px` font sizes for headings. Use CSS clamp() functions.

- **Hero & Display (`var(--text-hero)`)**
  - Bound: `clamp(2.5rem, 5vw + 1rem, 4rem)`. Massive impact, sharp serif display.
- **H1 Header (`var(--text-primary)`)**
  - Bound: `clamp(2rem, 4vw, 3rem)`. Used for "Hand Made Bespoke Candles" level emphasis.
- **H2 Header (`var(--text-secondary)`)**
  - Bound: `clamp(1.5rem, 3vw, 2.25rem)`. Used for "Best Sellers" sections.
- **Micro Type (`var(--text-micro)`)**
  - Fixed: `0.75rem` (12px) or `0.6875rem` (11px). Extremely tracked out (`letter-spacing: 0.1em; text-transform: uppercase`). Used for "Customer Testimonials" labels or author attribution.

## 3. Paragraph Formatting & Rhythm
- The optimal line length for body copy is ~60 characters. Use `max-width` on paragraphs (e.g., `max-width: 560px;`) rather than letting text flow endlessly across `1440px`.
- Line-height must be strictly:
  - `1.1` to `1.2` for `RL Limo` Headings to keep descenders tight.
  - `1.5` to `1.8` for `Suisse Int'l` Body text for premium readability and breathing room.
