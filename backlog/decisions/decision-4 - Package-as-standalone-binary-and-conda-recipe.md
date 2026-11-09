---
id: decision-4
title: Package gh-meta as both a gh CLI extension binary and a Conda package
date: '2026-11-09'
status: accepted
---

## Context

Users install GitHub CLI extensions via `gh extension install Archont561/gh-meta` (expecting precompiled `gh-meta-<os>-<arch>[.exe]` release assets), while reproducible developer and Nix/Pixi environments consume Conda packages built by `rattler-build`.

## Decision

Maintain dual first-class distribution targets:
1. Standalone release binary built from `crates/gh-meta` and published under `gh-meta-<os>-<arch>[.exe]` with `SHA256SUMS`.
2. Conda package defined in `crates/gh-meta/recipe/recipe.yaml` + `crates/gh-meta/recipe/variants.yaml`, built and smoke-tested via `rattler-build` (`pixi run -e packaging package`).

Keep `Cargo.toml`, `pixi.toml`, `crates/gh-meta/recipe/recipe.yaml`, and `package.json` versions locked in parity via `automation/bump_version.py` (`pixi run automation bump_version`).

## Consequences

- CI builds and tests both the standalone release binary (`cargo build --release --locked`) and the Conda `.conda` archive (`rattler-build`) on pull requests.
- Release workflows assemble both asset families onto each tagged GitHub Release.
