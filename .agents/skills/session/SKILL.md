---
name: session
description: Reconstruct the project state at the start of a session or whenever chat history is missing or incomplete.
---

# Session

Use before planning or editing when a session begins or prior context was condensed.

1. Read `AGENTS.md`, the current request, and workspace state (`git status --short`, active branch, and backlog records). Treat live files as the source of truth.
2. Verify Pixi availability (`command -v pixi`); if absent, run `sh scripts/bootstrap.sh` from the repository root and export `PATH="$HOME/.local/bin:$PATH"`.
3. Install Git hooks via `pixi run --frozen --no-install hooks-install` when `.git/hooks/pre-commit` is missing.
4. Survey the backlog with `pixi run --frozen backlog task list --plain` and `pixi run --frozen backlog milestone list --plain` and read relevant ADRs in `backlog/decisions/`.
5. Verify generated files (`scripts/restore.sh`, `.vale.ini`, `.vale/styles/`, sandbox workflows) via `pixi run --frozen sandbox-check` and `pixi run --frozen automation prose_check` instead of editing generated outputs directly.
6. Report only directly observed command results and test outputs at handoff.
