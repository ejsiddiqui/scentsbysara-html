# PRD — Homepage Design (Scents by Sara)

Design the homepage for **Scents by Sara**, a premium body-shape scented candle brand rooted in scent science, female empowerment, and wellness rituals.

This homepage must look and feel like a calm, editorial luxury ecommerce experience inspired by:

- Aesop  
- Jo Malone  
- Neom  

Launch target: **March 2026**  
Audience: wellness-focused, design-conscious women aged **20–50**

---

# ✅ Brand System Reference (Required)

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

## Overall Aesthetic

- Clean, minimalist luxury layout with generous whitespace.
- Calm, slow, sensory feel — never loud or overly commercial.
- Warm neutral backgrounds (avoid pure white).
- Base palette must use the official brand tones:

  - `#F9F6F2` (Soft Cream background)
  - `#E8E4DD` (Warm Light Grey sections)
  - `#CFC6B9` (Borders/dividers)
  - `#3F3229` (Primary text)
  - `#2D2B27` (CTA buttons)

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

- Use Tailwind CSS **12-column grid** throughout
- Max width container: `max-w-7xl`
- Generous padding: `px-6` to `px-8`

Whitespace and spacing are core to the brand.

See **brand-guidelines.md → Layout & Grid**.

---

# Homepage Structure

---

## Hero Section (Above the Fold)

- Must be a slider with **3 slides**
- Full-bleed warm editorial photography (body-shape candles)
- Reference hero images are placed in /references dir

Hero overlay content:

- Serif headline (RL Limo):
  “HAND MADE BESPOKE CANDLES”
- Short supporting line:
  “Rooted in sensory science, emotional wellbeing, and confidence.”
- Primary CTA button:
  “Shop Body Candles”
- Secondary CTA:
  “Explore Rituals”

### Button Rules
- Border radius MUST be `0`
- Primary background: `#2D2B27`

See **brand-guidelines.md → Buttons & Interactions**.

---

## Navigation & Header

Top header includes:

- Subtle announcement bar:
  “Launching March 2026”

Main nav:

- Shop  
- Collections  
- Rituals  
- Our Story  
- Contact  

Right side icons:

- Account  
- Wishlist  
- Cart  

### Iconography Rule
Use Lucide icons only:

- Size: 24px
- Stroke: 1px
- Colour: `#3F3229`

See **brand-guidelines.md → Iconography**.

Sticky header on scroll with reduced height.

---

# Homepage Sections (In Order)

---

## 1. Bestsellers Strip

- Horizontal row of 3–4 products
- Each card includes:

  - Product image
  - Name + price
  - Quick View or Add to Cart CTA

Hover interaction should be minimal:

- Slight lift or gentle opacity shift

No rounded corners.

---

## 2. Brand Story / Founder Moment

Split editorial block:

- Image: founder ritual moment
- Text: scent science + empowerment

Add serif pull quote for warmth.

CTA: “Discover Our Story”

Typography must follow brand guidelines exactly.

---

## 3. Collections Overview

Grid or carousel featuring:

- Body Candles  
- Plus Size  
- 24K Gold Candles  
- Custom Candles  

Each card includes:

- Atmospheric image
- Collection name (serif)
- One-line ritual description (sans-serif)
- CTA: Shop Collection

---

## 4. Rituals & Wellbeing Content Teaser

Editorial content blocks such as:

- Rituals for Confidence  
- Evening Unwind  
- Morning Reset  

Calm copy + warm lifestyle imagery.

CTA: Explore Rituals

---

## 5. Sensory Science / Scent Story Section

Quiet infographic-style layout:

3–4 points:

- Clean formulations  
- Mood-support scent science  
- Handmade + cruelty-free  
- Eco-conscious rituals  

Use Lucide icons (1px stroke).

Avoid busy visuals.

---

## 6. Testimonials / Social Proof

Horizontal slider of reviews:

- Refined typography
- Minimal framing
- Calm emotional language

Optional: “Loved by our community”

---

## 7. Newsletter & Community Block

Headline example:

- “Join the Ritual”
- “Stay in the Scent Circle”

One-line invite + email form.

Background may use subtle warmth (no strong gradients).

Primary button uses brand CTA styling.

---

## 8. Footer

Three-column layout:

Left:
- FAQs
- Candle Care
- Shipping
- Returns
- Privacy
- Terms

Center:
- Social Lucide icons (IG, TikTok, Pinterest)

