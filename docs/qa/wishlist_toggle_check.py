from __future__ import annotations

import os
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


REPO_ROOT = Path(__file__).resolve().parents[2]
PORT = 4173
MOBILE_VIEWPORT = {"width": 390, "height": 844}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return


def start_server() -> ThreadingHTTPServer:
    os.chdir(REPO_ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", PORT), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.25)
    return server


def assert_wishlist_toggle(page_path: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport=MOBILE_VIEWPORT)
        page = context.new_page()

        try:
            page.goto(f"http://127.0.0.1:{PORT}/{page_path}", wait_until="load", timeout=60000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(250)

            toggle = page.locator(".product-card .product-card-wishlist").first
            toggle.wait_for(state="visible", timeout=3000)

            initial_state = toggle.get_attribute("aria-pressed")
            assert initial_state == "false", f"{page_path}: expected default aria-pressed=false, got {initial_state!r}"

            toggle.click()
            toggled_state = toggle.get_attribute("aria-pressed")
            assert toggled_state == "true", f"{page_path}: expected aria-pressed=true after click, got {toggled_state!r}"

            toggle.click()
            reset_state = toggle.get_attribute("aria-pressed")
            assert reset_state == "false", f"{page_path}: expected aria-pressed=false after second click, got {reset_state!r}"
        finally:
            context.close()
            browser.close()


def main() -> None:
    server = start_server()
    try:
        assert_wishlist_toggle("shop.html")
        assert_wishlist_toggle("product.html")
        print("Wishlist toggle checks passed.")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
