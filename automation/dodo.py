"""Central doit task registry consolidating gh-repoconf repository automation."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

from automation import (
    advisory_cache,
    audit_local,
    bump_version,
    change_scope,
    changelog,
    check_advisory_exception,
    check_backlog_status,
    check_coverage,
    check_packages,
    check_skills,
    commit_range,
    gherkin_lint,
    prose,
    repo_check,
    rude_clean,
)

DOIT_CONFIG = {
    "default_tasks": ["check_policy"],
    "verbosity": 2,
    "dep_file": ".doit.db",
}


def _checked(exit_code: int) -> bool:
    """Convert a standard integer exit code into doit's boolean action contract."""
    return exit_code == 0


def _advisory_cache(
    action: str = "key",
    cargo_home: str = "",
    extra: Sequence[str] | None = None,
) -> bool:
    selected = extra[0] if extra else action
    argv = [selected]
    if cargo_home:
        argv.extend(["--cargo-home", cargo_home])
    return _checked(advisory_cache.main(argv))


def task_advisory_cache() -> dict[str, Any]:
    """Compute or reset the weekly RustSec advisory-database cache."""
    return {
        "actions": [(_advisory_cache,)],
        "params": [
            {
                "name": "action",
                "long": "action",
                "default": "key",
                "type": str,
                "help": "Cache action ('key' or 'clean')",
            },
            {
                "name": "cargo_home",
                "long": "cargo-home",
                "default": "",
                "type": str,
                "help": "Override CARGO_HOME path for cleaning",
            },
        ],
        "pos_arg": "extra",
    }


def _advisory_exception(print_path: bool = False) -> bool:
    argv = ["--print-path"] if print_path else []
    return _checked(check_advisory_exception.main(argv))


def task_advisory_exception() -> dict[str, Any]:
    """Verify RustSec advisory exceptions match Cargo.lock and docs."""
    return {
        "actions": [(_advisory_exception,)],
        "params": [
            {
                "name": "print_path",
                "long": "print-path",
                "default": False,
                "type": bool,
                "help": "Print the transitive dependency chain",
            },
        ],
    }


def _audit_offline(require: bool = False) -> bool:
    argv = ["--require"] if require else []
    return _checked(audit_local.main(argv))


def task_audit_offline() -> dict[str, Any]:
    """Run cargo-audit locally when an advisory database clone exists."""
    return {
        "actions": [(_audit_offline,)],
        "params": [
            {
                "name": "require",
                "long": "require",
                "default": False,
                "type": bool,
                "help": "Fail when no local advisory database is present",
            },
        ],
    }


def _backlog_check(list_tasks: bool = False) -> bool:
    argv = ["--list"] if list_tasks else []
    return _checked(check_backlog_status.main(argv))


def task_backlog_check() -> dict[str, Any]:
    """Verify backlog task statuses match acceptance criteria checkboxes."""
    return {
        "actions": [(_backlog_check,)],
        "params": [
            {
                "name": "list_tasks",
                "long": "list",
                "default": False,
                "type": bool,
                "help": "Print status summary per task",
            },
        ],
    }


def _bump_version(
    version: str = "",
    check: bool = False,
    dry_run: bool = False,
    relock: bool = False,
    print_version: bool = False,
    extra: Sequence[str] | None = None,
) -> bool:
    argv: list[str] = []
    if extra:
        argv.extend(extra)
    elif version:
        argv.append(version)
    if check:
        argv.append("--check")
    if dry_run:
        argv.append("--dry-run")
    if relock:
        argv.append("--relock")
    if print_version:
        argv.append("--print-version")
    return _checked(bump_version.main(argv))


def task_bump_version() -> dict[str, Any]:
    """Verify or bump synchronized manifest versions across the workspace."""
    return {
        "actions": [(_bump_version,)],
        "params": [
            {
                "name": "version",
                "long": "version",
                "short": "v",
                "default": "",
                "type": str,
                "help": "New semver version to record",
            },
            {
                "name": "check",
                "long": "check",
                "default": False,
                "type": bool,
                "help": "Verify version parity across files",
            },
            {
                "name": "dry_run",
                "long": "dry-run",
                "default": False,
                "type": bool,
                "help": "Preview version updates without writing",
            },
            {
                "name": "relock",
                "long": "relock",
                "default": False,
                "type": bool,
                "help": "Refresh Cargo.lock offline after bumping",
            },
            {
                "name": "print_version",
                "long": "print-version",
                "default": False,
                "type": bool,
                "help": "Print current workspace version",
            },
        ],
        "pos_arg": "extra",
    }


def _version_check() -> bool:
    return _checked(bump_version.main(["--check"]))


def task_version_check() -> dict[str, Any]:
    """Verify version parity across Cargo, Pixi, Conda recipe, and package.json."""
    return {"actions": [_version_check]}


def _change_scope() -> bool:
    return _checked(change_scope.main([]))


def task_change_scope() -> dict[str, Any]:
    """Classify whether a CI change touches only documentation files."""
    return {"actions": [_change_scope]}


def _changelog(
    action: str = "regen",
    version: str = "",
    date: str = "",
    extra: Sequence[str] | None = None,
) -> bool:
    argv = list(extra) if extra else [action]
    if version and version not in argv:
        argv.append(version)
    if date:
        argv.extend(["--date", date])
    return _checked(changelog.main(argv))


