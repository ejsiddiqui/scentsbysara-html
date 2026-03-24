---
name: qa-audit
description: Use when auditing one or more storefront pages for visual regressions, responsive issues, token drift, console/runtime failures, broken interactions, or release readiness against the repo's reference screenshots and QA scripts.
---

# QA Audit

Audit storefront pages with evidence, not guesswork. Use the repo's own reference screenshots, QA scripts, interaction checklists, and release blockers to verify whether a page is actually ready.

## When to Use

- Reviewing a page before completion, handoff, or commit
- Checking a route against `references/<page-name>/` screenshots
- Verifying responsive behavior across desktop, tablet, and mobile widths
- Looking for console errors, horizontal overflow, broken JS behavior, or token drift
- Producing implementation evidence under `docs/qa/implementation/<TASK-ID>/`

Do not use this skill to install QA tooling. Use `qa-guardrails` when the task is setting up or extending the QA system itself.

## Audit Workflow

### Step 1: Auto-Scope

Determine which pages need auditing from the current diff.

1. Run `git diff ejaz...HEAD --name-only` to list changed files (use a different base branch if the user specifies one).
2. Map changed files to affected pages using the table below.
3. If **shared files** changed, list all potentially affected pages and **ask the user** which to include.
4. If no diff is available (e.g., fresh branch or auditing from scratch), ask the user to specify pages manually.
5. Display the final audit scope and any pages explicitly excluded.

#### File-to-Page Mapping

**Direct mappings:**

| File | Affected Page |
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

**Shared files (all pages potentially affected — ask user to confirm scope):**

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

#### Special Rules

- Treat `index.html` as the approved baseline. Do not suggest homepage changes unless explicitly requested.
- If `assets/js/forms.js` changes, both `your-story.html` and `contact.html` are affected.

### Step 2: Run Automated Checks (Scoped Pages Only)

1. **Start local server:** `python -m http.server 4173`
   - If port 4173 is already in use, check for an existing server process and reuse it, or ask the user to free the port.
2. **Viewport audit:** `python docs/qa/viewport_audit.py --page <page1> <page2> ...`
   - Review the generated `docs/qa/sweep-<timestamp>/` screenshots and `report.json`.
   - Any console error or horizontal overflow is a release blocker.
3. **Token audit:** `python docs/qa/token_audit.py --page <page1> <page2> ...`
   - Rules live in `docs/qa/token_rules.json`.
   - Any `fail`, `missing_selector`, or `invalid_token` triggers the resolution flow below.

### Step 3: Token Failure Resolution

For each token failure (`fail`, `missing_selector`, `invalid_token`):

1. Present the failure details: selector, property, expected token, actual value.
2. Ask the user:
   - **(A) Bug** — the CSS needs to be fixed to match the token rule.
   - **(B) Intentional** — the CSS is correct (e.g., customer-requested change), update the rule to match.
3. If **(A)**: Add to the blockers list. Fix the CSS during or after the audit.
4. If **(B)**: Run `python docs/qa/token_audit.py --page <page> --update-rules` to update `token_rules.json`.

### Step 4: Interaction Checklist

1. Load `docs/qa/interaction_checks.json` for the scoped pages.
2. For each scoped page, include both its page-specific checks AND the `_shared` checks (header, mobile menu, search, footer accordion, currency, cart badge).
3. Walk through each check — verify via browser or Playwright.
4. Mark each: **pass** / **fail** / **skipped** (with reason).
5. Any failed primary interaction is a release blocker.
6. If a scoped page has no entry in `interaction_checks.json`, warn and note it as "untested (no interaction checks defined)" in the report.

### Step 5: Optional E2E

- Triggered by user request or `--e2e` flag.
- Run Playwright tests for scoped pages via the `e2e-testing` skill.
- Failures are added to the blocker list.

## Release Blockers

- Any console error
- Any horizontal overflow
- Any broken primary interaction
- Any token audit `fail`, `missing_selector`, or `invalid_token` (unless resolved as intentional rule update)
- Any obvious mismatch against approved reference sections

## Output Contract

When finishing an audit, provide a report with:

```
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

Save audit evidence under `docs/qa/implementation/<TASK-ID>/` when the task requires a completion record.

## Repo References

- `docs/qa/agent-workflow.md`
- `docs/qa/viewport_audit.py`
- `docs/qa/token_audit.py`
- `docs/qa/token_rules.json`
- `docs/qa/interaction_checks.json`
- `references/`
