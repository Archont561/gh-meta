# Releasing and Trusted Publishing

The `.github/workflows/release.yml` workflow builds cross-platform binaries and
native packages across five targets (`x86_64-unknown-linux-musl` /
`manylinux_2_28`, `aarch64-unknown-linux-musl` / `manylinux_2_28`,
`x86_64-apple-darwin`, `aarch64-apple-darwin`, and `x86_64-pc-windows-msvc`)
and publishes strictly through GitHub OIDC Trusted Publishing (`id-token: write`)
with zero long-lived secrets or API tokens.

## Triggering a release or dry run

- **Dry-run artifact build and verification**: dispatch `release.yml` manually
  from GitHub Actions with `version` left empty. The `preflight`, `build`, and
  `verify` jobs produce and smoke-test all binaries, `.conda` packages, PyPI
  wheels and `sdist`, and generated `npm` packages without publishing.
- **Tag release**: run `pixi run --frozen automation bump_version <semver> --relock`,
  commit, tag `v<semver>`, and push the tag. `preflight` checks that the tag
  matches `Cargo.toml`, `pixi.toml`, `crates/gh-repoconf/recipe/recipe.yaml`, and
  `package.json` before any platform build starts.

## One-time Trusted Publisher setup

Create three GitHub repository environments (`prefix`, `pypi`, and `npm`) and
register `Archont561/gh-repoconf` with workflow `.github/workflows/release.yml` on
each registry:

1. **prefix.dev (`prefix` environment)**: authorize OIDC uploads to channel
   `archont561/archont561`. `publish_prefix` uploads `.conda` artifacts using
   `rattler-build upload prefix` with `--generate-attestation`.
2. **PyPI (`pypi` environment)**: create a pending or active Trusted Publisher
   for project `gh-repoconf` on `pypi.org`. `publish_pypi` publishes wheels and the
   source distribution through `pypa/gh-action-pypi-publish`.
3. **npm (`npm` environment)**: link Trusted Publishing on `npmjs.com` for
   `gh-repoconf` and the five `@archont561/gh-repoconf-*` platform packages
   (`linux-x64`, `linux-arm64`, `darwin-x64`, `darwin-arm64`, and `win32-x64`).
   For a new npm package, publish an initial bootstrap release manually or with
   CLI trust configuration before tag-driven `cargo-npm` runs with `--provenance`.

`crates.io` publishing is intentionally omitted from the release workflow.
