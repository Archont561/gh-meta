"""File-based GitHub Actions step outputs, summaries, and annotations."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def set_output(name: str, value: str, path: Path | str | None = None) -> None:
    """Write a step output to GITHUB_OUTPUT or print when running locally."""
    target = _target(path, "GITHUB_OUTPUT")
    if target is None:
        print(f"{name}={value}")
        return

    if "\n" in value:
        delimiter = f"EOF_{name}"
        block = f"{name}<<{delimiter}\n{value}\n{delimiter}\n"
    else:
        block = f"{name}={value}\n"
    with target.open("a", encoding="utf-8") as handle:
        handle.write(block)


def append_summary(markdown: str, path: Path | str | None = None) -> None:
    """Append a markdown section to GITHUB_STEP_SUMMARY or print locally."""
    target = _target(path, "GITHUB_STEP_SUMMARY")
    if target is None:
        print(markdown)
        return
    with target.open("a", encoding="utf-8") as handle:
        handle.write(f"{markdown.rstrip()}\n\n")


def set_error(message: str) -> None:
    """Emit a GitHub Actions error annotation to stderr."""
    print(f"::error::{message}", file=sys.stderr)


def _target(path: Path | str | None, variable: str) -> Path | None:
    if path is not None:
        return Path(path)
    location = os.environ.get(variable)
    return Path(location) if location else None
