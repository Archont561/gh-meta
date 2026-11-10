# Architecture overview

## Workspace layers

`gh-repoconf` separates core logic from CLI delivery and repository tooling:

1. **`crates/gh-repoconf-core`** — domain-independent core crate (`VERSION` and
   version banner formatting today; future config model, diff planner, and
   template engine).
2. **`crates/gh-repoconf`** — standalone CLI binary (`gh-repoconf`), `gh` CLI
   extension entrypoint, PyPI (`maturin`) manifest, and `rattler-build` Conda
   packaging recipe under `crates/gh-repoconf/recipe/`.
3. **`automation/` and `dodo.py`** — Python automation modules, shared helpers
   under `automation/lib/`, `pytest-bdd` BDD suite under
   `automation/{features,tests}/`, and unified `doit` CLI task registry in
   `dodo.py`.
4. **`scripts/`** — shell setup and sandbox restore launchers (`restore.sh`,
   `bootstrap.sh`, `install_hooks.sh`).

## Planned interactive UI (`clifacet`)

Per [decision-2](../../backlog/decisions/decision-2%20-%20Adopt-clifacet-for-interactive-UI.md),
interactive wizards, confirmations, and terminal views adopt
[`Archont561/clifacet`](https://github.com/Archont561/clifacet).

`clifacet` 0.5.0 is a runtime dependency of the `gh-repoconf` binary crate with
**every frontend feature disabled**. Its mandatory surface is the command seam
(`Command`), its failure type (`Failure`), and `secret::Secret`; the interactive
(`inquire`) and full-screen (`ratatui` + `crossterm`) frontends stay off until a
command needs one, which keeps standalone binary and Conda recipe builds small.
`gh-repoconf-core` keeps no runtime dependencies.

## Distribution targets

- **GitHub Releases and `gh` extension (`gh extension install Archont561/gh-repoconf`)**:
  precompiled release assets named `gh-repoconf-<os>-<arch>[.exe]` accompanied
  by `.conda` archives and `SHA256SUMS`.
- **prefix.dev (`archont561/archont561`)**: native `.conda` packages built from
  `crates/gh-repoconf/recipe/recipe.yaml` and `crates/gh-repoconf/recipe/variants.yaml`
  via `rattler-build` and uploaded via GitHub OIDC (`prefix` environment).
- **PyPI (`gh-repoconf`)**: binary CLI wheels (`manylinux_2_28`, macOS, and Windows)
  and source distribution built via `maturin` (`crates/gh-repoconf/pyproject.toml`)
  and published via OIDC (`pypi` environment).
- **npm (`gh-repoconf` and `@archont561/gh-repoconf-*`)**: main wrapper package and
  five scoped platform binary packages generated and published via `cargo-npm`
  (`[package.metadata.npm]` in `crates/gh-repoconf/Cargo.toml`) using OIDC with
  provenance (`npm` environment).

See [Releasing and Trusted Publishing](../guides/releasing.md) for tag
validation, dry runs, and registry Trusted Publisher configuration.
