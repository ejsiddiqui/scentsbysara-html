from __future__ import annotations

import json
import os
import threading
import time
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


REPO_ROOT = Path(__file__).resolve().parents[2]
PAGES = [
    "index.html",
    "body-candles.html",
    "our-story.html",
    "your-story.html",
    "shop.html",
    "product.html",
    "cart.html",
    "checkout.html",
    "contact.html",
    "scar-collection.html",
    "sculpted-collection.html",
    "gifts.html",
]
VIEWPORTS = [
    (1920, 1080),
    (1440, 1024),
    (1024, 1366),
    (768, 1024),
    (390, 844),
    (375, 812),
]
PORT = 4173


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


def run_audit(pages: list[str] | None = None) -> dict:
    if pages is None:
        pages = PAGES
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = REPO_ROOT / "docs" / "qa" / f"sweep-{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    base_url = f"http://127.0.0.1:{PORT}"

    report: dict[str, object] = {
        "timestamp": stamp,
        "base_url": base_url,
        "out_dir": str(out_dir),
        "results": [],
        "summary": {
            "total_checks": 0,
            "overflow_failures": 0,
            "console_error_failures": 0,
        },
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for page_name in pages:
                page_key = page_name.replace(".html", "")
                for width, height in VIEWPORTS:
                    context = browser.new_context(viewport={"width": width, "height": height})
                    page = context.new_page()
                    console_errors: list[str] = []
                    page.on(
                        "console",
                        lambda msg: console_errors.append(msg.text)
                        if msg.type == "error"
                        else None,
                    )

                    url = f"{base_url}/{page_name}"
                    page.goto(url, wait_until="load", timeout=60000)
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(300)

                    overflow_data = page.evaluate(
                        """
                        () => {
                          const doc = document.documentElement;
                          const hasOverflow = doc.scrollWidth > doc.clientWidth + 1;
                          const offenders = [];
                          const nodes = document.querySelectorAll("body *");
                          for (const node of nodes) {
                            if (offenders.length >= 12) break;
                            const rect = node.getBoundingClientRect();
                            if (rect.right > window.innerWidth + 1 || rect.left < -1) {
                              offenders.push({
                                tag: node.tagName.toLowerCase(),
                                className: node.className || "",
                                right: Number(rect.right.toFixed(2)),
                                left: Number(rect.left.toFixed(2))
                              });
                            }
                          }
                          return {
                            hasOverflow,
                            scrollWidth: doc.scrollWidth,
                            clientWidth: doc.clientWidth,
                            offenders
                          };
                        }
                        """
                    )

                    shot_name = f"{page_key}-{width}.png"
                    page.screenshot(path=str(out_dir / shot_name), full_page=True)

                    entry = {
                        "page": page_name,
                        "viewport": {"width": width, "height": height},
                        "screenshot": shot_name,
                        "overflow": overflow_data,
                        "console_errors": console_errors,
                    }
                    report["results"].append(entry)
                    report["summary"]["total_checks"] += 1
                    if overflow_data["hasOverflow"]:
                        report["summary"]["overflow_failures"] += 1
                    if console_errors:
                        report["summary"]["console_error_failures"] += 1

                    context.close()
        finally:
            browser.close()

    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = [
        f"Viewport Sweep: {report['summary']['total_checks']} checks",
        f"Overflow failures: {report['summary']['overflow_failures']}",
        f"Console error failures: {report['summary']['console_error_failures']}",
        "",
    ]
    for item in report["results"]:
        overflow = item["overflow"]
        has_issue = overflow["hasOverflow"] or bool(item["console_errors"])
        if not has_issue:
            continue
        lines.append(
            f"- {item['page']} @ {item['viewport']['width']}x{item['viewport']['height']}: "
            f"overflow={overflow['hasOverflow']} console_errors={len(item['console_errors'])}"
        )
    (out_dir / "report.txt").write_text("\n".join(lines), encoding="utf-8")
    return report


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Viewport sweep audit")
    parser.add_argument(
        "--page",
        nargs="+",
        help="Specific pages to audit (e.g., --page shop.html cart.html). Defaults to all pages.",
    )
    args = parser.parse_args()

    if args.page:
        # Validate provided pages exist in known list
        unknown = [p for p in args.page if p not in PAGES]
        if unknown:
            print(f"Warning: unknown pages will still be audited: {unknown}")
        pages_to_audit = args.page
    else:
        pages_to_audit = PAGES

    server = start_server()
    try:
        report = run_audit(pages_to_audit)
        print(json.dumps(report["summary"], indent=2))
        print(report["out_dir"])
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
