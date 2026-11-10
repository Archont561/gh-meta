---
id: doc-1
title: gh-repoconf Product and Architecture Specification
type: specification
created_date: '2026-11-09'
---

# gh-repoconf Specification

> *Your `.github/` directory, managed as code.*

## 1. Purpose

`gh-repoconf` is a standalone Rust CLI binary and GitHub CLI (`gh`) extension that enables teams to declare, validate, diff, and apply `.github/` repository files and GitHub repository metadata declaratively as code.

## 2. Initial Repository Foundation (`m-0`: Version-only Scaffold)

The initial scaffold establishes repository infrastructure, packaging, CI, BDD test harnesses, and license boundaries before domain workflows land:

- **Two-crate workspace**:
  - `crates/gh-repoconf-core` — core library crate currently exporting `pub const VERSION: &str = env!("CARGO_PKG_VERSION");` and `format_version_banner`, tested via `rstest-bdd` Gherkin features.
  - `crates/gh-repoconf` — standalone CLI binary (`gh-repoconf`) wrapping `gh-repoconf-core`, tested end-to-end as a compiled binary via `rstest-bdd` and `assert_cmd`.
- **Dual binary and Conda packaging**:
  - Standalone precompiled `gh` CLI extension assets (`gh-repoconf-<os>-<arch>[.exe]` + `SHA256SUMS`).
  - `crates/gh-repoconf/recipe/recipe.yaml` + `crates/gh-repoconf/recipe/variants.yaml` built and smoke-tested via `rattler-build`.
- **Python automation toolkit, `doit` CLI, and BDD suite**:
  - Unified `doit` task registry in `dodo.py` (`pixi run automation <task>`) backed by standalone modules under `automation/` (`bump_version.py`, `changelog.py`, `prose.py`, `gherkin_lint.py`, `check_skills.py`, `check_backlog_status.py`, `check_packages.py`, `check_coverage.py`, `audit_local.py`, `advisory_cache.py`, `check_advisory_exception.py`, `change_scope.py`, `commit_range.py`, `repo_check.py`) and shared helpers in `automation/lib/`.
  - Python BDD specs under `automation/features/*.feature` driven by `pytest-bdd` in `automation/tests/`.
  - Shell setup and sandbox restore launchers (`restore.sh`, `bootstrap.sh`, `install_hooks.sh`) under `scripts/`.

## 3. Target Interactive UI Architecture (`m-1`+)

- Interactive terminal workflows (guided configuration initialization, plan confirmation prompts, interactive diff inspection, and selection prompts) will adopt [`Archont561/clifacet`](https://github.com/Archont561/clifacet) as recorded in [decision-2](../decisions/decision-2%20-%20Adopt-clifacet-for-interactive-UI.md).
- `Archont561/clifacet` is intentionally deferred from `Cargo.toml` during `m-0` so initial standalone binary and Conda recipe builds stay lean and deterministic.
- Domain modules (configuration schema, GitHub REST/GraphQL/CLI clients, plan/diff/apply reconciler, `.github/` file templates, policy validators) will be introduced incrementally under `crates/` through dedicated backlog tasks once `m-0` is established.
