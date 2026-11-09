# Running the checks

Every CI gate maps to a locked Pixi task so local runs match automation.

## Rust and packaging checks

```sh
pixi run --locked fmt-check
pixi run --locked clippy
pixi run --locked test-all
pixi run --locked coverage
pixi run --locked automation check_packages
pixi run --locked build-release
pixi run --locked -e packaging package
pixi run --locked -e pypi package-pypi
```

## Python automation and BDD checks

```sh
pixi run --locked lint-python
pixi run --locked format-python-check
pixi run --locked typecheck
pixi run --locked test-automation
pixi run --locked test-automation-cov
pixi run --locked automation list
pixi run --locked automation lint_gherkin
```

## Policy, prose, and workflow checks

```sh
pixi run --locked alint
pixi run --locked sandbox-check
pixi run --locked actionlint
pixi run --locked lint-toml
pixi run --locked docs-lint
pixi run --locked check-links-offline
pixi run --locked automation check_policy
```

Individual `doit` automation tasks can also run independently (or in parallel
with `-n`):

```sh
pixi run --locked automation repo_check
pixi run --locked automation bump_version --check
pixi run --locked automation skills_check
pixi run --locked automation backlog_check
pixi run --locked automation advisory_exception
pixi run --locked automation prose_check
pixi run --locked automation lint_prose
pixi run --locked automation changelog_check
```

## Dependency advisory exception

`deny.toml` and `.cargo/audit.toml` currently carry an explicit exception for
`RUSTSEC-2026-0374` (`basic-toml`, dev-dependency only via `rstest-bdd`).
`pixi run --locked automation advisory_exception` verifies against `Cargo.lock` that
this transitive edge still exists and automatically fails once removed so the
exception is retired cleanly:

```text
rstest-bdd 0.6.0 → i18n-embed 0.16.0 → i18n-embed-impl 0.8.4 → i18n-config 0.4.8 → basic-toml 0.1.10
```
