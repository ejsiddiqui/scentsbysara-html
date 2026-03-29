# Project Context: Scents by Sara (SBS)

## Overview
Scents by Sara is a premium luxury body candle e-commerce brand. This repository contains the development of the Shopify Online Store 2.0 theme, utilizing an existing HTML mockup as a functionality reference and Figma designs as the primary visual source of truth.

## Core Directories
- `/theme/`: **Active Development.** Shopify Online Store 2.0 theme. Managed as a separate Git repository.
- `/html/`: **Functionality Reference.** Completed HTML mockup (90% done). Use for component behavior, JS logic, and CSS token names.
- `/figma-exports/`: **Visual Source of Truth.** Primary reference for all visual decisions (layout, typography, color, spacing).
- `/docs/`: Implementation plans, QA reports, and task lists.
- `/scripts/`: Python scripts for QA and screenshot capture.

## Technical Architecture
- **Platform:** Shopify Basic, Online Store 2.0.
- **CSS:** Vanilla CSS with Liquid-generated custom properties (`theme/snippets/design-tokens.liquid`).
- **JavaScript:** Vanilla ES modules, Web Components (Custom Elements). No jQuery or heavy frameworks.
- **Assets:** Assets served directly via Shopify's pipeline; no build step for CSS/JS.
- **Markets:** Multi-market support for GBP (UK), AED (UAE), and USD (US).

## Design & QA Hierarchy
| Source | Priority | Usage |
|--------|----------|-------|
| `figma-exports/figma-<page>.png` | **Highest** | Visual QA, Layout, Typography, Colors |
| `html/` | Secondary | Component Logic, Token Names, JS Behavior |
| `references/` | None | **Do NOT use** (Outdated) |

## Development Workflow
### 1. Git & Deployment
- **Git Commit:** Commits should follow Conventional Commits (e.g., `feat:`, `fix:`, `docs:`).
- **Shopify Push:** Use `shopify theme push --theme 147874775176` to deploy.
- **Verification:** Always use `?preview_theme_id=147874775176` to bypass CDN cache.

### 2. QA Process
- Load Figma reference.
- Use `agent-browser` to take live screenshots of the store.
- Perform visual diff and style spot-checks (font-size, color, spacing).

## Key Style Patterns
- **Full-width toggle:** Controlled via section settings.
- **Decorative lines:** Use pseudo-elements (`::after`) on headings instead of `<hr>`.
- **Serif vs Sans:** Serif (`Rl Limo`) for decorative headings; Sans (`Suisse Int'l`) for body and UI.

## Store Details
- **Store URL:** `https://scentsbysara-dev.myshopify.com`
- **Store Password:** `ahttey`
- **Theme ID:** `147874775176`

## Lessons Learned
- **CDN Cache:** Regular store URL can be cached for up to 30 mins; use `preview_theme_id` for fresh renders.
- **Figma > HTML:** Never assume HTML mockup's visual accuracy; Figma is always the final word.
- **Shopify Auto-commits:** Shopify auto-commits to the theme repo; always pull before pushing and resolve conflicts in favor of local changes if necessary.
