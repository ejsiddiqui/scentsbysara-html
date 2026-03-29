"""Capture a full-page screenshot of the live Shopify theme using Playwright."""

import os
from playwright.sync_api import Browser, Page


UNLOCK_SELECTOR = 'input[type="password"]'
UNLOCK_SUBMIT = 'button[type="submit"]'


def _unlock_store(page: Page, password: str) -> None:
    """Unlock a password-protected Shopify dev store if the password gate appears."""
    if page.query_selector(UNLOCK_SELECTOR):
        page.fill(UNLOCK_SELECTOR, password)
        page.click(UNLOCK_SUBMIT)
        page.wait_for_load_state("domcontentloaded")


def capture_theme_screenshot(
    browser: Browser,
    url: str,
    viewport_width: int,
    output_path: str,
    password: str | None = None,
) -> str:
    """
    Open the theme URL in Playwright, capture a full-page screenshot.
    Returns the path to the saved screenshot.
    """
    context = browser.new_context(viewport={"width": viewport_width, "height": 900})
    page = context.new_page()
    try:
        page.goto(url, wait_until="domcontentloaded")
        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass  # networkidle timeout is acceptable on complex pages
        if password:
            _unlock_store(page, password)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        page.screenshot(path=output_path, full_page=True)
        return output_path
    finally:
        context.close()
