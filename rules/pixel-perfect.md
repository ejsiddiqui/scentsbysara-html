# Pixel Perfect Standards & Rules

## 1. Definition of "Pixel Perfect"
"Pixel Perfect" in this project signifies a **zero-tolerance threshold for layout and structural deviations** when comparing implemented HTML/CSS against the authorized design imagery.
- Elements must structurally mirror reference dimensions, typography, spacing, and relational flow exactly.
- A 1-2px organic anti-aliasing text rendering difference across browsers is acceptable; however, structural logic, alignment grids, padding ratios, container boundaries, and background colors must be exact.

## 2. Rule Enforcement
- **Do:** Extract specific hexadecimal codes, font sizes, and layout constraints systematically using the defined Token Structure.
- **Do:** Utilize CSS custom properties (`var(--token)`) for all measurements and colors.
- **Don't:** "Eyeball" distances.
- **Don't:** Implement arbitrary "magic numbers" (e.g., `margin-top: 31px;`). You must use defined spacing constants natively built into the `spacing-system.md` parameters.
- **Don't:** Invent UI elements or hover states that do not exist or strictly align with the `interaction-rules.md`.

## 3. Visual Verification Checklist
Every page component must undergo this mental check before moving to QA verification:
- [ ] Do bounding boxes of text exact-match the reference?
- [ ] Is the left-side gutter alignment completely flush down the page?
- [ ] Is the hero minimum height properly calculated based on the reference imagery cropping?
- [ ] Does the font weight scale properly according to the reference? (E.g., `500` vs `400`).
- [ ] Are buttons the exact correct padding and font-letter-spacing?

## 4. Code Discipline Standards
- **Naming Conventions:** Class names must be semantic, component-based, and heavily structured to prevent CSS collisions. E.g., `.site-header`, `.ys-community-grid`, `.card-desc`.
- **CSS Precedence:** Do not use `!`important as a band-aid. Fix specificity conflicts structurally.
- **DOM Depth:** Keep HTML shallow. Avoid unneeded wrapper `div`s.

## 5. Border-Radius Rules
- **Rule:** The Scents by Sara visual identity is rooted in sharp, premium editorial aesthetics.
- **Enforcement:** `border-radius: 0px` is the absolute rule for all UI elements—inputs, buttons, cards, imagery containers, and modals.
- **Exception:** Only use masking rounded elements if explicitly drawn as such in a very specific editorial layout within a provided asset.

## 6. Container & Baseline Widths
- **Header Max Height:** `130px`.
- **Section Max Width (Full Bleed):** `1920px`.
- **Content Max Width (Text/Grid Bounds):** `1720px`.
- **Gutter Rule:** Side spacing on large desktops must be rigorously locked to `100px`.
