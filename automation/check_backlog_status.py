#!/usr/bin/env python3
"""Verify that every backlog task card's status matches its acceptance criteria checkboxes."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "backlog" / "tasks"

STATUS = re.compile(r"^status:\s*(?P<status>.+?)\s*$", re.MULTILINE)
CRITERION = re.compile(r"^- \[(?P<mark>[ xX])\] #\d+", re.MULTILINE)
AC_BLOCK = re.compile(r"<!-- AC:BEGIN -->(?P<body>.*?)<!-- AC:END -->", re.DOTALL)

DONE = "Done"


@dataclass(frozen=True)
class Task:
    """One backlog task reduced to status and checked criterion counts."""

    path: Path
    status: str
    met: int
    total: int

    @property
    def identifier(self) -> str:
        return self.path.name.split(" - ", 1)[0].upper()

    @property
    def finished(self) -> bool:
        return self.total > 0 and self.met == self.total


def parse(path: Path) -> Task | None:
    """Read a backlog card's status and acceptance criterion marks."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    status = STATUS.search(text)
    if status is None:
        return None
    block = AC_BLOCK.search(text)
    body = block.group("body") if block else ""
    marks = [match.group("mark").lower() for match in CRITERION.finditer(body)]
    return Task(
        path=path,
        status=status.group("status").strip("'\""),
        met=sum(1 for mark in marks if mark == "x"),
        total=len(marks),
    )


def load(directory: Path = TASKS) -> list[Task]:
    """Load all task cards under `directory` in sorted filename order."""
    if not directory.is_dir():
        return []
    tasks = (parse(path) for path in sorted(directory.glob("*.md")))
    return [task for task in tasks if task is not None]


def problems(tasks: Iterable[Task]) -> list[str]:
    """Return consistency errors between card statuses and checked criteria."""
    found = []
    for task in tasks:
        if task.status == DONE and task.met < task.total:
            found.append(
                f"{task.identifier} is Done with {task.total - task.met} of {task.total} "
                "acceptance criteria unchecked"
            )
        elif task.status != DONE and task.finished:
            found.append(
                f"{task.identifier} has every acceptance criterion met but is {task.status!r}"
            )
    return found


def main(argv: Sequence[str] | None = None, directory: Path | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", action="store_true", help="print status summary per task")
    arguments = parser.parse_args(argv)

    tasks = load(directory or TASKS)
    found = problems(tasks)

    if arguments.list:
        for task in tasks:
            print(f"{task.identifier}\t{task.status}\t{task.met}/{task.total}")
        return 0

    if found:
        for problem in found:
            print(f"backlog-status: {problem}", file=sys.stderr)
        return 1

    claimed = sum(1 for task in tasks if task.finished)
    print(f"backlog-status: {len(tasks)} task(s) agree with their criteria ({claimed} complete)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
