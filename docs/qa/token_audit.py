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
RULES_PATH = Path(__file__).resolve().with_name("token_rules.json")
PORT = 4173
DEFAULT_VIEWPORTS = [
    (1920, 1080),
    (768, 1024),
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


def start_server() -> ThreadingHTTPServer:
    os.chdir(REPO_ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", PORT), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.25)
    return server


def load_rules(requested_pages: list[str] | None) -> dict[str, list[dict[str, str]]]:
    if not RULES_PATH.exists():
        raise FileNotFoundError(f"Missing rules file: {RULES_PATH}")

    raw_rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw_rules, dict):
        raise ValueError("token_rules.json must be an object keyed by page name.")

    selected: dict[str, list[dict[str, str]]] = {}
    for page_name, page_rules in raw_rules.items():
        if requested_pages and page_name not in requested_pages:
            continue
        if not isinstance(page_rules, list):
            raise ValueError(f"Rules for {page_name} must be a list.")
        selected[page_name] = page_rules

    if requested_pages:
        missing_pages = [page for page in requested_pages if page not in selected]
        if missing_pages:
            raise ValueError(f"No token rules found for page(s): {', '.join(missing_pages)}")

    if not selected:
        raise ValueError("No token rules selected. Add rules or pass valid --page values.")

    return selected


def build_viewports(widths: list[int] | None) -> list[tuple[int, int]]:
    if not widths:
        return DEFAULT_VIEWPORTS
    return [(width, KNOWN_HEIGHTS.get(width, 1080)) for width in widths]


def run_audit(
    selected_rules: dict[str, list[dict[str, str]]],
    viewports: list[tuple[int, int]],
) -> dict:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = REPO_ROOT / "docs" / "qa" / f"token-audit-{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    base_url = f"http://127.0.0.1:{PORT}"

    report: dict[str, object] = {
        "timestamp": stamp,
        "base_url": base_url,
        "out_dir": str(out_dir),
        "results": [],
        "summary": {
            "total_checks": 0,
            "passes": 0,
            "failures": 0,
            "missing_selectors": 0,
            "invalid_tokens": 0,
        },
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for page_name, page_rules in selected_rules.items():
                for width, height in viewports:
                    context = browser.new_context(viewport={"width": width, "height": height})
                    page = context.new_page()
                    page.goto(f"{base_url}/{page_name}", wait_until="load", timeout=60000)
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(250)

                    checks = page.evaluate(
                        """
                        (rules) => {
                          const canonicalize = (property, value) => {
                            const probe = document.createElement("div");
                            probe.style.setProperty(property, value);
                            document.body.appendChild(probe);
                            const computed = getComputedStyle(probe).getPropertyValue(property).trim();
                            probe.remove();
                            return computed;
                          };

                          const root = getComputedStyle(document.documentElement);

                          // Collect all CSS custom properties from :root for reverse-lookup
                          const allTokens = {};
                          for (const sheet of document.styleSheets) {
                            try {
                              for (const cssRule of sheet.cssRules) {
                                if (cssRule.selectorText === ':root') {
                                  for (const prop of cssRule.style) {
                                    if (prop.startsWith('--')) {
                                      allTokens[prop] = root.getPropertyValue(prop).trim();
                                    }
                                  }
                                }
                              }
                            } catch (e) {}
                          }

                          return rules.map((rule) => {
                            if (Array.isArray(rule.widths) && rule.widths.length && !rule.widths.includes(window.innerWidth)) {
                              return null;
                            }

                            const tokenValue = root.getPropertyValue(rule.token).trim();
                            const expected = canonicalize(rule.property, `var(${rule.token})`);
                            const nodes = Array.from(document.querySelectorAll(rule.selector));

                            if (!tokenValue || !expected) {
                              return {
                                selector: rule.selector,
                                property: rule.property,
                                token: rule.token,
                                description: rule.description || "",
                                status: "invalid_token",
                                expected,
                                tokenValue,
                                totalMatches: nodes.length,
                                offenders: [],
                                matched_token: null,
                              };
                            }

                            if (!nodes.length) {
                              return {
                                selector: rule.selector,
                                property: rule.property,
                                token: rule.token,
                                description: rule.description || "",
                                status: "missing_selector",
                                expected,
                                tokenValue,
                                totalMatches: 0,
                                offenders: [],
                                matched_token: null,
                              };
                            }

                            const offenders = [];
                            nodes.forEach((node, idx) => {
                              const actual = getComputedStyle(node).getPropertyValue(rule.property).trim();
                              if (actual !== expected) {
                                offenders.push({
                                  index: idx,
                                  actual,
                                  text: (node.textContent || "").trim().slice(0, 100),
                                });
                              }
                            });

                            // For failures, find which token the actual value maps to
                            let matched_token = null;
                            if (offenders.length) {
                              const actual = offenders[0].actual;
                              for (const [tokenName, tokenVal] of Object.entries(allTokens)) {
                                if (tokenName === rule.token) continue;
                                const canonVal = canonicalize(rule.property, `var(${tokenName})`);
                                if (canonVal === actual) {
                                  matched_token = tokenName;
                                  break;
                                }
                              }
                            }

                            return {
                              selector: rule.selector,
                              property: rule.property,
                              token: rule.token,
                              description: rule.description || "",
                              status: offenders.length ? "fail" : "pass",
                              expected,
                              tokenValue,
                              totalMatches: nodes.length,
                              offenders,
                              matched_token,
                            };
                          });
                        }
                        """,
                        page_rules,
                    )

                    for check in checks:
                        if not check:
                            continue
                        report["results"].append(
                            {
                                "page": page_name,
                                "viewport": {"width": width, "height": height},
                                "check": check,
                            }
                        )
                        report["summary"]["total_checks"] += 1
                        status = check["status"]
                        if status == "pass":
                            report["summary"]["passes"] += 1
                        elif status == "fail":
                            report["summary"]["failures"] += 1
                        elif status == "missing_selector":
                            report["summary"]["missing_selectors"] += 1
                        elif status == "invalid_token":
                            report["summary"]["invalid_tokens"] += 1

                    context.close()
        finally:
            browser.close()

    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        f"Token Audit: {report['summary']['total_checks']} checks",
        f"Passes: {report['summary']['passes']}",
        f"Failures: {report['summary']['failures']}",
        f"Missing selectors: {report['summary']['missing_selectors']}",
        f"Invalid tokens: {report['summary']['invalid_tokens']}",
        "",
    ]

    for entry in report["results"]:
        check = entry["check"]
        if check["status"] == "pass":
            continue
        lines.append(
            f"- {entry['page']} @ {entry['viewport']['width']}x{entry['viewport']['height']} | "
            f"{check['selector']} -> {check['property']} ({check['status']})"
        )
        lines.append(
            f"  expected: {check['expected']} from var({check['token']}) [{check['tokenValue']}]"
        )
        if check["status"] == "fail":
            for offender in check["offenders"][:5]:
                lines.append(
                    f"  actual: {offender['actual']} | text=\"{offender['text']}\""
                )

    (out_dir / "report.txt").write_text("\n".join(lines), encoding="utf-8")
    return report


def apply_rule_updates(report: dict) -> int:
    """Update token_rules.json with matched tokens from audit failures.

    Returns the number of rules updated.
    """
    raw_rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    updated = 0

    for entry in report["results"]:
        check = entry["check"]
        if check["status"] != "fail" or not check.get("matched_token"):
            continue

        page_name = entry["page"]
        page_rules = raw_rules.get(page_name, [])
        viewport = entry["viewport"]

        for rule in page_rules:
            if rule["selector"] != check["selector"]:
                continue
            if rule["property"] != check["property"]:
                continue
            if rule["token"] == check["matched_token"]:
                continue
            # For width-scoped rules, only update if viewport matches
            if rule.get("widths") and viewport["width"] not in rule["widths"]:
                continue

            old_token = rule["token"]
            rule["token"] = check["matched_token"]
            updated += 1
            print(
                f"[update-rules] {page_name} | {rule['selector']} "
                f"({rule['property']}): {old_token} -> {check['matched_token']}"
            )

    if updated:
        RULES_PATH.write_text(
            json.dumps(raw_rules, indent=4) + "\n", encoding="utf-8"
        )
        print(f"[update-rules] Updated {updated} rule(s) in {RULES_PATH.name}")
    else:
        print("[update-rules] No token changes detected to update.")

    return updated


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit CSS token compliance for selectors defined in docs/qa/token_rules.json."
    )
    parser.add_argument(
        "--page",
        action="append",
        help="Page to audit (repeatable), e.g. --page product.html",
    )
    parser.add_argument(
        "--width",
        action="append",
        type=int,
        help="Viewport width to audit (repeatable), e.g. --width 1920 --width 768",
    )
    parser.add_argument(
        "--update-rules",
        action="store_true",
        help="Update token_rules.json with actual token values instead of failing. "
        "Use when design token usage has intentionally changed.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selected_rules = load_rules(args.page)
    viewports = build_viewports(args.width)

    server = start_server()
    try:
        report = run_audit(selected_rules, viewports)
        print(json.dumps(report["summary"], indent=2))
        print(report["out_dir"])
    finally:
        server.shutdown()
        server.server_close()

    summary = report["summary"]
    failed = summary["failures"] + summary["missing_selectors"] + summary["invalid_tokens"]

    if failed and args.update_rules:
        apply_rule_updates(report)
        return

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
