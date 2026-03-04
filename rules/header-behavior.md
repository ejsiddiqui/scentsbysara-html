# Header Behavior Architecture

This document governs the layout, constraints, and interactive mechanics of the `site-header`.

## 1. Structural Constraints

- **Maximum Height (Strict):** `135px`.
  - The header must under no circumstances exceed `135px` on desktop.
  - If the logo and navigation links require breathing room, rely on `translateY` or flex alignment within this rigid threshold.

## 2. Desktop Layout Engine

- **Centering:** `logo` sits dead center of the viewport.
- **Navigation:** Main categories (`SHOP ALL`, `GIFTS`, `OUR STORY`, `YOUR STORY`, `CONTACT US`) cluster around the logo or flank it on the left.
- **Utility:** Icons (`Account (User)`, `Wishlist (Heart)`, `Cart (Bag)`) cluster hard to the right boundary. While `Search (Magnifying Glass)` is on left.
- All groups use `flex` alignment (`align-items: center`).

## 3. The Sticky Scroll Interaction Rule

The header must feel completely un-intrusive when browsing massive imagery content down the page.

- **On Load:** Positioned relative or absolute at the top.
- **On Scroll Down (`window.scrollY > 0` and direction = `down`):**
  - Add class `.header-hidden`.
  - CSS translates the header upwards completely off-screen: `transform: translateY(-100%);`
  - Transition timing MUST be smooth: `transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);`
- **On Scroll Up (direction = `up`):**
  - Remove `.header-hidden`, add `.header-scrolled`.
  - Header is fixed to top (`position: fixed; top: 0; left: 0; width: 100%; z-index: var(--z-header);`).
  - Add a highly subtle `border-bottom: 1px solid var(--border-light);` or extremely soft shadow to detach it from content scrolling underneath.

## 4. Mobile Header Pivot

- **Threshold:** At `1024px`, the desktop text navigation is hidden (`display: none`).
- **Layout Shift:**
  - The left side houses search and bag icons.
  - The logo stays in the center but the smaller version of the logo is used.
  - The right side houses the Hamburger Menu.
- **Hamburger Rules:**
  - Must have strictly bounds `min-height: 44px; min-width: 44px;` for touch mechanics.
  - Sits flush right against the `20px` responsive gutter bound.
