---
id: decision-2
title: Adopt Archont561/clifacet for interactive CLI and TUI workflows
date: '2026-11-09'
status: accepted
---

## Context

`gh-repoconf` will eventually present interactive setup wizards, diff reviews, confirmation prompts, and terminal UI flows for managing `.github/` repositories as code. Early scaffolding requires choosing the UI abstraction layer without bloating initial `VERSION`-only builds.

## Decision

Adopt [`Archont561/clifacet`](https://github.com/Archont561/clifacet) as the target interactive CLI/TUI framework for `gh-repoconf` once interactive workflows begin in milestone `m-1`. Do not wire `clifacet` (or heavy terminal UI crates) into `Cargo.toml` during the `m-0` version-only scaffold so standalone release builds and Conda recipe builds remain fast and minimal.

## Consequences

- `m-0` keeps runtime dependencies restricted to `clap` (lean features) and `gh-repoconf-core`.
- Adding `clifacet` later requires a dedicated backlog task under `m-1` with BDD scenario coverage across headless/scripted terminal frontends.
