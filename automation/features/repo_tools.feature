Feature: Repository automation and policy tools

  Python automation tools enforce Gherkin hygiene, backlog acceptance criteria
  consistency, skill frontmatter and lockfile alignment, prose configuration
  rendering, and safe offline security checks.

  Scenario: Discover and lint every Gherkin feature file in the repository
    Given the live gh-repoconf repository workspace
    When the Gherkin linter scans the workspace
    Then the Gherkin linter exits with code 0
    And feature files from both crates and automation are linted

  Scenario: Reject a backlog task marked Done with unchecked acceptance criteria
    Given a temporary backlog directory containing a Done task with an unchecked criterion
    When the backlog status guard validates that directory
    Then the backlog status guard exits with code 1

  Scenario: Accept a backlog task marked Done when every acceptance criterion is checked
    Given a temporary backlog directory containing a Done task with all criteria checked
    When the backlog status guard validates that directory
    Then the backlog status guard exits with code 0

  Scenario: Verify offline audit behavior with and without --require
    Given an isolated CARGO_HOME without an advisory database clone
    When the local audit wrapper runs without --require
    Then the local audit wrapper decides "skip"
    When the local audit wrapper runs with --require
    Then the local audit wrapper decides "fail"

  Scenario: Validate repository Agent Skills and lockfile
    Given the live gh-repoconf repository workspace
    When the skills validator inspects the workspace
    Then the skills validator finds zero problems
