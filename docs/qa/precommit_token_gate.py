from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RULES_PATH = Path(__file__).resolve().with_name("token_rules.json")
GLOBAL_TRIGGER_FILES = {
    "css/design-tokens.css",
    "css/layout.css",
    "css/components.css",
    "css/responsive.css",
}


def get_staged_files() -> set[str]:
    cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"]
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print("[token-gate] Unable to read staged files.")
        print(result.stderr.strip())
        return set()
    return {line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()}


def load_rule_pages() -> list[str]:
    if not RULES_PATH.exists():
        return []
    raw = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return []
    pages = [str(page) for page in raw.keys()]
    return sorted(pages)


def page_css_file(page_name: str) -> str:
    stem = Path(page_name).stem
    return f"assets/css/{stem}.css"


def resolve_pages_to_audit(staged_files: set[str], rule_pages: list[str]) -> list[str]:
    if not staged_files or not rule_pages:
        return []

    if staged_files.intersection(GLOBAL_TRIGGER_FILES):
        return rule_pages

    selected: set[str] = set()
    for page in rule_pages:
        if page in staged_files:
            selected.add(page)
            continue
        if page_css_file(page) in staged_files:
            selected.add(page)

    return sorted(selected)


def run_token_audit(pages: list[str], *, update_rules: bool = False) -> int:
    cmd = [sys.executable, "docs/qa/token_audit.py"]
    for page in pages:
        cmd.extend(["--page", page])
    if update_rules:
        cmd.append("--update-rules")

    print(f"[token-gate] Running token audit for: {', '.join(pages)}")
    result = subprocess.run(cmd, cwd=REPO_ROOT, check=False)
    return result.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pre-commit gate that runs the token audit on staged files."
    )
    parser.add_argument(
        "--update-rules",
        action="store_true",
        help="Update token_rules.json with actual token values instead of blocking "
        "the commit. Use when design token usage has intentionally changed.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    staged_files = get_staged_files()
    rule_pages = load_rule_pages()
    pages = resolve_pages_to_audit(staged_files, rule_pages)

    if not pages:
        print("[token-gate] Skipped (no token-relevant staged changes).")
        return 0

    code = run_token_audit(pages, update_rules=args.update_rules)
    if code != 0 and not args.update_rules:
        print("[token-gate] Blocking commit due to token audit failures.")
        print("[token-gate] Tip: re-run with --update-rules to accept the changes.")
    else:
        print("[token-gate] Passed.")
    return 0 if args.update_rules else code


if __name__ == "__main__":
    raise SystemExit(main())
