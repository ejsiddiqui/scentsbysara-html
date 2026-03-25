// @ts-check
/**
 * E2E Test Template — Scents by Sara
 *
 * Copy this file and rename to match the page you are testing:
 *   tests/{page-name}.spec.js
 *
 * Run with:
 *   npx playwright test tests/{page-name}.spec.js
 */

const { test, expect } = require('@playwright/test');

const BASE = 'http://localhost:3000';

// ─── PAGE NAME ─────────────────────────────────────────────────

test.describe('Page Name (filename.html)', () => {

    test('page loads with correct title and key elements', async ({ page }) => {
        await page.goto(`${BASE}/filename.html`);
        await page.waitForLoadState('networkidle');

        // Title check
        await expect(page).toHaveTitle(/Expected Title/i);

        // Header/nav visible
        await expect(page.locator('.brand-logo')).toBeVisible();

        // Key section visible
        await expect(page.locator('#sectionId')).toBeVisible();

        // Screenshot
        await page.screenshot({
            path: 'tests/screenshots/page-name.png',
            fullPage: true,
        });
    });

    test('links point to correct targets', async ({ page }) => {
        await page.goto(`${BASE}/filename.html`);
        await page.waitForLoadState('networkidle');

        // Example: verify CTA links
        const ctaLinks = page.locator('.cta-selector');
        const count = await ctaLinks.count();

        for (let i = 0; i < count; i++) {
            const href = await ctaLinks.nth(i).getAttribute('href');
            expect(href).toMatch(/target-page\.html/);
        }
    });

    test('interactive component works correctly', async ({ page }) => {
        await page.goto(`${BASE}/filename.html`);
        await page.waitForLoadState('networkidle');

        // Example: toggle interaction
        const trigger = page.locator('.toggle-trigger');
        const panel = page.locator('.toggle-panel');

        // Initial state
        await expect(panel).not.toBeVisible();

        // Click to open
        await trigger.click();
        await page.waitForTimeout(400);
        await expect(panel).toBeVisible();

        // Click to close
        await trigger.click();
        await page.waitForTimeout(400);
        await expect(panel).not.toBeVisible();

        await page.screenshot({
            path: 'tests/screenshots/page-name-interaction.png',
        });
    });

});


// ─── NAVIGATION FLOW ───────────────────────────────────────────

test.describe('Navigation from Page Name', () => {

    test('navigates to target page via CTA', async ({ page }) => {
        await page.goto(`${BASE}/filename.html`);
        await page.waitForLoadState('networkidle');

        // Click the CTA
        await page.locator('.cta-selector').first().click();
        await page.waitForLoadState('networkidle');

        // Verify destination
        await expect(page).toHaveURL(/target-page\.html/);

        await page.screenshot({
            path: 'tests/screenshots/nav-to-target.png',
        });
    });

});
