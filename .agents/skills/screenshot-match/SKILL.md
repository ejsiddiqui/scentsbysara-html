---
name: screenshot-match
description: Visual QA audit comparing Figma PNG exports against live Shopify theme. Use when asked to compare, audit, or verify visual fidelity between Figma designs and the live theme. Captures screenshots with Playwright, then Claude reads both images directly and produces actionable Markdown reports (Critical/Notable/Marginal) covering typography, spacing, colors, and layout. No API key required.
---

# Screenshot Match Skill

Compare Figma design exports against the live Shopify theme. Claude reads both images directly — no external API key needed.

## Prerequisites

Install dependencies (one-time):
```bash
pip install -r .agents/skills/screenshot-match/scripts/requirements.txt
playwright install chromium
```

Ensure the Shopify dev server is running:
```bash
cd theme && shopify theme dev --store=scentsbysara-dev.myshopify.com
```

## Workflow

### Step 1 — Capture screenshots

```bash
python .agents/skills/screenshot-match/scripts/audit.py --page homepage --password <pwd>
```

This outputs the paths to both images, e.g.:
```
  Figma PNG:        docs/qa-reports/screenshots/screenshot-match-homepage-1440-figma.png
  Theme screenshot: docs/qa-reports/screenshots/screenshot-match-homepage-1440-theme.png
  Font families:    Cormorant Garamond, Jost
  Brand colors:     #1a1a1a, #f5f0eb, #c9a96e
```

### Step 2 — Read and compare both images

Use the Read tool to open both image files. Compare them visually, looking for differences in:

- **Typography** — font-family, font-size, font-weight, line-height, letter-spacing, color
- **Spacing & Layout** — padding, margin, gap, alignment, positioning
- **Colors & Backgrounds** — background-color, border-color, text color
- **Components & Sizing** — button size, image dimensions, component proportions

Use the design hints from Step 1 output (font families, brand colors) to make precise identifications rather than approximations.

### Step 3 — Ask clarifying questions if needed

If anything is genuinely unclear from the images (e.g. two similar fonts that are hard to distinguish, an exact hex color), ask the user before finalising the report. Be specific about what you can't determine.

### Step 4 — Write the report

Save the report to `docs/qa-reports/screenshot-match-<page>-<YYYY-MM-DD-HHMM>.md` using the format below.

## Report Format

```markdown
# Screenshot Match Report — <Page> — <YYYY-MM-DD HH:MM>

**Figma source:** <path>
**Theme URL:** <url>
**Viewport:** <N>px
**Figma screenshot:** <path>
**Theme screenshot:** <path>

## Summary
- Critical: N
- Notable: N
- Marginal: N

---

## Typography

| Element | Property | Expected (Figma) | Actual (Theme) | Severity |
|---------|----------|-----------------|----------------|----------|
| Hero heading | font-family | Cormorant Garamond | Jost | Critical |

## Spacing & Layout

| Element | Property | Expected (Figma) | Actual (Theme) | Severity |
|---------|----------|-----------------|----------------|----------|
| Hero section | padding-top | 120px | 80px | Critical |

## Colors & Backgrounds

...

## Components & Sizing

...
```

## Severity Levels

| Severity | Meaning |
|----------|---------|
| Critical | Wrong font-family, color channel diff >20, size diff >16px, missing element |
| Notable | Size diff 8–16px, color channel diff 10–20, layout misalignment |
| Marginal | Subtle diff within acceptable tolerance |

## CLI Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--page <name>` | all | Capture specific page (name from config) |
| `--url <url>` | from config | Override Shopify dev server URL |
| `--password <pwd>` | from config | Shopify store password |
| `--no-interactive` | off | Skip interactive viewport prompts |
| `--output <path>` | `docs/qa-reports/` | Screenshot output directory |
| `--dry-run` | off | Validate config, no browser calls |

## Setup

1. Export Figma frames as PNGs → drop into `figma-exports/` (repo root)
2. Add page entries to `.agents/skills/screenshot-match/config/page-mappings.json`
3. Start Shopify dev server
4. Run Step 1 above — then read images and write report
