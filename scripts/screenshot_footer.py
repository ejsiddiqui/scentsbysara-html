from playwright.sync_api import sync_playwright
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs', 'qa-reports', 'screenshots')
os.makedirs(OUTPUT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # Desktop screenshot
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:9292')
    page.wait_for_load_state('domcontentloaded')
    page.wait_for_timeout(2000)
    # Full page screenshot first to inspect
    page.screenshot(path=os.path.join(OUTPUT_DIR, 'footer-debug-fullpage.png'), full_page=True)
    print('Full page screenshot saved')

    footer = page.locator('footer.footer-section')
    footer.screenshot(path=os.path.join(OUTPUT_DIR, 'footer-desktop-1440.png'))
    print('Desktop footer screenshot saved')

    # Mobile screenshot
    page2 = browser.new_page(viewport={'width': 390, 'height': 844})
    page2.goto('http://127.0.0.1:9292')
    page2.wait_for_load_state('domcontentloaded')
    page2.wait_for_timeout(2000)
    footer2 = page2.locator('footer.footer-section')
    footer2.screenshot(path=os.path.join(OUTPUT_DIR, 'footer-mobile-390.png'))
    print('Mobile footer screenshot saved')

    browser.close()
    print('Done')
