# QA Audit Skill Improvement — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve the QA audit skill with diff-based auto-scoping, per-page interaction checklists, token failure resolution flow, and optional E2E integration.

**Architecture:** Three deliverables — (1) add `--page` flag to `viewport_audit.py` + add missing pages, (2) create `docs/qa/interaction_checks.json` with checklists for all 12 pages, (3) rewrite `.agents/skills/qa-audit/SKILL.md` with the new 5-step workflow.

**Tech Stack:** Python (argparse for viewport_audit.py), JSON (interaction checks), Markdown (skill file)

**Spec:** `docs/superpowers/specs/2026-03-24-qa-audit-skill-improvement-design.md`

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Modify | `docs/qa/viewport_audit.py` | Add `--page` flag + 3 missing pages |
| Create | `docs/qa/interaction_checks.json` | Per-page interaction checklists for all 12 pages |
| Rewrite | `.agents/skills/qa-audit/SKILL.md` | New 5-step scoped audit workflow |

---

### Task 1: Add `--page` flag and missing pages to `viewport_audit.py`

**Files:**
- Modify: `docs/qa/viewport_audit.py:15-25` (PAGES list), `docs/qa/viewport_audit.py:160-172` (main function)

- [ ] **Step 1: Add the 3 missing pages to PAGES list**

In `docs/qa/viewport_audit.py`, update the `PAGES` list (line 15-25) to include all 12 pages:

```python
PAGES = [
    "index.html",
    "body-candles.html",
    "our-story.html",
    "your-story.html",
    "shop.html",
    "product.html",
    "cart.html",
    "checkout.html",
    "contact.html",
    "scar-collection.html",
    "sculpted-collection.html",
    "gifts.html",
]
```

- [ ] **Step 2: Add argparse with `--page` flag**

Replace the `main()` function (lines 160-172) with:

```python
def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Viewport sweep audit")
    parser.add_argument(
        "--page",
        nargs="+",
        help="Specific pages to audit (e.g., --page shop.html cart.html). Defaults to all pages.",
    )
    args = parser.parse_args()

    if args.page:
        # Validate provided pages exist in known list
        unknown = [p for p in args.page if p not in PAGES]
        if unknown:
            print(f"Warning: unknown pages will still be audited: {unknown}")
        pages_to_audit = args.page
    else:
        pages_to_audit = PAGES

    server = start_server()
    try:
        report = run_audit(pages_to_audit)
        print(json.dumps(report["summary"], indent=2))
        print(report["out_dir"])
    finally:
        server.shutdown()
        server.server_close()
```

- [ ] **Step 3: Update `run_audit` to accept a pages parameter**

Change the `run_audit` signature (line 51) from:

```python
def run_audit() -> dict:
```

to:

```python
def run_audit(pages: list[str] | None = None) -> dict:
    if pages is None:
        pages = PAGES
```

And update line 72 from `for page_name in PAGES:` to `for page_name in pages:`.

- [ ] **Step 4: Verify the script still works without `--page` flag**

Run: `python docs/qa/viewport_audit.py --help`
Expected: Shows usage with `--page` option documented.

Run (dry check): Confirm `python docs/qa/viewport_audit.py` still works with all 12 pages as default.

- [ ] **Step 5: Commit**

```bash
git add docs/qa/viewport_audit.py
git commit -m "feat: add --page flag and 3 missing pages to viewport_audit.py"
```

---

### Task 2: Create `docs/qa/interaction_checks.json`

**Files:**
- Create: `docs/qa/interaction_checks.json`

- [ ] **Step 1: Create the interaction checks file**

Create `docs/qa/interaction_checks.json` with the full per-page checklists:

