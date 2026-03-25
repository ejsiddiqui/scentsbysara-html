---
name: e2e-testing
description: Write and run comprehensive end-to-end tests using Playwright. Use when creating new E2E test suites, verifying cross-page user journeys, testing interactive components, capturing visual regression screenshots, or validating the full application flow from homepage through checkout.
---

# End-to-End Testing

Write and run comprehensive Playwright E2E tests that verify every page, interaction, and cross-page user journey in Scents by Sara.

## Prerequisites

- Node.js installed
- Project dependencies installed: `npm install`
- Playwright browsers installed: `npx playwright install chromium`
- Local dev server running on `http://localhost:3000`

## Project Test Architecture

```
tests/
  qa-runner.js        # Custom standalone test runner (node tests/qa-runner.js)
  qa.spec.js          # Playwright Test spec file (npx playwright test)
  qa-report.json      # JSON test results
  screenshots/        # Captured test screenshots
  test-results/       # Playwright output directory
  unit/               # Jest unit tests (separate from E2E)
```

### Two test runners

| Runner | Command | When to use |
|--------|---------|-------------|
| Custom runner | `npm run test:e2e` or `node tests/qa-runner.js` | Quick pass/fail summary with JSON report |
| Playwright Test | `npx playwright test` | Full Playwright reporting, parallel execution, retries |

Both target `http://localhost:3000` with a 1440×900 Chromium viewport.

## Workflow

1. Identify what to test
   - New page? Create a full page-level test suite.
   - New feature/interaction? Add tests to the relevant page suite.
   - Bug fix? Write a regression test that reproduces the bug, then verify the fix.
   - Use `references/testing-checklist.md` to ensure complete coverage.

2. Structure the test file
   - Place Playwright Test specs in `tests/` with the naming pattern `*.spec.js`.
   - Group tests by page using `test.describe('Page Name (filename.html)', () => { ... })`.
   - Order tests: page load → static content → interactions → navigation flows.
   - Use `references/test-template.js` as a starting point.

3. Write page-level tests
   - **Page load**: Title, critical elements visible, no console errors.
   - **Content verification**: Headings, link targets (`href` attributes), image sources.
   - **Component count**: Correct number of product cards, links, etc.
   - **Screenshot capture**: Full-page screenshot for visual reference.

4. Write interaction tests
   - **Click behaviors**: Buttons, toggles, accordions, filter chips.
   - **Hover states**: Mega-menu, tooltips, button hover effects.
   - **Form inputs**: Quantity stepper, email signup, search.
   - **State changes**: Verify DOM changes (class toggling, aria attributes, visibility).
   - Use `waitForTimeout()` after interactions to allow animations to complete.

5. Write cross-page journey tests
   - Test complete user flows that span multiple pages:
     - Homepage → Shop → Product → Cart → Checkout
     - Product breadcrumb → Shop → Homepage
     - Mega-menu → Shop page
   - Verify URLs after each navigation step.
   - Capture screenshots at each waypoint.

6. Handle assertions
   - Use Playwright's `expect()` with built-in matchers:
     - `toBeVisible()`, `toHaveText()`, `toHaveAttribute()`, `toHaveURL()`
     - `toHaveCount()` for verifying element counts
     - `toHaveClass()` for CSS state verification
   - For the custom runner, use the `assert(condition, message)` helper.

7. Capture evidence
   - Take screenshots at key states (page load, after interaction, error states).
   - Save to `tests/screenshots/` with descriptive filenames: `{page}-{state}.png`.
   - Take full-page screenshots for layout verification: `{ fullPage: true }`.

8. Run and verify
   - Run all E2E tests: `npm run test:e2e`
   - Run Playwright specs: `npx playwright test`
   - Run specific test file: `npx playwright test tests/qa.spec.js`
   - Review `tests/qa-report.json` for results summary.
   - Review `tests/screenshots/` for visual evidence.

9. Report results
   - List all tests run with pass/fail status.
   - For failures: include error message, screenshot, and suggested fix.
   - Overall summary: total passed, total failed, coverage gaps.

## Writing Test Patterns

### Page load test
```javascript
test('page loads with key elements', async ({ page }) => {
    await page.goto(`${BASE}/page.html`);
    await page.waitForLoadState('networkidle');

    await expect(page).toHaveTitle(/Expected Title/i);
    await expect(page.locator('.key-element')).toBeVisible();
    await page.screenshot({ path: 'tests/screenshots/page.png', fullPage: true });
});
```

### Interaction test
```javascript
test('accordion opens and closes', async ({ page }) => {
    await page.goto(`${BASE}/product.html`);
    await page.waitForLoadState('networkidle');

    const trigger = page.locator('.accordion-trigger').nth(0);
    await expect(trigger).toHaveAttribute('aria-expanded', 'false');

    await trigger.click();
    await page.waitForTimeout(400);
    await expect(trigger).toHaveAttribute('aria-expanded', 'true');
});
```

### Navigation flow test
```javascript
test('full purchase journey', async ({ page }) => {
    await page.goto(`${BASE}/index.html`);
    await page.waitForLoadState('networkidle');

    // Navigate to shop
    await page.locator('.hero-actions a').click();
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/shop\.html/);

    // Navigate to product
    await page.locator('.shop-now-btn').first().click();
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL(/product\.html/);
});
```

## Operating Rules

- Always wait for `networkidle` after `goto()` before interacting with the page.
- Use `waitForTimeout()` after click/hover interactions that trigger animations (300–600ms).
- Never rely on element indices that may change — prefer `data-*` attributes or semantic selectors.
- Always capture screenshots as evidence, even for passing tests.
- Keep tests independent — each test should not depend on state from a previous test.
- Use descriptive test names that explain what is being verified, not how.
- Test at 1440×900 viewport by default (matches `playwright.config.js`).

## Output Contract

When finishing, present:
1. Tests written (count and descriptions)
2. Test results (passed/failed with details)
3. Screenshots captured (list with descriptions)
4. Coverage gaps (any pages or interactions not yet tested)

## References

- `references/test-template.js`: Starter template for new Playwright E2E test suites.
- `references/testing-checklist.md`: Coverage checklist for all pages and user journeys.
