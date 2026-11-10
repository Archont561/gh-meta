# Version-only scaffold

`gh-repoconf` begins as an intentional **version-only scaffold** (`decision-3`)
before full `.github/` configuration synchronization features land.

## Current behavior

- `crates/gh-repoconf-core` exports `VERSION: &str = env!("CARGO_PKG_VERSION")`
  and `format_version_banner(binary: &str) -> String`.
- `crates/gh-repoconf` exposes `gh-repoconf --version`, `-V`, `gh-repoconf version`, and
  `--help` backed by `gh-repoconf-core`, and depends on `clifacet` 0.5.0 with every
  frontend feature disabled. Credentials route through
  `clifacet::secret::Secret`, so `gh_repoconf::redacted` renders them as
  `[redacted]`.
- `crates/gh-repoconf/recipe/recipe.yaml` packages the standalone `gh-repoconf` binary
  into a Conda artifact and tests `gh-repoconf --version` and `gh-repoconf --help`.
- `automation/` and `automation/dodo.py` deliver workspace version checking
  (`bump_version.py`), prose config rendering (`prose.py`), Gherkin linting
  (`gherkin_lint.py`), unified `doit` task execution (`pixi run automation`),
  and Python `pytest-bdd` acceptance specs under `automation/features/`.

## Graduation criteria

Expanding beyond `VERSION` and CLI boilerplate requires a dedicated task in
milestone `m-1` (starting with `rep-002`) with Gherkin scenarios first.
