# Repository layout reference

```text
.
├── .agents/skills/        # Project-local and locked Agent Skills
├── .alint/schemas/        # JSON schemas validated by alint
├── .cargo/                # Cargo audit configuration
├── .devcontainer/         # Devcontainer image and bootstrap setup
├── .github/               # Issue forms, PR template, Dependabot, CI/release workflows
├── .vale/styles/          # Rendered House style and synced Vale packages
├── automation/            # Python automation modules, `lib/`, `features/`, `tests/`
├── backlog/               # Product spec, ADRs, milestones, and Backlog.md tasks
├── crates/
│   ├── gh-repoconf-core/      # Core crate (`src/`, `features/`, `tests/`, `LICENSE`)
│   └── gh-repoconf/           # CLI crate (`src/`, `recipe/`, `pyproject.toml`, `features/`, `tests/`, `LICENSE`)
├── docs/                  # Canonical user and developer documentation
├── scripts/               # Shell setup and sandbox restore scripts (`restore.sh`, `bootstrap.sh`, `install_hooks.sh`)
├── Cargo.toml             # Root Cargo workspace manifest
├── automation/dodo.py     # Unified doit automation task registry (`pixi run automation`)
├── pixi.toml              # Locked Pixi workspace and task definitions
├── pixi-sandbox.toml      # Sandbox publication policy
├── package.json           # Developer Bun CLI manifest
├── vale.toml              # Authored prose lint policy
├── AGENTS.md              # AI agent operational instructions
└── CLAUDE.md -> AGENTS.md # Symlink for Claude Code compatibility
```
