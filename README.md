# Offline sandbox (orphan branch)

Built 2026-11-10T22:17:41Z from commit `19428ae` for platform `linux-64`.
`pixi.lock` sha256 `d628481fe286f419465def0f515f372a9282c110188657f2ae5319732d3e0373`.

The verified self-bootstrap binary is stored at `.pixi-sandbox/tools/linux-64/pixi-sandbox`. The branch root intentionally contains documentation only.

| env | platform | packed | unpacked | files |
| --- | --- | ---: | ---: | ---: |
| `default` | linux-64 | 564.3 MiB | 2190.3 MiB | 95 |

Cargo dependencies: **204 crates**, 272.1 MiB (loose) from `Cargo.lock` sha256 `28fd2d31f25e…`; restore materialises them to `.pixi-sandbox/vendor/`. Built with cargo 1.99.1 (5f94df478 2026-08-27); rustc 1.99.1 (58cf8f9c3 2026-10-13).


## Restore on the disconnected machine

```bash
./.pixi-sandbox/tools/linux-64/pixi-sandbox doctor --branch-location . --verify
./.pixi-sandbox/tools/linux-64/pixi-sandbox restore --branch-location . --output-path <project> --force
# then, from <project> with no network, use pixi as the sole entrypoint:
pixi install --frozen --offline
pixi run --frozen -- cargo build --offline
```

Every manifest blob is verified before it is written into the working tree.
