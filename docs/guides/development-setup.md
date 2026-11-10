# Development setup

The locked developer environment lives in `pixi.toml` and `pixi.lock`
(`linux-64`).

## Provisioning with Pixi

Install Pixi (`v0.81.0` or newer), then provision both Pixi and Bun tools:

```sh
pixi install --locked
pixi run --locked bun-install
pixi run --locked install-hooks
```

To build and verify the standalone binary directly:

```sh
pixi run --locked build-release
./target/release/gh-repoconf --version
```

To build and smoke-test the Conda package with `rattler-build`:

```sh
pixi run --locked -e packaging package
```

## Restoring from the developer sandbox

When restoring an offline or sandboxed host without fetching Conda packages
from `conda-forge`, run the generated launcher from the repository root:

```sh
sh scripts/restore.sh
export PATH="$HOME/.local/bin:$PATH"
pixi run --frozen --no-install hooks-install
```

`scripts/restore.sh` and its publishing workflows are generated from
`pixi-sandbox.toml` via `pixi-sandbox init`. Verify consistency with:

```sh
pixi run --locked sandbox-check
```
