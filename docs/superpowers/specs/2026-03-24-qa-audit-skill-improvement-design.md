# QA Audit Skill Improvement — Design Spec

**Date:** 2026-03-24
**Branch:** desktop_changes
**Status:** Draft

## Problem Statement

The current QA audit skill has two pain points:

1. **Functional/interaction testing is manual and easy to forget** — no structured checklist for per-page interactions (mobile menu, cart actions, gallery swipes, filters, etc.), so coverage depends on the agent's memory.
2. **Full-sweep audits waste time** — every audit runs against all pages regardless of what changed, making the feedback loop slow for small changes.

## Design: Smart Default with Escape Hatches

A single workflow that auto-detects scope from `git diff`, lets the user override, runs scoped automated checks, walks through an interaction checklist, and optionally triggers E2E tests.

---

## 1. File-to-Page Mapping & Auto-Scope

The skill starts by running `git diff` against the base branch (or last commit) to detect changed files, then maps them to affected pages.

### Direct Mappings (inside the skill)

| File pattern | Affected page |
|---|---|
| `index.html` | `index.html` |
| `shop.html`, `assets/js/shop.js` | `shop.html` |
| `product.html`, `assets/js/product.js` | `product.html` |
| `cart.html`, `assets/js/cart.js` | `cart.html` |
| `checkout.html`, `assets/js/checkout.js` | `checkout.html` |
| `your-story.html`, `assets/js/forms.js` | `your-story.html` |
| `our-story.html` | `our-story.html` |
| `contact.html`, `assets/js/forms.js` | `contact.html` |
| `body-candles.html` | `body-candles.html` |
| `scar-collection.html` | `scar-collection.html` |
| `sculpted-collection.html` | `sculpted-collection.html` |
| `gifts.html` | `gifts.html` |

### Shared Files (all pages potentially affected)

| File | Reason |
|---|---|
| `css/design-tokens.css` | Token values used by every page |
| `css/layout.css` | Container/grid system |
| `css/components.css` | Reusable UI components |
| `css/responsive.css` | Breakpoint rules |
| `assets/js/main.js` | Header, mobile menu, shared behavior |
| `assets/js/shared-layout.js` | Layout utilities |
| `assets/js/cart-state.js` | Cart state (header cart count on all pages, plus cart/product/checkout interactions) |
| `assets/js/currency.js` | Currency selector (all pages with prices) |
| `assets/js/choices.min.js` | Vendor dropdown library (used by 10+ pages) |
| `partials/site-header.html` | Shared header partial (all pages) |
| `partials/site-footer.html` | Shared footer partial (all pages) |
| `partials/mobile-menu.html` | Mobile menu partial (all pages) |

**Note:** `assets/js/qa-overlay.js` is dev-only tooling and is excluded from diff tracking.

When a shared file changes, the skill lists all potentially affected pages and asks the user which to include in the audit scope.

### Base Branch

The default base for `git diff` is `ejaz` (the main branch). The skill should accept an override if the user specifies a different base (e.g., `git diff some-other-branch...HEAD`).

### Fallback

If no diff is available (e.g., auditing from scratch or a fresh branch), the skill asks the user to specify pages manually.

---

## 2. Interaction Checks Data File

A new file `docs/qa/interaction_checks.json` stores per-page interaction checklists.

### Structure

```json
{
  "shop.html": [
    {
      "id": "shop-filters",
      "description": "Filter buttons toggle product visibility",
      "selector": ".filter-btn"
    },
    {
      "id": "shop-sort",
      "description": "Sort dropdown reorders product grid",
      "selector": ".sort-select"
    }
  ],
  "product.html": [
    {
      "id": "product-gallery",
      "description": "Gallery thumbnail click swaps main image",
      "selector": ".gallery-thumb"
    },
    {
      "id": "product-add-to-cart",
      "description": "Add to cart updates cart state and shows confirmation",
      "selector": ".add-to-cart-btn"
    }
  ]
}
```

### Fields

- `id` — stable identifier for the check
- `description` — what the agent verifies
- `selector` — CSS selector hint for where to look

### Conventions

- Populated for all 12 pages based on their current JS behaviors
- Updated as pages evolve — same pattern as `token_rules.json`
- The skill iterates these during audit and marks each pass/fail/skipped
- If a scoped page has no entry in `interaction_checks.json`, the skill warns and notes it as "untested (no interaction checks defined)" in the report

