# Mobile Submenu Slide-In Navigation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the SHOP accordion in the mobile overlay menu with a dual-panel slide-in navigation that keeps the header fixed and animates the submenu in from the right.

**Architecture:** The `.mobile-menu-body` becomes a clipping viewport (`overflow: hidden`). Inside it, a `.mobile-menu-panels` container is absolutely positioned and 200% wide, holding two flex-column panels side by side. A `submenu-active` class on the panels container drives a `translateX(-50%)` transition to switch between panels. Each panel independently scrolls.

**Tech Stack:** Vanilla HTML, CSS (custom properties, CSS transitions), Vanilla JS (DOM, classList, event listeners). No build step. Open any `.html` file directly in a browser to verify.

---

## File Map

| File | Change |
|------|--------|
| `css/components.css` | Add panel-slide CSS, remove accordion-specific rules |
| `css/responsive.css` | Verify existing mobile overrides still apply; no structural changes expected |
| `partials/site-header.html` | Restructure `.mobile-menu-body` to dual-panel layout |
| `assets/js/main.js` | Remove accordion logic, add panel-slide logic, update `MOBILE_MENU_TEMPLATE` and integrity check |
| `partials/mobile-menu.html` | Sync to match `site-header.html` (reference file only, not loaded by pages) |

---

## Task 1: Update CSS — Replace Accordion Rules with Panel-Slide Rules

**Files:**
- Modify: `css/components.css`

### Steps

- [ ] **Step 1: Remove accordion-specific CSS rules from `components.css`**

  Locate and delete the following four rule blocks (they have no use after the HTML restructure):

  ```css
  /* DELETE this block */
  .mobile-shop-toggle-icon {
      flex-shrink: 0;
      transition: transform 0.2s ease;
  }

  /* DELETE this block */
  .mobile-nav-item-shop.expanded .mobile-shop-toggle-icon {
      transform: rotate(90deg);
  }

  /* DELETE this block */
  .mobile-shop-panel {
      display: grid;
      gap: var(--space-lg);
      margin-top: var(--space-md);
      overflow: hidden;
      opacity: 0;
      max-height: 0;
      transition: max-height 0.18s ease, opacity 0.14s ease;
  }

  /* DELETE this block */
  .mobile-shop-panel[hidden] {
      display: none;
  }
  ```

- [ ] **Step 2: Update `.mobile-menu-body` — add `position: relative` and `overflow: hidden`**

  Current rule (around line 700):
  ```css
  .mobile-menu-body {
      display: flex;
      flex: 1;
      flex-direction: column;
  }
  ```

  Replace with:
  ```css
  .mobile-menu-body {
      display: flex;
      flex: 1;
      flex-direction: column;
      position: relative;
      overflow: hidden;
  }
  ```

- [ ] **Step 3: Add new panel-slide CSS rules**

  Add the following block immediately after the updated `.mobile-menu-body` rule:

  ```css
  .mobile-menu-panels {
      position: absolute;
      top: 0;
      left: 0;
      bottom: 0;
      width: 200%;
      display: flex;
      flex-direction: row;
      transition: transform 0.32s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  }

  .mobile-menu-panels.submenu-active {
      transform: translateX(-50%);
  }

  .mobile-panel-main,
  .mobile-panel-sub {
      width: 50%;
      flex-shrink: 0;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
      display: flex;
      flex-direction: column;
      padding-bottom: calc(var(--space-lg) + env(safe-area-inset-bottom, 0px));
  }

  .mobile-shop-groups {
      display: grid;
      gap: var(--space-lg);
      padding: var(--space-md) 0;
  }

  .sub-nav-bar {
      display: flex;
      align-items: center;
      height: 48px;
      padding: 0 var(--gutter);
      flex-shrink: 0;
  }

  .sub-nav-label {
      flex: 1;
      text-align: center;
      font-family: var(--font-sans);
      font-size: var(--text-body);
      line-height: 1.25;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--text-primary);
  }
  ```

- [ ] **Step 4: Verify `responsive.css` needs no structural changes**

  Open `css/responsive.css`. The overrides for `.mobile-menu-content`, `.mobile-menu-top`, `.mobile-menu-brand img`, `.mobile-menu-footer` all still exist in the new structure and are unaffected. The removed selectors (`.mobile-shop-panel`, `.mobile-shop-toggle-icon`) have no entries in `responsive.css`. No edits needed.

