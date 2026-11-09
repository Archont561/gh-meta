<h1 align="center">Welcome to gh-meta 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
  <a href="docs/README.md" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://github.com/Archont561/gh-meta/graphs/commit-activity" target="_blank">
    <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" />
  </a>
  <a href="https://github.com/Archont561/gh-meta/blob/main/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/github/license/Archont561/gh-meta" />
  </a>
</p>

> Your .github/ directory, managed as code. Currently an early version-only scaffold establishing the two-crate Rust workspace, packaging pipelines, and repository automation before domain commands land.

### 🏠 [Homepage](https://github.com/Archont561/gh-meta#readme)

## Documentation

The [`docs/`](docs/README.md) directory is the source of truth for using and
working on this repository:

- [Documentation index](docs/README.md) — everything, organized by purpose
- [Development setup](docs/guides/development-setup.md) — clone, restore the locked developer sandbox, install hooks
- [Running the checks](docs/guides/running-the-checks.md) — the CI suite locally
- [Releasing and Trusted Publishing](docs/guides/releasing.md) — tag-triggered cross-platform releases via GitHub OIDC
- [Pixi tasks](docs/reference/pixi-tasks.md) — the locked task catalog
- [Repository layout](docs/reference/repository-layout.md) — what lives where and why
- [Version-only scaffold](docs/concepts/version-only-scaffold.md) — why the workspace exposes only `VERSION`
- [Architecture overview](docs/architecture/overview.md) — components, planned `clifacet` UI, and distribution targets
- [Documentation standard](docs/development/documentation.md) — how documentation is maintained here

The [backlog](backlog/README.md) tracks planned work; the specification
(`backlog/docs/`) and its decisions (`backlog/decisions/`) describe the
planned design. Planned capabilities are not implemented capabilities — no
`.github/` synchronization commands exist yet.

## Install

```sh
pixi install --locked
```

## Usage

```sh
pixi run --locked build-release
./target/release/gh-meta --version
```

Build the Conda package (`crates/gh-meta/recipe/`) or PyPI distributions (`crates/gh-meta/pyproject.toml`) locally:

```sh
pixi run --locked -e packaging package
pixi run --locked -e pypi package-pypi
```

## Run tests

```sh
pixi run --locked test-all
```

## Author

👤 **Archont561**

- GitHub: [@Archont561](https://github.com/Archont561)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/Archont561/gh-meta/issues). You can also take a look at the [contributing guide](https://github.com/Archont561/gh-meta/blob/main/CONTRIBUTING.md).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2026 [Archont561](https://github.com/Archont561).<br />
This project is [MIT](https://github.com/Archont561/gh-meta/blob/main/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
