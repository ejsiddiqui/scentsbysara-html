---
name: qa-audit
description: Use when auditing one or more storefront pages for visual regressions, responsive issues, token drift, console/runtime failures, broken interactions, or release readiness against the repo's reference screenshots and QA scripts.
---

# QA Audit

Audit storefront pages with evidence, not guesswork. Use the repo's own reference screenshots, QA scripts, and release blockers to verify whether a page is actually ready.

## When to Use

- Reviewing a page before completion, handoff, or commit
- Checking a route against `references/<page-name>/` screenshots
- Verifying responsive behavior across desktop, tablet, and mobile widths
- Looking for console errors, horizontal overflow, broken JS behavior, or token drift
- Producing implementation evidence under `docs/qa/implementation/<TASK-ID>/`

Do not use this skill to install QA tooling. Use `qa-guardrails` when the task is setting up or extending the QA system itself.

## Audit Workflow

1. Define scope before testing
   - List the exact pages being audited.
   - Map each page to its reference folder under `references/`.
   - Treat `index.html` as the approved baseline and do not suggest homepage changes unless explicitly requested.
   - Note shared files that can affect multiple pages: `css/*.css`, `assets/js/main.js`, `assets/js/shared-layout.js`, `assets/js/cart-state.js`.

2. Run the local preview
   - Start the static site from repo root:
     ```bash
     python -m http.server 4173
     ```
   - Use `http://127.0.0.1:4173`.

3. Perform visual and responsive checks
   - Compare each target page to its `references/<page-name>/` screenshots section-by-section.
   - Verify layout at `1920`, `1440`, `1024`, `768`, `390`, and `375` widths.
   - Reuse homepage patterns for spacing, typography, header/footer behavior, and component structure when judging consistency.
   - Treat these as blockers:
     - horizontal overflow
     - broken alignment or stacking
     - missing imagery or incorrect aspect ratios
     - mismatched spacing/typography against the shared design language

4. Run automated viewport QA
   - Run:
     ```bash
     python docs/qa/viewport_audit.py
     ```
   - Review the generated `docs/qa/sweep-<timestamp>/` screenshots and `report.json`.
   - Any console error or horizontal overflow is a release blocker.

5. Run token and typography compliance checks
   - Run token audit for each affected page:
     ```bash
     python docs/qa/token_audit.py --page <page>.html
     ```
   - Treat any `fail`, `missing_selector`, or `invalid_token` result as a blocker.
   - Rules live in `docs/qa/token_rules.json`.
   - If a design change is intentional and approved, update rules explicitly instead of ignoring failures:
     ```bash
     python docs/qa/token_audit.py --page <page>.html --update-rules
     ```

6. Check functional behavior
   - Verify the page-specific scripts in `assets/js/` still work as expected.
   - Check navigation, filters, selects, gallery behavior, cart actions, form validation, and checkout interactions relevant to the audited page.
   - Flag broken links, missing `alt` text, dead buttons, and JS-driven states that fail silently.

7. Save evidence and report findings
   - Save audit evidence under `docs/qa/implementation/<TASK-ID>/` when the task requires a completion record.
   - Report findings ordered by severity with:
     - page
     - breakpoint
     - selector or component
     - expected behavior
     - actual behavior
     - blocker status

## Release Blockers

- Any console error
- Any horizontal overflow
- Any broken primary interaction
- Any token audit `fail`, `missing_selector`, or `invalid_token`
- Any obvious mismatch against approved reference sections

## Output Contract

When finishing an audit, provide:

1. Pages audited
2. Commands run
3. Blockers found or explicit confirmation that none were found
4. Evidence location, if artifacts were saved
5. Residual risks or untested areas, if any

## Repo References

- `docs/qa/agent-workflow.md`
- `docs/qa/viewport_audit.py`
- `docs/qa/token_audit.py`
- `docs/qa/token_rules.json`
- `references/`
