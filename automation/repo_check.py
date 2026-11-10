#!/usr/bin/env python3
"""Verify cross-file repository invariants that sit outside single-tool linters."""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check_repo(root: Path = ROOT) -> list[str]:
    """Return human-readable problems across repository structure and parity contracts."""
    problems: list[str] = []

    root_license = root / "LICENSE"
    if not root_license.is_file():
        problems.append("missing root LICENSE file")
    else:
        expected_license = root_license.read_text(encoding="utf-8")
        for crate in ("gh-repoconf-core", "gh-repoconf"):
            crate_license = root / "crates" / crate / "LICENSE"
            if not crate_license.is_file():
                problems.append(f"missing crate LICENSE: crates/{crate}/LICENSE")
            elif crate_license.read_text(encoding="utf-8") != expected_license:
                problems.append(f"crates/{crate}/LICENSE differs from root LICENSE")

    claude = root / "CLAUDE.md"
    if not claude.is_symlink() or str(claude.readlink()) != "AGENTS.md":
        problems.append("CLAUDE.md must be a symlink pointing to AGENTS.md")

    restore = root / "scripts" / "restore.sh"
    if not restore.is_file():
        problems.append("missing generated scripts/restore.sh")

    sandbox_path = root / "pixi-sandbox.toml"
    if sandbox_path.is_file():
        sandbox = tomllib.loads(sandbox_path.read_text(encoding="utf-8"))
        bundles = sandbox.get("bundle", [])
        if not bundles or bundles[0].get("platforms") != ["linux-64"]:
            problems.append("pixi-sandbox.toml must configure linux-64 developer bundle")

    return problems


def main(root: Path = ROOT) -> int:
    problems = check_repo(root)
    if problems:
        for problem in problems:
            print(f"repo-check: {problem}", file=sys.stderr)
        return 1
    print("repo-check: all repository invariants hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
