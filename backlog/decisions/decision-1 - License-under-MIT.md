---
id: decision-1
title: License gh-repoconf under MIT
date: '2026-11-09'
status: accepted
---

## Context

`gh-repoconf` needs an unambiguous, permissive open-source license matching `Archont561/*` Rust and Conda packages prior to publishing crates, standalone binaries, or `.conda` packages.

## Decision

License the entire `gh-repoconf` repository, its Cargo workspace (`gh-repoconf-core`, `gh-repoconf`), and its Conda recipe (`crates/gh-repoconf/recipe/recipe.yaml`) under the **MIT License** using a single root `LICENSE` file copied into each publishable crate directory (`crates/gh-repoconf-core/LICENSE`, `crates/gh-repoconf/LICENSE`).

## Consequences

- `Cargo.toml` sets `license = "MIT"` at `[workspace.package]` and crates inherit `license.workspace = true`.
- `deny.toml` allows `MIT` alongside compatible dependency licenses.
- `automation/repo_check.py` and `automation/check_packages.py` assert root and crate `LICENSE` parity.
