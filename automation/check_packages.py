#!/usr/bin/env python3
"""Verify crate package listings (`cargo package --list`) and registry metadata."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tomllib
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CRATES = ("gh-meta-core", "gh-meta")

REQUIRED_FILES = ("Cargo.toml", "README.md", "LICENSE", "src/lib.rs")
FORBIDDEN_PREFIXES = (
    ".pixi/",
    ".pixi-sandbox/",
    "node_modules/",
    "target/",
    ".git/",
    "output/",
    "recipe/",
)
FORBIDDEN_SUFFIXES = (".feature",)
FORBIDDEN_BASENAMES = ("pyproject.toml",)
METADATA = ("description", "license", "repository", "rust-version")
NPM_EXPECTED_TARGETS = (
    "x86_64-unknown-linux-musl",
    "aarch64-unknown-linux-musl",
    "x86_64-apple-darwin",
    "aarch64-apple-darwin",
    "x86_64-pc-windows-msvc",
)

Runner = Callable[[Sequence[str], Path], str]


@dataclass(frozen=True)
class Finding:
    """One packaging violation on a crate."""

    kind: str
    detail: str

    def __str__(self) -> str:
        return f"{self.kind}: {self.detail}"


def package_files(crate: str, root: Path = ROOT, run: Runner | None = None) -> list[str]:
    """List files that `cargo package` would include for `crate`."""
    command = ["cargo", "package", "--list", "--locked", "-p", crate, "--allow-dirty"]
    output = (run or _run)(command, root)
    return [line for line in output.splitlines() if line and line == line.strip()]


def _run(command: Sequence[str], root: Path) -> str:
    try:
        completed = subprocess.run(command, cwd=root, capture_output=True, text=True, check=True)
    except FileNotFoundError as error:
        raise ValueError(f"cargo is not available: {error}") from error
    except subprocess.CalledProcessError as error:
        raise ValueError(
            f"`{' '.join(command)}` failed: {error.stderr.strip() or error.stdout.strip()}"
        ) from error
    return completed.stdout


def contents(crate: str, files: Sequence[str]) -> list[Finding]:
    """Check required and forbidden paths in a crate's package listing."""
    missing = [name for name in REQUIRED_FILES if name not in files]
    forbidden = [name for name in files if _repository_only(name)]

    findings = []
    if missing:
        findings.append(Finding("missing-file", f"{crate} does not package: {', '.join(missing)}"))
    if forbidden:
        findings.append(
            Finding(
                "forbidden-file",
                f"{crate} would package repository-only paths: {', '.join(forbidden)}",
            )
        )
    return findings


def _repository_only(name: str) -> bool:
    return (
        name.startswith(FORBIDDEN_PREFIXES)
        or name.endswith(FORBIDDEN_SUFFIXES)
        or Path(name).name in FORBIDDEN_BASENAMES
    )


def manifest(root: Path, crate: str) -> tuple[dict, dict]:
    """Load crate `[package]` and workspace `[workspace.package]` tables."""
    package = _table(root / "crates" / crate / "Cargo.toml", "package")
    workspace = _table(root / "Cargo.toml", "workspace", "package")
    return package, workspace


def _table(path: Path, *keys: str) -> dict:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    for key in keys:
        data = data.get(key, {})
    return data


def resolve_metadata(package: dict, workspace: dict) -> dict:
    """Resolve `workspace = true` metadata fields against root Cargo.toml."""
    resolved = {}
    for key in METADATA:
        if key not in package:
            continue
        value = package[key]
        if isinstance(value, dict) and value.get("workspace") is True:
            value = workspace.get(key)
        if value is not None:
            resolved[key] = value
    return resolved