def task_changelog() -> dict[str, Any]:
    """Render, print, check, or extract release notes for CHANGELOG.md."""
    return {
        "actions": [(_changelog,)],
        "params": [
            {
                "name": "action",
                "long": "action",
                "default": "regen",
                "type": str,
                "help": "Action ('regen', 'check', 'print', or 'notes')",
            },
            {
                "name": "version",
                "long": "version",
                "short": "v",
                "default": "",
                "type": str,
                "help": "Version for 'notes'",
            },
            {
                "name": "date",
                "long": "date",
                "default": "",
                "type": str,
                "help": "ISO release date for 'notes'",
            },
        ],
        "pos_arg": "extra",
    }


def _changelog_check() -> bool:
    return _checked(changelog.main(["check"]))


def task_changelog_check() -> dict[str, Any]:
    """Verify CHANGELOG.md matches rendered Conventional Commit history."""
    return {"actions": [_changelog_check]}


def _check_coverage(report: str = "coverage/lcov.info", extra: Sequence[str] | None = None) -> bool:
    path = extra[0] if extra else report
    return _checked(check_coverage.main([path]))


def task_check_coverage() -> dict[str, Any]:
    """Enforce the 90% Rust source-line coverage gate on LCOV output."""
    return {
        "actions": [(_check_coverage,)],
        "params": [
            {
                "name": "report",
                "long": "report",
                "default": "coverage/lcov.info",
                "type": str,
                "help": "Path to LCOV report",
            },
        ],
        "pos_arg": "extra",
    }


def _check_packages(list_files: bool = False) -> bool:
    argv = ["--list"] if list_files else []
    return _checked(check_packages.main(argv))


def _rude_clean() -> bool:
    return _checked(rude_clean.main())


def task_rude_clean() -> dict[str, Any]:
    """Enforce the `rude` Clean Code thresholds configured in `rude.toml`."""
    return {"actions": [(_rude_clean,)]}


def task_check_packages() -> dict[str, Any]:
    """Verify crate package listings and registry packaging metadata."""
    return {
        "actions": [(_check_packages,)],
        "params": [
            {
                "name": "list_files",
                "long": "list",
                "default": False,
                "type": bool,
                "help": "Print packaged file counts per crate",
            },
        ],
    }


def _commit_range(action: str = "check", extra: Sequence[str] | None = None) -> bool:
    selected = extra[0] if extra else action
    return _checked(commit_range.main([selected]))


def task_commit_range() -> dict[str, Any]:
    """Validate Conventional Commits across the CI push or pull request range."""
    return {
        "actions": [(_commit_range,)],
        "params": [
            {
                "name": "action",
                "long": "action",
                "default": "check",
                "type": str,
                "help": "Action ('check' or 'resolve')",
            },
        ],
        "pos_arg": "extra",
    }


def _lint_gherkin(root: str = "") -> bool:
    argv = ["--root", root] if root else []
    return _checked(gherkin_lint.main(argv))


def task_lint_gherkin() -> dict[str, Any]:
    """Lint all features/*.feature files across crates and automation."""
    return {
        "actions": [(_lint_gherkin,)],
        "params": [
            {
                "name": "root",
                "long": "root",
                "default": "",
                "type": str,
                "help": "Repository root override for feature discovery",
            },
        ],
    }


def _prose_write() -> bool:
    return _checked(prose.main(["write"]))


def task_prose_write() -> dict[str, Any]:
    """Render .vale.ini and GhRepoconf Vale styles incrementally from vale.toml."""
    return {
        "actions": [_prose_write],
        "file_dep": ["vale.toml", "automation/prose.py"],
        "targets": [
            ".vale.ini",
            str(Path(".vale/styles/config/vocabularies/GhRepoconf/accept.txt")),
            str(Path(".vale/styles/GhRepoconf/American.yml")),
        ],
    }


def _prose_sync() -> bool:
    return _checked(prose.main(["sync"]))


def task_prose_sync() -> dict[str, Any]:
    """Render Vale config and download pinned upstream style packages."""
    return {
        "actions": [_prose_sync],
        "task_dep": ["prose_write"],
    }


def _prose_check() -> bool:
    return _checked(prose.main(["check"]))


def task_prose_check() -> dict[str, Any]:
    """Verify committed Vale files match vale.toml without modifying disk."""
    return {"actions": [_prose_check]}


def _lint_prose() -> bool:
    return _checked(prose.main(["lint"]))


def task_lint_prose() -> dict[str, Any]:
    """Verify Vale config parity and lint prose across maintained Markdown."""
    return {
        "actions": [_lint_prose],
        "task_dep": ["prose_check"],
    }


def _repo_check() -> bool:
    return _checked(repo_check.main())


def task_repo_check() -> dict[str, Any]:
    """Verify cross-file license, symlink, and sandbox parity invariants."""
    return {"actions": [_repo_check]}


def _skills_check() -> bool:
    return _checked(check_skills.main())


def task_skills_check() -> dict[str, Any]:
    """Validate project-local Agent Skills and skills-lock.json."""
    return {"actions": [_skills_check]}


def task_check_policy() -> dict[str, Any]:
    """Run all read-only Python repository, packaging, and prose checks."""
    return {
        "actions": None,
        "task_dep": [
            "repo_check",
            "version_check",
            "check_packages",
            "skills_check",
            "backlog_check",
            "advisory_exception",
            "lint_gherkin",
            "lint_prose",
            "changelog_check",
        ],
    }
