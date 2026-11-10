"""pytest-bdd bindings for automation/features/version_sync.feature."""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from automation import bump_version

ROOT = Path(__file__).resolve().parents[2]
scenarios("../features/version_sync.feature")


@dataclass
class VersionWorkspace:
    path: Path
    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""
    problems: list[str] = field(default_factory=list)


def _copy_manifests(dst: Path) -> None:
    (dst / "crates" / "gh-repoconf" / "recipe").mkdir(parents=True, exist_ok=True)
    for rel in (
        "Cargo.toml",
        "pixi.toml",
        "package.json",
        "crates/gh-repoconf/recipe/recipe.yaml",
    ):
        shutil.copy2(ROOT / rel, dst / rel)
    for crate in bump_version.WORKSPACE_CRATES:
        crate_dir = dst / "crates" / crate
        crate_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "crates" / crate / "Cargo.toml", crate_dir / "Cargo.toml")


@pytest.fixture
def workspace(tmp_path: Path) -> VersionWorkspace:
    return VersionWorkspace(path=tmp_path)


@given("the live gh-repoconf repository workspace")
def given_live_workspace(workspace: VersionWorkspace) -> None:
    workspace.path = ROOT


@given(parsers.parse('a temporary workspace at version "{version}"'))
def given_temp_workspace(workspace: VersionWorkspace, tmp_path: Path, version: str) -> None:
    _copy_manifests(tmp_path)
    workspace.path = tmp_path
    assert (
        version
        == bump_version.versions(
            (tmp_path / "Cargo.toml").read_text(encoding="utf-8"),
            (tmp_path / "pixi.toml").read_text(encoding="utf-8"),
            (tmp_path / "crates" / "gh-repoconf" / "recipe" / "recipe.yaml").read_text(
                encoding="utf-8"
            ),
            (tmp_path / "package.json").read_text(encoding="utf-8"),
        )[0].value
    )


@given(parsers.parse('the temporary Conda recipe context version is changed to "{version}"'))
def corrupt_recipe_version(workspace: VersionWorkspace, version: str) -> None:
    recipe = workspace.path / "crates" / "gh-repoconf" / "recipe" / "recipe.yaml"
    text = recipe.read_text(encoding="utf-8")
    recipe.write_text(
        text.replace('version: "0.1.0"', f'version: "{version}"', 1), encoding="utf-8"
    )


@given(parsers.parse('crate "{crate}" pins explicit version "{version}" instead of inheriting'))
def pin_crate_version(workspace: VersionWorkspace, crate: str, version: str) -> None:
    manifest = workspace.path / "crates" / crate / "Cargo.toml"
    text = manifest.read_text(encoding="utf-8")
    manifest.write_text(
        text.replace("version.workspace = true", f'version = "{version}"', 1),
        encoding="utf-8",
    )


@when("the version checker inspects all workspace manifests")
@when("the version checker inspects the temporary workspace")
def run_check(workspace: VersionWorkspace, capsys: pytest.CaptureFixture[str]) -> None:
    workspace.problems = bump_version.check_root(workspace.path)
    workspace.exit_code = bump_version.main(["--check"], root=workspace.path)
    captured = capsys.readouterr()
    workspace.stdout = captured.out
    workspace.stderr = captured.err


@when(parsers.parse('the bump tool updates the temporary workspace to "{version}"'))
def run_bump(workspace: VersionWorkspace, capsys: pytest.CaptureFixture[str], version: str) -> None:
    workspace.exit_code = bump_version.main([version], root=workspace.path)
    captured = capsys.readouterr()
    workspace.stdout = captured.out
    workspace.stderr = captured.err


@then(parsers.parse("the version check exits with code {code:d}"))
@then(parsers.parse("the bump tool exits with code {code:d}"))
def assert_exit_code(workspace: VersionWorkspace, code: int) -> None:
    assert workspace.exit_code == code, workspace.stderr or workspace.stdout


@then("all manifest version sites record the same version")
def assert_sites_equal(workspace: VersionWorkspace) -> None:
    assert workspace.problems == []


@then(parsers.parse('the version checker reports drift in "{site}"'))
def assert_drift_reported(workspace: VersionWorkspace, site: str) -> None:
    assert site in workspace.stderr


@then("the version checker reports an explicit crate version pin")
def assert_pin_reported(workspace: VersionWorkspace) -> None:
    assert "must declare version.workspace = true" in workspace.stderr


@then(
    parsers.parse(
        'the version checker on the temporary workspace reports "{version}" across all manifests'
    )
)
def assert_bumped_cleanly(workspace: VersionWorkspace, version: str) -> None:
    assert bump_version.check_root(workspace.path) == []
    sites = bump_version.versions(
        (workspace.path / "Cargo.toml").read_text(encoding="utf-8"),
        (workspace.path / "pixi.toml").read_text(encoding="utf-8"),
        (workspace.path / "crates" / "gh-repoconf" / "recipe" / "recipe.yaml").read_text(
            encoding="utf-8"
        ),
        (workspace.path / "package.json").read_text(encoding="utf-8"),
    )
    assert all(site.value == version for site in sites), sites