def metadata(crate: str, package: dict, workspace: dict) -> list[Finding]:
    """Verify every required registry metadata field resolves cleanly."""
    missing = [key for key in METADATA if key not in package]
    resolved = resolve_metadata(package, workspace)
    unresolvable = [
        key
        for key in METADATA
        if key in package and isinstance(package[key], dict) and key not in resolved
    ]

    findings = []
    if missing:
        findings.append(Finding("missing-metadata", f"{crate} declares no {', '.join(missing)}"))
    if unresolvable:
        findings.append(
            Finding(
                "unresolvable-metadata",
                f"{crate} inherits {', '.join(unresolvable)} from workspace without a value",
            )
        )
    return findings


def packaging_configs(root: Path = ROOT) -> list[Finding]:
    """Verify PyPI (maturin) and npm (cargo-npm) configuration on `crates/gh-meta`."""
    findings: list[Finding] = []
    cli_cargo = root / "crates" / "gh-meta" / "Cargo.toml"
    cli_pkg = _table(cli_cargo, "package")
    npm_meta = cli_pkg.get("metadata", {}).get("npm", {})

    if npm_meta.get("prefix") != "@archont561/gh-meta-":
        findings.append(
            Finding("invalid-npm-metadata", "crates/gh-meta prefix must be '@archont561/gh-meta-'")
        )
    if npm_meta.get("bins") != ["gh-meta"]:
        findings.append(Finding("invalid-npm-metadata", "crates/gh-meta bins must be ['gh-meta']"))
    if tuple(npm_meta.get("targets", ())) != NPM_EXPECTED_TARGETS:
        findings.append(
            Finding(
                "invalid-npm-metadata",
                "crates/gh-meta targets must match the five native release triples",
            )
        )
    publish_cfg = npm_meta.get("custom", {}).get("publishConfig", {})
    if publish_cfg.get("access") != "public" or publish_cfg.get("provenance") is not True:
        findings.append(
            Finding(
                "invalid-npm-metadata",
                "crates/gh-meta custom.publishConfig must enable public access and provenance",
            )
        )

    pyproject = root / "crates" / "gh-meta" / "pyproject.toml"
    if not pyproject.is_file():
        findings.append(
            Finding("missing-pypi-manifest", "crates/gh-meta/pyproject.toml is missing")
        )
        return findings

    py_data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    project = py_data.get("project", {})
    maturin = py_data.get("tool", {}).get("maturin", {})
    if project.get("name") != "gh-meta":
        findings.append(Finding("invalid-pypi-manifest", "project.name must be 'gh-meta'"))
    if "version" not in project.get("dynamic", []):
        findings.append(
            Finding("invalid-pypi-manifest", "project.dynamic must include 'version' from Cargo")
        )
    if project.get("license") != "MIT":
        findings.append(Finding("invalid-pypi-manifest", "project.license must be 'MIT'"))
    if maturin.get("bindings") != "bin":
        findings.append(Finding("invalid-pypi-manifest", "tool.maturin.bindings must be 'bin'"))
    if maturin.get("locked") is not True:
        findings.append(Finding("invalid-pypi-manifest", "tool.maturin.locked must be true"))
    return findings


def check(
    crates: Sequence[str] = CRATES, root: Path = ROOT, run: Runner | None = None
) -> list[Finding]:
    """Check package listings and metadata across workspace crates."""
    findings = []
    for crate in crates:
        files = package_files(crate, root=root, run=run)
        package, workspace = manifest(root, crate)
        findings.extend(contents(crate, files))
        findings.extend(metadata(crate, package, workspace))
    findings.extend(packaging_configs(root=root))
    return findings


def main(argv: Sequence[str] | None = None, root: Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", action="store_true", help="print packaged file counts")
    arguments = parser.parse_args(argv)

    findings = check(root=root)
    if findings:
        for finding in findings:
            print(f"check-packages: {finding}", file=sys.stderr)
        return 1

    if arguments.list:
        for crate in CRATES:
            print(f"{crate}: {len(package_files(crate, root=root))} files")
    print(f"check-packages: {', '.join(CRATES)} package only release files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
