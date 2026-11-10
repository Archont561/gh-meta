# Contributing to gh-meta

`gh-meta` is an early scaffold for managing `.github/` configuration as code.
The `clifacet` command seam is wired with no frontend enabled; domain commands
have not landed yet. Read the specification and ADRs under
[backlog/](backlog/README.md) before proposing new features, and avoid
presenting planned capabilities as implemented.

## Development setup

The locked Pixi workspace targets `linux-64` (`pixi.toml`, `pixi.lock`).
Install Pixi (or restore the published sandbox), then run:

```sh
pixi install --locked
pixi run --locked bun-install
pixi run --locked install-hooks
```

See [the development setup guide](docs/guides/development-setup.md) for the
full onboarding walkthrough, sandbox restoration via `scripts/restore.sh`,
and troubleshooting notes.

## Making changes

1. Survey active tasks and ADRs using `pixi run --locked backlog`. Update task
   cards through the `backlog` CLI rather than hand-editing files.
2. Keep Rust code, features, and BDD tests inside the owning crate
   (`crates/gh-meta-core/` or `crates/gh-meta/`), Python automation modules
   and BDD tests under `automation/` (`automation/lib/`,
   `automation/features/`, `automation/tests/`) registered in `dodo.py`, and
   shell bootstrap helpers under `scripts/`.
3. Write a Gherkin scenario and failing BDD test before adding new
   user-visible behavior.
4. Keep canonical documentation under [docs/](docs/README.md) accurate in
   accordance with
   [the documentation standard](docs/development/documentation.md).

## Running the checks

```sh
pixi run --locked fmt-check
pixi run --locked clippy
pixi run --locked test-all
pixi run --locked coverage
pixi run --locked test-automation
pixi run --locked lint-python
pixi run --locked format-python-check
pixi run --locked typecheck
pixi run --locked alint
pixi run --locked automation check_policy
pixi run --locked docs-lint
pixi run --locked actionlint
```

See [running the checks](docs/guides/running-the-checks.md) for details on
every gate.

## Pull requests

Use Conventional Commits (verified by `convco` via `lefthook` and CI). Follow
the checklist in
[the pull request template](.github/PULL_REQUEST_TEMPLATE.md) and file issues
using [the issue forms](.github/ISSUE_TEMPLATE/).
