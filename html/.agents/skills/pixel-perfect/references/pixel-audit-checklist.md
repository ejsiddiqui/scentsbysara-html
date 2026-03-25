# Pixel-Perfect Audit Checklist

Use this checklist for every page. Fill in measurements before coding and verify again after implementation.

## Page Info
- Page name:
- Reference file(s):
- Viewport(s) tested:
- Date audited:

---

## 1) Full-Bleed & Edge Alignment
- [ ] Hero/banner extends full viewport width (no side gaps)
- [ ] Container content centered within `max-width: 1440px`
- [ ] Equal left/right margins at every breakpoint
- [ ] No horizontal scrollbar at any viewport width
- [ ] Background sections (footer, newsletter, etc.) extend edge-to-edge

## 2) Spacing System
- [ ] Section-to-section vertical spacing matches brand spec
- [ ] All spacing values use design tokens (no magic numbers)
- [ ] Component internal padding is consistent
- [ ] Grid gaps between repeated items are uniform
- [ ] Outer page margins: measured vs expected

## 3) Typography
- [ ] Headings use `rl-limo, sans-serif` — weight 400
- [ ] Body/UI uses `"Suisse Intl", sans-serif` — weight 400
- [ ] Font sizes match reference (measure each heading level)
- [ ] Line heights verified per text element
- [ ] Letter-spacing correct (buttons: `0.05em`, headings: as specified)
- [ ] Text-transform applied correctly (buttons: uppercase)
- [ ] Text block widths and wrapping match reference
- [ ] No system font fallback visible (fonts loaded correctly)

## 4) Color Tokens
- [ ] All colors resolve to `tokens.css` CSS custom properties
- [ ] No raw hex values outside `:root` block
- [ ] Background: `--bg-surface` (#F9F6F2), not white (#FFFFFF)
- [ ] Primary text: `--text-primary` (#3F3229), not black (#000000)
- [ ] Muted text: `--text-muted` (#A49483)
- [ ] Borders: `--border` (#CFC6B9)
- [ ] Dark sections: `--bg-ink` (#2D2B27)
- [ ] Hover/focus state colors are correct

## 5) Borders & Radius
- [ ] `border-radius: 0px` on all elements (max `2px` if justified)
- [ ] No rounded corners on buttons, cards, inputs, modals
- [ ] Button styling: uppercase, 14px, `letter-spacing: 0.05em`, sharp corners
- [ ] Input field borders visible with `--input-border` color

## 6) Component Fidelity
- [ ] Product cards: image ratio, title alignment, price position, CTA
- [ ] Navigation: link spacing, active states, hover effects
- [ ] Icons: Lucide only, 24px, 1px stroke, color inherits
- [ ] Footer: column layout, social links, payment icons
- [ ] Mega-menu: layout, hover behavior, link targets

## 7) Responsive Breakpoints

### Desktop (1440px)
- [ ] Layout matches reference exactly
- [ ] All grid columns align properly

### Tablet (768px–1024px)
- [ ] Grid collapses gracefully
- [ ] Text remains readable, images proportional

### Mobile (375px)
- [ ] Content stacks correctly
- [ ] Touch targets ≥ 44×44px
- [ ] No content cropped or overflowing
- [ ] Mobile nav functions correctly

## 8) Interactions & States
- [ ] Hover states on buttons, links, cards
- [ ] Focus states visible for accessibility
- [ ] Sticky header behavior correct
- [ ] Transitions/animations feel smooth (`--transition: 240ms ease`)

---

## 9) Deviation Report

| # | Location | Expected | Actual | Severity | Fix |
|---|----------|----------|--------|----------|-----|
| 1 |          |          |        |          |     |
| 2 |          |          |        |          |     |
| 3 |          |          |        |          |     |
