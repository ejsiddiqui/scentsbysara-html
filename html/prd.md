# PRD — Homepage Design (Scents by Sara)

Design the homepage for **Scents by Sara**, a premium body-shape scented candle brand rooted in scent science, female empowerment, and wellness rituals.

This homepage must look and feel like a calm, editorial luxury e-commerce experience inspired by:

- Aesop  
- Jo Malone  
- Neom  

**Language Preference** For language and spellings, we will use British English.

Launch target: **March 2026**  
Audience: wellness-focused, design-conscious women aged **20–50**

---

## ✅ Brand System Reference (Required)

All design and UI decisions must strictly follow:

➡️ **brand-guidelines.md**

This includes:

- Typography rules  
- Colour palette usage  
- Button styling (radius 0)  
- Layout grid system  
- Iconography rules  
- Hero photography direction  

No component should deviate from these guidelines.

---

### Superseding Layout Directives (Authoritative)

These directives supersede all previous layout instructions in this PRD and other project docs wherever conflicts exist.

0. All screenshots in `references/sections/` are captured from the `1920px` design baseline.All other breakpoints must be responsive adaptations of this baseline.
1. Add `1920px` as the wide desktop layout breakpoint.
2. For view-ports above `1920px`, the page behaves as a boxed layout.
3. The layout is section-based. Each section behaves as a row.
4. Each section has a default design width of `1920px`, while still supporting `width: 100%`.
5. Default container width is `1800px` with `60px` left and right margins inside the section.
6. The `.container` width for `1920px` above screens should be `1920px`.
7. `.container-full` is a full-width container (`100%`) with no side margins.

---

## Design Reference

1- Design reference for each page section by section is available in `references/sections/<page-name>`. e.g. Design reference for `home` page can be found in `references/sections/home` dir.
2- Images to be used are available in `assets/images/` dir.
Note: All screenshots have been taken on `1920px` view-port, so that they should be adjusted for other screen sizes.

---

## Overall Aesthetic

- Clean, minimalist luxury layout with generous whitespace.
- Calm, slow, sensory feel — never loud or overly commercial.
- Warm neutral backgrounds (avoid pure white).
- Base palette must use the official brand tones:

  - `#F9F6F2` (Soft Cream background)
  - `#E8E4DD` (Warm Light Grey sections)
  - `#CFC6B9` (Borders/dividers)
  - `#3F3229` (Primary text)
  - `#2D2B27` (dark text)

See **brand-guidelines.md → Colour System**.

---

## Typography (Strict)

Typography must match the brand system:

### Headlines

- RL Limo Regular (serif)
- Used for hero titles, section headings, ritual statements

### Body + UI

- Suisse Intl Regular (sans-serif)
- Used for navigation, labels, product cards, buttons

See **brand-guidelines.md → Typography System**.

---

## Layout Rules

- `1920px` is the primary desktop reference breakpoint.
- Use section rows as structural layout units.
- Each section must support `width: 100%` with a `1920px` design baseline.
- Default content container:
  - width: `1800px`
  - side margins: `60px` each (inside a `1920px` section)
- For viewport widths above `1920px`, keep content boxed and centered. With `.container` max-width `1920px`.
- Use `.container-full` for intentionally full-bleed content with no side margins.

Whitespace and spacing are core to the brand.

See **brand-guidelines.md → Layout & Grid**.

---

## Common Sections

---

### Small Hero Section

- Usually a `380px` high in desktop
- It has a heading (tokens: --text-t1, --text-on-dark), and body text (tokens: --text-h3, --text-on-dark)
- Full-bleed warm editorial photography used as a background-image.
- Reference hero image `references/body-candles/1-hero.png`

### Button Rules

- Border radius MUST be `0`
- Primary background: `--bg-primary-dark`

See **brand-guidelines.md → Buttons & Interactions**.

---

## Navigation & Header

Top header includes:

- Subtle announcement bar:
  “Launching March 2026”

Main nav:

- Shop  
- Gifts
- Our Story
- Your Story  
- Contact Us

Right side icons:

- Account  
- Wishlist  
- Cart  

Left side icons:

- Search

### Iconography Rule

- Use provided svg icons
- If icon not available, use Lucide icons
  - Size: 24px
  - Stroke: 1px
  - Colour: `#3F3229`

See **brand-guidelines.md → Iconography**.

Sticky header on scroll with reduced height.

## Mobile Navigation

- For screens `1024px` and below, the mobile navigation is displayed and main nav is hidden.

---

## Coding Style (Important)

- The code should be modular and reusable
- Try to use the already created css/classes instead of writing new css
- Many sections are repeating on different pages, try to reuse the same structure and css.
- Write new css only, if is not already covered in other classes
- For font-size, font-color, background-color etc use design tokens instead of writing raw values
- Use qa-guardrails skills to verify the design
- The design must be tested and verified before committing