```json
{
  "index.html": [
    {
      "id": "home-hero-dots",
      "description": "Hero slider dot navigation switches slides",
      "selector": ".home-hero .slider-dots .dot"
    },
    {
      "id": "home-hero-swipe",
      "description": "Hero slider responds to drag/swipe gestures",
      "selector": ".hero-slider"
    },
    {
      "id": "home-bestsellers-carousel",
      "description": "Bestsellers carousel prev/next buttons scroll products",
      "selector": "[data-carousel-prev], [data-carousel-next]"
    },
    {
      "id": "home-testimonials-dots",
      "description": "Testimonials slider dot navigation switches slides",
      "selector": ".testimonials-section .slider-dots .dot"
    }
  ],
  "shop.html": [
    {
      "id": "shop-filter-toggle",
      "description": "Filter button opens/closes the filter overlay panel",
      "selector": ".filter-btn"
    },
    {
      "id": "shop-filter-apply",
      "description": "Apply filters button filters the product grid",
      "selector": ".apply-filters"
    },
    {
      "id": "shop-filter-clear",
      "description": "Clear filters button resets all filter selections",
      "selector": ".clear-filters"
    },
    {
      "id": "shop-sort",
      "description": "Sort dropdown reorders product grid",
      "selector": "#sort-select"
    },
    {
      "id": "shop-color-swatch",
      "description": "Color swatch selection updates product card image",
      "selector": ".swatch"
    },
    {
      "id": "shop-size-select",
      "description": "Size dropdown selects product variant",
      "selector": ".size-select"
    },
    {
      "id": "shop-add-to-bag",
      "description": "Add to bag button adds item to cart and updates cart badge",
      "selector": ".btn-shop-now"
    }
  ],
  "product.html": [
    {
      "id": "product-gallery-thumbs",
      "description": "Gallery thumbnail click swaps main image",
      "selector": ".thumb-wrap"
    },
    {
      "id": "product-gallery-arrows",
      "description": "Gallery prev/next arrows navigate images",
      "selector": ".product-gallery-arrow"
    },
    {
      "id": "product-gallery-swipe",
      "description": "Gallery viewport responds to touch swipe",
      "selector": ".product-gallery-viewport"
    },
    {
      "id": "product-color-swatch",
      "description": "Color swatch selection updates variant and label",
      "selector": ".swatch-lg"
    },
    {
      "id": "product-size-pill",
      "description": "Size/shape pill selection updates variant",
      "selector": ".pill-btn"
    },
    {
      "id": "product-quantity",
      "description": "Quantity +/- buttons update count within valid range",
      "selector": ".qty-btn"
    },
    {
      "id": "product-add-to-bag",
      "description": "Add to bag button adds item to cart and shows confirmation",
      "selector": ".btn-add-bag"
    },
    {
      "id": "product-accordion",
      "description": "Accordion headers expand/collapse detail sections",
      "selector": ".accordion-header"
    }
  ],
  "cart.html": [
    {
      "id": "cart-quantity-adjust",
      "description": "Quantity +/- buttons update item count and recalculate totals",
      "selector": "[data-qty-change]"
    },
    {
      "id": "cart-remove-item",
      "description": "Remove button removes item and updates totals",
      "selector": "[data-remove-line]"
    },
    {
      "id": "cart-empty-state",
      "description": "Empty cart shows empty state message with continue shopping link",
      "selector": "#cart-empty"
    },
    {
      "id": "cart-totals-display",
      "description": "Subtotal, shipping, tax, and total display correctly",
      "selector": "#cart-subtotal, #cart-shipping, #cart-tax, #cart-total"
    },
    {
      "id": "cart-checkout-link",
      "description": "Checkout button navigates to checkout page",
      "selector": "a[href=\"checkout.html\"]"
    }
  ],
  "checkout.html": [
    {
      "id": "checkout-form-validation",
      "description": "Required fields show validation errors when empty on submit",
      "selector": ".field-error"
    },
    {
      "id": "checkout-card-formatting",
      "description": "Card number auto-formats with spaces, expiry as MM/YY",
      "selector": "#cardnumber, #expiry, #cvc"
    },
    {
      "id": "checkout-order-summary",
      "description": "Order summary shows correct items, subtotal, shipping, tax, total",
      "selector": "#checkout-summary-items, #checkout-total"
    },
    {
      "id": "checkout-submit",
      "description": "Complete order button submits form with validation",
      "selector": "button[type=\"submit\"]"
    }
  ],
  "your-story.html": [
    {
      "id": "story-form-validation",
      "description": "Required fields show validation errors when empty on submit",
      "selector": ".field-error"
    },
    {
      "id": "story-char-counter",
      "description": "Character counter updates as user types in textarea",
      "selector": "[data-counter-for]"
    },
    {
      "id": "story-form-submit",
      "description": "Submit button triggers validation and shows status message",
      "selector": "button[type=\"submit\"]"
    }
  ],
  "our-story.html": [
    {
      "id": "our-story-cta",
      "description": "Shop all CTA button navigates to shop page",
      "selector": "a[href=\"shop.html\"]"
    }
  ],
  "contact.html": [
    {
      "id": "contact-form-validation",
      "description": "Required fields show validation errors when empty on submit",
      "selector": ".field-error"
    },
    {
      "id": "contact-char-counter",
      "description": "Message character counter updates as user types",
      "selector": "[data-counter-for=\"contact-message\"]"
    },
    {
      "id": "contact-topic-dropdown",
      "description": "Topic dropdown selects subject category",
      "selector": "#contact-topic"
    },
    {
      "id": "contact-form-submit",
      "description": "Submit button triggers validation and shows status message",
      "selector": "button[type=\"submit\"]"
    }
  ],
  "body-candles.html": [
    {
      "id": "body-candles-product-links",
      "description": "Product card links navigate to product page",
      "selector": ".product-image-wrap, .product-btn"
    },
    {
      "id": "body-candles-cta",
      "description": "Feature CTA button navigates to target page",
      "selector": ".btn-solid"
    },
    {
      "id": "body-candles-prices",
      "description": "Product prices display and update with currency selection",
      "selector": "[data-price-gbp]"
    }
  ],
  "scar-collection.html": [
    {
      "id": "scar-filter-toggle",
      "description": "Filter button opens/closes filter overlay",
      "selector": ".filter-btn"
    },
    {
      "id": "scar-sort",
      "description": "Sort dropdown reorders product grid",
      "selector": "#sort-select"
    },
    {
      "id": "scar-color-swatch",
      "description": "Color swatch selection updates product card",
      "selector": ".swatch"
    },
    {
      "id": "scar-size-select",
      "description": "Size dropdown selects product variant",
      "selector": ".size-select"
    },
    {
      "id": "scar-product-link",
      "description": "Product card navigates to product page",
      "selector": ".product-btn"
    }
  ],
  "sculpted-collection.html": [
    {
      "id": "sculpted-filter-toggle",
      "description": "Filter button opens/closes filter overlay",
      "selector": ".filter-btn"
    },
    {
      "id": "sculpted-sort",
      "description": "Sort dropdown reorders product grid",
      "selector": "#sort-select"
    },
    {
      "id": "sculpted-color-swatch",
      "description": "Color swatch selection updates product card",
      "selector": ".swatch"
    },
    {
      "id": "sculpted-size-select",
      "description": "Size dropdown selects product variant",
      "selector": ".size-select"
    },
    {
      "id": "sculpted-product-link",
      "description": "Product card navigates to product page",
      "selector": ".product-btn"
    }
  ],
  "gifts.html": [
    {
      "id": "gifts-product-links",
      "description": "Product card links navigate to product page",
      "selector": ".product-image-wrap, .product-btn"
    },
    {
      "id": "gifts-collection-cta",
      "description": "Discover collection buttons navigate to collection pages",
      "selector": ".btn-solid"
    },
    {
      "id": "gifts-prices",
      "description": "Product prices display and update with currency selection",
      "selector": "[data-price-gbp]"
    }
  ],
  "_shared": [
    {
      "id": "shared-hamburger",
      "description": "Hamburger button opens mobile menu overlay",
      "selector": ".hamburger-btn"
    },
    {
      "id": "shared-mobile-menu-close",
      "description": "Mobile menu overlay closes on close button or overlay click",
      "selector": ".mobile-menu-overlay"
    },
    {
      "id": "shared-mobile-shop-submenu",
      "description": "Mobile shop toggle opens submenu panel, back button returns",
      "selector": ".mobile-shop-toggle, .sub-back-btn"
    },
    {
      "id": "shared-search-toggle",
      "description": "Search toggle opens/closes search overlay",
      "selector": ".search-toggle"
    },
    {
      "id": "shared-header-scroll",
      "description": "Header hides on scroll down, shows on scroll up",
      "selector": ".site-header"
    },
    {
      "id": "shared-footer-accordion",
      "description": "Footer accordion sections expand/collapse on mobile",
      "selector": ".footer-accordion-trigger"
    },
    {
      "id": "shared-currency-select",
      "description": "Currency dropdown updates all prices on page",
      "selector": "[data-currency-select]"
    },
    {
      "id": "shared-cart-badge",
      "description": "Cart badge count updates when items are added/removed",
      "selector": "[data-cart-count]"
    }
  ]
}
```

