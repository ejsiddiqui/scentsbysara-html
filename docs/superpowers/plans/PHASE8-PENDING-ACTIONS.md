# Phase 8 — Pending Actions

> **As of 2026-03-26.** Phases 1–7 are complete. Phase 8 code-implementable work is done.
> The following items require either a live Shopify dev store or Shopify admin access.

---

## A. Requires Live Shopify Dev Store

Run `shopify theme dev --store=scentsbysara-dev.myshopify.com` first, then:

### Task 8.1: Responsive QA
Test every page at these breakpoints: **375px, 390px, 768px, 1024px, 1440px, 1920px**

Pages to test:
- [ ] Homepage
- [ ] Product page
- [ ] Collection page (Shop All)
- [ ] Cart page + drawer
- [ ] Our Story
- [ ] Your Story
- [ ] Contact
- [ ] Search results
- [ ] 404 page

Fix any layout issues, then run `shopify theme check` and fix all lint errors.

### Task 8.2: Accessibility Audit
Run Lighthouse or axe DevTools on every page. Target: **90+ accessibility score**.

Checklist:
- [ ] All images have alt text
- [ ] All form inputs have labels
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Focus indicators visible on all interactive elements
- [ ] Skip-to-content link works
- [ ] Keyboard navigation: mega menu, cart drawer, modals, accordions
- [ ] Screen reader: variant selection announces price/availability changes
- [ ] ARIA attributes correct: dialogs (`aria-modal`, `aria-labelledby`), carousels, accordions

> Note: `aria-modal="true"` has been added to cart drawer, search modal, and mobile menu dialogs as of 2026-03-26.

### Task 8.3: SEO Verification
- [ ] Verify with Google Rich Results Test (product JSON-LD structured data)
- URL to test: your Shopify dev store product page URL

### Task 8.4: Performance Optimization
Run Lighthouse Performance on mobile. Target: **80+ score**.

- [ ] Run audit on homepage, product page, collection page
- [ ] Confirm all below-fold images are `loading="lazy"`
- [ ] Confirm hero/first product image is `loading="eager"` with `fetchpriority="high"`
- [ ] Confirm fonts are preloaded (already in `theme.liquid`)
- [ ] Check for layout shift (CLS) — image containers should have `aspect-ratio`
- [ ] Run `shopify theme check` — fix any warnings

---

## B. Requires Shopify Admin Access

### Task 8.6: Checkout Branding
Go to: **Shopify Admin → Settings → Checkout → Customize**

- [ ] Upload logo (use the long horizontal version)
- [ ] Set primary color: `#3F3229` (Mocha)
- [ ] Set background color: `#F9F6F2` (Sand)
- [ ] Set accent color: `#A39382` (Taupe)
- [ ] Set font to match brand (closest available to Suisse Int'l)
- [ ] Screenshot and compare with brand guidelines

### Task 8.7: Shopify Markets Configuration
Go to: **Shopify Admin → Settings → Markets**

- [ ] Configure Primary market: **United Kingdom (GBP)**
- [ ] Add International market 1: **United Arab Emirates (AED)**
- [ ] Add International market 2: **United States (USD)**
- [ ] Test currency selector in announcement bar shows all 3 options
- [ ] Test prices display in correct currency when market is switched

---

## C. Final Production QA Checklist

Once all above tasks are complete:

- [ ] All pages render correctly at all breakpoints (375px → 1920px)
- [ ] Lighthouse accessibility: 90+ on all pages
- [ ] Lighthouse performance: 80+ mobile on all pages
- [ ] All forms submit correctly (contact, newsletter, story submission)
- [ ] Cart flow: add to cart → drawer → cart page → checkout works end-to-end
- [ ] Variant selection: all combinations work, out-of-stock handled gracefully
- [ ] Filtering/sorting: works on all collection pages
- [ ] Navigation: mega menu, mobile menu, search all work
- [ ] Currency: GBP, USD, AED all display correctly
- [ ] SEO: meta tags present, structured data validates
- [ ] Theme customizer: founder can edit all content, images, colors, fonts
- [ ] No console errors on any page
- [ ] All Shopify-required templates present (gift_card, 404, password, search) ✅
- [ ] Checkout: branded with logo, colors, fonts

---

## Code Changes Made in Phase 8 (2026-03-26)

The following code fixes were implemented:

| File | Change |
|---|---|
| `theme/assets/base.css` | Added `.visually-hidden` utility class (used by `search-modal.liquid`) |
| `theme/snippets/cart-drawer.liquid` | Added `aria-modal="true"` and `aria-labelledby="cart-drawer-title"` to dialog |
| `theme/snippets/search-modal.liquid` | Added `aria-modal="true"` and `aria-label` to dialog |
| `theme/sections/header.liquid` | Added `aria-modal="true"` and `aria-label` to mobile menu dialog |
| `theme/sections/main-product.liquid` | Added `aria-live="polite"` and `aria-atomic="true"` to price region |
