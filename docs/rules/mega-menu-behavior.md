# Mega Menu Interaction Guidelines

This module dictates the mechanics behind the hover-activated massive navigation expansion panel.

## 1. Trigger Enforcement

- **Desktop Only:** The mega menu only functions on desktop (`>= 1024px`) where hover states (`:hover`) are reliable.
- **Primary Trigger:** Hovering over specific `.nav-item` links (e.g., "SHOP ALL" or "BEST SELLERS") containing a mega menu child element.
- **Debounce / Delay:** To prevent erratic flashing if a user quickly drags their mouse across the header, implement a tiny CSS transition delay or rely on `0.2s` opacity timing to soften the trigger. No JS timeouts are necessary for simple hovers, but CSS transitions are mandatory. 

## 2. Layout & Bounding Box

- **Width Structure:** The mega menu spans `100vw` or strict to the `1720px` container width.
- **Display Status:**
  - Base: `opacity: 0; pointer-events: none; transform: translateY(-10px); visibility: hidden;`
  - Hover: `opacity: 1; pointer-events: auto; transform: translateY(0); visibility: visible;`
- **Duration Constraints:** `transition: opacity 0.3s ease, transform 0.3s ease, visibility 0.3s;`

## 3. Visual Styling Requirements
- **Background:** `var(--bg-primary)` (White Sand) or `var(--bg-secondary)` (Neutral Stone). It must strictly separate from the underlying page content.
- **Typography:** Navigation category titles use `RL Limo` (`var(--text-h3)`). Individual links use `Suisse Int'l` small caps (`var(--text-micro)`).
- **Images:** If the mega menu displays featured product imagery (like "SHE IS GRACE"), these must utilize `aspect-ratio` bounds (e.g., `3/4`) and strict `object-fit: cover` to maintain exact alignment in the grid row.

## 4. Mobile Prohibition
Under NO circumstances does the Mega Menu hover-logic port to mobile.
At `<= 1024px`, mega menu items must convert into a stacked accordion (`details` / `summary` setup or JS toggles) within the full-screen Hamburger overlay menu. The nested links become indented lists.
