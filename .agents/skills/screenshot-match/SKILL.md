---
name: screenshot-match
description: Visual QA audit comparing Figma PNG exports against live Shopify theme using Claude Vision API. Use when asked to compare, audit, or verify visual fidelity between Figma designs and the live theme. Produces actionable Markdown reports (Critical/Notable/Marginal) covering typography, spacing, colors, and layout.
---

# Screenshot Match Skill

Compare Figma design exports against the live Shopify theme using Claude Vision API.

## Prerequisites

Install dependencies (one-time):
```bash
pip install -r .agents/skills/screenshot-match/scripts/requirements.txt
playwright install chromium
```

Set API key:
```bash
export ANTHROPIC_API_KEY=sk-...
```

Ensure the Shopify dev server is running:
```bash
cd theme && shopify theme dev --store=scentsbysara-dev.myshopify.com
```

## Quick Start

```bash
# Audit all configured pages
python .agents/skills/screenshot-match/scripts/audit.py

# Audit specific page
python .agents/skills/screenshot-match/scripts/audit.py --page homepage

# Skip interactive questions
python .agents/skills/screenshot-match/scripts/audit.py --no-interactive

# Dry run (validate config, no browser/API)
python .agents/skills/screenshot-match/scripts/audit.py --dry-run
```

## CLI Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--page <name>` | all | Audit specific page (name from config) |
| `--url <url>` | from config | Override Shopify dev server URL |
| `--password <pwd>` | from config | Shopify store password |
| `--no-interactive` | off | Skip clarifying questions, use hints only |
| `--output <path>` | `docs/qa-reports/` | Report output directory |
| `--dry-run` | off | Validate config and list pages, no browser/API |

## Setup

1. Export Figma frames as PNGs → drop into `figma-exports/` (repo root)
2. Add page entries to `.agents/skills/screenshot-match/config/page-mappings.json`
3. Set `ANTHROPIC_API_KEY` environment variable
4. Run the audit

## Workflow

1. Run audit → report at `docs/qa-reports/screenshot-match-<page>-<datetime>.md`
2. Answer any clarifying questions if prompted
3. Review report → pass to Claude or Codex to fix issues
4. Re-run to verify fixes

## Severity Levels

| Severity | Meaning |
|----------|---------|
| Critical | Wrong font-family, color channel diff >20, size diff >16px, missing element |
| Notable | Size diff 8–16px, color channel diff 10–20, layout misalignment |
| Marginal | Subtle diff within acceptable tolerance |
