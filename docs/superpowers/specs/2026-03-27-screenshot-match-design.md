# Screenshot Match — Design Spec

**Date:** 2026-03-27
**Status:** Approved

---

## Goal

Build a new agent skill (`screenshot-match`) that compares manually-exported Figma PNG screenshots against the live Shopify theme, using Claude Vision API to identify specific visual differences, and produces actionable Markdown reports that Claude or Codex can act on to fix issues.

---

## Architecture

New skill at `.agents/skills/screenshot-match/` — fully independent of `visual-qa`.

### Pipeline (per page)

1. Load Figma PNG from `figma-exports/` folder
2. Playwright captures a screenshot of the live theme at the matching viewport
3. Both images sent to Claude Vision API with a structured prompt (including `hints` context)
4. AI returns a list of specific visual differences grouped by category
5. If AI response contains uncertainty markers ("appears to be", "possibly", "unclear") → extract questions, ask user, re-run with answers injected (max one re-run per page)
6. Differences formatted into a `.md` report

### File Structure

```
.agents/skills/screenshot-match/
├── SKILL.md
├── config/
│   └── page-mappings.json
├── scripts/
│   ├── audit.py          — CLI entry point & orchestrator
│   ├── capture_theme.py  — Playwright screenshot capture
│   ├── compare.py        — Claude Vision API call & response parsing
│   ├── report.py         — Markdown report generator
│   └── requirements.txt
```

---

## Configuration

**`config/page-mappings.json`:**

```json
{
  "defaults": {
    "themeBaseUrl": "http://127.0.0.1:9292",
    "figmaDir": "figma-exports",
    "storePassword": "",
    "hints": {
      "fontFamilies": ["Cormorant Garamond", "Jost"],
      "brandColors": ["#1a1a1a", "#f5f0eb", "#c9a96e"],
      "notes": ""
    }
  },
  "pages": [
    {
      "name": "Homepage",
      "figmaImage": "homepage-1440.png",
      "themeUrl": "/",
      "viewport": 1440
    }
  ]
}
```

**`hints`** pre-answers common AI ambiguities so the Vision API returns precise values (exact font names, hex colors) rather than approximations.

Each page entry requires:
- `name` — display name used in reports and CLI filtering
- `figmaImage` — filename relative to `figmaDir`
- `themeUrl` — path on the Shopify dev server (e.g. `/`, `/collections/all`)
- `viewport` — integer width in px (e.g. `1440`); if omitted, asked interactively at runtime

---

## CLI

```bash
# Audit all pages
python .agents/skills/screenshot-match/scripts/audit.py

# Single page
python .agents/skills/screenshot-match/scripts/audit.py --page homepage

# Skip interactive clarifying questions (use hints only)
python .agents/skills/screenshot-match/scripts/audit.py --no-interactive

# Override theme server URL
python .agents/skills/screenshot-match/scripts/audit.py --url http://127.0.0.1:9292

# Shopify dev store password
python .agents/skills/screenshot-match/scripts/audit.py --password <pwd>

# Override output directory
python .agents/skills/screenshot-match/scripts/audit.py --output docs/qa-reports
```

---

## Clarifying Questions

The skill asks targeted questions in two situations:

1. **Missing config values** — if `viewport` is missing from a page entry, ask before capturing the theme screenshot
2. **AI uncertainty** — after Claude Vision analysis, if the response contains uncertainty markers ("appears to be", "possibly", "unclear"), extract those specific questions, present them to the user, then re-run the comparison with the answers injected into the prompt

Maximum one re-run per page to avoid loops. Use `--no-interactive` to suppress all questions and rely only on `hints`.

---

## Claude Vision Comparison (`compare.py`)

**Model:** `claude-sonnet-4-6` with vision input

**Prompt structure:**
- System: instructs Claude to act as a visual QA reviewer, output structured diff tables only
- User message includes:
  - Figma PNG (base64)
  - Theme screenshot (base64)
  - `hints` context (font families, brand colors, notes)
  - Request for differences grouped by: Typography, Spacing & Layout, Colors & Backgrounds, Components & Sizing
  - Request for severity classification per issue

**Response parsing:**
- Expect Markdown tables in the response
- Parse into structured `Issue` objects: `element`, `property`, `expected`, `actual`, `severity`
- If parsing fails, save raw AI response to report with `[PARSE ERROR]` label and continue

---

## Report Format

Reports saved to `docs/qa-reports/screenshot-match-<page>-<YYYY-MM-DD-HHMM>.md`

Screenshots saved alongside:
- `docs/qa-reports/screenshots/screenshot-match-<page>-<vp>-figma.png`
- `docs/qa-reports/screenshots/screenshot-match-<page>-<vp>-theme.png`

### Report structure

```markdown
# Screenshot Match Report — Homepage — 2026-03-27 14:30

**Figma source:** figma-exports/homepage-1440.png
**Theme URL:** http://127.0.0.1:9292/
**Viewport:** 1440px

## Summary
- Critical: 3
- Notable: 7
- Marginal: 2

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

### Severity Levels

| Severity | Meaning |
|----------|---------|
| Critical | Wrong font-family, color channel diff >20, size diff >16px, missing element |
| Notable | Size diff 8–16px, color channel diff 10–20, layout misalignment |
| Marginal | Subtle diff within acceptable tolerance |

---

## Error Handling

| Situation | Behaviour |
|-----------|-----------|
| Figma PNG not found | Print error with expected path, skip page |
| Theme server not reachable | Retry 3 times with prompt to start server, then exit |
| `ANTHROPIC_API_KEY` not set | Exit immediately with clear message |
| AI response unparseable | Save raw response to report with `[PARSE ERROR]`, continue |
| Element flagged by AI not found in theme | Report as `Unknown` severity |

---

## Dependencies

**`requirements.txt`:**
```
playwright>=1.40.0
anthropic>=0.25.0
Pillow>=10.0.0
```

**One-time setup:**
```bash
pip install -r .agents/skills/screenshot-match/scripts/requirements.txt
playwright install chromium
export ANTHROPIC_API_KEY=sk-...
```

---

## Workflow

1. Export Figma frames as PNGs → drop into `figma-exports/`
2. Add page entries to `config/page-mappings.json`
3. Start Shopify dev server: `cd theme && shopify theme dev --store=scentsbysara-dev.myshopify.com`
4. Run: `python .agents/skills/screenshot-match/scripts/audit.py --page homepage`
5. Answer any clarifying questions if prompted
6. Review report at `docs/qa-reports/screenshot-match-homepage-*.md`
7. Pass report to Claude/Codex to fix issues
8. Re-run to verify fixes

---

## What This Skill Is Not

- Not a pixel diff tool — it uses AI vision to identify semantic differences, not raw pixel counts
- Not a replacement for `visual-qa` — `visual-qa` compares HTML mockups via computed CSS (precise, property-level). `screenshot-match` compares Figma PNGs via AI vision (approximate, broader coverage). Use both together for full coverage.
