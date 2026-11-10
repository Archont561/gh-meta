---
id: rep-001
title: Establish version-only two-crate scaffold, tooling, and packaging
status: Done
priority: high
milestone: m-0
labels:
  - scaffold
  - cli
  - packaging
created_date: '2026-11-09'
updated_date: '2026-11-09'
---

## Description

Scaffold `Archont561/gh-repoconf` with the minimal `gh-repoconf-core` and `gh-repoconf` Rust workspace, MIT license, `rattler-build` Conda recipe, Pixi and sandbox configuration, Python repository automation scripts, Rust (`rstest-bdd`) and Python (`pytest-bdd`) test suites, documentation, and CI/release workflows.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Workspace contains `crates/gh-repoconf-core` exporting `VERSION` and `crates/gh-repoconf` standalone CLI binary under MIT license.
- [x] #2 `recipe/recipe.yaml` and `recipe/variants.yaml` build and smoke-test the `gh-repoconf` Conda package via `rattler-build`.
- [x] #3 Rust (`rstest-bdd`) and Python (`pytest-bdd`) BDD test suites pass with all lockfiles (`Cargo.lock`, `pixi.lock`, `bun.lock`) resolved.
- [x] #4 All linters (`clippy`, `ruff`, `mypy`, `alint`, `gherlint`, `vale`, `markdownlint-cli2`, `actionlint`, `taplo`) and architectural decisions (`doc-1`, `decision-1`..`decision-4`) are committed and passing.
<!-- AC:END -->

## Final Summary

Implemented the two-crate `VERSION`-only scaffold (`gh-repoconf-core` and `gh-repoconf`), Conda recipe (`recipe/`), Pixi/sandbox/Bun manifests and lockfiles, Python automation tools, Rust and Python BDD test suites, documentation, and CI/release workflows.
