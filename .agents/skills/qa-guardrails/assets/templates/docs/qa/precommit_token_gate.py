from __future__ import annotations

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
    return sorted(str(page) for page in raw.keys())


def page_css_candidates(page_name: str) -> list[str]:
    stem = Path(page_name).stem
    return [
        f"assets/css/{stem}.css",
        f"css/{stem}.css",
    ]


def resolve_pages_to_audit(staged_files: set[str], rule_pages: list[str]) -> list[str]:
    if not staged_files or not rule_pages:
        return []

    global_css_changed = any(path.startswith("css/") and path.endswith(".css") for path in staged_files)
    if staged_files.intersection(GLOBAL_TRIGGER_FILES) or global_css_changed:
        return rule_pages

    selected: set[str] = set()
    for page in rule_pages:
        if page in staged_files:
            selected.add(page)
            continue
        if any(candidate in staged_files for candidate in page_css_candidates(page)):
            selected.add(page)

    return sorted(selected)


def run_token_audit(pages: list[str]) -> int:
    cmd = [sys.executable, "docs/qa/token_audit.py"]
    for page in pages:
        cmd.extend(["--page", page])

    print(f"[token-gate] Running token audit for: {', '.join(pages)}")
    result = subprocess.run(cmd, cwd=REPO_ROOT, check=False)
    return result.returncode


def main() -> int:
    staged_files = get_staged_files()
    rule_pages = load_rule_pages()
    pages = resolve_pages_to_audit(staged_files, rule_pages)

    if not pages:
        print("[token-gate] Skipped (no token-relevant staged changes).")
        return 0

    code = run_token_audit(pages)
    if code != 0:
        print("[token-gate] Blocking commit due to token audit failures.")
    else:
        print("[token-gate] Passed.")
    return code


if __name__ == "__main__":
    raise SystemExit(main())

