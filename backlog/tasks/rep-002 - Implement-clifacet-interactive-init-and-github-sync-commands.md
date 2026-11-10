---
id: rep-002
title: Implement clifacet interactive init and GitHub metadata plan workflows
status: To Do
priority: medium
milestone: m-1
labels:
  - cli
  - ui
dependencies:
  - rep-001
created_date: '2026-11-09'
updated_date: '2026-11-09'
---

## Description

Introduce the declarative `.github/` configuration schema, repository state planner, and interactive CLI/TUI workflows powered by `Archont561/clifacet` (per `decision-2`).

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Document config schema and Gherkin scenarios for `gh-repoconf init` and `gh-repoconf plan` before adding implementation crates.
- [ ] #2 Add `Archont561/clifacet` dependency and headless BDD tests covering scripted interactive prompts.
- [ ] #3 Update `docs/` and release verification checks to cover new interactive commands.
<!-- AC:END -->
