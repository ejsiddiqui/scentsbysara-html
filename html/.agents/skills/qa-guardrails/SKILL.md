---
name: qa-guardrails
description: Use when setting up or running automated visual QA and CSS token compliance gates for static or server-rendered web projects, especially when preventing layout regressions, console/runtime issues, and design-token drift before manual QA or commits.
---

# QA Guardrails

Install and run a reusable QA workflow that combines viewport sweeps, token audits, and pre-commit blocking for token-relevant changes.

## Workflow

1. Bootstrap workflow files in the target repository
   - Run:
     ```bash
     python .agents/skills/qa-guardrails/scripts/install_qa_guardrails.py --repo <target-repo>
     ```
   - Use `--force` only when you intentionally want to overwrite existing workflow files.

2. Configure token rules
   - Edit `docs/qa/token_rules.json`.
   - Keep each rule as:
     - `selector`
     - `property`
     - `token`
     - `description`
   - Start with high-risk selectors first (headings, price text, CTAs, critical labels).

3. Enable hook-based commit gate
   - In target repo root:
     ```bash
     git config core.hooksPath .githooks
     ```
   - Gate behavior:
     - Runs token audit only when staged changes are token-relevant.
     - Blocks commit on `fail`, `missing_selector`, or `invalid_token`.

4. Run visual QA sweep
   - Command:
     ```bash
     python docs/qa/viewport_audit.py
     ```
   - Blockers:
     - Any console error
     - Any horizontal overflow
   - Optional strict mode:
     ```bash
     python docs/qa/viewport_audit.py --fail-on-blockers
     ```

5. Run token compliance audit
   - Single page:
     ```bash
     python docs/qa/token_audit.py --page product.html
     ```
   - Multiple pages:
     ```bash
     python docs/qa/token_audit.py --page product.html --page shop.html --page checkout.html
     ```
   - Blockers:
     - Any `fail`
     - Any `missing_selector`
     - Any `invalid_token`

6. Expand rules when new drift is found
   - Add a new rule immediately after discovering a token bug.
   - Re-run token audit for affected pages.

7. Ship gate before completion claims
   - Run token audit for changed pages.
   - Run viewport audit for changed flows/pages.
   - Confirm zero blockers in both reports.
   - Save evidence under `docs/qa/implementation/<TASK-ID>/`.

## Bundled Assets

- Installer script:
  - `scripts/install_qa_guardrails.py`
- Bootstrapped templates:
  - `assets/templates/docs/qa/agent-workflow.md`
  - `assets/templates/docs/qa/viewport_audit.py`
  - `assets/templates/docs/qa/token_audit.py`
  - `assets/templates/docs/qa/precommit_token_gate.py`
  - `assets/templates/docs/qa/token_rules.json`
  - `assets/templates/.githooks/pre-commit`

## Operating Rules

- Prefer these scripts over ad-hoc one-off QA commands so output stays consistent.
- Treat console errors and horizontal overflow as release blockers.
- Never merge token-sensitive UI changes with token-audit blockers still present.
- Keep workflow outputs timestamped and committed only when intentionally preserving evidence.

