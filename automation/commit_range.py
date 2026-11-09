#!/usr/bin/env python3
"""Check conventional commits over the exact commit range introduced by a CI event."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence

DEFAULT_DEPTH = 20
NO_BASE = "0" * 40

Runner = Callable[[Sequence[str]], int]


def resolve_range(event: str, pr_base: str = "", push_base: str = "") -> str:
    """Resolve the git range for a pull request or push event."""
    if event == "pull_request" and pr_base:
        return f"{pr_base}..HEAD"
    if push_base and push_base != NO_BASE:
        return f"{push_base}..HEAD"
    return ""


def command(range_: str, depth: int = DEFAULT_DEPTH) -> list[str]:
    """Return the `convco check` argv list."""
    if range_:
        return ["convco", "check", range_]
    return ["convco", "check", "-n", str(depth)]


def check(event: str, pr_base: str = "", push_base: str = "") -> list[str]:
    """Build the commit check invocation for a CI event."""
    return command(resolve_range(event, pr_base, push_base))


def main(
    argv: Sequence[str] | None = None,
    env: Mapping[str, str] | None = None,
    run: Runner | None = None,
) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("action", nargs="?", default="check", choices=["check", "resolve"])
    arguments = parser.parse_args(argv)

    environment = os.environ if env is None else env
    invocation = check(
        environment.get("EVENT", ""),
        environment.get("PR_BASE", ""),
        environment.get("PUSH_BASE", ""),
    )

    if arguments.action == "resolve":
        print(" ".join(invocation))
        return 0

    execute = run or _run
    try:
        return execute(invocation)
    except FileNotFoundError:
        print("commit-range: convco is not on PATH; run via Pixi", file=sys.stderr)
        return 1


def _run(argv: Sequence[str]) -> int:
    return subprocess.run(list(argv), check=False).returncode


if __name__ == "__main__":
    sys.exit(main())
