#!/usr/bin/env python3
"""Maintain the weekly RustSec advisory-database cache for CI."""

from __future__ import annotations

import argparse
import datetime
import os
import sys
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.lib.git import reset_clean_clone  # noqa: E402

Runner = Callable[[Sequence[str]], object]


def cache_key(today: datetime.date | None = None) -> str:
    """Return `<ISO year>-W<ISO week>` for weekly advisory DB caching."""
    date = today or datetime.datetime.now(datetime.UTC).date()
    iso = date.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def clean(paths: Iterable[Path], run: Runner | None = None) -> list[Path]:
    """Reset any restored advisory DB clones."""
    return [path for path in paths if reset_clean_clone(path, run=run)]


def default_paths(cargo_home: Path | None = None, home: Path | None = None) -> list[Path]:
    """Return default advisory-db locations under CARGO_HOME or ~/.cargo."""
    cargo = cargo_home if cargo_home is not None else (home or Path.home()) / ".cargo"
    paths = [cargo / "advisory-db"]
    nested = cargo / "advisory-dbs"
    if nested.is_dir():
        paths.extend(sorted(child for child in nested.iterdir() if child.is_dir()))
    return paths


def main(
    argv: Sequence[str] | None = None,
    today: datetime.date | None = None,
    output: Path | str | None = None,
    run: Runner | None = None,
) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("action", choices=["key", "clean"])
    parser.add_argument("--cargo-home", type=Path)
    arguments = parser.parse_args(argv)

    if arguments.action == "key":
        from automation.lib.github_actions import set_output

        set_output("week", cache_key(today), path=output)
        return 0

    redirected = os.environ.get("CARGO_HOME")
    cargo_home = arguments.cargo_home or (Path(redirected) if redirected else None)
    cleaned = clean(default_paths(cargo_home=cargo_home), run=run)
    print(f"advisory-cache: cleaned {len(cleaned)} clone(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
