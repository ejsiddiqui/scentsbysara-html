# Visual QA Skill — Design Spec

**Date:** 2026-03-27
**Location:** `.agents/skills/visual-qa/`
**Replaces:** `.agents/skills/match-design/`, `.agents/skills/pixel-perfect/`

## Purpose

Automate visual QA by comparing HTML mockups (`/html/`) against the live Shopify theme (`/theme/`). Uses Playwright to render both sources in a real browser, extracts computed styles section-by-section at multiple viewports, and produces an actionable Markdown report for AI agents (Claude Code, Codex, Gemini) to implement fixes.

## Core Workflow

1. Agent invokes skill (e.g., "audit the homepage")
2. Skill checks if Shopify dev server is reachable at configured URL
   - If not reachable: asks user to start it, waits for confirmation, retries
3. Spins up a local HTTP server for `/html/` directory
4. Reads page-section mapping config (`config/page-mappings.json`)
5. For each section, at each viewport:
   a. Opens mockup page in Playwright, scrolls to section, extracts computed styles
   b. Opens Shopify theme page in Playwright, scrolls to section, extracts computed styles
   c. Diffs the values with configurable tolerance
   d. Takes screenshots of both for visual reference
6. Compiles Markdown report grouped by: Page > Section > Category (Viewport)
7. Saves report to `docs/qa-reports/`
8. After fixes are implemented, re-run audit to verify

### Pre-extraction Requirements

- **Font loading:** The script must wait for `document.fonts.ready` before extracting styles, to avoid capturing fallback font values
- **Dynamic content:** Only the default/visible state is audited. For slideshows, the first/active slide is captured. Hidden elements (cart drawer, mobile menu) are skipped unless explicitly targeted via `--section`
- **Static file serving:** `serve_html.py` serves the entire `/html/` directory tree (CSS, fonts, images, JS) to ensure accurate rendering

## Viewports

| Set | Widths |
|-----|--------|
| **Core** (default) | 1920px, 1440px, 768px, 480px |
| **Full** (`--viewports full`) | 1920px, 1440px, 1024px, 768px, 480px, 390px |

## Audit Categories & Properties

### 1. Typography
- `font-family`, `font-size`, `font-weight`, `font-style`
- `line-height`, `letter-spacing`, `text-transform`
- `color`, `text-align`, `text-decoration`

### 2. Sizes & Spacing
- `width`, `height`, `min-width`, `max-width`, `min-height`, `max-height`
- `padding` (all 4 sides), `margin` (all 4 sides)
- `border-width`, `border-style`, `border-color`, `border-radius`
- `box-shadow` (used as sub-pixel border workaround in this project)

### 3. Layout & Positioning
- `display`, `flex-direction`, `justify-content`, `align-items`, `gap`
- `grid-template-columns`, `grid-template-rows`
- `position`, `top`, `right`, `bottom`, `left`

### 4. Images
- Rendered container `width`, `height`, aspect ratio
- `object-fit`, `object-position`, `border-radius`
- Visual screenshot diff (with `--image-diff` flag)

### 5. Icons & SVGs
- Rendered `width`, `height`
- `fill`, `stroke`, `color`
- Spacing/margins around the icon
- SVG content/path comparison (with `--svg-compare` flag)

### 6. Backgrounds & Visual
- `background-color`, `background-image`
- `box-shadow`, `opacity`

## Element Matching Strategy

Elements within sections are matched explicitly via the `elements` array in the config. Each entry maps a named element between mockup and theme using CSS selectors:

```json
{
  "name": "Hero Slideshow",
  "mockupSelector": ".hero-section",
  "themeSelector": ".hero-slideshow",
  "themeFile": "sections/hero-slideshow.liquid",
  "elements": [
    { "name": "Title", "mockup": ".hero-title", "theme": ".hero__title" },
    { "name": "Subtitle", "mockup": ".hero-subtitle", "theme": ".hero__subtitle" },
    { "name": "CTA Button", "mockup": ".hero-cta", "theme": ".hero__cta" }
  ]
}
```

