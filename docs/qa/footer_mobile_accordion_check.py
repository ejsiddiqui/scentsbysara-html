from __future__ import annotations

import argparse
import json
import os
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


REPO_ROOT = Path(__file__).resolve().parents[2]
PORT = 4173
DEFAULT_TASK_ID = "mobile-footer-accordion-20260314"
FOOTER_PAGES = ["shop.html", "index.html"]


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


def add_footer_checks(page, result: dict, page_name: str, out_dir: Path) -> None:
    sections = page.locator(".site-footer .footer-links-col")
    section_count = sections.count()

    result["checks"].append(
        {
            "name": f"{page_name} renders four footer accordion sections",
            "passed": section_count == 4,
            "actual": section_count,
            "expected": 4,
        }
    )

    for index in range(section_count):
        section = sections.nth(index)
        trigger = section.locator(".footer-accordion-trigger")
        panel = section.locator(".footer-link-list")
        icon = section.locator(".footer-accordion-icon")

        trigger_exists = trigger.count() == 1
        panel_state = (
            panel.evaluate(
                """
                (node) => {
                    const styles = window.getComputedStyle(node);
                    return {
                        display: styles.display,
                        maxHeight: styles.maxHeight,
                        opacity: styles.opacity,
                        paddingBottom: styles.paddingBottom
                    };
                }
                """
            )
            if panel.count() == 1
            else {"display": "", "maxHeight": "", "opacity": "", "paddingBottom": ""}
        )
        aria_expanded = trigger.get_attribute("aria-expanded") if trigger_exists else None
        icon_text = icon.inner_text().strip() if icon.count() == 1 else None
        transition_data = (
            panel.evaluate(
                """
                (node) => {
                    const styles = window.getComputedStyle(node);
                    return {
                        property: styles.transitionProperty,
                        duration: styles.transitionDuration
                    };
                }
                """
            )
            if panel.count() == 1
            else {"property": "", "duration": ""}
        )

        result["checks"].extend(
            [
                {
                    "name": f"{page_name} section {index + 1} has accordion trigger",
                    "passed": trigger_exists,
                    "actual": trigger.count(),
                    "expected": 1,
                },
                {
                    "name": f"{page_name} section {index + 1} starts collapsed",
                    "passed": aria_expanded == "false"
                    and panel_state["maxHeight"] in {"0px", "0"}
                    and panel_state["opacity"] in {"0", "0.0"},
                    "actual": {
                        "aria_expanded": aria_expanded,
                        "panel_state": panel_state,
                    },
                    "expected": {
                        "aria_expanded": "false",
                        "maxHeight": "0px",
                        "opacity": "0",
                    },
                },
                {
                    "name": f"{page_name} section {index + 1} shows plus icon when collapsed",
                    "passed": icon_text == "+",
                    "actual": icon_text,
                    "expected": "+",
                },
                {
                    "name": f"{page_name} section {index + 1} has slide transition styling",
                    "passed": "max-height" in transition_data["property"] and transition_data["duration"] != "0s",
                    "actual": transition_data,
                    "expected": {
                        "property_contains": "max-height",
                        "duration_not": "0s",
                    },
                },
            ]
        )

    if section_count:
        first_trigger = page.locator(".site-footer .footer-accordion-trigger").first
        first_panel = page.locator(".site-footer .footer-link-list").first
        first_icon = page.locator(".site-footer .footer-accordion-icon").first

        if first_trigger.count() == 1 and first_panel.count() == 1 and first_icon.count() == 1:
            first_trigger.click()
            page.wait_for_timeout(250)

            result["checks"].extend(
                [
                    {
                        "name": f"{page_name} first section expands on tap",
                        "passed": first_trigger.get_attribute("aria-expanded") == "true"
                        and first_panel.evaluate(
                            """
                            (node) => {
                                const styles = window.getComputedStyle(node);
                                return styles.maxHeight !== '0px' && styles.opacity !== '0';
                            }
                            """
                        ),
                        "actual": {
                            "aria_expanded": first_trigger.get_attribute("aria-expanded"),
                            "panel_state": first_panel.evaluate(
                                """
                                (node) => {
                                    const styles = window.getComputedStyle(node);
                                    return {
                                        maxHeight: styles.maxHeight,
                                        opacity: styles.opacity,
                                        paddingBottom: styles.paddingBottom
                                    };
                                }
                                """
                            ),
                        },
                        "expected": {
                            "aria_expanded": "true",
                            "maxHeight_not": "0px",
                            "opacity_not": "0",
                        },
                    },
                    {
                        "name": f"{page_name} first section icon flips to minus",
                        "passed": first_icon.inner_text().strip() == "-",
                        "actual": first_icon.inner_text().strip(),
                        "expected": "-",
                    },
                ]
            )

    page.screenshot(path=str(out_dir / f"{page_name.replace('.html', '')}-footer-mobile-accordion-check.png"), full_page=True)


