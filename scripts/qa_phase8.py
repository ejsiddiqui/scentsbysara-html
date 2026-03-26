"""
Phase 8 QA Script - Scents by Sara Shopify Theme
"""
import sys, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:9292"
STORE_PASSWORD = "ahttey"
RESULTS = []

VIEWPORTS = [
    ("mobile-375",  375,  812),
    ("tablet-768",  768, 1024),
    ("desktop-1440",1440, 900),
]

def log(category, status, detail):
    icon = "[PASS]" if status == "PASS" else "[FAIL]" if status == "FAIL" else "[WARN]"
    print(f"{icon} {category}: {detail}")
    RESULTS.append({"category": category, "status": status, "detail": detail})

def unlock(page):
    """Enter store password if the password gate is shown."""
    if "/password" in page.url or page.locator("form[action*='password']").count() > 0:
        pwd_input = page.locator("input[name='password']").first
        if pwd_input.count() > 0:
            pwd_input.fill(STORE_PASSWORD)
            page.locator("button[type='submit'], input[type='submit']").first.click()
            page.wait_for_load_state("networkidle", timeout=15000)

def goto(page, path, viewport=(1440, 900)):
    page.set_viewport_size({"width": viewport[0], "height": viewport[1]})
    resp = page.goto(BASE + path, wait_until="domcontentloaded", timeout=25000)
    unlock(page)
    try:
        page.wait_for_load_state("networkidle", timeout=12000)
    except Exception:
        pass  # networkidle can be slow on Shopify proxy
    return resp

# ─── Tests ───────────────────────────────────────────────────────────────────

def test_page_loads(browser):
    print("\n--- Page Load & Console Errors ---")
    pages_to_test = [
        ("Homepage",    "/"),
        ("Collections", "/collections/all"),
        ("Cart",        "/cart"),
        ("Search",      "/search?q=candle"),
        ("Contact",     "/pages/contact"),
        ("Our Story",   "/pages/our-story"),
    ]
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors_by_page = {}

    for name, path in pages_to_test:
        errs = []
        page.on("console", lambda m, e=errs: e.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e, lst=errs: lst.append(str(e)))
        try:
            resp = goto(page, path)
            status = resp.status if resp else 0
            if status == 404:
                log(name, "WARN", f"HTTP 404 — page not yet created in Shopify Admin")
            elif status >= 400:
                log(name, "FAIL", f"HTTP {status}")
            else:
                real_errs = [e for e in errs if not any(x in e.lower() for x in [
                    "favicon","gtm","analytics","cdn.shopify",
                    "shop.app","hotreload","content security policy","csp","frame-ancestors",
                    "failed to load resource","net::err","blocked by client",
                ])]
                if real_errs:
                    for e in real_errs[:2]:
                        log(name, "FAIL", f"Console error: {e[:100]}")
                else:
                    log(name, "PASS", f"HTTP {status} — no console errors")
        except Exception as e:
            log(name, "FAIL", f"Exception: {str(e)[:80]}")
        page._listeners = {}  # clear listeners

    ctx.close()

def test_responsive(browser):
    print("\n--- Responsive Screenshots ---")
    pages_to_snap = [("/", "homepage"), ("/collections/all", "collections"), ("/cart", "cart")]
    for path, slug in pages_to_snap:
        for vp_name, w, h in VIEWPORTS:
            ctx = browser.new_context(viewport={"width": w, "height": h})
            page = ctx.new_page()
            try:
                goto(page, path, (w, h))
                out = f"/tmp/qa-{slug}-{vp_name}.png"
                page.screenshot(path=out, full_page=True)
                log(f"{slug}@{vp_name}", "PASS", f"Screenshot saved")
            except Exception as e:
                log(f"{slug}@{vp_name}", "FAIL", str(e)[:80])
            ctx.close()