---

## 3. Audit Workflow (5 Steps)

Replaces the current 7-step generic workflow.

### Step 1: Auto-Scope

1. Run `git diff` against base branch
2. Map changed files → affected pages using the mapping table
3. If shared files changed: list all potentially affected pages, ask user to confirm scope
4. If no diff available: ask user to specify pages
5. Display final audit scope + any pages explicitly excluded

### Step 2: Run Automated Checks (Scoped Pages Only)

1. Start local server: `python -m http.server 4173` — if port 4173 is already in use, check for an existing server process and reuse it, or ask the user to free the port
2. Viewport audit: `python docs/qa/viewport_audit.py --page <page1> <page2> ...` (scoped to affected pages only)
3. Token audit: `python docs/qa/token_audit.py --page <page1> <page2> ...`
4. Any console error, overflow, or token failure = blocker (with resolution, see below)

### Step 3: Token Failure Resolution

For each token failure (`fail`, `missing_selector`, `invalid_token`):

1. Present failure details: selector, property, expected token, actual value
2. Ask the user:
   - **(A) Bug** — CSS needs to be fixed to match the token rule
   - **(B) Intentional** — CSS is correct (e.g., customer-requested change), update the rule
3. If (A): Add to blockers list, fix CSS during or after audit
4. If (B): Run `python docs/qa/token_audit.py --page <page> --update-rules` to update `token_rules.json`

### Step 4: Interaction Checklist

1. Load `docs/qa/interaction_checks.json` for scoped pages
2. Walk through each check, verify via browser or Playwright
3. Mark each: pass / fail / skipped (with reason)
4. Any failed primary interaction = blocker

### Step 5: Optional E2E

- Triggered by user request or `--e2e` flag
- Run Playwright tests for scoped pages via `e2e-testing` skill
- Failures added to blocker list

---

## 4. Output Contract & Evidence

### Report Format

```markdown
## QA Audit Report — <date>

### Scope
- Branch: <branch> vs <base>
- Changed files: <list>
- Pages audited: <list>
- Pages excluded (untested): <list with reason>

### Automated Results
- Viewport audit: X checks, Y failures
- Token audit: X checks, Y failures
  - Resolved as bug: <list>
  - Resolved as rule update: <list>

### Interaction Checklist
| Page | Check | Status | Notes |
|------|-------|--------|-------|
| shop.html | Filter buttons toggle visibility | pass | |
| shop.html | Sort dropdown reorders grid | fail | Dropdown doesn't close |

### E2E Results (if run)
- Tests run: X, Passed: Y, Failed: Z

### Blockers
- <grouped by type: overflow, console, token, interaction, e2e>

### Residual Risk
- <untested pages and why>

### Evidence
- Viewport screenshots: docs/qa/sweep-<timestamp>/
- Token report: docs/qa/token-audit-<timestamp>/
- Saved to: docs/qa/implementation/<TASK-ID>/
```

---

## 5. What Stays, What Changes, What's New

### Stays the same

- `token_audit.py` — no changes
- `token_rules.json` — same structure, updated via existing `--update-rules` flag
- Pre-commit hook — unchanged
- `references/` folder structure — unchanged
- Evidence saved under `docs/qa/implementation/<TASK-ID>/`

### Script changes (narrow scope)

- `viewport_audit.py` — add `--page` flag for scoped audits (optional; without flag, audits all pages as before). Also add 3 missing pages to the default list: `scar-collection.html`, `sculpted-collection.html`, `gifts.html`

### Workflow changes

- Skill workflow: 7 generic steps → 5 scoped, interactive steps
- Token failures prompt user for resolution direction (bug vs rule update)
- Report format expanded with interaction results, resolution decisions, residual risk

### New artifacts

- `docs/qa/interaction_checks.json` — per-page interaction checklists (initial population for all 12 pages)
- File-to-page mapping table inside the skill (structural, not a separate file)

### No changes to

- `index.html` or any HTML pages
- CSS or JS files
- `token_audit.py`, `precommit_token_gate.py`
- Other skills (`qa-guardrails`, `e2e-testing`, `pixel-perfect`)

---

## Release Blockers (unchanged)

- Any console error
- Any horizontal overflow
- Any broken primary interaction
- Any token audit `fail`, `missing_selector`, or `invalid_token` (unless resolved as intentional rule update)
- Any obvious mismatch against approved reference sections
