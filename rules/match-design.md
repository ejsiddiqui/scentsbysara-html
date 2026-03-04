# Match Design Guidelines

## 1. Implementation Philosophy
The design assets provided (`home-page.png`, `shop-page.png`, etc.) are the unyielding source of truth. As a senior engineer, your job is not to interpret the design into a framework, but to engineer the browser to exactly replicate the design artifact using fluid, responsive logic.

## 2. Measurement Standards
When matching a static `.png` or `.jpeg` design reference:

### Establishing the Base
1. Identify the container width of the screenshot (often `1440px`, `1720px`, or `1920px`).
2. Identify the outermost gutters. For Scents by Sara, standard desktop gutters are locked to `100px`.
3. If a screenshot deviates (e.g., using `64px` gutters), the layout system must programmatically accommodate the page-specific exception without breaking global defaults.

### Extracting Spatial Relationships
- Look at the whitespace between the H1 to the subtext. Is it tight? Is it loose? Translate this to the nearest `--space-*` token (e.g., `--space-md` or `16px`).
- Never arbitrarily set a padding without comparing its vertical impact against the screenshot's spatial rhythm.

## 3. The "Overlay Method"
To guarantee a match design:
1. Build the structure in HTML/CSS.
2. In the browser (via tools or an integrated testing overlay), place the provided `.png` asset at `50%` opacity directly over your implementation.
3. Compare the "bleed". If text, borders, or images ghost outside the reference lines, the design is not matched.
4. Correct the CSS `padding`, `margin`, or `gap` until the ghosting is eradicated.

## 4. Constraint Handling
- **Do:** Use `min-height`, `aspect-ratio`, and `object-fit: cover` to ensure images perfectly match the proportions of the reference, regardless of the intrinsic image size loaded from the server.
- **Don't:** Force fixed heights on text-bearing elements. Use `padding` and allowing the content to dictate flow while matching the visual volume.

## 5. Visual Hierarchy Match
Verify that font weights (`font-weight: 300, 400, 500`) exactly match the perceived boldness in the design. Often an image will render a `400` weight as seemingly bolder; rely on the `typography-system.md` to establish the closest technical truth.
