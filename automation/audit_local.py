#!/usr/bin/env python3
"""Run cargo-audit locally only when an advisory database clone is present."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def database_path(cargo_home: str | None, home: Path) -> Path:
    """Resolve the cargo-audit database clone location."""
    if cargo_home:
        return Path(cargo_home) / "advisory-db"
    return home / ".cargo" / "advisory-db"


def database_ready(path: Path) -> bool:
    """Return True if a cloned RustSec database exists."""
    return (path / "crates").is_dir()


def decide(ready: bool, require: bool) -> str:
    """Return `run`, `skip`, or `fail`."""
    if ready:
        return "run"
    return "fail" if require else "skip"


def audit_command(database: Path) -> list[str]:
    """Return offline `cargo audit` command line."""
    return ["cargo", "audit", "--db", str(database), "--no-fetch", "--stale", "--deny", "warnings"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require",
        action="store_true",
        help="fail when no local advisory database is present",
    )
    args = parser.parse_args(argv)

    database = database_path(os.environ.get("CARGO_HOME"), Path.home())
    ready = database_ready(database)
    action = decide(ready, args.require)

    if action == "skip":
        print(
            f"audit: no local advisory database at {database}; offline audit skipped",
            file=sys.stderr,
        )
        return 0
    if action == "fail":
        print(
            f"audit: missing required advisory database at {database}",
            file=sys.stderr,
        )
        return 1

    result = subprocess.run(audit_command(database), cwd=ROOT, check=False)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
