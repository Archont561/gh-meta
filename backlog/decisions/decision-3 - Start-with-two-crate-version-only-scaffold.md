---
id: decision-3
title: Start with a minimal two-crate version-only Cargo workspace
date: '2026-11-09'
status: accepted
---

## Context

The full product vision spans multiple functional domains (schema modeling, `.github/` templates, GitHub API synchronization, drift detection, and interactive UX). Creating empty placeholder crates prematurely slows compilation, inflates CI, and obscures actual implemented behavior.

## Decision

Begin with a cohesive two-crate Rust workspace:
1. `crates/gh-meta-core` — library crate exposing `VERSION = env!("CARGO_PKG_VERSION")` and banner formatting.
2. `crates/gh-meta` — standalone CLI binary crate (`gh-meta`) wrapping `gh-meta-core`.

Both crates maintain co-located `{src,features,tests}` directories with `rstest-bdd` feature specs verified before new crates or exports are introduced.

## Consequences

- `alint` and `automation/check_packages.py` enforce `crates/*/{src,features,tests}` invariants on the two crates.
- All user-facing documentation explicitly labels the current state as a version-only scaffold until domain tasks land.
