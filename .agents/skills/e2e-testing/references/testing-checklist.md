# E2E Testing Coverage Checklist

Use this checklist to ensure complete test coverage across all pages and user journeys.

## Page-Level Coverage

### Homepage (index.html)
- [ ] Page loads with correct title
- [ ] Logo visible
- [ ] Navigation links present (Shop, Gifts, Collections, etc.)
- [ ] Hero section: headline visible, Shop Now CTA → shop.html
- [ ] Best Sellers: 4 product cards rendered
- [ ] Product card CTAs → product.html
- [ ] Collections section visible
- [ ] Collection Discover Now CTAs → shop.html
- [ ] Mega-menu opens on Shop hover
- [ ] Mega-menu links point to correct targets
- [ ] Newsletter signup form visible
- [ ] Footer visible with correct links
- [ ] Full-page screenshot captured

### Shop Page (shop.html)
- [ ] Page loads with correct title
- [ ] "Shop All" heading visible
- [ ] Filter button visible
- [ ] Sort select visible with expected options (Featured, Price: Low to High, etc.)
- [ ] 6 product cards rendered
- [ ] All Shop Now buttons → product.html
- [ ] Filter panel opens on click
- [ ] Filter panel closes on second click
- [ ] Size chip filtering hides non-matching cards
- [ ] "All" chip resets filter
- [ ] Sort changes card order
- [ ] Screenshots captured (default, filter open, filter active)

### Product Page (product.html)
- [ ] Page loads with correct title
- [ ] Breadcrumb: Home → index.html, Body Candles → shop.html
- [ ] Product gallery main image visible
- [ ] Gallery thumbnail swap works (click thumb → main image changes)
- [ ] Product title correct ("She Is Lust")
- [ ] Add to Bag button shows price (£)
- [ ] Quantity stepper: plus updates price
- [ ] Quantity stepper: minus updates price (minimum 1)
- [ ] Accordion opens on click (aria-expanded toggles)
- [ ] Accordion closes on second click
- [ ] You May Also Like section visible
- [ ] You May Also Like cards → product.html
- [ ] Full-page screenshot captured

### Cart Page (cart.html)
- [ ] Page loads with correct title
- [ ] Cart items display correctly
- [ ] Quantity update works
- [ ] Item removal works
- [ ] Subtotal/total calculations correct
- [ ] Checkout CTA → checkout.html
- [ ] Empty cart state displays correctly

### Checkout Page (checkout.html)
- [ ] Page loads with correct title
- [ ] Form fields visible (name, email, address, payment)
- [ ] Form validation works (empty fields, invalid email)
- [ ] Order summary visible
- [ ] Place Order button present

### Your Story Page (your-story.html)
- [ ] Page loads with correct title
- [ ] Content sections visible
- [ ] Images load correctly
- [ ] Navigation back to homepage works

---

## Cross-Page Journey Coverage

### Primary Purchase Flow
- [ ] Homepage → Shop (hero CTA)
- [ ] Shop → Product (Shop Now card)
- [ ] Product → Cart (Add to Bag)
- [ ] Cart → Checkout (Checkout CTA)

### Navigation Journeys
- [ ] Mega-menu → Shop page
- [ ] Breadcrumb Product → Shop → Home
- [ ] Footer links navigate correctly
- [ ] Logo click → Homepage from any page

### Filter & Sort Journey
- [ ] Shop: Apply filter → verify cards hidden
- [ ] Shop: Change sort → verify order changes
- [ ] Shop: Reset filter → verify all cards shown
- [ ] Shop: Filter + sort combined

---

## Interaction Coverage

### Hover States
- [ ] Mega-menu hover open/close
- [ ] Button hover effects
- [ ] Product card hover effects
- [ ] Navigation link hover states

### Click Interactions
- [ ] Accordion open/close
- [ ] Gallery thumbnail swap
- [ ] Quantity stepper (+/-)
- [ ] Filter panel toggle
- [ ] Filter chip selection
- [ ] Add to Bag
- [ ] Cart item quantity update
- [ ] Cart item removal

### Form Interactions
- [ ] Newsletter email submission
- [ ] Checkout form validation
- [ ] Search functionality (if present)

---

## Test Evidence

| Page | Screenshot | Status |
|------|-----------|--------|
| Homepage | `homepage.png` | |
| Homepage mega-menu | `homepage-mega-menu.png` | |
| Shop page | `shop-page.png` | |
| Shop filter active | `shop-filter-active.png` | |
| Product page | `product-page.png` | |
| Cart page | `cart-page.png` | |
| Checkout page | `checkout-page.png` | |
| Your Story | `your-story-page.png` | |
| Nav: Shop→Product | `nav-product-page.png` | |
