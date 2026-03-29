# Claude Code Guidelines — Scents by Sara

## Design Reference Sources

| Source | Purpose | Priority |
|--------|---------|----------|
| `figma-exports/figma-<page>.png` | **Primary design reference** — all visual decisions (layout, typography, colour, spacing) | **Highest — supersedes everything** |
| `html/` | **Functionality reference** — component behaviour, interaction patterns, CSS token names | Secondary — consult for how things work, not how they look |
| `references/<page>/` | Old screenshot snapshots — outdated | Do NOT use |

**Rules:**
- **Figma is always right visually.** When Figma and the HTML mockup conflict on appearance, follow Figma.
- **HTML mockup is right functionally.** Consult it for component logic, token names, JS behaviour, and responsive patterns.
- Always load `figma-exports/figma-<page>.png` before writing any CSS. Never assume — read the design first.

---

## Deployment Workflow

Pushing to git does **not** deploy to Shopify. Two separate steps are always required:

### Step 1 — Commit and push to git
```bash
# Parent repo (html mockup, docs, skills)
cd /path/to/scentsbysara-v3
git add theme/sections/<file>
git commit -m "fix(...): ..."
git push origin shopify-theme

# Theme repo (Shopify theme files)
cd theme/
git add sections/<file>
git commit -m "fix(...): ..."
git pull origin main --no-rebase --strategy-option=ours  # Shopify auto-commits; pull first
git push origin main
```

### Step 2 — Deploy to live Shopify store
```bash
cd theme/
shopify theme push --theme 147874775176 --only sections/<file>.liquid --allow-live
```

### Step 3 — Verify (bypass CDN cache)
```
https://scentsbysara-dev.myshopify.com?preview_theme_id=147874775176
```

> The regular store URL caches rendered HTML at Shopify's CDN for 5–30 minutes.
> `?preview_theme_id=` bypasses this and serves a fresh render every time.

**Store details:**
- Theme name: SBS — ID: `147874775176`
- Store URL: `https://scentsbysara-dev.myshopify.com`
- Store password: `ahttey`

---

## QA Workflow (Every Section)

Before touching any code — and after every push:

1. **Load the reference:** Open `figma-exports/figma-<page>.png`
2. **Screenshot the live section:**
   ```bash
   agent-browser open "https://scentsbysara-dev.myshopify.com?preview_theme_id=147874775176"
   agent-browser eval 'document.querySelector(".section-class").scrollIntoView()'
   agent-browser screenshot
   ```
3. **Visual diff — check all of these:**
   - Column proportions and gap values
   - Font size, weight, family, line-height for each text element
   - Spacing: padding, margin, gap between items
   - Colors: use `getComputedStyle` to confirm token values
   - Decorative elements: dividers, lines, pseudo-elements
   - Full-width vs container-constrained layout

4. **Computed style spot-checks:**
   ```bash
   agent-browser eval 'window.getComputedStyle(document.querySelector(".selector")).fontSize'
   agent-browser eval 'window.getComputedStyle(document.querySelector(".selector")).color'
   agent-browser eval 'getComputedStyle(document.documentElement).getPropertyValue("--token-name")'
   ```

---

## CSS Token Sources

All tokens are defined in `theme/snippets/design-tokens.liquid`. Cross-reference with `html/css/design-tokens.css` for any token missing from the theme.

Key tokens used frequently:

| Token | Value | Usage |
|-------|-------|-------|
| `--color-slate` | `#2D2B27` | Body text, description paragraphs |
| `--color-muted` | `#A39382` | Muted headings, secondary text |
| `--color-taupe` | `#A39382` | Eyebrows, decorative lines |
| `--color-foreground` | `#3F3229` (mocha) | Default body text |
| `--text-body-large` | `18px` | Item descriptions, lead text |
| `--text-h1` | `47px` (from settings) | Primary headings |
| `--font-sans` | Suisse Int'l | Body/UI text |
| `--font-serif` | Rl Limo | Decorative headings |
| `--inner-gutter` | `80px` | Content column inner padding |
| `--space-lg` | `32px` | Spacing between elements |

---

## Common Patterns

### Full-width section toggle
```liquid
{{- /* schema setting */ -}}
{ "type": "checkbox", "id": "full_width", "label": "Full width", "default": false }

{{- /* section class */ -}}
class="... {% if section.settings.full_width %} section--full-width{% endif %}"

{{- /* CSS override */ -}}
#Section-{{ section.id }}.section--full-width .container {
  width: 100%;
  max-width: 100%;
  padding-inline: 0;
}
```

### Decorative heading underline
```css
.heading {
  position: relative;
  padding-bottom: var(--space-lg);
  margin-bottom: var(--space-lg);
}
.heading:after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 190px;
  height: 1px;
  background-color: var(--color-taupe);
}
```

### Shopify merge conflict pattern
Shopify auto-commits changes to the theme git repo (commits titled "Update from Shopify for theme SBS"). When pulling, conflicts are expected — always keep our local version:
```bash
git checkout --ours sections/<file>.liquid
git add sections/<file>.liquid
```

---

## Lessons Learned

- **`git push` ≠ Shopify deploy.** Always follow with `shopify theme push`.
- **CDN cache:** The store URL caches for up to 30 min. Always verify with `?preview_theme_id=`.
- **Visual QA first:** Read the Figma export before writing any CSS. Identify ALL differences before touching code.
- **`font-serif` class in HTML:** Check if item headings/subheadings should use sans or serif — don't assume.
- **Gap and column ratios matter:** `0.92fr / 1.08fr` vs `repeat(2, 1fr)` and `clamp(1.75rem, 4vw, 5rem)` vs `0` are visually significant — always verify against design.
- **Pseudo-elements over `<hr>`:** Decorative lines below headings should use `::after`, not `<hr>`, so spacing and color inherit from the heading element.
