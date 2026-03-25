# Scents by Sara Shopify Theme Plan v2

## Summary
- Build a custom Shopify OS 2.0 theme using Skeleton as the starter and Horizon as a reference only.
- Rebuild the current storefront into native Shopify templates, sections, snippets, settings, and structured content instead of porting the HTML literally.
- Scope includes all current storefront pages, with standard Shopify checkout constraints and wishlist deferred to phase 2.

## Implementation Changes
- Repository and setup:
  - Use a separate long-term Shopify theme repo.
  - Keep the current HTML storefront available as a frozen visual reference during migration; temporary side-by-side work is acceptable, but not a required permanent repo layout.
  - Set up Shopify CLI, Theme Check, a dev store, and preview workflow first.
- Theme architecture:
  - Default to Liquid, JSON templates, snippets, section settings, and small JS modules.
  - Use richer JS only where needed: cart drawer, predictive search, filters/sort, sliders, and mobile navigation.
  - Do not make Web Components or import maps a mandatory foundation requirement.
- Settings and design system:
  - Port the existing token system into theme CSS variables.
  - Expose only merchant-meaningful settings globally: logos, brand color schemes, typography choices actually supported by the store, spacing density, card behavior, social links, and localization UI toggles.
  - Keep implementation-level tokens in CSS instead of exposing every token in `settings_schema.json`.
  - Explicitly decide font delivery: self-host licensed brand fonts if allowed; otherwise use documented fallbacks until licensing/assets are confirmed.
- Content and template model:
  - Menus via Shopify Navigation.
  - Products, collections, media, pricing, and filters via native Shopify objects and Search & Discovery.
  - Reusable editorial content via metaobjects only where reuse is real: testimonials, ritual cards, founder/story entries, collection callouts.
  - Single-use page content via section/block settings.
  - `Your Story` v1 uses a native contact-style submission flow only; displayed community stories are curated separately through metaobjects. No implied auto-publish or customer image-upload workflow unless a moderation flow is added later.
  - Reviews stay app-block-compatible. Wishlist remains UI-only or omitted in v1 and is implemented in phase 2.
- Route mapping:
  - Home: hero, featured collection, commitment/values, collections overview, editorial split sections, testimonials, newsletter.
  - Shop/body-candles/scar-collection/sculpted-collection/gifts: start from one main collection template; add alternate collection templates only for routes with genuinely different hero/editorial layouts.
  - Product: main product, recommendations, editorial blocks, accordions, reviews slot, related content.
  - Our Story / Your Story / Contact: page templates composed from reusable editorial sections.
  - Cart and search are in scope. Checkout is branding/handoff only.
- Delivery sequence:
  - Phase 1: theme foundation, tokens, base CSS, layout shell, header/footer/localization.
  - Phase 2: product card, collection grid, PDP core, cart drawer/page.
  - Phase 3: homepage composition and remaining collection variants.
  - Phase 4: editorial pages and forms.
  - Phase 5: search, SEO, accessibility, performance, and launch QA.
  - Phase 6: optional non-launch templates such as password, gift card, and blog placeholders only after launch-critical routes are complete.

## Test Plan
- Visual parity QA against the current HTML reference at 1920, 1440, 1024, 768, 390, and 375.
- Theme editor QA: images, menus, colors, content blocks, and template assignments must all be editable without code changes.
- Commerce QA: product selection, add to cart, cart updates, collection filters/sort, predictive search, checkout handoff.
- Market QA: country/currency selector, price display, and market-aware messaging, without hardcoding market list in the implementation plan.
- Form QA: contact form and `Your Story` submission flow, plus the curated story-display workflow.
- Accessibility and performance QA before launch.

## Assumptions
- Standard Shopify checkout, not Shopify Plus checkout customization.
- Multi-market and currency-aware now; translation prepared later, not delivered in v1.
- Wishlist is phase 2.
- Skeleton remains the base; Horizon is reference-only.
- Separate repos are preferred long-term.
