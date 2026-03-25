from __future__ import annotations

import argparse
import json
import os
import threading
import time
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_VIEWPORTS = [
    (1920, 1080),
    (1440, 1024),
    (1024, 1366),
    (768, 1024),
    (390, 844),
    (375, 812),
]
KNOWN_HEIGHTS = {
    1920: 1080,
    1440: 1024,
    1024: 1366,
    768: 1024,
    390: 844,
    375: 812,
}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return


def discover_pages() -> list[str]:
    return sorted(path.name for path in REPO_ROOT.glob("*.html") if path.is_file())


def build_viewports(widths: list[int] | None) -> list[tuple[int, int]]:
    if not widths:
        return DEFAULT_VIEWPORTS
    return [(width, KNOWN_HEIGHTS.get(width, 1080)) for width in widths]


def start_server(port: int) -> ThreadingHTTPServer:
    os.chdir(REPO_ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", port), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.25)
    return server


def run_audit(
    pages: list[str],
    viewports: list[tuple[int, int]],
    port: int,
    settle_ms: int,
) -> dict:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = REPO_ROOT / "docs" / "qa" / f"sweep-{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    base_url = f"http://127.0.0.1:{port}"

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
                for width, height in viewports:
                    context = browser.new_context(viewport={"width": width, "height": height})
                    page = context.new_page()
                    console_errors: list[str] = []
                    page.on(
                        "console",
                        lambda msg: console_errors.append(msg.text)
                        if msg.type == "error"
                        else None,
                    )

                    page.goto(f"{base_url}/{page_name}", wait_until="load", timeout=60000)
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(settle_ms)

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run multi-page, multi-viewport visual/runtime QA checks."
    )
    parser.add_argument(
        "--page",
        action="append",
        help="HTML page to include (repeatable), e.g. --page index.html",
    )
    parser.add_argument(
        "--width",
        action="append",
        type=int,
        help="Viewport width to include (repeatable), e.g. --width 1920 --width 768",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=4173,
        help="Local server port (default: 4173).",
    )
    parser.add_argument(
        "--settle-ms",
        type=int,
        default=300,
        help="Post-network-idle delay in milliseconds (default: 300).",
    )
    parser.add_argument(
        "--fail-on-blockers",
        action="store_true",
        help="Exit with code 1 when overflow or console errors are found.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pages = args.page if args.page else discover_pages()
    if not pages:
        raise SystemExit("No HTML pages found. Add --page or place HTML files in repo root.")

    viewports = build_viewports(args.width)
    server = start_server(args.port)
    try:
        report = run_audit(pages, viewports, args.port, args.settle_ms)
        print(json.dumps(report["summary"], indent=2))
        print(report["out_dir"])
    finally:
        server.shutdown()
        server.server_close()

    if args.fail_on_blockers:
        summary = report["summary"]
        blockers = summary["overflow_failures"] + summary["console_error_failures"]
        if blockers:
            raise SystemExit(1)


if __name__ == "__main__":
    main()