- If `elements` is omitted, only the section container itself is audited
- The `scaffold_mappings.py` script generates a starting point by scanning both directories, matching by common class name fragments and structural position — but element mappings are primarily hand-authored since class names differ between mockup and theme
- If a selector in `elements` does not match any element on the page, the script logs it as **Unknown** ("Element not found: `.hero-cta` in theme") and continues with the remaining elements. All Unknown items are listed prominently in the report summary so stale config is easy to spot

## Tolerance & Severity

**Configurable tolerance** — default 2px, adjustable via `--tolerance` flag.

### Numeric properties (font-size, padding, width, etc.)

| Severity | Criteria |
|----------|----------|
| Critical | diff > tolerance * 2 (default >4px), or missing property |
| Notable | tolerance < diff <= tolerance * 2 (default 2-4px), or color diff > 5 in any RGB channel |
| Marginal | 0 < diff <= tolerance (default 0-2px) — flagged, not ignored |

### Color properties (color, background-color, border-color, fill, stroke)

Colors are parsed into RGB channels and diffed per channel:

| Severity | Criteria |
|----------|----------|
| Critical | any channel diff > 10 |
| Notable | any channel diff > 5 |
| Marginal | any channel diff > 0 |

### Non-numeric properties (font-family, display, flex-direction, text-transform, etc.)

Any mismatch is automatically **Critical** — these are intentional design choices, not rounding errors.

### Unknown

Element selector not found on the page. Could indicate stale config, renamed selector, or section not yet implemented. Not a styling issue — a config maintenance signal.

## Section Mapping Config

File: `config/page-mappings.json`

```json
{
  "defaults": {
    "themeBaseUrl": "http://127.0.0.1:9292",
    "htmlBaseUrl": "http://127.0.0.1:8080",
    "htmlBaseDir": "html",
    "tolerance": 2,
    "viewports": {
      "core": [1920, 1440, 768, 480],
      "full": [1920, 1440, 1024, 768, 480, 390]
    }
  },
  "pages": [
    {
      "name": "Homepage",
      "mockup": "index.html",
      "theme": "/",
      "sections": [
        {
          "name": "Hero Slideshow",
          "mockupSelector": ".hero-section",
          "themeSelector": ".hero-slideshow",
          "themeFile": "sections/hero-slideshow.liquid"
        }
      ]
    }
  ]
}
```

A scaffold script (`scripts/scaffold_mappings.py`) generates the initial config by scanning `/html/` and `/theme/sections/`. The `themeFile` field is informational only — it appears in the report to help the developer/agent locate the file to fix, but is not used functionally by the audit script.

## Report Format

Saved to `docs/qa-reports/visual-qa-<page>-<datetime>.md` (e.g., `visual-qa-homepage-2026-03-27-1430.md`). Timestamp includes HH:MM so same-day re-audits are preserved for comparison.

```markdown
# Visual QA Report: Homepage
**Date:** 2026-03-27 | **Viewports:** 1920px, 1440px, 768px, 480px
**Tolerance:** 2px | **Flags:** --image-diff

## Summary
- Critical: 3 | Notable: 7 | Marginal: 12

## Hero Slideshow
**Theme file:** `theme/sections/hero-slideshow.liquid`
**Screenshots:** `docs/qa-reports/screenshots/homepage-hero-1440.png` (section-level, not per-element)

### Typography (1440px)
| Element | Property | Expected | Actual | Severity |
|---------|----------|----------|--------|----------|
| `.hero__title` | font-size | 64px | 58px | Critical |
| `.hero__subtitle` | letter-spacing | 2px | 1px | Notable |
| `.hero__subtitle` | color | #8B7355 | #8A7254 | Marginal |
```

## CLI Interface

