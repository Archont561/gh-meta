# Project name

The project is named **`gh-repoconf`**, recorded in
`decision-5`. The decision rests on what each distribution channel allows, not
on preference.

## Why the name is constrained by channels

Three of the four channels the project ships to are either permanent or
name-driven:

| Channel | Constraint |
| --- | --- |
| PyPI (`maturin`) | Package names are never released once taken |
| npm (`cargo-npm`) | Scoped as `@archont561/gh-repoconf-*`, so always available |
| prefix.dev | The `archont561/archont561` channel is owned by this project |
| GitHub | The repository name sets the `gh` command, because an extension ships `<repo>-<os>-<arch>` binaries |

The `gh-` prefix satisfies the extension convention and keeps the unprefixed
namespace in reserve, which is why one spelling serves both.

## Current names

| Artifact | Name |
| --- | --- |
| Repository | `Archont561/gh-repoconf` |
| `gh` command | `gh repoconf` |
| Release assets | `gh-repoconf-<os>-<arch>[.exe]` |
| Conda package | `gh-repoconf` |
| PyPI distribution | `gh-repoconf` |
| npm packages | `@archont561/gh-repoconf-*` |
| Crates | `repoconf`, `repoconf-core` |
| Shipped binary | `gh-repoconf` |

The crates use the bare identifier because Cargo requires one, while the shipped
binary keeps the `gh-` prefix. No crate is published to crates.io, so the crate
name carries no collision risk.

## Rename status

The name is frozen. The repository content still uses `gh-repoconf` throughout; the
rename is a separate change, and renaming the GitHub repository itself is a
Settings action for the maintainer. GitHub redirects old paths, so existing links
keep resolving.