## Future Considerations

Homepage should leave modular space for:

- AI Scent Advisor teaser (“Find Your Ritual Scent”)
- Future wellness categories (diffusers, fragrances)

Components must remain modular and reusable.

---

## Product Detail Page — `product.html`

All design decisions must adhere to `brand-guidelines.md`. The product page must match `screenshots/product-page.png`.

---

## Page Structure

---

### Breadcrumb

- Uppercase, Suisse Intl, 0.78rem
- Path: `SHOP / BODY CANDLES / [Product Name]`
- Primary colour `--text-primary` with hover to full primary

---

### Product Gallery + Form (2-column split)

#### Left — Gallery

- Large main product image (aspect ratio 3:4)
- Wishlist/heart icon top-right of main image
- 3 or more thumbnail images below in a row, use left/right slider if more images
- Clicking a thumbnail swaps the main image with a fade transition
- Gallery is `position: sticky` on desktop (top: 140px to clear header)

#### Right — Product Form

- Subtitle (small uppercase): "Stretch Mark Body Candle" (tokens: --text-body-large, --text-primary-dark)
- Product title (RL Limo serif, uppercase): "She Is Lust" (tokens: --text-h1, --text-primary-dark)
- Price: e.g. "£20.20" (tokens: --text-body-large, --font-sans, font-weight:300)

**Colour selector:**

- Label: `COLOUR: [Active Colour]`
- 3 circular colour swatches (Caramel / Chestnut / Ivory)
- Active swatch: ring outline

**Body Shape selector:**

- Label: `BODY SHAPE: [Active Size]`
- Toggle buttons: Slim / Curvy / Plus Size
- Active button: secondary colour fill with primary-text color (`--bg-secondary`, `--text-primary`)

**Scent selector:**

- Label: `SCENT: [Active Scent]`
- Toggle buttons: Vanilla / Lavender
- Design token same as `Body Shape` selector

**Quantity + CTA row:**

- `-` / number input / `+` stepper (min 1, max 99)
- "Add to Bag — £[price]" primary CTA button (full flex-fill)
- CTA label updates dynamically when qty changes
- On click: button shows "✓ Added to Bag" for 1.8s then reverts

**Accordions** (below divider, one open at a time):

Following tabs would be shown in accordion except `Description`, description would be above Accordion. However, visually it would be like accordion below. By default, all tabs would be closed.

Tokens: Heading (tokens: --text-body, --text-primary-dark, font-weight: 600), text: --text-body, --text-primary-dark.

- Description: (Above Accordion)
- Craft & Intention
- How to Use
- Dimensions & Ingredients

Accordion trigger: uppercase label + `+` icon (rotates 45° when open).  
Panel animates open via `max-height` transition.

---

### Scents Section

- Section heading: "SCENTS" (standard section headings, reuse, tokens: --text-h2, --text-primary-dark)
- Use background-images, no text overlay

---

### Commitment Split

Same structure as homepage commitment section:

- Left: full-height image (`assets/images/our-commitment-left.png`)
- Right: eyebrow + heading + intro copy + credentials list

**Credentials:**

- Vegan
- Paraben-Free
- Phthalate-Free
- IFRA-Certified

---

### You May Also Like

This section is same `Best Sellers` section on homepage. So reuse the home page layout/css, while having content from this page.

---

### Reviews

- Heading: "WHAT OUR CUSTOMERS ARE SAYING" (standard section heading)
- 3-column review card grid
- Each card:
  - Reviewer name + location
  - Star rating (text label + star glyphs)
  - Review title (uppercase)
  - Purchase metadata line (scent/size/colour)
  - Review body copy (italic)
- Pagination row (← 1/1 →) below the grid

---

## Responsive Behaviour

| Breakpoint | Change |
|---|---|
| ≤ 1024px | Product section stacks (gallery above form) |
| ≤ 768px | Reviews grid stacks to 1 column |

---

## Files

| File | Role |
|---|---|
| `product.html` | Complete product detail page HTML |
| `styles/product.css` | All product-page-specific CSS |
| `scripts/product.js` | Gallery swap, swatches, toggles, qty stepper, accordion |

---

End of PRD

## Implementation Notes (2026-03-01)

- Added dedicated route templates and styling for `our-story.html` (`assets/css/our-story.css`) and `contact.html` (`assets/css/contact.css`).
- Added shared commerce persistence via `assets/js/cart-state.js` and flow-specific modules (`cart.js`, `checkout.js`).
- Added shared form validation for story/contact flows via `assets/js/forms.js`.
- Checkout now uses a focused checkout footer layout rather than the heavy global newsletter/footer block.