def test_header(browser):
    print("\n--- Header ---")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    goto(page, "/")

    # Logo (image logo, text logo, or logo link)
    logo = page.locator(".header__logo, .logo, .site-header .logo-image, header a[href='/']").first
    if logo.count() > 0 and logo.is_visible():
        log("Header", "PASS", "Logo visible on desktop")
    else:
        log("Header", "WARN", "Logo element not found - may need logo uploaded in customizer")

    # Nav links
    nav_links = page.locator("nav a, .header-nav a").all()
    log("Header", "PASS" if len(nav_links) >= 3 else "FAIL", f"{len(nav_links)} nav links")

    # Cart icon
    if page.locator("[data-open-cart]").count() > 0:
        log("Header", "PASS", "Cart icon present")
    else:
        log("Header", "FAIL", "Cart icon [data-open-cart] not found")

    # Skip-to-content
    skip = page.locator(".skip-to-content, a[href='#MainContent']")
    log("Header", "PASS" if skip.count() > 0 else "FAIL",
        "Skip-to-content link present" if skip.count() > 0 else "Skip-to-content missing")

    # Sticky: scroll and check header still visible
    page.evaluate("window.scrollTo(0, 600)")
    page.wait_for_timeout(500)
    header = page.locator("header, .site-header, header-component").first
    log("Header", "PASS" if header.is_visible() else "WARN",
        "Header visible after scroll (sticky)" if header.is_visible() else "Header not visible after scroll")

    # Mobile hamburger
    page.set_viewport_size({"width": 375, "height": 812})
    page.wait_for_timeout(300)
    hamburger = page.locator("[aria-label*='menu'], [aria-label*='Menu']").first
    log("Header:mobile", "PASS" if hamburger.count() > 0 else "WARN",
        "Hamburger button present at 375px" if hamburger.count() > 0 else "Hamburger not found")
    ctx.close()

def test_cart_drawer(browser):
    print("\n--- Cart Drawer ---")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    goto(page, "/")

    # Use desktop cart button (desktop-only-inline at 1440px)
    trigger = page.locator(".header-action--cart.desktop-only-inline").first
    if trigger.count() == 0:
        # fallback: any data-open-cart
        trigger = page.locator("[data-open-cart]").nth(1)
    if trigger.count() == 0:
        log("CartDrawer", "FAIL", "No cart trigger found")
        ctx.close(); return

    trigger.click()
    page.wait_for_timeout(800)

    dialog = page.locator(".cart-drawer-dialog").first
    if dialog.count() > 0 and dialog.is_visible():
        log("CartDrawer", "PASS", "Drawer opens on click")
        log("CartDrawer", "PASS" if dialog.get_attribute("aria-modal") == "true" else "FAIL",
            "aria-modal=true" if dialog.get_attribute("aria-modal") == "true" else "aria-modal missing")
        close = page.locator("[data-dialog-close]").first
        if close.is_visible():
            close.click()
            page.wait_for_timeout(500)
            log("CartDrawer", "PASS" if not dialog.is_visible() else "FAIL",
                "Drawer closes on X button" if not dialog.is_visible() else "Drawer did not close")
    else:
        log("CartDrawer", "FAIL", "Drawer did not open")
    ctx.close()

def test_search(browser):
    print("\n--- Predictive Search ---")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    goto(page, "/")

    btn = page.locator("[aria-label='Search']").first
    if btn.count() == 0:
        btn = page.locator("[aria-label*='Search']").first
    if btn.count() == 0:
        log("Search", "FAIL", "Search button not found"); ctx.close(); return

    btn.click()
    page.wait_for_timeout(700)

    inp = page.locator("input[type='search'], .search-input").first
    if inp.count() > 0 and inp.is_visible():
        log("Search", "PASS", "Search overlay opens")
        # Check aria-modal on dialog
        dlg = page.locator(".search-dialog").first
        log("Search", "PASS" if dlg.get_attribute("aria-modal") == "true" else "FAIL",
            "Search dialog aria-modal=true" if dlg.get_attribute("aria-modal") == "true" else "aria-modal missing on search dialog")
        inp.fill("candle")
        page.wait_for_timeout(1500)
        results = page.locator(".search-results").first
        log("Search", "PASS" if results.count() > 0 else "WARN",
            "Results area rendered" if results.count() > 0 else "Results area not found")
        page.screenshot(path="/tmp/qa-search-results.png")
    else:
        log("Search", "FAIL", "Search input not visible")
    ctx.close()

