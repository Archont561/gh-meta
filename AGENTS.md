# AGENTS.md

> Guidance for AI coding agents working in this repository. Verify live state
> in workspace files, manifests, and test output before acting.

## Start each session with environment and hook setup

Before surveying the backlog or editing files, verify Pixi is installed with
`command -v pixi`. If missing, run `sh scripts/restore.sh` (or
`bash scripts/bootstrap.sh`) from the repository root, export
`PATH="$HOME/.local/bin:$PATH"`, and confirm `pixi --version`. Once Pixi is
ready, run `pixi run --locked install-hooks` at the start of every session.

## Start each session with a backlog survey

Survey active planning records before picking work:

```sh
pixi run --locked backlog instructions overview
pixi run --locked backlog milestone list --plain
pixi run --locked backlog task list --status "In Progress" --plain
pixi run --locked backlog task list --status "To Do" --plain
```

Read `backlog/docs/` and `backlog/decisions/` before modifying workspace
boundaries. Manage task cards through `pixi run --locked backlog`, never by
editing task Markdown manually.

## Engineering rules

- Keep the Cargo workspace at the intentional **version-only scaffold**
  (`crates/gh-repoconf-core` and `crates/gh-repoconf`, decision-3) until an approved
  backlog task relaxes it. The single recorded exception is `clifacet` 0.5.0
  with every frontend feature disabled; enabling a frontend needs the `m-1`
  task decision-2 requires.
- Keep runtime dependencies minimal in `m-0`; interactive workflows target
  `Archont561/clifacet` (decision-2) in milestone `m-1`.
- Keep every crate's `Cargo.toml` inheriting `version.workspace = true`, and
  sync manifest versions via `pixi run --locked automation bump_version`.
- Keep product code, features, and BDD tests inside `crates/*/{src,features,tests}`,
  Python automation and BDD suites inside `automation/{lib,features,tests}`
  registered through `automation/dodo.py`, and shell launchers in `scripts/`.
- Never edit generated outputs directly: update `vale.toml` and run
  `pixi run --locked automation prose_sync`; update `pixi-sandbox.toml` and run
  `pixi-sandbox init`.
- Keep root `LICENSE` (MIT) and `crates/*/LICENSE` identical.
- Follow Conventional Commits (`convco`, `.versionrc`).

## Testing and verification

- `pixi run --locked test-all` — Rust workspace tests (`nextest`) and doctests.
- `pixi run --locked coverage` — Rust LCOV coverage gate (>= 90% source lines).
- `pixi run --locked test-automation` — Python `pytest-bdd` and unit tests.
- `pixi run --locked automation list` — list unified `doit` automation tasks in `automation/dodo.py`.
- `pixi run --locked -e packaging package` — Conda `rattler-build` verification.
- `pixi run --locked -e pypi package-pypi` — PyPI wheel and `sdist` verification.
- See [docs/guides/running-the-checks.md](docs/guides/running-the-checks.md)
  for the complete gate list.

## Boundaries (durable)

- ✅ **Always**: run tests and linters via `pixi run --locked`; write Gherkin
  BDD scenarios for new behaviors; keep `docs/` synchronized with code.
- ⚠️ **Ask first**: expanding crate boundaries beyond the two-crate scaffold;
  adding runtime dependencies; editing `.github/workflows/` release rules.
- 🚫 **Never**: commit secrets or tokens; push, tag, merge, or publish without
  explicit user authorization; bypass hooks with `--no-verify`; replace
  `CLAUDE.md` symlink with a copy.

<!-- markdownlint-disable MD022 MD032 MD034 MD036 -->
<!-- agents-md:begin id=overview -->
## Overview
gh-repoconf — Your .github/ directory, managed as code. Early version-only Rust CLI scaffold with developer CLIs provisioned here and in pixi.lock. Stack: node.
<!-- agents-md:end id=overview -->

<!-- agents-md:begin id=commands -->
## Commands
- Install: `npm install`
- Build: `npm run build`
- Test: `npm run test`
- Lint: `npm run lint`
- Typecheck: `npm run typecheck`
- Format: `npm run format`
<!-- agents-md:end id=commands -->

<!-- agents-md:begin id=testing -->
## Testing
_TBD: how tests are run and what must pass before a change is considered done_
<!-- agents-md:end id=testing -->

<!-- agents-md:begin id=structure -->
## Project structure
Top-level: `automation/`, `backlog/`, `crates/`, `docs/`, `scripts/`. `automation/dodo.py` registers Python automation CLI tasks via `doit`.
<!-- agents-md:end id=structure -->

<!-- agents-md:begin id=conventions -->
## Code style & conventions
_TBD: formatter/linter, naming, import patterns, anything an agent should match_
<!-- agents-md:end id=conventions -->

<!-- agents-md:begin id=git -->
## Git & PR workflow
Default branch `main`. Remote: https://github.com/Archont561/gh-repoconf. _TBD: commit/PR conventions, how changes ship (CI? automated releases?)_
<!-- agents-md:end id=git -->

<!-- agents-md:begin id=gotchas -->
## Gotchas & hard-won lessons
_TBD: framework quirks and things that have broken before + how they were fixed — add to this after every incident_
<!-- agents-md:end id=gotchas -->

<!-- agents-md:begin id=security -->
## Security & secrets
Never commit real secrets.
<!-- agents-md:end id=security -->

<!-- agents-md:begin id=boundaries -->
## Boundaries
- ✅ **Always**: run tests/typecheck before committing; keep code in owning crates and `automation/`
- ⚠️ **Ask first**: risky changes — adding dependencies, touching release/CI workflows
- 🚫 **Never**: commit secrets or API keys; edit generated output or `node_modules/`; force-push `main`
<!-- agents-md:end id=boundaries -->
<!-- markdownlint-enable MD022 MD032 MD034 MD036 -->

## How this file is maintained

Marked sections inside `agents-md:begin/end` comments are refreshed by
`pixi run --locked agents-md`. Durable human-maintained sections outside those
markers are preserved across runs. `CLAUDE.md` symlinks to this file.