**Note:** The `_shared` key holds interactions from `main.js` that apply to all pages. The skill should include `_shared` checks for every audited page.

- [ ] **Step 2: Validate JSON is well-formed**

Run: `python -c "import json; json.load(open('docs/qa/interaction_checks.json')); print('valid')"`
Expected: `valid`

- [ ] **Step 3: Commit**

```bash
git add docs/qa/interaction_checks.json
git commit -m "feat: add per-page interaction checklists for QA audit"
```

---

### Task 3: Rewrite the QA audit skill

**Files:**
- Rewrite: `.agents/skills/qa-audit/SKILL.md`

- [ ] **Step 1: Rewrite the skill file**

Replace the entire content of `.agents/skills/qa-audit/SKILL.md` with:

````markdown
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
````

- [ ] **Step 2: Review the skill for completeness**

Verify the skill references all the correct file paths, commands, and conventions from the spec.

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/qa-audit/SKILL.md
git commit -m "feat: rewrite qa-audit skill with scoped workflow and interaction checklists"
```

---

### Task 4: Final Verification

- [ ] **Step 1: Verify viewport_audit.py runs with `--page` flag**

Run: `python docs/qa/viewport_audit.py --page shop.html --help` or a quick sanity check.

- [ ] **Step 2: Verify interaction_checks.json is valid**

Run: `python -c "import json; d=json.load(open('docs/qa/interaction_checks.json')); print(f'{len(d)} pages, {sum(len(v) for v in d.values())} checks')"`
Expected: `13 pages, XX checks` (12 pages + `_shared`)

- [ ] **Step 3: Verify skill file renders correctly**

Read `.agents/skills/qa-audit/SKILL.md` and confirm all markdown tables, code blocks, and structure are well-formed.

- [ ] **Step 4: Commit all remaining changes (if any)**

```bash
git status
# If any unstaged changes remain, stage and commit
```
