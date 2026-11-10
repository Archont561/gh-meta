# gh-repoconf Documentation

This directory is the canonical user-facing knowledge layer of `gh-repoconf`.
Every document here reflects verified repository state and is checked by
`markdownlint-cli2`, `Vale`, `lychee`, and `alint`.

## Areas

| Area | Purpose |
| --- | --- |
| [guides/](guides/) | Onboarding setup and check execution workflows |
| [concepts/](concepts/) | Scope and design of the version-only scaffold |
| [architecture/](architecture/) | Crate boundaries, UI plans, and distribution targets |
| [reference/](reference/) | Locked Pixi tasks and repository directory invariants |
| [development/](development/) | Documentation standard and review criteria |

## Entry points

- [Development setup](guides/development-setup.md)
- [Running the checks](guides/running-the-checks.md)
- [Releasing and Trusted Publishing](guides/releasing.md)
- [Version-only scaffold](concepts/version-only-scaffold.md)
- [Architecture overview](architecture/overview.md)
- [Project name](architecture/project-name.md) — why `gh-repoconf`, and what was rejected
- [Pixi tasks reference](reference/pixi-tasks.md)
- [Repository layout reference](reference/repository-layout.md)
- [Documentation standard](development/documentation.md)
