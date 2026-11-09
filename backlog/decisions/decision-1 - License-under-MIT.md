---
id: decision-1
title: License gh-meta under MIT
date: '2026-11-09'
status: accepted
---

## Context

`gh-meta` needs an unambiguous, permissive open-source license matching `Archont561/*` Rust and Conda packages prior to publishing crates, standalone binaries, or `.conda` packages.

## Decision

License the entire `gh-meta` repository, its Cargo workspace (`gh-meta-core`, `gh-meta`), and its Conda recipe (`crates/gh-meta/recipe/recipe.yaml`) under the **MIT License** using a single root `LICENSE` file copied into each publishable crate directory (`crates/gh-meta-core/LICENSE`, `crates/gh-meta/LICENSE`).

## Consequences

- `Cargo.toml` sets `license = "MIT"` at `[workspace.package]` and crates inherit `license.workspace = true`.
- `deny.toml` allows `MIT` alongside compatible dependency licenses.
- `automation/repo_check.py` and `automation/check_packages.py` assert root and crate `LICENSE` parity.
