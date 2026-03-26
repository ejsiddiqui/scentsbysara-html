"""
Capture side-by-side screenshots: HTML mockup (live server) vs Shopify dev store.
Saves to C:/tmp/compare/
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_SHOPIFY  = "http://127.0.0.1:9292"
BASE_HTML     = "http://127.0.0.1:5500/html"
STORE_PASSWORD = "ahttey"
OUT_DIR = Path("C:/tmp/compare")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PAGES = [
    # label         html path                  shopify path
    ("homepage",    "/index.html",             "/"),
    ("shop",        "/shop.html",              "/collections/all"),
    ("scar-coll",   "/scar-collection.html",   "/collections/all"),
    ("product",     "/product.html",           None),          # nav from collection
    ("cart",        "/cart.html",              "/cart"),
    ("contact",     "/contact.html",           "/pages/contact"),
    ("our-story",   "/our-story.html",         "/pages/our-story"),
    ("your-story",  "/your-story.html",        "/pages/your-story"),
]

WIDTH = 1440

def unlock(page):
    try:
        if "/password" in page.url or page.locator("form[action*='password']").count() > 0:
            pwd = page.locator("input[name='password']").first
            if pwd.count() > 0:
                pwd.fill(STORE_PASSWORD)
                page.locator("button[type='submit'], input[type='submit']").first.click()
                page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass

def shot(browser, url, path, is_shopify=False):
    ctx = browser.new_context(viewport={"width": WIDTH, "height": 900})
    page = ctx.new_page()
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        if is_shopify:
            unlock(page)
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass
        page.wait_for_timeout(1200)   # let webfonts settle
        page.screenshot(path=str(path), full_page=True)
        print(f"  OK  {path.name}")
    except Exception as e:
        print(f"  ERR {path.name}: {e}")
    finally:
        ctx.close()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    print(f"Output: {OUT_DIR}\n")

    for label, html_path, shopify_path in PAGES:
        print(f"[{label}]")
        shot(browser, BASE_HTML + html_path,
             OUT_DIR / f"{label}-html.png", is_shopify=False)

        if shopify_path:
            shot(browser, BASE_SHOPIFY + shopify_path,
                 OUT_DIR / f"{label}-shopify.png", is_shopify=True)
        else:
            # Navigate to first product from collection
            ctx = browser.new_context(viewport={"width": WIDTH, "height": 900})
            pg = ctx.new_page()
            try:
                pg.goto(BASE_SHOPIFY + "/collections/all",
                        wait_until="domcontentloaded", timeout=25000)
                unlock(pg)
                pg.wait_for_load_state("networkidle", timeout=10000)
                link = pg.locator("product-card a, .product-card a").first
                if link.count() > 0:
                    href = link.get_attribute("href")
                    pg.goto(BASE_SHOPIFY + href,
                            wait_until="domcontentloaded", timeout=25000)
                    pg.wait_for_load_state("networkidle", timeout=10000)
                    pg.wait_for_timeout(1200)
                pg.screenshot(path=str(OUT_DIR / f"{label}-shopify.png"),
                              full_page=True)
                print(f"  OK  {label}-shopify.png")
            except Exception as e:
                print(f"  ERR {label}-shopify.png: {e}")
            finally:
                ctx.close()

    browser.close()
print("\nDone.")
