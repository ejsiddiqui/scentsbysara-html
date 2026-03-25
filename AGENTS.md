# Repository Guidelines

## Project Overview
Scents by Sara — luxury body candle e-commerce brand. This repo contains:
- `/html/` — Completed HTML mockup (90% done). Reference-only during Shopify development.
- `/theme/` — Shopify Online Store 2.0 theme (active development).
- `/docs/superpowers/plans/` — Implementation plans for Shopify theme.
- `/references/` — Design reference screenshots.

## Project Structure

### Shopify Theme (`/theme/`)
```
theme/
  assets/          — CSS files + JS modules (ES modules, no build step)
  config/          — settings_schema.json, settings_data.json
  layout/          — theme.liquid, password.liquid
  locales/         — en.default.json, en.default.schema.json
  sections/        — Liquid sections + section group JSON files
  snippets/        — Reusable Liquid partials
  templates/       — JSON templates (Online Store 2.0)
```

### HTML Mockup Reference (`/html/`)
The completed HTML mockup is the visual source of truth. When building Shopify sections, cross-reference:
- `html/index.html` — Homepage layout and sections
- `html/product.html` — Product detail page
- `html/shop.html` — Shop/collection page
- `html/cart.html` — Cart page
- `html/css/design-tokens.css` — All color, spacing, typography tokens
- `html/css/components.css` — Button, card, form component styles
- `html/css/responsive.css` — Breakpoint-specific styles

## Current Status & Scope
- HTML mockup phase is complete. Do not modify files in `/html/` unless explicitly requested.
- Active work is on the Shopify theme in `/theme/`.
- Follow the implementation plan: `docs/superpowers/plans/2026-03-26-shopify-theme-development.md`

## Architecture Decisions
- **Platform:** Shopify Basic plan, Online Store 2.0
- **JS approach:** Vanilla ES modules with Web Components (Custom Elements), no build step, import maps
- **CSS approach:** Liquid-generated CSS custom properties from theme settings + `base.css`
- **Sections/Blocks:** JSON templates with sections everywhere for full theme customizer support
- **Cart:** Drawer + full cart page, using Shopify Cart API + Section Rendering API
- **Variants:** Single product with variants (Shape: Slim/Curvy/Plus-Size, Colour: Ivory/Caramel/Mocha)
- **Filtering:** Shopify native Storefront Filtering API (not custom JS)
- **Navigation:** Shopify native menu system + mega menu via theme settings
- **Markets:** GBP (UK), AED (UAE), USD (US) — 3 markets on Basic plan
- **Reviews:** Judge.me app integration
- **UGC (Your Story):** Contact form for submission, metaobjects for display
- **Checkout:** Shopify native (Basic plan), brand-styled with logo/colours/fonts

## Build, Test, and Development Commands
- `cd theme && shopify theme dev --store=<store>.myshopify.com` — Start local Shopify theme development server
- `shopify theme check` — Lint theme for Shopify best practices and Liquid errors
- `shopify theme push` — Push theme to Shopify store (use with caution)
- `shopify theme pull` — Pull latest theme from Shopify store
- No build step for CSS/JS — all files served directly via Shopify's asset pipeline

## Coding Style & Naming Conventions
- **Liquid:** Use Shopify's Online Store 2.0 patterns — JSON templates, sections with schemas, snippets for reuse
- **CSS:** Use CSS custom properties generated from theme settings via `design-tokens.liquid`. Never hardcode colours or spacing — use `var(--token)` references
- **JavaScript:** Vanilla ES modules, Web Components (Custom Elements). Use `@theme/` namespace in import maps. No jQuery, no frameworks
- **Naming:** kebab-case for files and CSS classes (e.g., `hero-slideshow.liquid`, `.product-card`)
- **Indentation:** 2-space indentation in Liquid/HTML/CSS/JS files
- **Sections:** Every section must have a complete schema with settings, blocks, and presets
- **Accessibility:** All interactive elements need ARIA attributes. All images need alt text. Minimum WCAG AA contrast
- **Reuse:** Extract repeated patterns into snippets. If a component appears on 2+ pages, it must be a snippet
- **Design tokens:** All visual values (colours, fonts, spacing, border-radius) must come from theme settings or CSS custom properties — never raw values
- **British English:** Use British spelling in all user-facing strings (colour, customise, etc.)

## Testing & QA Guidelines
- Primary validation is visual QA against the HTML mockup in `/html/`
- Test every page at: 375px, 390px, 768px, 1024px, 1440px, 1920px
- Run `shopify theme check` before committing to catch Liquid errors
- Treat console errors and horizontal overflow as release blockers
- Use the QA checklist at the end of each phase in the implementation plan
- QA process: Test -> Verify against mockup -> Fix -> Re-test -> Commit

## Commit & Pull Request Guidelines
- Follow Conventional Commit prefixes: `feat:`, `fix:`, `docs:`, `chore:`, `perf:`
- Keep commits scoped by section or feature area (e.g., header, product-card, cart-drawer)
- Commit after every completed task, not just phases
- Never commit broken code — verify theme loads without errors first
- PRs should include: summary, affected sections, before/after screenshots
