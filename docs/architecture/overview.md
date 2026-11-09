# Architecture overview

## Workspace layers

`gh-meta` separates core logic from CLI delivery and repository tooling:

1. **`crates/gh-meta-core`** — domain-independent core crate (`VERSION` and
   version banner formatting today; future config model, diff planner, and
   template engine).
2. **`crates/gh-meta`** — standalone CLI binary (`gh-meta`), `gh` CLI
   extension entrypoint, PyPI (`maturin`) manifest, and `rattler-build` Conda
   packaging recipe under `crates/gh-meta/recipe/`.
3. **`automation/` and `dodo.py`** — Python automation modules, shared helpers
   under `automation/lib/`, `pytest-bdd` BDD suite under
   `automation/{features,tests}/`, and unified `doit` CLI task registry in
   `dodo.py`.
4. **`scripts/`** — shell setup and sandbox restore launchers (`restore.sh`,
   `bootstrap.sh`, `install_hooks.sh`).

## Planned interactive UI (`clifacet`)

Per [decision-2](../../backlog/decisions/decision-2%20-%20Adopt-clifacet-for-interactive-UI.md),
interactive wizards, confirmations, and terminal views will adopt
[`Archont561/clifacet`](https://github.com/Archont561/clifacet). Initial `m-0`
releases omit `clifacet` from runtime dependencies so standalone binary and
Conda recipe builds remain small and fast while version/packaging/BDD pipelines
stabilize.

## Distribution targets

- **GitHub Releases and `gh` extension (`gh extension install Archont561/gh-meta`)**:
  precompiled release assets named `gh-meta-<os>-<arch>[.exe]` accompanied
  by `.conda` archives and `SHA256SUMS`.
- **prefix.dev (`archont561/archont561`)**: native `.conda` packages built from
  `crates/gh-meta/recipe/recipe.yaml` and `crates/gh-meta/recipe/variants.yaml`
  via `rattler-build` and uploaded via GitHub OIDC (`prefix` environment).
- **PyPI (`gh-meta`)**: binary CLI wheels (`manylinux_2_28`, macOS, and Windows)
  and source distribution built via `maturin` (`crates/gh-meta/pyproject.toml`)
  and published via OIDC (`pypi` environment).
- **npm (`gh-meta` and `@archont561/gh-meta-*`)**: main wrapper package and
  five scoped platform binary packages generated and published via `cargo-npm`
  (`[package.metadata.npm]` in `crates/gh-meta/Cargo.toml`) using OIDC with
  provenance (`npm` environment).

See [Releasing and Trusted Publishing](../guides/releasing.md) for tag
validation, dry runs, and registry Trusted Publisher configuration.
