"""Tests for prose rendering and Vale configuration hygiene."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

from automation import prose
from automation.prose import ConfigError

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def config() -> dict:
    return prose.load()


def test_committed_vale_tree_matches_vale_toml(config: dict) -> None:
    assert prose.differences(config, root=ROOT) == []


def test_every_package_is_pinned_to_a_release_url(config: dict) -> None:
    for package in config["packages"]:
        assert package.startswith("https://github.com/"), package
        assert "/releases/download/" in package, package
        assert package.endswith(".zip"), package


def test_unpinned_package_is_refused(tmp_path: Path) -> None:
    manifest = tmp_path / "vale.toml"
    manifest.write_text(
        (ROOT / "vale.toml")
        .read_text(encoding="utf-8")
        .replace(
            "https://github.com/vale-cli/Microsoft/releases/download/v0.15.1/Microsoft.zip",
            "Microsoft",
        ),
        encoding="utf-8",
    )
    with pytest.raises(ConfigError, match="pin release URL"):
        prose.load(manifest)


def test_disabled_rules_always_explain_why(config: dict) -> None:
    for name, spec in config["rules"].items():
        if name.startswith(f"{prose.STYLE}."):
            continue
        if str(spec.get("level", "")).upper() == "NO":
            assert str(spec.get("reason", "")).strip(), f"{name} lacks reason"


def test_disabled_rule_without_reason_is_refused(tmp_path: Path) -> None:
    manifest = tmp_path / "vale.toml"
    manifest.write_text(
        (ROOT / "vale.toml")
        .read_text(encoding="utf-8")
        .replace(
            'reason = "Guides have no first-person author voice."',
            'reason = ""',
        ),
        encoding="utf-8",
    )
    with pytest.raises(ConfigError, match="without a `reason`"):
        prose.load(manifest)


def test_vocabulary_contains_project_terms_without_duplicates(config: dict) -> None:
    accept = config["accept"]
    assert "gh-meta" in accept
    assert "gh-meta-core" in accept
    assert len(accept) == len(set(accept))


def test_invalid_toml_is_refused(tmp_path: Path) -> None:
    manifest = tmp_path / "vale.toml"
    manifest.write_text("sources = [", encoding="utf-8")
    with pytest.raises((ConfigError, tomllib.TOMLDecodeError)):
        prose.load(manifest)
