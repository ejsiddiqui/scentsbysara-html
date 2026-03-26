---
name: visual-qa
description: Visual QA audit comparing HTML mockups against live Shopify theme. Use when asked to audit, QA, compare, or verify visual fidelity between mockup and theme. Compares computed CSS styles section-by-section at multiple viewports and generates actionable Markdown reports with severity levels (Critical/Notable/Marginal/Unknown). Replaces match-design and pixel-perfect skills.
---

# Visual QA Skill

Automate visual QA by comparing HTML mockups (`/html/`) against the live Shopify theme using Playwright.

## Prerequisites

Install dependencies (one-time):
```bash
pip install -r .agents/skills/visual-qa/scripts/requirements.txt
playwright install chromium
```

Ensure the Shopify dev server is running:
```bash
cd theme && shopify theme dev --store=scentsbysara-dev.myshopify.com
```

## Quick Start

```bash
# Audit entire site (core viewports: 1920, 1440, 768, 480)
python .agents/skills/visual-qa/scripts/audit.py

# Audit specific page
python .agents/skills/visual-qa/scripts/audit.py --page homepage

# Audit specific section (requires --page)
python .agents/skills/visual-qa/scripts/audit.py --page homepage --section "Hero Slideshow"

# Full viewports (adds 1024, 390)
python .agents/skills/visual-qa/scripts/audit.py --viewports full

# With image visual diff
python .agents/skills/visual-qa/scripts/audit.py --image-diff

# Validate config without running browser
python .agents/skills/visual-qa/scripts/audit.py --dry-run
```

## CLI Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--page <name>` | all | Audit specific page (name from config) |
| `--section <name>` | all | Audit specific section (requires `--page`) |
| `--url <url>` | `http://127.0.0.1:9292` | Shopify dev server URL |
| `--viewports full` | core | Use full viewport set |
| `--tolerance <px>` | 2 | Pixel tolerance threshold |
| `--image-diff` | off | Enable visual screenshot diff for images |
| `--svg-compare` | off | Enable SVG content/path comparison |
| `--output <path>` | `docs/qa-reports/` | Report output directory |
| `--dry-run` | off | Validate config and list sections |
| `--password <pwd>` | from config | Shopify store password for dev store |

## Configuration

Edit `config/page-mappings.json` to define page-to-section-to-element mappings.

To detect config drift after mockup changes:
```bash
python .agents/skills/visual-qa/scripts/scaffold_mappings.py --diff
```

## Workflow

1. Run audit → get report at `docs/qa-reports/visual-qa-<page>-<datetime>.md`
2. Implement fixes based on report (each issue lists element, property, expected/actual, severity, theme file)
3. Re-run audit → verify fixes
4. Repeat until no Critical or Notable issues remain
5. Marginal issues are acceptable (flagged, not blocking)

## Severity Levels

| Severity | Meaning |
|----------|---------|
| Critical | Large diff (>tolerance*2), non-numeric mismatch, color channel diff >10, missing property |
| Notable | Medium diff (tolerance to tolerance*2), color channel diff >5 |
| Marginal | Within tolerance but non-zero |
| Unknown | Selector not found — stale config signal |

## Report Format

Reports saved to `docs/qa-reports/visual-qa-<page>-<YYYY-MM-DD-HHMM>.md`

Grouped by: **Page > Section > Category (Viewport)**

Each issue row: Element selector | Property | Expected | Actual | Severity

Unknown selectors listed prominently in report summary.

## Handling Mockup Changes

Run scaffold diff after mockup updates:
```bash
python .agents/skills/visual-qa/scripts/scaffold_mappings.py --diff
```

Output shows: new pages, stale selectors, new elements found in HTML.
