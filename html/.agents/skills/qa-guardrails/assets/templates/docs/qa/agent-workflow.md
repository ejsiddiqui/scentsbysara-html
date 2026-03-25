# Agent QA Workflow

This workflow catches token/typography drift and layout/runtime regressions before manual QA.

## 0) One-Time Hook Setup

Enable repository-managed hooks:

```bash
git config core.hooksPath .githooks
```

After setup, each commit runs token audit when token-relevant files are staged.

## 1) Run Visual + Runtime QA

Run viewport sweep:

```bash
python docs/qa/viewport_audit.py
```

Optional strict mode (non-zero exit on blockers):

```bash
python docs/qa/viewport_audit.py --fail-on-blockers
```

Blockers:
- Any console errors
- Any horizontal overflow

## 2) Run Token Compliance QA

Run token audit:

```bash
python docs/qa/token_audit.py --page product.html
```

Multiple pages:

```bash
python docs/qa/token_audit.py --page product.html --page shop.html --page cart.html --page checkout.html
```

Blockers:
- Any `fail`
- Any `missing_selector`
- Any `invalid_token`

Rules live in `docs/qa/token_rules.json`.

## 3) Expand Rules When New Bugs Are Found

When QA finds a new token bug, add a rule with:
- `selector`
- `property`
- `token`
- `description`

Example:

```json
{
    "selector": ".product-price",
    "property": "font-size",
    "token": "--text-body-large",
    "description": "Product price should use body-large size."
}
```

## 4) Ship Gate

Before claiming a page is done:
- Run `python docs/qa/token_audit.py --page <page>.html`
- Run `python docs/qa/viewport_audit.py` (or targeted visual sweep)
- Confirm zero blockers in both reports
- Save implementation evidence under `docs/qa/implementation/<TASK-ID>/`