- [ ] **Step 5: Commit**

  ```bash
  git add css/components.css
  git commit -m "style: replace mobile shop accordion CSS with dual-panel slide rules"
  ```

---

## Task 2: Restructure HTML — Dual-Panel Layout in `site-header.html`

**Files:**
- Modify: `partials/site-header.html`

`site-header.html` is the **source of truth** — it is loaded by all pages via `data-shared-partial="site-header"`. `partials/mobile-menu.html` is a reference copy and is updated in Task 4.

### Steps

- [ ] **Step 1: Locate the `.mobile-menu-body` block in `site-header.html`**

  Find the opening `<div class="mobile-menu-body">` (around line 168). The block currently contains:
  - `.mobile-nav-links.mobile-nav-primary` (with `.mobile-nav-item-shop` accordion inside)
  - `.mobile-menu-footer`

- [ ] **Step 2: Replace the entire `.mobile-menu-body` block with the dual-panel structure**

  Replace from `<div class="mobile-menu-body">` to its closing `</div>` with:

  ```html
  <div class="mobile-menu-body">
      <div class="mobile-menu-panels">

          <!-- Panel 1: Main Navigation -->
          <div class="mobile-panel-main">
              <nav class="mobile-nav-links mobile-nav-primary" role="navigation" aria-label="Mobile Navigation">
                  <div class="mobile-nav-item mobile-nav-item-shop">
                      <button class="mobile-shop-toggle" type="button" aria-expanded="false" aria-haspopup="true">
                          <span>SHOP</span>
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"
                              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                              <polyline points="9 6 15 12 9 18"></polyline>
                          </svg>
                      </button>
                  </div>
                  <a href="gifts.html">GIFTS</a>
                  <a href="our-story.html">OUR STORY</a>
                  <a href="your-story.html">YOUR STORY</a>
                  <a href="shop.html">WISHLIST</a>
                  <a href="contact.html">CONTACT</a>
              </nav>

              <div class="mobile-menu-footer">
                  <a href="contact.html" class="btn-outline full-width-btn mobile-menu-cta">LOG IN</a>
                  <a href="contact.html" class="btn-outline full-width-btn mobile-menu-cta">JOIN OUR NEWSLETTER</a>
                  <div class="mobile-menu-meta">
                      <div class="mobile-menu-social">
                          <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
                              <img src="assets/icons/instagram.svg" alt="" aria-hidden="true">
                          </a>
                          <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
                              <img src="assets/icons/facebook.svg" alt="" aria-hidden="true">
                          </a>
                          <a href="https://tiktok.com" target="_blank" rel="noopener noreferrer" aria-label="TikTok">
                              <img src="assets/icons/tiktok.svg" alt="" aria-hidden="true">
                          </a>
                          <a href="https://pinterest.com" target="_blank" rel="noopener noreferrer" aria-label="Pinterest">
                              <img src="assets/icons/pinterest.svg" alt="" aria-hidden="true">
                          </a>
                      </div>
                      <div class="mobile-menu-currency">
                          <select data-currency-select aria-label="Mobile currency">
                              <option value="AED">AED</option>
                              <option value="GBP">GBP £</option>
                              <option value="USD">USD $</option>
                              <option value="EUR">EUR €</option>
                          </select>
                      </div>
                  </div>
              </div>
          </div>

          <!-- Panel 2: Shop Submenu -->
          <div class="mobile-panel-sub">
              <div class="sub-nav-bar">
                  <button class="icon-btn sub-back-btn" aria-label="Back to menu">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"
                          stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                          <polyline points="15 18 9 12 15 6"></polyline>
                      </svg>
                  </button>
                  <span class="sub-nav-label">SHOP</span>
                  <button class="icon-btn sub-close-btn" aria-label="Close menu">
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"
                          stroke-linecap="round" aria-hidden="true">
                          <line x1="18" y1="6" x2="6" y2="18"></line>
                          <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                  </button>
              </div>
              <div class="mobile-shop-groups">
                  <div class="mobile-shop-group">
                      <h3>POPULAR</h3>
                      <a href="shop.html">Shop All</a>
                      <a href="shop.html">Bestsellers</a>
                  </div>
                  <div class="mobile-shop-group">
                      <h3>BODY CANDLES</h3>
                      <a href="body-candles.html">All Body Candles</a>
                      <a href="product.html">She is You</a>
                      <a href="product.html">She is Strength</a>
                      <a href="product.html">She is Real</a>
                      <a href="product.html">She is Power</a>
                      <a href="product.html">She is Timeless</a>
                      <a href="product.html">She is Beauty</a>
                  </div>
                  <div class="mobile-shop-group">
                      <h3>SHOP BY SIZE</h3>
                      <a href="shop.html">Slim</a>
                      <a href="shop.html">Curvy</a>
                      <a href="shop.html">Plus Size</a>
                  </div>
                  <div class="mobile-shop-group">
                      <h3>SHOP BY COLLECTION</h3>
                      <a href="scar-collection.html">Scar Collection</a>
                      <a href="sculpted-collection.html">Sculpted Collection</a>
                  </div>
              </div>
          </div>

      </div>
  </div>
  ```

