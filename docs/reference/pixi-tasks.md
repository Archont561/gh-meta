# Pixi tasks reference

Core environment, Rust, Bun, and packaging tasks live in `pixi.toml`. Python
repository automation tasks are consolidated under `dodo.py` and invoked
through `pixi run automation <task>` (`doit`).

## Pixi tasks

| Task | Purpose |
| --- | --- |
| `setup` | Bootstrap session environment, hooks, and smoke checks |
| `install-hooks` | Install `lefthook` hooks from `lefthook.yml` |
| `bun-install` | Provision locked Bun CLI dependencies |
| `agents-md` | Refresh marked sections of `AGENTS.md` |
| `backlog` | Run `backlog.md` CLI |
| `skills` | Run `skills` CLI |
| `automation` | Run `doit` tasks registered in `dodo.py` (`pixi run automation list`) |
| `fmt` / `fmt-check` | Format or verify Rust code via `cargo fmt` |
| `clippy` | Run Clippy over all workspace targets with `-D warnings` |
| `test` / `test-doc` / `test-all` | Run `cargo nextest` BDD/unit suites and Rust doctests |
| `coverage` | Generate Rust LCOV report and run `doit check_coverage` (90% threshold) |
| `build-release` | Compile `target/release/gh-meta` with `--locked` |
| `lint-python` / `format-python-check` | Check `dodo.py` and `automation/` with `ruff` |
| `typecheck` | Type-check `dodo.py` and `automation/` with `mypy` |
| `test-automation` / `test-automation-cov` | Run Python `pytest-bdd` and unit test suites |
| `alint` | Check `.alint.yml` repository structural rules |
| `docs-lint` | Lint Markdown with `markdownlint-cli2` |
| `check-links` / `check-links-offline` | Validate Markdown links with `lychee` |
| `actionlint` | Lint `.github/workflows/*.yml` with embedded `shellcheck` |
| `lint-toml` | Verify TOML formatting with `taplo` |
| `sandbox-check` | Verify generated sandbox files against `pixi-sandbox.toml` |
| `deny` / `audit` | Run `cargo deny` and `cargo audit` checks |
| `-e packaging package` | Build and smoke-test Conda package via `rattler-build` |
| `-e pypi package-pypi` | Build PyPI binary wheel and source distribution via `maturin` |

## `doit` automation tasks (`pixi run automation <task>`)

| Task | Purpose |
| --- | --- |
| `list` | List all discovered `task_*` commands from `dodo.py` |
| `check_policy` | Run all read-only Python policy, packaging, prose, and changelog checks |
| `repo_check` | Check cross-file license, symlink, and sandbox parity |
| `version_check` / `bump_version` | Verify or bump synchronized manifest versions |
| `check_packages` | Verify `cargo package --list` contents and registry metadata |
| `check_coverage` | Normalize and validate LCOV source-line coverage |
| `skills_check` | Verify `.agents/skills/` and `skills-lock.json` |
| `backlog_check` | Verify backlog task statuses match acceptance criteria |
| `advisory_exception` | Check RustSec exception against `Cargo.lock` |
| `advisory_cache` / `audit_offline` | Manage weekly advisory cache and offline `cargo audit` |
| `lint_gherkin` | Lint all `features/*.feature` files across crates and automation |
| `prose_write` / `prose_sync` / `prose_check` / `lint_prose` | Render, verify, and run Vale prose checks |
| `changelog` / `changelog_check` | Render, inspect, or verify `CHANGELOG.md` |
| `change_scope` / `commit_range` | Classify CI doc-only diffs and validate commit ranges |
