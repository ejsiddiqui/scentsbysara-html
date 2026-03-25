# Mobile Submenu Slide-In Navigation

**Date:** 2026-03-24
**Status:** Approved

## Overview

Replace the current mobile menu's inline accordion for the SHOP submenu with a dual-panel slide-in navigation. When the user taps a main menu item that has a submenu (currently only SHOP), the submenu slides in from the right, replacing the main nav view within the menu body. The mobile menu header (logo, cart, search, hamburger icons) remains unchanged at all times.

## Behaviour

### Main menu state
- The mobile overlay menu works exactly as it does today (slides in from the right of the viewport).
- SHOP is displayed as a tappable row with a right-pointing chevron icon.
- All other nav links (GIFTS, OUR STORY, etc.) remain unchanged.

### Submenu state (after tapping SHOP)
- The main nav panel slides out to the left.
- The SHOP submenu panel slides in from the right, appearing within the same menu body area.
- The mobile menu header (`mobile-menu-top`) is **unchanged and always visible**.
- Below the header, a secondary nav bar appears containing:
  - **Left:** back arrow icon — tapping returns to the main menu
  - **Centre:** "SHOP" label (uppercase, matching existing typography)
  - **Right:** X (close) icon — tapping closes the entire mobile overlay
  - **No border-bottom** on this secondary nav bar
- Below the secondary nav bar: the SHOP submenu content groups (scrollable).

### Closing behaviour
- Back arrow → slide back to main nav (submenu closes, main nav slides back in)
- X icon → closes the entire mobile overlay (same as the existing close button)
- Existing close button in `mobile-menu-top` → continues to close the overlay
- Escape key → continues to close the overlay
- Nav link click → closes the overlay (existing behaviour, unchanged)
- Opening the menu always starts at the main nav (submenu is reset on close)

## Implementation Approach

**Dual-panel slide (Option A)** — the menu body acts as a clipping viewport. Two panels sit side-by-side inside a flex container that is 200% wide. A CSS transform slides both panels in unison.

## Architecture

### HTML structure (`partials/site-header.html`, `MOBILE_MENU_TEMPLATE` in `main.js`, `partials/mobile-menu.html`)

```
.mobile-menu-overlay
  .mobile-menu-content.container
    .mobile-menu-top                        ← unchanged (logo + icons)
    .mobile-menu-body                       ← clipping viewport (overflow: hidden)
      .mobile-menu-panels                   ← flex row, 200% wide, translates on state
        .mobile-panel-main                  ← 50% width, scrollable
          .mobile-nav-links.mobile-nav-primary
            .mobile-nav-item.mobile-nav-item-shop
              button.mobile-shop-toggle     ← SHOP row (chevron SVG icon removed from markup)
            a GIFTS
            a OUR STORY
            a YOUR STORY
            a WISHLIST
            a CONTACT
          .mobile-menu-footer
        .mobile-panel-sub                   ← 50% width, scrollable
          .sub-nav-bar                      ← back | SHOP | X (no border-bottom)
            button.sub-back-btn
            span.sub-nav-label  "SHOP"
            button.sub-close-btn
          .mobile-shop-groups               ← shop group content (scrollable area)
            .mobile-shop-group × 4
```

### CSS (`css/components.css`, `css/responsive.css`)

**`.mobile-menu-body`**
- Add `overflow: hidden; position: relative`

**`.mobile-menu-panels`** (new)
- `display: flex; flex-direction: row; width: 200%; height: 100%`
- `transition: transform 0.32s cubic-bezier(0.25, 0.46, 0.45, 0.94)`

**`.mobile-menu-panels.submenu-active`** (new)
- `transform: translateX(-50%)`

**`.mobile-panel-main`, `.mobile-panel-sub`** (new)
- `width: 50%; flex-shrink: 0; overflow-y: auto; display: flex; flex-direction: column`

**`.sub-nav-bar`** (new)
- `display: flex; align-items: center; height: 48px; padding: 0 var(--gutter)`
- No `border-bottom`

**`.sub-nav-label`** (new)
- `flex: 1; text-align: center`
- Typography matching existing `.mobile-nav-links a` (font-family, size, letter-spacing, uppercase)

**Remove** (accordion-specific, no longer needed):
- `.mobile-shop-panel` rules
- `.mobile-shop-panel[hidden]` rule
- `.mobile-shop-toggle-icon` transition rule
- `.mobile-nav-item-shop.expanded .mobile-shop-toggle-icon` rotation rule

**Keep** (still used):
- `.mobile-shop-toggle` base styles (reused for the SHOP button row)
- `.mobile-shop-group` and `.mobile-shop-group h3/a` styles (content is the same)
- All `.mobile-nav-links`, `.mobile-nav-item`, `.mobile-menu-footer` styles

### JavaScript (`assets/js/main.js`)

**Remove:**
- `setShopMenuExpanded()` function
- `SHOP_PANEL_DURATION_MS` constant
- `mobileShopPanel` variable
- `shopPanelTimeoutId` variable
- All calls to `setShopMenuExpanded()`

**Add:**
- `mobileMenuPanels` — `document.querySelector('.mobile-menu-panels')`
- `subBackBtn` — `document.querySelector('.sub-back-btn')`
- `subCloseBtn` — `document.querySelector('.sub-close-btn')`
- `openSubMenu()` — adds `submenu-active` to `.mobile-menu-panels`; sets `aria-expanded="true"` on `.mobile-shop-toggle`
- `closeSubMenu()` — removes `submenu-active`; sets `aria-expanded="false"` on `.mobile-shop-toggle`

**Update:**
- `applyClosedState()` — call `closeSubMenu()` instead of `setShopMenuExpanded(false)` so submenu resets on overlay close
- `openMenu()` — call `closeSubMenu()` instead of `setShopMenuExpanded(false)` to reset on re-open
- `.mobile-shop-toggle` click handler → calls `openSubMenu()` (replaces accordion toggle)
- `ensureMobileMenuIntegrity()` integrity check — replace `hasShopPanel` check (`.mobile-shop-panel`) with check for `.mobile-panel-sub`

**Event listeners added:**
- `subBackBtn` click → `closeSubMenu()`
- `subCloseBtn` click → `closeMenu()`

## Accordion isolation

The following accordion implementations are **not affected**:
- **Product page** (`product.js`): uses `.accordion` / `.accordion-header` / `.accordion-body` classes — entirely separate
- **Footer** (`main.js`): uses `.footer-accordion-trigger` / `.footer-accordion-icon` / `.footer-links-col` — entirely separate

## Files changed

| File | Change |
|------|--------|
| `partials/site-header.html` | Restructure mobile menu body to dual-panel layout |
| `assets/js/main.js` | Remove accordion logic, add panel-slide logic, update `MOBILE_MENU_TEMPLATE` and integrity check |
| `css/components.css` | Replace accordion CSS with panel-slide CSS |
| `css/responsive.css` | Update any matching responsive overrides for removed/renamed selectors |
| `partials/mobile-menu.html` | Sync with site-header.html for consistency. `site-header.html` is the source of truth — it is loaded by all pages via `data-shared-partial="site-header"`. `mobile-menu.html` is not loaded by any page and exists as a reference copy only. |
