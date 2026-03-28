# Footer Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the Shopify footer match the approved mockup design across desktop, tablet, and mobile while keeping Shopify-native payment badges.

**Architecture:** Keep the existing footer section and settings model, but update the footer markup and CSS in place. Use a focused Playwright verification script as the regression harness for footer rendering, then validate with screenshot captures and `shopify theme check`.

**Tech Stack:** Shopify Liquid, section-scoped CSS in Liquid, Playwright via Python, Shopify Theme Check

---

### Task 1: Add a failing footer verification script

**Files:**
- Create: `scripts/check_footer.py`
- Test: `scripts/check_footer.py`

**Step 1: Write the failing test**

Create a Playwright-based footer check that asserts:
- at `1440px`, the footer shows at least 4 social links
- at `1440px`, the desktop footer logo has rendered width greater than `250px`
- at `390px`, the mobile logo has rendered width between `56px` and `66px`
- at `390px`, the social row is visible

**Step 2: Run test to verify it fails**

Run: `python scripts/check_footer.py`

Expected: FAIL on current footer rendering and icon/design mismatches.

**Step 3: Write minimal implementation**

Implement only the script and its assertions, no footer changes yet.

**Step 4: Run test to verify it fails**

Run: `python scripts/check_footer.py`

Expected: non-zero exit code with failing footer checks.

**Step 5: Commit**

```bash
git -C theme add ../scripts/check_footer.py
git -C theme commit -m "test: add footer verification script"
```

### Task 2: Swap social icons to the mockup assets

**Files:**
- Modify: `theme/sections/footer.liquid`
- Reference: `html/assets/icons/instagram.svg`
- Reference: `html/assets/icons/facebook.svg`
- Reference: `html/assets/icons/tiktok.svg`
- Reference: `html/assets/icons/pinterest.svg`

**Step 1: Write the failing test**

Extend or use the footer verification script to assert that:
- footer social icons are present at `1440px` and `390px`
- their rendered width/height align with the mockup targets

**Step 2: Run test to verify it fails**

Run: `python scripts/check_footer.py`

Expected: FAIL because current icons do not match the approved source/design target.

**Step 3: Write minimal implementation**

Update `theme/sections/footer.liquid` to render social icons using the theme asset pipeline with copies of the mockup icon assets in the theme.

**Step 4: Run test to verify it passes**

Run: `python scripts/check_footer.py`

Expected: social icon assertions pass, other footer assertions may still fail.

**Step 5: Commit**

```bash
git -C theme add sections/footer.liquid
git -C theme commit -m "feat: align footer social icons with design assets"
```

### Task 3: Fix footer desktop brand row and responsive logo rendering

**Files:**
- Modify: `theme/sections/footer.liquid`

**Step 1: Write the failing test**

Ensure the verification script asserts:
- desktop logo renders with visible width at `1024px` and `1440px`
- mobile logo renders at `390px`
- bottom row positions brand and payment areas correctly enough to avoid zero-size brand output

**Step 2: Run test to verify it fails**

Run: `python scripts/check_footer.py`

Expected: FAIL on desktop logo visibility.

**Step 3: Write minimal implementation**

Adjust footer markup/CSS so the desktop wordmark renders correctly and the mobile symbol remains intact.

**Step 4: Run test to verify it passes**

Run: `python scripts/check_footer.py`

Expected: desktop/mobile logo assertions pass.

**Step 5: Commit**

```bash
git -C theme add sections/footer.liquid
git -C theme commit -m "fix: restore footer brand rendering across breakpoints"
```

### Task 4: Match newsletter and menu styling to the mockup

**Files:**
- Modify: `theme/sections/footer.liquid`
- Reference: `html/partials/site-footer.html`
- Reference: `html/css/components.css`
- Reference: `html/css/responsive.css`

**Step 1: Write the failing test**

Add assertions for:
- newsletter heading size and visibility envelope
- button width at `390px`
- social row spacing envelope
- footer height ranges at `1440px` and `390px`

**Step 2: Run test to verify it fails**

Run: `python scripts/check_footer.py`

Expected: FAIL on layout/spacing checks.

**Step 3: Write minimal implementation**

Retune footer spacing, heading typography, menu heading styling, accordion spacing, and responsive breakpoints.

**Step 4: Run test to verify it passes**

Run: `python scripts/check_footer.py`

Expected: targeted checks pass.

**Step 5: Commit**

```bash
git -C theme add sections/footer.liquid
git -C theme commit -m "feat: align footer layout and typography with mockup"
```

### Task 5: Verify and refresh visual QA artefacts

**Files:**
- Modify: `.agents/skills/visual-qa/config/page-mappings.json`
- Create or update: `docs/qa-reports/footer-visual-qa-2026-03-28.md`
- Create or update: `docs/qa-reports/screenshots/*`

**Step 1: Write the failing test**

Use the existing footer comparison report as the failing baseline.

**Step 2: Run test to verify it fails**

Run:
- `python scripts/check_footer.py`
- `shopify theme check`

Expected: all footer checks should pass after implementation; if not, keep iterating.

**Step 3: Write minimal implementation**

Refresh targeted screenshot captures and update the footer QA report if needed.

**Step 4: Run test to verify it passes**

Run:
- `python scripts/check_footer.py`
- `shopify theme check`

Expected: exit code `0` for both commands.

**Step 5: Commit**

```bash
git -C theme add sections/footer.liquid ../docs/qa-reports ../scripts/check_footer.py ../.agents/skills/visual-qa/config/page-mappings.json
git -C theme commit -m "test: verify footer visual parity"
```
