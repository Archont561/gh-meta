#!/usr/bin/env python3
"""Verify that the RustSec advisory exception matches Cargo.lock and docs."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCKFILE = ROOT / "Cargo.lock"
DENY = ROOT / "deny.toml"
AUDIT = ROOT / ".cargo" / "audit.toml"
DOCS = ROOT / "docs" / "guides" / "running-the-checks.md"

ADVISORY = "RUSTSEC-2026-0374"
SECTION = "## Dependency advisory exception"
CRATE = "rstest-bdd"
TARGET = "basic-toml"
SEPARATOR = " → "

PACKAGE = re.compile(r"^\[\[package\]\]$")
NAME = re.compile(r'^name = "(.*)"$')
VERSION = re.compile(r'^version = "(.*)"$')
DEPENDENCY = re.compile(r'^"(.*)",$')
PATH_LINE = re.compile(rf"^[a-z0-9_.-]+ \d[^\s]*(?:{SEPARATOR}[a-z0-9_.-]+ \d[^\s]*)+$")


@dataclass(frozen=True)
class Finding:
    """One discrepancy around the advisory exception."""

    kind: str
    detail: str

    def __str__(self) -> str:
        return f"{self.kind}: {self.detail}"


def load_lock(path: Path = LOCKFILE) -> dict:
    """Parse package dependency edges from `Cargo.lock`."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise ValueError(f"cannot read {path}: {error}") from error

    packages: list[dict] = []
    current: dict | None = None
    in_dependencies = False
    for line in text.splitlines():
        stripped = line.strip()
        if PACKAGE.match(stripped):
            current = {"name": "", "version": "", "dependencies": []}
            packages.append(current)
            in_dependencies = False
            continue
        if current is None:
            continue
        if (match := NAME.match(stripped)) is not None:
            current["name"] = match.group(1)
            in_dependencies = False
        elif (match := VERSION.match(stripped)) is not None:
            current["version"] = match.group(1)
            in_dependencies = False
        elif stripped == "dependencies = [":
            in_dependencies = True
        elif in_dependencies and (match := DEPENDENCY.match(stripped)) is not None:
            current["dependencies"].append(match.group(1).split(" ")[0])
        elif stripped == "]":
            in_dependencies = False
    return {"package": [package for package in packages if package["name"]]}


def dependency_path(lock: dict, start: str, target: str) -> list[tuple[str, str]] | None:
    """Return shortest dependency path from `start` to `target`."""
    versions = {package["name"]: package.get("version", "") for package in lock["package"]}
    if start not in versions or target not in versions:
        return None
    edges = {package["name"]: package.get("dependencies", []) for package in lock["package"]}
    queue: list[list[str]] = [[start]]
    seen = {start}
    while queue:
        chain = queue.pop(0)
        for neighbour in edges.get(chain[-1], []):
            if neighbour in seen:
                continue
            if neighbour == target:
                return [(name, versions.get(name, "")) for name in (*chain, neighbour)]
            seen.add(neighbour)
            queue.append([*chain, neighbour])
    return None


def render_path(path: list[tuple[str, str]] | None) -> str:
    """Format dependency path as `name ver → name ver`."""
    if not path:
        return ""
    return SEPARATOR.join(f"{name} {version}".strip() for name, version in path)


def documented_path(text: str) -> str:
    """Extract the quoted dependency path from the advisory docs section."""
    for line in _section(text, SECTION).splitlines():
        stripped = line.strip()
        if PATH_LINE.match(stripped):
            return stripped
    return ""


def _section(text: str, heading: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == heading:
            level = len(heading) - len(heading.lstrip("#"))
            body = []
            for candidate in lines[index + 1 :]:
                stripped = candidate.strip()
                if stripped.startswith("#") and len(stripped) - len(stripped.lstrip("#")) <= level:
                    break
                body.append(candidate)
            return "\n".join(body)
    return ""


def exceptions(deny: str, audit: str) -> dict[str, set[str]]:
    """Return ignored RustSec IDs from `deny.toml` and `.cargo/audit.toml`."""
    return {"deny": _ignored(deny), "audit": _ignored(audit)}


def _ignored(text: str) -> set[str]:
    ids: set[str] = set()
    collecting = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not collecting:
            if not stripped.startswith("ignore"):
                continue
            collecting = True
        ids.update(re.findall(r"RUSTSEC-\d{4}-\d{4}", stripped))
        if "]" in stripped:
            collecting = False
    return ids


def check(root: Path = ROOT) -> list[Finding]:
    """Validate advisory exception necessity and documentation parity."""
    lock = load_lock(root / LOCKFILE.name)
    path = dependency_path(lock, CRATE, TARGET)
    ignored = exceptions(
        (root / DENY.name).read_text(encoding="utf-8"),
        (root / ".cargo" / "audit.toml").read_text(encoding="utf-8"),
    )

    if path is None:
        return [
            Finding(
                "stale-exception",
                f"{TARGET} is no longer reachable from {CRATE}; drop {ADVISORY} exceptions",
            )
        ]

    findings = []
    for name, pathname in (("deny", DENY.name), ("audit", ".cargo/audit.toml")):
        if ADVISORY not in ignored[name]:
            findings.append(
                Finding(
                    "missing-exception",
                    f"{pathname} must ignore {ADVISORY} while {render_path(path)} exists",
                )
            )

    docs_file = root / "docs" / "guides" / "running-the-checks.md"
    quoted = documented_path(docs_file.read_text(encoding="utf-8"))
    actual = render_path(path)
    if quoted != actual:
        findings.append(
            Finding(
                "documented-path",
                f"{docs_file.relative_to(root)} quotes '{quoted}' instead of '{actual}'",
            )
        )
    return findings


def main(argv: Sequence[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--print-path", action="store_true")
    arguments = parser.parse_args(argv)

    lock = load_lock(root / LOCKFILE.name)
    path = dependency_path(lock, CRATE, TARGET)
    if arguments.print_path:
        print(render_path(path) if path else f"{TARGET} is not in graph")
        return 0

    findings = check(root)
    if findings:
        for finding in findings:
            print(f"check-advisory: {finding}", file=sys.stderr)
        return 1
    print(f"check-advisory: {ADVISORY} is warranted ({render_path(path)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
