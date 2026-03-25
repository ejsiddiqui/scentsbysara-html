from __future__ import annotations

import argparse
import os
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "templates"
TEMPLATE_FILES = [
    "docs/qa/agent-workflow.md",
    "docs/qa/viewport_audit.py",
    "docs/qa/token_audit.py",
    "docs/qa/precommit_token_gate.py",
    "docs/qa/token_rules.json",
    ".githooks/pre-commit",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install reusable QA guardrail files into a target repository."
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to target repository root (default: current directory).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview operations without writing files.",
    )
    return parser.parse_args()


def install_file(repo_root: Path, rel_path: str, force: bool, dry_run: bool) -> str:
    source = TEMPLATE_ROOT / rel_path
    target = repo_root / rel_path
    existed_before = target.exists()

    if not source.exists():
        return f"missing-template: {rel_path}"

    if existed_before and not force:
        return f"skipped-existing: {rel_path}"

    if dry_run:
        action = "overwrite" if existed_before else "create"
        return f"{action}: {rel_path}"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    if rel_path == ".githooks/pre-commit":
        try:
            mode = os.stat(target).st_mode
            os.chmod(target, mode | 0o111)
        except OSError:
            pass

    action = "overwrote" if existed_before else "created"
    return f"{action}: {rel_path}"


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo).resolve()

    if not repo_root.exists():
        print(f"Target repo does not exist: {repo_root}")
        return 1

    if not TEMPLATE_ROOT.exists():
        print(f"Template directory not found: {TEMPLATE_ROOT}")
        return 1

    print(f"Installing QA guardrails into: {repo_root}")
    print(f"Mode: {'dry-run' if args.dry_run else 'write'}")
    print("")

    for rel_path in TEMPLATE_FILES:
        result = install_file(repo_root, rel_path, args.force, args.dry_run)
        print(f"- {result}")

    print("")
    print("Next steps:")
    print("1. Edit docs/qa/token_rules.json for your selectors/tokens.")
    print("2. Enable hooks: git config core.hooksPath .githooks")
    print("3. Run visual sweep: python docs/qa/viewport_audit.py")
    print("4. Run token audit: python docs/qa/token_audit.py --page <page>.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
