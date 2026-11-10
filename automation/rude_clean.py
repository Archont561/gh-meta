#!/usr/bin/env python3
"""Gate the `rude` Clean Code thresholds, which `rude` alone reports as warnings.

`rude-clean-code` declares every threshold rule at ``Severity.WARNING`` and the
``rude`` CLI returns ``1`` only when it counted an *error*. A plain
``rude check`` therefore prints violations and still exits ``0``, which is not a
gate. This wrapper treats any reported diagnostic as a failure, so the policy in
``rude.toml`` actually holds CI.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "rude.toml"


def target_paths(root: Path = ROOT) -> list[str]:
    """Return the hand-written automation sources, excluding ``automation/tests``.

    Test functions are long by design, so the policy does not cover them; see
    the scope note in ``rude.toml``.
    """
    candidates = [*(root / "automation").glob("*.py")]
    return [str(path) for path in sorted(candidates) if path.is_file()]


def run_rude(root: Path = ROOT) -> subprocess.CompletedProcess[str]:
    """Run ``rude`` against the configured policy and return the raw result."""
    return subprocess.run(
        ["rude", "check", *target_paths(root), "--config", str(CONFIG), "--format", "compact"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )


def main(root: Path = ROOT) -> int:
    try:
        result = run_rude(root)
    except FileNotFoundError:
        print("rude-clean: `rude` is not installed", file=sys.stderr)
        return 1

    findings = [line for line in result.stdout.splitlines() if line.strip()]
    if not findings:
        if result.returncode != 0:
            # rude failed without diagnostics: bad config or a missing path.
            sys.stderr.write(result.stderr)
            return result.returncode
        print("rude-clean: all Clean Code thresholds hold")
        return 0

    for line in findings:
        print(f"rude-clean: {line}", file=sys.stderr)
    print(f"rude-clean: {len(findings)} Clean Code threshold(s) exceeded", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