```bash
python .agents/skills/visual-qa/scripts/audit.py [options]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--page <name>` | all | Audit specific page |
| `--section <name>` | all | Audit specific section (requires `--page`) |
| `--url <url>` | `http://127.0.0.1:9292` | Shopify dev server URL |
| `--viewports full` | core | Use full viewport set |
| `--tolerance <px>` | 2 | Pixel tolerance threshold |
| `--image-diff` | off | Enable visual screenshot diff for images |
| `--svg-compare` | off | Enable SVG content/path comparison |
| `--output <path>` | `docs/qa-reports/` | Report output directory |
| `--dry-run` | off | Validate config and list sections without running browser |

## Handling Mockup Changes & New Pages

When the HTML mockup is updated (selectors renamed, elements added, style values changed) or new pages are added to `/html/`, the config may become stale. The `scaffold_mappings.py` script supports a `--diff` mode to detect drift:

```bash
python .agents/skills/visual-qa/scripts/scaffold_mappings.py --diff
```

Output:
```
NEW pages: faq.html (not in config)
STALE selectors: .hero-cta renamed to .hero-button in index.html
NEW elements: .newsletter-disclaimer found in index.html .newsletter-section
```

**How changes are handled:**
- **Selector renamed in mockup** → audit logs it as Unknown for that element; `--diff` identifies the rename
- **New elements added to a section** → not audited until added to config; `--diff` flags them
- **Style values changed in mockup** → audit picks these up automatically (reads computed styles live, no caching)
- **New HTML page added** → not audited until added to `page-mappings.json`; `--diff` flags the new file

**Recommended workflow after mockup changes:**
1. Run `scaffold_mappings.py --diff` to see what changed
2. Update `page-mappings.json` accordingly
3. Re-run the audit

## Re-audit Loop

1. Agent runs audit -> gets report with issues
2. Agent implements fixes based on the report
3. Agent runs audit again (same command) -> new report
4. Repeat until no critical or notable issues remain
5. Marginal issues are acceptable (logged but not blocking)

Previous reports are preserved (date in filename) for comparison.

## Dev Server Handling

The skill assumes the Shopify dev server is already running. If it cannot reach the configured URL:
1. Prompts the user to start the dev server
2. Waits for user confirmation
3. Retries the connection (max 3 attempts, 5-second intervals)
4. Exits with a clear error if still unreachable after retries

The HTML mockup server (`serve_html.py`) is started/stopped automatically by the audit script on the configured `htmlBaseUrl` port (default 8080). If the port is occupied, it fails fast with a clear error.

## Dependencies

- **Python 3.10+**
- **playwright** — browser automation and style extraction
- **Pillow** — image screenshot diff (only needed with `--image-diff` flag)

Prerequisites:
```bash
pip install playwright Pillow
playwright install chromium
```

A `requirements.txt` is included in the skill's `scripts/` directory.

## File Structure

```
.agents/skills/visual-qa/
├── SKILL.md                        — Skill instructions & workflow
├── config/
│   └── page-mappings.json          — Page/section mapping config
├── scripts/
│   ├── audit.py                    — Main audit script (Playwright)
│   ├── scaffold_mappings.py        — Generate initial page-mappings.json
│   ├── serve_html.py               — HTTP server for /html/ directory
│   ├── extract_styles.py           — Computed style extraction helpers
│   └── requirements.txt            — Python dependencies
└── references/
    └── properties.md               — Audited CSS properties by category
```

## Key Design Decisions

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Comparison method | Hybrid: computed styles + screenshots | Catches both subtle property mismatches and visual layout issues |
| Browser rendering | Playwright for both mockup and theme | Accurate computed styles after CSS cascade, media queries, font loading |
| Mapping approach | JSON config file | Reliable, defined once, serves as documentation |
| Tolerance | Configurable with marginal flagging | Focuses on real issues while surfacing minor differences |
| Image audit | Dimensions + object-fit by default | Avoids false positives from CDN differences; visual diff via flag |
| Icon/SVG audit | Size + color + spacing by default | SVG path comparison via flag for suspected wrong icons |
| Report format | Markdown with tables | Human-readable and AI-agent-parseable |
| Dev server | User-managed with graceful prompting | Avoids auth/session complexity |
