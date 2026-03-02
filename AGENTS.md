# Repository Guidelines

## Project Structure & Module Organization
This repository contains a static storefront.
- Root HTML pages: `index.html`, `shop.html`, `product.html`, `body-candles.html`,`cart.html`, `checkout.html`, `contact.html`, `our-story.html`, `your-story.html`.
- Shared styling system: `css/design-tokens.css`, `css/layout.css`, `css/components.css`, `css/responsive.css`.
- Page behavior scripts: `assets/js/` (for example `main.js`, `shop.js`, `product.js`, `cart-state.js`).
- Media assets: `assets/images/`, `assets/icons/`, `assets/fonts/`.
- QA evidence and audits: `docs/qa/`; planning/review docs: `docs/review/`, `docs/task/`.
- Visual references: `references/`, organized by page and section assets used for matching.

## Current Status & Scope Rules
- `index.html` (homepage) is the approved baseline and is fully responsive.
- Do not change homepage HTML/CSS unless explicitly requested.
- Other pages currently contain known layout/consistency issues and should be fixed.
- Reuse homepage design patterns (spacing, typography, header/footer behavior, components, tokens) when updating other pages.
- For page fixes, use reference screenshots from `references/<page-name>/` and match section-by-section. Don't use screenshot images in code,they are for reference only. Images to be used can be found in `assets/images/` dir.


## Build, Test, and Development Commands
No build step is required for static pages.
- `python -m http.server 4173` from repo root: run local preview at `http://127.0.0.1:4173`.
- `python docs/qa/viewport_audit.py`: run multi-page, multi-breakpoint Playwright sweep; outputs screenshots and `report.json` under `docs/qa/sweep-<timestamp>/`.
- `python docs/qa/token_audit.py --page product.html`: run token/typography compliance checks from `docs/qa/token_rules.json` and output report artifacts under `docs/qa/token-audit-<timestamp>/`.
- `git config core.hooksPath .githooks`: enable repo-managed pre-commit hooks (includes token audit gate).
- `git status --short`: verify only intended files changed before commit.

## Coding Style & Naming Conventions
- Use semantic HTML and keep page-specific logic in `assets/js/<page>.js`.
- Use CSS variables from `css/design-tokens.css`; do not hardcode off-palette colors.
- Always use typographic scale tokens from `css/design-tokens.css` (for example `--text-body-large`) instead of raw/random `px` values for UI typography.
- Match existing naming: kebab-case files and classes (for example `our-story.html`, `.announcement-bar`).
- Preserve current formatting style (4-space indentation in HTML/CSS/JS files).
- Make resuable and maintainable code, and resuse where possible
- Keep global layout changes in shared CSS files; keep page-specific tweaks isolated.
- Keep page specific to minimum, use shared css files where possible.
- For repeating sections e.g. product-grid, section with two halves, etc are repeating many times. Same CSS and html should be used.

## Testing Guidelines
- Primary validation is visual and functional QA, not unit tests.
- For UI changes, run `python docs/qa/viewport_audit.py` and review screenshots at 1920, 1440, 1024, 768, 390, and 375 widths.
- For token-sensitive changes (colors, font-size, typography hierarchy), run `python docs/qa/token_audit.py --page <page>.html` and treat any `fail`, `missing_selector`, or `invalid_token` result as a blocker.
- Log evidence in `docs/qa/implementation/<TASK-ID>/` when completing fixes.
- Treat console errors and horizontal overflow as release blockers.

## Commit & Pull Request Guidelines
- Follow Conventional Commit prefixes used in history: `feat:`, `fix:`, `docs:`, `test(qa):`, `chore:`.
- Keep commits scoped by page or feature area (for example header, cart state, checkout validation).
- PRs should include: concise summary, affected routes/files, linked task/issue, and before/after screenshots for desktop + mobile.
