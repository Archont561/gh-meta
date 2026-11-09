#!/usr/bin/env bash
set -euo pipefail

if ! command -v pixi >/dev/null 2>&1; then
  curl -fsSL https://pixi.sh/install.sh | PIXI_VERSION=v0.83.0 sh
  export PATH="$HOME/.pixi/bin:$PATH"
fi

pixi install --locked
pixi run --locked bun-install
pixi run --locked install-hooks
