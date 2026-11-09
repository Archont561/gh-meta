# Documentation standard

Documentation in `docs/` is the maintained source of truth for `gh-meta`
behavior, tooling, and architecture.

## Principles

1. **Documentation is part of the product**: code or workflow changes must
   update canonical `docs/` files in the same change.
2. **Describe verified behavior only**: clearly distinguish the current
   `VERSION`-only scaffold from planned `m-1` capabilities.
3. **One canonical home**: link rather than duplicating reference tables.

## Validation layers

- `alint` (`.alint.yml`): structural file, layout, and link invariants.
- `markdownlint-cli2` (`.markdownlint-cli2.jsonc`): Markdown style and syntax.
- `Vale` (`vale.toml` -> `.vale.ini`): spelling, house terms, and prose rules.
- `lychee`: broken internal and external link verification.