Right:
- Minimal newsletter signup

Bottom row:
- Logo + payment icons (subtle)

---

# Product & Interaction Details

Product cards must include:

- Variant indication (wax tones, sizes)
- Minimal hover state
- Clean CTA path to:

  - Shop All  
  - Custom Candle page  

All mobile layouts stack gracefully.

---

# Tone of Voice

Copy must be:

- Calm
- Warm
- Confident
- Empathetic

Focus on feelings:

- Grounded
- Confident
- Soft rituals

Avoid aggressive marketing language.

---

# Future Considerations

Homepage should leave modular space for:

- AI Scent Advisor teaser (“Find Your Ritual Scent”)
- Future wellness categories (diffusers, fragrances)

Components must remain modular and reusable.

---

# Product Detail Page — `product.html`

All design decisions must adhere to `brand-guidelines.md`. The product page must match `screenshots/product-page.png`.

---

## Page Structure

---

### Breadcrumb

- Uppercase, Suisse Intl, 0.78rem
- Path: `SHOP / BODY CANDLES / [Product Name]`
- Muted colour `rgba(63,50,41, 0.55)` with hover to full primary

---

### Product Gallery + Form (2-column split)

**Left — Gallery**

- Large main product image (aspect ratio 3:4)
- Wishlist/heart icon top-right of main image
- 3 thumbnail images below in a row
- Clicking a thumbnail swaps the main image with a fade transition
- Gallery is `position: sticky` on desktop (top: 140px to clear header)

**Right — Product Form**

- Subtitle (small uppercase): "Stretch Mark Body Candle"
- Product title (RL Limo serif, uppercase): "She Is Lust"
- Price: e.g. "£20.20"
- Horizontal divider

**Colour selector:**
- Label: `COLOUR: [Active Colour]`
- 3 circular colour swatches (Caramel / Chestnut / Ivory)
- Active swatch: ring outline

**Size selector:**
- Label: `BODY SHAPE / PLUS SIZE`
- Toggle buttons: Slim / Curvy / Plus Size
- Active button: dark fill (`#2D2B27`), inverse text

**Scent selector:**
- Label: `SCENT: [Active Scent]`
- Toggle buttons: Vanilla / Lavender

**Quantity + CTA row:**
- `-` / number input / `+` stepper (min 1, max 99)
- "Add to Bag — £[price]" dark CTA button (full flex-fill)
- CTA label updates dynamically when qty changes
- On click: button shows "✓ Added to Bag" for 1.8s then reverts

**Accordions** (below divider, one open at a time):
- Description
- Craft & Intention
- How to Use
- Dimensions & Ingredients

Accordion trigger: uppercase label + `+` icon (rotates 45° when open).  
Panel animates open via `max-height` transition.

---

### Scents Section

- Section heading: "SCENTS" (centred, RL Limo)
- 2 full-bleed editorial photo cards side by side, no gap:
  - **Vanilla** — warm image, text overlay (scent name + Top Notes / Heart / Base Notes)
  - **Lavender** — floral image, same overlay structure
- Image dims to ~60% brightness to support text legibility
- Hover: subtle image zoom + slight extra dimming

---

### Commitment Split

Same structure as homepage commitment section:
- Left: full-height image (`our-commitment-left.png`)
- Right: eyebrow + heading + intro copy + credentials list

**Credentials:**
- Vegan
- Paraben-Free
- Phthalate-Free
- IFRA-Certified

Each credential is separated by a subtle hairline border.

---

### You May Also Like

- Heading: "YOU MAY ALSO LIKE" (centred, RL Limo)
- 4-column product grid reusing `.products-grid` and `.product-card`
- Each card: image, product name, sub-label, price, "Shop Now" outline CTA

---

### Reviews

- Heading: "WHAT OUR CUSTOMERS ARE SAYING" (centred, RL Limo)
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
| ≤ 768px | Product section stacks (gallery above form) |
| ≤ 768px | Scents grid stacks to 1 column |
| ≤ 768px | Reviews grid stacks to 1 column |
| ≤ 640px | Add to Bag stretches full width |
| ≤ 640px | Size toggles wrap |

---

## Files

| File | Role |
|---|---|
| `product.html` | Complete product detail page HTML |
| `styles/product.css` | All product-page-specific CSS |
| `scripts/product.js` | Gallery swap, swatches, toggles, qty stepper, accordion |

---

End of PRD