def test_mobile_menu(browser):
    print("\n--- Mobile Menu ---")
    ctx = browser.new_context(viewport={"width": 375, "height": 812})
    page = ctx.new_page()
    goto(page, "/", (375, 812))

    btn = page.locator("[aria-label*='Open menu'], [aria-label*='menu']").first
    if btn.count() == 0:
        log("MobileMenu", "FAIL", "Hamburger not found"); ctx.close(); return

    btn.click()
    page.wait_for_timeout(700)
    dlg = page.locator(".mobile-menu-dialog").first
    if dlg.count() > 0 and dlg.is_visible():
        log("MobileMenu", "PASS", "Menu opens")
        log("MobileMenu", "PASS" if dlg.get_attribute("aria-modal") == "true" else "FAIL",
            "aria-modal=true" if dlg.get_attribute("aria-modal") == "true" else "aria-modal missing")
        page.screenshot(path="/tmp/qa-mobile-menu.png")
    else:
        log("MobileMenu", "FAIL", "Menu dialog not visible after hamburger click")
    ctx.close()

def test_collection(browser):
    print("\n--- Collection Page ---")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    goto(page, "/collections/all")

    products = page.locator("product-card, .product-card").all()
    log("Collection", "PASS" if len(products) > 0 else "FAIL",
        f"{len(products)} product cards rendered")

    h1 = page.locator("h1").first
    log("Collection", "PASS" if h1.is_visible() else "FAIL",
        f"H1: '{h1.inner_text()[:40]}'" if h1.is_visible() else "H1 missing")

    sort = page.locator("select[name='sort_by']").first
    log("Collection", "PASS" if sort.count() > 0 else "WARN",
        "Sort dropdown present" if sort.count() > 0 else "Sort dropdown not found")

    filter_btn = page.locator(".filter-btn, [class*='filter-toggle']").first
    log("Collection", "PASS" if filter_btn.count() > 0 else "WARN",
        "Filter button present" if filter_btn.count() > 0 else "Filter button not found")

    # Mobile: 2-col grid
    page.set_viewport_size({"width": 375, "height": 812})
    page.wait_for_timeout(400)
    page.screenshot(path="/tmp/qa-collection-mobile.png")
    log("Collection:mobile", "PASS", "Screenshot at 375px saved")
    ctx.close()

def test_product(browser):
    print("\n--- Product Page ---")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    goto(page, "/collections/all")

    link = page.locator("product-card a, .product-card a, .product-card-link").first
    if link.count() == 0:
        log("Product", "FAIL", "No product link on collection page"); ctx.close(); return

    href = link.get_attribute("href")
    goto(page, href)

    # Gallery
    log("Product", "PASS" if page.locator("[data-product-section], .product-page-section").count() > 0 else "FAIL",
        "Product section rendered")

    # Variant picker
    vp = page.locator("variant-picker")
    log("Product", "PASS" if vp.count() > 0 else "WARN",
        f"Variant picker present ({vp.count()})" if vp.count() > 0 else "No variant-picker found")

    # Price with aria-live
    price_live = page.locator("[aria-live='polite']")
    log("Product", "PASS" if price_live.count() > 0 else "FAIL",
        "aria-live region for price present" if price_live.count() > 0 else "aria-live missing on price")

    # ATC button
    atc = page.locator("[data-add-to-cart], .add-to-cart, .product-form button[type='submit']")
    log("Product", "PASS" if atc.count() > 0 else "WARN",
        "Add to cart button present" if atc.count() > 0 else "ATC button not found (product may have no variants in dev store)")

    # Accordions
    acc = page.locator("details.accordion").all()
    log("Product", "PASS" if len(acc) > 0 else "WARN", f"{len(acc)} accordion(s)")

    # Breadcrumbs
    bc = page.locator(".breadcrumbs, nav[aria-label*='Breadcrumb']")
    log("Product", "PASS" if bc.count() > 0 else "WARN",
        "Breadcrumbs present" if bc.count() > 0 else "Breadcrumbs not found")

    # Try add to cart
    if atc.count() > 0 and not atc.first.is_disabled():
        atc.first.click()
        page.wait_for_timeout(1500)
        cart_drawer = page.locator(".cart-drawer-dialog")
        log("Product:ATC", "PASS" if cart_drawer.is_visible() else "WARN",
            "Cart drawer opened after ATC" if cart_drawer.is_visible() else "Cart drawer did not open after ATC")

    page.screenshot(path="/tmp/qa-product-desktop.png")
    log("Product", "PASS", "Screenshot saved")
    ctx.close()

