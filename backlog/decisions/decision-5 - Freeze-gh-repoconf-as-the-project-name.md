---
id: decision-5
title: Freeze gh-repoconf as the project name
date: '2026-11-10'
status: accepted
---

## Context

The project shipped as **`gh-meta`** — *Your `.github/` directory, managed as code.*
As scope discussions widened toward other repository concerns (`.devcontainer`,
non-GitHub forges, contributor scaffolding), the name was re-examined, because
`gh-meta` describes a narrow slice ("metadata") while the maintenance chores it
removes are broader: generated files, license parity, version agreement, agent instructions,
and release plumbing are all "repository configuration", not `.github/` files.

A rename has four distribution channels, three of which are permanent:

- **PyPI** (`maturin`) — package names are never released.
- **npm** (`cargo-npm`) — scoped under `@archont561/`, so always available.
- **prefix.dev** — the `archont561/archont561` channel is owned by this project.
- **GitHub** — the repository name drives `gh extension install` and the `gh`
  command name, because an extension's binary must be `<repo>-<os>-<arch>`.

## Decision

Adopt **`gh-repoconf`** as the project name, and use it consistently on every
channel. `metarepo` was considered first and rejected.

`metarepo` was rejected on evidence, not taste:

- `metarepo` on PyPI is owned by `blejdfist` (v0.1.2, 2020) — a manifest-driven
  git repository dependency manager exposing a `git meta` command. Publishing
  there would ship the wrong tool under the name.
- `metarepo` on npm is `1.0.0`. On crates.io it is `0.83.0`, 44 versions.
- The word is crowded on GitHub: `nextools/metarepo` (82★), `blejdfist/git-metarepo`
  (21★), `adamhjk/metarepo` (20★, "creates package repositories for all sorts of
  different package repo formats") — the last is the proposed expanded scope,
  already built and already named that.

`gh-repoconf` was verified free on every channel at decision time: PyPI (404),
npm (404), the owned prefix.dev channel, and **zero** `gh-repoconf` repositories
on GitHub. The unprefixed `repoconf` is taken on PyPI
(`Vaastav-Technologies/py-repoconf`, `0.0.0.dev0`), whose summary — "centrally
configure your decentralised git repo" — is adjacent in intent. The `gh-` prefix
keeps the namespace free and matches the extension convention, so one spelling
serves both constraints.

## Consequences

- The `gh` command is **`gh repoconf`**; release assets are
  `gh-repoconf-<os>-<arch>[.exe]`; the Conda and PyPI packages are `gh-repoconf`.
- npm packages keep the existing scoped shape, `@archont561/gh-repoconf-*`.
- Cargo needs a bare identifier: the crates are `repoconf` and `repoconf-core`,
  while the shipped binary remains `gh-repoconf`. No crate is published to
  crates.io, so the crate name carries no collision risk.
- Documentation, badges, and repository URLs move to `Archont561/gh-repoconf`.
  GitHub redirects the old paths, so existing links keep resolving.
- Renaming the GitHub repository itself is a Settings action for the maintainer;
  the repository content rename is a separate change from this record.
