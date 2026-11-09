# Version-only scaffold

`gh-meta` begins as an intentional **version-only scaffold** (`decision-3`)
before full `.github/` configuration synchronization features land.

## Current behavior

- `crates/gh-meta-core` exports `VERSION: &str = env!("CARGO_PKG_VERSION")`
  and `format_version_banner(binary: &str) -> String`.
- `crates/gh-meta` exposes `gh-meta --version`, `-V`, `gh-meta version`, and
  `--help` backed by `gh-meta-core`.
- `crates/gh-meta/recipe/recipe.yaml` packages the standalone `gh-meta` binary
  into a Conda artifact and tests `gh-meta --version` and `gh-meta --help`.
- `automation/` and `dodo.py` deliver workspace version checking
  (`bump_version.py`), prose config rendering (`prose.py`), Gherkin linting
  (`gherkin_lint.py`), unified `doit` task execution (`pixi run automation`),
  and Python `pytest-bdd` acceptance specs under `automation/features/`.

## Graduation criteria

Expanding beyond `VERSION` and CLI boilerplate requires a dedicated task in
milestone `m-1` (starting with `ghm-002`) with Gherkin scenarios first.