def test_homepage_sections(browser):
    print("\n--- Homepage Sections ---")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    goto(page, "/")

    # Hero slideshow
    hero = page.locator(".home-hero, slideshow-component, .hero-slide")
    log("Homepage", "PASS" if hero.count() > 0 else "FAIL",
        f"Hero slideshow present ({hero.count()} elements)" if hero.count() > 0 else "Hero slideshow missing")

    # Slideshow dots
    dots = page.locator(".slideshow-dot, .slideshow-controls")
    log("Homepage", "PASS" if dots.count() > 0 else "WARN",
        "Slideshow dots present" if dots.count() > 0 else "Slideshow dots not found")

    # Product cards (featured collection)
    cards = page.locator("product-card, .product-card").all()
    log("Homepage", "PASS" if len(cards) >= 4 else "WARN",
        f"{len(cards)} product card(s) on homepage")

    # Collections grid
    coll_grid = page.locator(".collections-grid, [id*='CollectionsGrid']")
    log("Homepage", "PASS" if coll_grid.count() > 0 else "WARN",
        "Collections grid section present" if coll_grid.count() > 0 else "Collections grid section not found by selector")

    # Footer newsletter
    newsletter = page.locator(".newsletter-form, form[action*='contact'], #FooterNewsletterForm")
    log("Homepage", "PASS" if newsletter.count() > 0 else "WARN",
        "Newsletter form in footer" if newsletter.count() > 0 else "Newsletter form not found")

    page.screenshot(path="/tmp/qa-homepage-desktop.png")
    log("Homepage", "PASS", "Full-page screenshot saved")
    ctx.close()

def test_images(browser):
    print("\n--- Image Accessibility ---")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    goto(page, "/")

    imgs = page.locator("img").all()
    missing = [i.get_attribute("src") or "?" for i in imgs
               if not i.get_attribute("alt") and i.get_attribute("alt") != ""]
    log("Images", "PASS" if not missing else "FAIL",
        f"All {len(imgs)} homepage images have alt" if not missing
        else f"{len(missing)} missing alt: {missing[0][:60]}")

    # Product page images
    goto(page, "/collections/all")
    link = page.locator(".product-card a, .product-card-link").first
    if link.count() > 0:
        goto(page, link.get_attribute("href"))
        imgs2 = page.locator("img").all()
        missing2 = [i.get_attribute("src") or "?" for i in imgs2
                    if not i.get_attribute("alt") and i.get_attribute("alt") != ""]
        log("Images:product", "PASS" if not missing2 else "FAIL",
            f"All {len(imgs2)} product page images have alt" if not missing2
            else f"{len(missing2)} missing alt on product page")
    ctx.close()

def test_forms(browser):
    print("\n--- Forms ---")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    goto(page, "/pages/contact")

    form = page.locator("form#contact-form, form[action*='contact']").first
    log("Forms:contact", "PASS" if form.count() > 0 else "FAIL",
        "Contact form present" if form.count() > 0 else "Contact form not found")

    if form.count() > 0:
        # Check labels
        inputs = page.locator("input[required], textarea[required]").all()
        labeled = 0
        for inp in inputs:
            inp_id = inp.get_attribute("id")
            if inp_id and page.locator(f"label[for='{inp_id}']").count() > 0:
                labeled += 1
        log("Forms:contact", "PASS" if labeled == len(inputs) else "WARN",
            f"{labeled}/{len(inputs)} required inputs have labels")
    ctx.close()

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Scents by Sara - Phase 8 QA")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        test_page_loads(browser)
        test_homepage_sections(browser)
        test_header(browser)
        test_cart_drawer(browser)
        test_search(browser)
        test_mobile_menu(browser)
        test_collection(browser)
        test_product(browser)
        test_images(browser)
        test_forms(browser)
        test_responsive(browser)

        browser.close()

    passed = sum(1 for r in RESULTS if r["status"] == "PASS")
    failed = sum(1 for r in RESULTS if r["status"] == "FAIL")
    warned = sum(1 for r in RESULTS if r["status"] == "WARN")

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed  |  {failed} failed  |  {warned} warnings")
    print("=" * 60)

    if failed:
        print("\nFAILURES:")
        for r in RESULTS:
            if r["status"] == "FAIL":
                print(f"  [FAIL] {r['category']}: {r['detail']}")

    if warned:
        print("\nWARNINGS:")
        for r in RESULTS:
            if r["status"] == "WARN":
                print(f"  [WARN] {r['category']}: {r['detail']}")

    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
