#!/usr/bin/env python3
"""Validate project-owned and locked Agent Skills under `.agents/skills/` and `skills-lock.json`."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_LOCAL = frozenset({"session", "regain-direction"})
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def check_skills(root: Path = ROOT) -> list[str]:
    """Validate skill directories, SKILL.md frontmatter, and skills-lock.json entries."""
    problems: list[str] = []
    directory = root / ".agents" / "skills"
    if not directory.is_dir() or directory.is_symlink():
        return [f"missing or symlinked skills directory: {directory}"]

    present = {p.name for p in directory.iterdir() if p.is_dir() or p.is_symlink()}
    for name in sorted(REQUIRED_LOCAL - present):
        problems.append(f"missing required local skill: {name}")

    lock_path = root / "skills-lock.json"
    if lock_path.is_file():
        try:
            locked = json.loads(lock_path.read_text(encoding="utf-8")).get("skills", {})
        except (OSError, json.JSONDecodeError) as error:
            problems.append(f"cannot read {lock_path}: {error}")
            locked = {}
        for name in sorted(set(locked) - present):
            problems.append(f"locked skill missing from .agents/skills/: {name}")

    for name in sorted(present):
        folder = directory / name
        path = folder / "SKILL.md"
        if not NAME.fullmatch(name):
            problems.append(f"invalid skill directory name: {name}")
        if folder.is_symlink() or path.is_symlink() or not path.is_file():
            problems.append(f"missing or symlinked SKILL.md: {name}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            problems.append(f"cannot read {path}: {error}")
            continue
        parts = text.split("---\n", 2)
        if len(parts) != 3 or parts[0] != "" or not parts[2].strip():
            problems.append(f"invalid frontmatter or empty body: {name}")
            continue
        fields: dict[str, str] = {}
        for line in parts[1].splitlines():
            key, separator, value = line.partition(":")
            if separator and key in ("name", "description"):
                if key in fields:
                    problems.append(f"duplicate {key}: {name}")
                fields[key] = value.strip().strip("\"'")
        if fields.get("name") != name:
            problems.append(f"frontmatter name does not match directory: {name}")
        if not fields.get("description"):
            problems.append(f"missing description: {name}")
    return problems


def main(root: Path = ROOT) -> int:
    problems = check_skills(root)
    if problems:
        for problem in problems:
            print(f"skills-check: {problem}", file=sys.stderr)
        return 1
    skill_count = sum(1 for p in (root / ".agents" / "skills").iterdir() if p.is_dir())
    print(f"skills-check: {skill_count} skill(s) validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
