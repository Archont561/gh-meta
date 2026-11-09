#!/usr/bin/env python3
"""Determine whether a CI change touches only documentation files."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.commit_range import resolve_range  # noqa: E402
from automation.lib.git import run_git  # noqa: E402
from automation.lib.github_actions import append_summary, set_output  # noqa: E402

DOCS_ONLY = "docs-only"
DOCUMENTATION_DIRECTORIES = ("backlog", "docs")
DOCUMENTATION_SUFFIX = ".md"
ROOT_DOCUMENT_PREFIX = "LICENSE"

Git = Callable[[Sequence[str]], tuple[int, str]]


def is_documentation(path: str) -> bool:
    """Return True when `path` is purely documentation."""
    parts = PurePosixPath(path).parts
    if not parts:
        return False
    if parts[0] in DOCUMENTATION_DIRECTORIES and len(parts) > 1:
        return True
    if len(parts) == 1 and parts[0].startswith(ROOT_DOCUMENT_PREFIX):
        return True
    return path.endswith(DOCUMENTATION_SUFFIX)


def documentation_only(paths: Sequence[str]) -> bool:
    """Return True when `paths` is non-empty and every entry is documentation."""
    return bool(paths) and all(is_documentation(path) for path in paths)


def diff_command(range_: str) -> list[str]:
    return ["git", "diff", "--name-only", "-z", "--no-renames", range_]


def changed_paths(range_: str, git: Git) -> tuple[list[str] | None, str]:
    """List paths changed in `range_`, or `(None, reason)` if indeterminate."""
    if not range_:
        return None, "there is no base commit to compare against"
    try:
        code, output = git(diff_command(range_))
    except FileNotFoundError:
        return None, "git is not installed"
    if code != 0:
        return None, f"git could not compute diff for `{range_}`"
    return [path for path in output.split("\0") if path], ""


def main(
    argv: Sequence[str] | None = None,
    env: Mapping[str, str] | None = None,
    git: Git | None = None,
) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.parse_args(argv)

    environment = os.environ if env is None else env
    range_ = resolve_range(
        environment.get("EVENT", ""),
        environment.get("PR_BASE", ""),
        environment.get("PUSH_BASE", ""),
    )
    paths, reason = changed_paths(range_, git or run_git)
    docs_only = paths is not None and documentation_only(paths)

    set_output(DOCS_ONLY, "true" if docs_only else "false", environment.get("GITHUB_OUTPUT"))
    heading = "**Documentation only**" if docs_only else "**Full CI**"
    detail = f"\n\nNot classified because {reason}." if reason else ""
    append_summary(f"### Change scope\n\n{heading}{detail}", environment.get("GITHUB_STEP_SUMMARY"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