- [ ] **Step 3: Manually verify HTML renders correctly in browser**

  Open `index.html` in a browser. Resize to mobile width (< 768px). Open the mobile menu:
  - The main nav (SHOP, GIFTS, OUR STORY, etc.) should be visible
  - The SHOP button should have a chevron on the right
  - The footer (LOG IN, NEWSLETTER, social icons, currency) should appear at the bottom
  - Tapping SHOP does nothing yet (JS not updated) — that is expected

- [ ] **Step 4: Commit**

  ```bash
  git add partials/site-header.html
  git commit -m "feat: restructure mobile menu body to dual-panel HTML layout"
  ```

---

## Task 3: Update JavaScript — Remove Accordion Logic, Wire Panel-Slide

**Files:**
- Modify: `assets/js/main.js`

### Steps

- [ ] **Step 1: Remove the accordion variables and constant**

  In the `/* --- Mobile Navigation Toggle --- */` section (around line 195), delete these three lines:

  ```javascript
  const mobileShopPanel = document.querySelector('.mobile-shop-panel');
  const SHOP_PANEL_DURATION_MS = 180;
  // ...
  let shopPanelTimeoutId = null;
  ```

  Also delete `const mobileShopItem = document.querySelector('.mobile-nav-item-shop');` — the `mobileShopItem` variable is only used inside `setShopMenuExpanded`, which is being removed.

- [ ] **Step 2: Delete the entire `setShopMenuExpanded` function**

  Delete from `const setShopMenuExpanded = (isExpanded) => {` to its closing `};` (approximately lines 210–247). This function and all its internal references to `shopPanelTimeoutId`, `mobileShopItem`, `mobileShopPanel` are eliminated.

- [ ] **Step 3: Add new panel-slide variables and functions**

  Directly after `const mobileShopToggle = document.querySelector('.mobile-shop-toggle');`, add:

  ```javascript
  const mobileMenuPanels = document.querySelector('.mobile-menu-panels');
  const subBackBtn = document.querySelector('.sub-back-btn');
  const subCloseBtn = document.querySelector('.sub-close-btn');

  const openSubMenu = () => {
      if (!mobileMenuPanels || !mobileShopToggle) return;
      mobileMenuPanels.classList.add('submenu-active');
      mobileShopToggle.setAttribute('aria-expanded', 'true');
  };

  const closeSubMenu = () => {
      if (!mobileMenuPanels || !mobileShopToggle) return;
      mobileMenuPanels.classList.remove('submenu-active');
      mobileShopToggle.setAttribute('aria-expanded', 'false');
  };
  ```

- [ ] **Step 4: Update `applyClosedState` — replace `setShopMenuExpanded(false)` with `closeSubMenu()`**

  In the `applyClosedState` function, change:
  ```javascript
  setShopMenuExpanded(false);
  ```
  to:
  ```javascript
  closeSubMenu();
  ```

