"""Tests verifying doit task discovery, contracts, and adapter helpers in automation/dodo.py."""

from __future__ import annotations

from pathlib import Path

import pytest
from doit.cmd_base import ModuleTaskLoader
from doit.task import dict_to_task

from automation import dodo

ROOT = Path(__file__).resolve().parents[2]


def test_dodo_task_discovery_and_metadata() -> None:
    config = ModuleTaskLoader(dodo).load_doit_config()
    assert config["default_tasks"] == ["check_policy"]
    names = sorted(name[5:] for name in dir(dodo) if name.startswith("task_"))
    expected = [
        "advisory_cache",
        "advisory_exception",
        "audit_offline",
        "backlog_check",
        "bump_version",
        "change_scope",
        "changelog",
        "changelog_check",
        "check_coverage",
        "check_packages",
        "check_policy",
        "commit_range",
        "lint_gherkin",
        "lint_prose",
        "prose_check",
        "prose_sync",
        "prose_write",
        "repo_check",
        "rude_clean",
        "skills_check",
        "version_check",
    ]
    assert names == expected

    for name in names:
        fn = getattr(dodo, f"task_{name}")
        assert fn.__doc__, f"task_{name} must have a docstring for `doit list`"
        spec = fn()
        task = dict_to_task({"name": name, **spec})
        assert task.name == name


def test_dodo_action_adapters_and_exit_mapping(monkeypatch: pytest.MonkeyPatch) -> None:
    assert dodo._checked(0) is True
    assert dodo._checked(1) is False

    recorded: list[tuple[str, object]] = []

    def stub(name: str, code: int = 0):
        def _inner(argv=None, **_kwargs) -> int:
            recorded.append((name, argv))
            return code

        return SimpleCallable(_inner)

    class SimpleCallable:
        def __init__(self, fn):
            self.main = fn

    monkeypatch.setattr(dodo, "advisory_cache", stub("advisory_cache"))
    monkeypatch.setattr(dodo, "check_advisory_exception", stub("check_advisory_exception"))
    monkeypatch.setattr(dodo, "audit_local", stub("audit_local"))
    monkeypatch.setattr(dodo, "check_backlog_status", stub("check_backlog_status"))
    monkeypatch.setattr(dodo, "bump_version", stub("bump_version"))
    monkeypatch.setattr(dodo, "change_scope", stub("change_scope"))
    monkeypatch.setattr(dodo, "changelog", stub("changelog"))
    monkeypatch.setattr(dodo, "check_coverage", stub("check_coverage"))
    monkeypatch.setattr(dodo, "check_packages", stub("check_packages"))
    monkeypatch.setattr(dodo, "commit_range", stub("commit_range"))
    monkeypatch.setattr(dodo, "gherkin_lint", stub("gherkin_lint"))
    monkeypatch.setattr(dodo, "prose", stub("prose"))
    monkeypatch.setattr(dodo, "repo_check", SimpleCallable(lambda: 0))
    monkeypatch.setattr(dodo, "check_skills", SimpleCallable(lambda: 1))

    assert dodo._advisory_cache("clean", "/tmp/c")
    assert dodo._advisory_exception(True)
    assert dodo._audit_offline(True)
    assert dodo._backlog_check(True)
    assert dodo._bump_version(
        version="0.2.0", check=True, dry_run=True, relock=True, print_version=True
    )
    assert dodo._bump_version(extra=["0.3.0"])
    assert dodo._version_check()
    assert dodo._change_scope()
    assert dodo._changelog("notes", "0.2.0", "2026-11-10")
    assert dodo._changelog_check()
    assert dodo._check_coverage("coverage/lcov.info")
    assert dodo._check_packages(True)
    assert dodo._commit_range("resolve")
    assert dodo._lint_gherkin(str(ROOT))
    assert dodo._prose_write()
    assert dodo._prose_sync()
    assert dodo._prose_check()
    assert dodo._lint_prose()
    assert dodo._repo_check() is True
    assert dodo._skills_check() is False

    assert ("advisory_cache", ["clean", "--cargo-home", "/tmp/c"]) in recorded
    assert ("check_advisory_exception", ["--print-path"]) in recorded
    assert ("audit_local", ["--require"]) in recorded
    assert ("check_backlog_status", ["--list"]) in recorded
    assert (
        "bump_version",
        ["0.2.0", "--check", "--dry-run", "--relock", "--print-version"],
    ) in recorded
    assert ("bump_version", ["0.3.0"]) in recorded
    assert ("changelog", ["notes", "0.2.0", "--date", "2026-11-10"]) in recorded
    assert ("check_packages", ["--list"]) in recorded
    assert ("commit_range", ["resolve"]) in recorded
    assert ("gherkin_lint", ["--root", str(ROOT)]) in recorded