def add_product_accordion_checks(page, result: dict, out_dir: Path) -> None:
    accordions = page.locator(".accordion")
    accordion_count = accordions.count()

    result["checks"].append(
        {
            "name": "product page exposes accordion blocks",
            "passed": accordion_count >= 4,
            "actual": accordion_count,
            "expected_at_least": 4,
        }
    )

    interactive_accordion = accordions.nth(1)
    trigger = interactive_accordion.locator(".accordion-header")
    panel = interactive_accordion.locator(".accordion-body")

    if trigger.count() == 1 and panel.count() == 1:
        before = panel.evaluate(
            """
            (node) => {
                const styles = window.getComputedStyle(node);
                return {
                    display: styles.display,
                    maxHeight: styles.maxHeight,
                    opacity: styles.opacity,
                    transitionProperty: styles.transitionProperty,
                    transitionDuration: styles.transitionDuration
                };
            }
            """
        )

        trigger.click()
        page.wait_for_timeout(250)

        after = panel.evaluate(
            """
            (node) => {
                const styles = window.getComputedStyle(node);
                return {
                    display: styles.display,
                    maxHeight: styles.maxHeight,
                    opacity: styles.opacity,
                };
            }
            """
        )

        result["checks"].extend(
            [
                {
                    "name": "product accordion starts collapsed",
                    "passed": before["maxHeight"] in {"0px", "0"} and before["opacity"] in {"0", "0.0"},
                    "actual": before,
                    "expected": {
                        "maxHeight": "0px",
                        "opacity": "0",
                    },
                },
                {
                    "name": "product accordion has slide transition styling",
                    "passed": "max-height" in before["transitionProperty"] and before["transitionDuration"] != "0s",
                    "actual": {
                        "transitionProperty": before["transitionProperty"],
                        "transitionDuration": before["transitionDuration"],
                    },
                    "expected": {
                        "property_contains": "max-height",
                        "duration_not": "0s",
                    },
                },
                {
                    "name": "product accordion expands with visible content",
                    "passed": after["maxHeight"] not in {"0px", "0"} and after["opacity"] != "0",
                    "actual": after,
                    "expected": {
                        "maxHeight_not": "0px",
                        "opacity_not": "0",
                    },
                },
            ]
        )

    page.screenshot(path=str(out_dir / "product-accordion-transition-check.png"), full_page=True)


def run_check(task_id: str) -> tuple[dict, int]:
    out_dir = REPO_ROOT / "docs" / "qa" / "implementation" / task_id
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "footer-mobile-accordion-report.json"
    base_url = f"http://127.0.0.1:{PORT}"

    result: dict[str, object] = {
        "base_url": base_url,
        "viewport": {"width": 390, "height": 844},
        "checks": [],
        "passed": True,
        "screenshots_dir": str(out_dir),
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for page_name in FOOTER_PAGES:
                context = browser.new_context(viewport={"width": 390, "height": 844})
                page = context.new_page()
                page.goto(f"{base_url}/{page_name}", wait_until="load", timeout=60000)
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(300)
                add_footer_checks(page, result, page_name, out_dir)
                context.close()

            product_context = browser.new_context(viewport={"width": 390, "height": 844})
            product_page = product_context.new_page()
            product_page.goto(f"{base_url}/product.html", wait_until="load", timeout=60000)
            product_page.wait_for_load_state("networkidle")
            product_page.wait_for_timeout(300)
            add_product_accordion_checks(product_page, result, out_dir)
            product_context.close()
        finally:
            browser.close()

    result["passed"] = all(check["passed"] for check in result["checks"])
    report_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result, 0 if result["passed"] else 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", default=DEFAULT_TASK_ID)
    args = parser.parse_args()

    server = start_server()
    try:
        result, exit_code = run_check(args.task_id)
        print(json.dumps(result, indent=2))
        raise SystemExit(exit_code)
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