- [ ] **Step 5: Update `openMenu` — replace `setShopMenuExpanded(false)` with `closeSubMenu()`**

  In the `openMenu` function, change:
  ```javascript
  setShopMenuExpanded(false);
  ```
  to:
  ```javascript
  closeSubMenu();
  ```

- [ ] **Step 6: Replace the `mobileShopToggle` click listener block**

  Find and delete the entire old listener block:
  ```javascript
  if (mobileShopToggle) {
      setShopMenuExpanded(false);
      mobileShopToggle.addEventListener('click', () => {
          const isExpanded = mobileShopToggle.getAttribute('aria-expanded') === 'true';
          setShopMenuExpanded(!isExpanded);
      });
  }
  ```

  Replace with:
  ```javascript
  if (mobileShopToggle) {
      mobileShopToggle.addEventListener('click', openSubMenu);
  }

  if (subBackBtn) {
      subBackBtn.addEventListener('click', closeSubMenu);
  }

  if (subCloseBtn) {
      subCloseBtn.addEventListener('click', (event) => {
          event.preventDefault();
          setMenuState(false);
      });
  }
  ```

- [ ] **Step 7: Update the `ensureMobileMenuIntegrity` integrity check**

  Find:
  ```javascript
  const hasShopToggle = !!mobileMenu.querySelector('.mobile-shop-toggle');

  const isIncomplete = !primaryNav
      || primaryLinkCount < 5
      || socialLinkCount < 4
      || !hasCurrency
      || !hasFooter
      || !hasShopToggle;
  ```

  Replace with:
  ```javascript
  const hasSubPanel = !!mobileMenu.querySelector('.mobile-panel-sub');

  const isIncomplete = !primaryNav
      || primaryLinkCount < 5
      || socialLinkCount < 4
      || !hasCurrency
      || !hasFooter
      || !hasSubPanel;
  ```

- [ ] **Step 8: Manually verify interaction in browser**

  Open `index.html` at mobile width. Test all scenarios:
  - Open mobile menu → main nav is shown, submenu is hidden (off-screen right)
  - Tap SHOP → submenu slides in from the right; back arrow and X are visible; "SHOP" label is centered; no border-bottom below the label bar
  - Tap back arrow → main nav slides back in
  - Tap X icon → entire mobile overlay closes
  - Tap existing close button (hamburger icon in `mobile-menu-top`) → overlay closes
  - Press Escape → overlay closes
  - Close overlay while on submenu → re-opening the overlay shows main nav (reset confirmed)
  - Tap a submenu link → overlay closes
  - Footer accordions on any page (e.g. `index.html`) → still work, unaffected
  - Product page (`product.html`) accordions → still work, unaffected

- [ ] **Step 9: Commit**

  ```bash
  git add assets/js/main.js
  git commit -m "feat: replace mobile shop accordion with panel-slide navigation"
  ```

---

## Task 4: Sync `MOBILE_MENU_TEMPLATE` and `mobile-menu.html`

**Files:**
- Modify: `assets/js/main.js` (the `MOBILE_MENU_TEMPLATE` string constant)
- Modify: `partials/mobile-menu.html`

### Steps

- [ ] **Step 1: Update `MOBILE_MENU_TEMPLATE` in `main.js`**

  The `MOBILE_MENU_TEMPLATE` string (lines 8–108) is the fallback injected when `ensureMobileMenuIntegrity()` detects a broken mobile menu. It must match the new dual-panel structure exactly — copy the `.mobile-menu-content` inner HTML from the updated `partials/site-header.html` (Task 2, Step 2) into the template string.

  The template should produce the same markup as `site-header.html`, starting from `<div class="mobile-menu-content container">` and ending at its closing `</div>`.

- [ ] **Step 2: Update `partials/mobile-menu.html`**

  Replace the content of `partials/mobile-menu.html` with the full updated markup from `site-header.html`, including the outer `<div class="mobile-menu-overlay" aria-hidden="true" inert>` wrapper.

  This file is not loaded by any page (all pages use `site-header` partial) but is kept as a reference copy.

- [ ] **Step 3: Commit**

  ```bash
  git add assets/js/main.js partials/mobile-menu.html
  git commit -m "chore: sync MOBILE_MENU_TEMPLATE and mobile-menu.html with new panel-slide structure"
  ```
