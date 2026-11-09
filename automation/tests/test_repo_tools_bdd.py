"""pytest-bdd bindings for automation/features/repo_tools.feature."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from automation import audit_local, check_backlog_status, check_skills, gherkin_lint

ROOT = Path(__file__).resolve().parents[2]
scenarios("../features/repo_tools.feature")


@dataclass
class ToolsState:
    root: Path = ROOT
    backlog_dir: Path | None = None
    cargo_home: Path | None = None
    exit_code: int = 0
    discovered_features: list[Path] = field(default_factory=list)
    skill_problems: list[str] = field(default_factory=list)
    audit_decision: str = ""


@pytest.fixture
def tools_state(tmp_path: Path) -> ToolsState:
    return ToolsState(backlog_dir=tmp_path / "tasks", cargo_home=tmp_path / "cargo_home")


@given("the live gh-meta repository workspace")
def given_live_repo(tools_state: ToolsState) -> None:
    tools_state.root = ROOT


@given("a temporary backlog directory containing a Done task with an unchecked criterion")
def given_inconsistent_task(tools_state: ToolsState) -> None:
    assert tools_state.backlog_dir is not None
    tools_state.backlog_dir.mkdir(parents=True, exist_ok=True)
    card = tools_state.backlog_dir / "task-1 - Sample.md"
    card.write_text(
        "---\nid: task-1\nstatus: Done\n---\n\n"
        "<!-- AC:BEGIN -->\n- [x] #1 Done item\n- [ ] #2 Missing item\n<!-- AC:END -->\n",
        encoding="utf-8",
    )


@given("a temporary backlog directory containing a Done task with all criteria checked")
def given_consistent_task(tools_state: ToolsState) -> None:
    assert tools_state.backlog_dir is not None
    tools_state.backlog_dir.mkdir(parents=True, exist_ok=True)
    card = tools_state.backlog_dir / "task-1 - Sample.md"
    card.write_text(
        "---\nid: task-1\nstatus: Done\n---\n\n"
        "<!-- AC:BEGIN -->\n- [x] #1 Done item\n- [x] #2 Second item\n<!-- AC:END -->\n",
        encoding="utf-8",
    )


@given("an isolated CARGO_HOME without an advisory database clone")
def given_empty_cargo_home(tools_state: ToolsState) -> None:
    assert tools_state.cargo_home is not None
    tools_state.cargo_home.mkdir(parents=True, exist_ok=True)


@when("the Gherkin linter scans the workspace")
def run_gherkin_linter(tools_state: ToolsState) -> None:
    tools_state.discovered_features = gherkin_lint.discover(tools_state.root)
    tools_state.exit_code = gherkin_lint.main(["--root", str(tools_state.root)])


@when("the backlog status guard validates that directory")
def run_backlog_guard(tools_state: ToolsState) -> None:
    tools_state.exit_code = check_backlog_status.main([], directory=tools_state.backlog_dir)


@when("the local audit wrapper runs without --require")
def run_audit_optional(tools_state: ToolsState) -> None:
    assert tools_state.cargo_home is not None
    ready = audit_local.database_ready(audit_local.database_path(str(tools_state.cargo_home), ROOT))
    tools_state.audit_decision = audit_local.decide(ready, require=False)


@when("the local audit wrapper runs with --require")
def run_audit_required(tools_state: ToolsState) -> None:
    assert tools_state.cargo_home is not None
    ready = audit_local.database_ready(audit_local.database_path(str(tools_state.cargo_home), ROOT))
    tools_state.audit_decision = audit_local.decide(ready, require=True)


@when("the skills validator inspects the workspace")
def run_skills_check(tools_state: ToolsState) -> None:
    tools_state.skill_problems = check_skills.check_skills(tools_state.root)


@then(parsers.parse("the Gherkin linter exits with code {code:d}"))
@then(parsers.parse("the backlog status guard exits with code {code:d}"))
def assert_tools_exit_code(tools_state: ToolsState, code: int) -> None:
    assert tools_state.exit_code == code


@then("feature files from both crates and automation are linted")
def assert_features_found(tools_state: ToolsState) -> None:
    rels = [p.relative_to(tools_state.root).as_posix() for p in tools_state.discovered_features]
    assert any(path.startswith("crates/") for path in rels), rels
    assert any(path.startswith("automation/") for path in rels), rels


@then(parsers.parse('the local audit wrapper decides "{decision}"'))
def assert_audit_decision(tools_state: ToolsState, decision: str) -> None:
    assert tools_state.audit_decision == decision


@then("the skills validator finds zero problems")
def assert_no_skill_problems(tools_state: ToolsState) -> None:
    assert tools_state.skill_problems == []
