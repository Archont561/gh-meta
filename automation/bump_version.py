#!/usr/bin/env python3
"""Record and verify release version parity across all workspace manifests."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tomllib
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_CRATES = ("gh-repoconf-core", "gh-repoconf")

SEMVER = re.compile(
    r"^(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
WORKSPACE_VERSION = re.compile(r'^version\s*=\s*"([^"]*)"\s*$')
CORE_REQUIREMENT = re.compile(r'^gh-repoconf-core\s*=\s*\{[^}]*version\s*=\s*"([^"]*)"')
RECIPE_VERSION = re.compile(r'^(\s*version\s*:\s*)"([^"]*)"\s*$')


@dataclass(frozen=True)
class Site:
    """One manifest entry holding the project version."""

    label: str
    value: str


def parse_version(value: str) -> str:
    """Validate semver syntax accepted by Cargo, Conda, and npm."""
    candidate = value.strip()
    if not SEMVER.fullmatch(candidate):
        raise ValueError(f"'{value}' is not a valid semver version such as 0.2.0 or 1.0.0-rc.1")
    return candidate


def _section(lines: list[str], header: str) -> tuple[int, int]:
    start = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("["):
            continue
        if start is not None:
            return start, index
        if stripped == header:
            start = index + 1
    if start is None:
        raise ValueError(f"missing {header} section")
    return start, len(lines)


def _read_section(text: str, header: str, pattern: re.Pattern[str]) -> str:
    lines = text.splitlines()
    start, end = _section(lines, header)
    for line in lines[start:end]:
        match = pattern.search(line)
        if match is not None:
            return match.group(1)
    raise ValueError(f"{header} has no line matching {pattern.pattern}")


def _rewrite_section(text: str, header: str, pattern: re.Pattern[str], value: str) -> str:
    lines = text.splitlines(keepends=True)
    start, end = _section(lines, header)
    for index in range(start, end):
        match = pattern.search(lines[index])
        if match is None:
            continue
        line = lines[index]
        lines[index] = line[: match.start(1)] + value + line[match.end(1) :]
        return "".join(lines)
    raise ValueError(f"{header} has no line matching {pattern.pattern}")


def _read_recipe_version(recipe_text: str) -> str:
    in_context = False
    for line in recipe_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line[0].isspace():
            in_context = stripped == "context:"
            continue
        if in_context:
            match = RECIPE_VERSION.match(line)
            if match is not None:
                return match.group(2)
    raise ValueError("crates/gh-repoconf/recipe/recipe.yaml has no context.version entry")


def _rewrite_recipe_version(recipe_text: str, version: str) -> str:
    lines = recipe_text.splitlines(keepends=True)
    in_context = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line[0].isspace():
            in_context = stripped == "context:"
            continue
        if in_context:
            match = RECIPE_VERSION.match(line)
            if match is not None:
                lines[index] = line[: match.start(2)] + version + line[match.end(2) :]
                return "".join(lines)
    raise ValueError("crates/gh-repoconf/recipe/recipe.yaml has no context.version entry")


def _read_package_json_version(package_json_text: str) -> str:
    data = json.loads(package_json_text)
    version = data.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("package.json has no non-empty version string")
    return version


def _rewrite_package_json_version(package_json_text: str, version: str) -> str:
    pattern = re.compile(r'("version"\s*:\s*")([^"]*)(")')
    updated, count = pattern.subn(rf"\g<1>{version}\g<3>", package_json_text, count=1)
    if count != 1:
        raise ValueError("package.json has no version field")
    return updated


def versions(cargo: str, pixi: str, recipe: str, package_json: str) -> list[Site]:
    """Read all five version sites across the workspace manifests."""
    return [
        Site(
            "Cargo.toml [workspace.package] version",
            _read_section(cargo, "[workspace.package]", WORKSPACE_VERSION),
        ),
        Site(
            "Cargo.toml [workspace.dependencies] gh-repoconf-core",
            _read_section(cargo, "[workspace.dependencies]", CORE_REQUIREMENT),
        ),
        Site(
            "pixi.toml [workspace] version",
            _read_section(pixi, "[workspace]", WORKSPACE_VERSION),
        ),
        Site("crates/gh-repoconf/recipe/recipe.yaml context.version", _read_recipe_version(recipe)),
        Site("package.json version", _read_package_json_version(package_json)),
    ]


def inconsistencies(cargo: str, pixi: str, recipe: str, package_json: str) -> list[str]:
    """Return mismatch descriptions whenever any manifest diverges from Cargo.toml."""
    sites = versions(cargo, pixi, recipe, package_json)
    expected = sites[0].value
    return [
        f"{site.label} is '{site.value}' but Cargo.toml [workspace.package] version is '{expected}'"
        for site in sites[1:]
        if site.value != expected
    ]


def bump(
    cargo: str, pixi: str, recipe: str, package_json: str, version: str
) -> tuple[str, str, str, str]:
    """Update all five version sites consistently."""
    new_cargo = _rewrite_section(cargo, "[workspace.package]", WORKSPACE_VERSION, version)
    new_cargo = _rewrite_section(new_cargo, "[workspace.dependencies]", CORE_REQUIREMENT, version)
    new_pixi = _rewrite_section(pixi, "[workspace]", WORKSPACE_VERSION, version)
    new_recipe = _rewrite_recipe_version(recipe, version)
    new_package_json = _rewrite_package_json_version(package_json, version)
    return new_cargo, new_pixi, new_recipe, new_package_json


def crate_pins(root: Path, crates: Sequence[str] = WORKSPACE_CRATES) -> list[str]:
    """Report any workspace crate pinning its own version instead of inheriting workspace."""
    problems = []
    for crate in crates:
        manifest = root / "crates" / crate / "Cargo.toml"
        try:
            package = tomllib.loads(manifest.read_text(encoding="utf-8")).get("package", {})
        except (OSError, tomllib.TOMLDecodeError) as error:
            problems.append(f"{manifest} cannot be read: {error}")
            continue
        declared = package.get("version")
        if isinstance(declared, dict) and declared.get("workspace") is True:
            continue
        problems.append(f"{manifest} must declare version.workspace = true instead of {declared!r}")
    return problems


def check_root(root: Path = ROOT) -> list[str]:
    """Check version parity and workspace inheritance under `root`."""
    cargo = (root / "Cargo.toml").read_text(encoding="utf-8")
    pixi = (root / "pixi.toml").read_text(encoding="utf-8")
    recipe = (root / "crates" / "gh-repoconf" / "recipe" / "recipe.yaml").read_text(
        encoding="utf-8"
    )
    package_json = (root / "package.json").read_text(encoding="utf-8")
    problems = inconsistencies(cargo, pixi, recipe, package_json)
    problems.extend(crate_pins(root))
    return problems


def relock(root: Path = ROOT) -> int:
    """Refresh Cargo.lock offline after a version bump."""
    cargo = shutil.which("cargo")
    if cargo is None:
        print("bump-version: cargo is not on PATH; Cargo.lock was not refreshed", file=sys.stderr)
        return 1
    result = subprocess.run(
        [cargo, "metadata", "--offline", "--format-version", "1"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"bump-version: relock failed:\n{result.stderr}", file=sys.stderr)
    return result.returncode


def main(argv: Sequence[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("version", nargs="?", help="new semver version to record")
    parser.add_argument("--print-version", action="store_true", help="print current version")
    parser.add_argument("--check", action="store_true", help="verify version parity across files")
    parser.add_argument("--dry-run", action="store_true", help="preview changes without writing")
    parser.add_argument("--relock", action="store_true", help="refresh Cargo.lock offline")
    arguments = parser.parse_args(argv)

    try:
        cargo_path = root / "Cargo.toml"
        pixi_path = root / "pixi.toml"
        recipe_path = root / "crates" / "gh-repoconf" / "recipe" / "recipe.yaml"
        pkg_path = root / "package.json"

        cargo = cargo_path.read_text(encoding="utf-8")
        pixi = pixi_path.read_text(encoding="utf-8")
        recipe = recipe_path.read_text(encoding="utf-8")
        pkg = pkg_path.read_text(encoding="utf-8")
        current = versions(cargo, pixi, recipe, pkg)[0].value

        if arguments.print_version:
            print(current)
            return 0
        if arguments.check:
            problems = check_root(root)
            for problem in problems:
                print(f"bump-version: {problem}", file=sys.stderr)
            if problems:
                return 1
            print(f"bump-version: all version sites and workspace crates match {current}")
            return 0
        if arguments.version is None:
            parser.error("a version is required unless --check or --print-version is passed")

        version = parse_version(arguments.version)
        if version == current:
            raise ValueError(f"{version} is already the recorded version")
        new_cargo, new_pixi, new_recipe, new_pkg = bump(cargo, pixi, recipe, pkg, version)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"bump-version: {error}", file=sys.stderr)
        return 1

    if arguments.dry_run:
        print(f"bump-version: would record {version} (was {current}) in:")
        for site in versions(new_cargo, new_pixi, new_recipe, new_pkg):
            print(f"  {site.label} = {site.value}")
        return 0

    cargo_path.write_text(new_cargo, encoding="utf-8")
    pixi_path.write_text(new_pixi, encoding="utf-8")
    recipe_path.write_text(new_recipe, encoding="utf-8")
    pkg_path.write_text(new_pkg, encoding="utf-8")
    print(f"bump-version: recorded {version} (was {current})")
    if arguments.relock:
        return relock(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
