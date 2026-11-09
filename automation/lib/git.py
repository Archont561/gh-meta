"""Shared Git subprocess helpers for automation modules."""

from __future__ import annotations

import subprocess
from collections.abc import Callable, Sequence
from pathlib import Path

GitRunner = Callable[[Sequence[str]], tuple[int, str]]


def run_git(argv: Sequence[str], cwd: Path | None = None) -> tuple[int, str]:
    """Execute a git command and return `(returncode, stdout)`."""
    completed = subprocess.run(list(argv), cwd=cwd, capture_output=True, text=True, check=False)
    return completed.returncode, completed.stdout


def is_shallow_repository(
    root: Path, run: Callable[[Sequence[str], Path], tuple[int, str]]
) -> bool:
    """Return True when `root` is a shallow Git checkout."""
    code, output = run(["git", "rev-parse", "--is-shallow-repository"], root)
    return code == 0 and output.strip() == "true"


def reset_clean_clone(path: Path, run: Callable[[Sequence[str]], object] | None = None) -> bool:
    """Reset and clean a cached Git clone directory if `.git` exists."""
    if not (path / ".git").is_dir():
        return False
    execute = run or _run_quiet
    execute(["git", "-C", str(path), "reset", "--hard", "HEAD"])
    execute(["git", "-C", str(path), "clean", "-ffdx"])
    return True


def _run_quiet(argv: Sequence[str]) -> object:
    return subprocess.run(list(argv), check=False, capture_output=True)
