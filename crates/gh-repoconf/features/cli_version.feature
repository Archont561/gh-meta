Feature: CLI version and help surface
  The initial gh-repoconf CLI reports help and version consistently via
  flags and subcommands while rejecting unknown options cleanly.

  Scenario: Display help via flag
    Given the "gh-repoconf" command with "--help"
    When it runs
    Then it exits with code 0
    And standard output mentions "Your .github/ directory, managed as code"
    And standard error is empty

  Scenario: Print version via long flag
    Given the "gh-repoconf" command with "--version"
    When it runs
    Then it exits with code 0
    And trimmed standard output equals "gh-repoconf 0.1.0"
    And standard error is empty

  Scenario: Print version via short flag
    Given the "gh-repoconf" command with "-V"
    When it runs
    Then it exits with code 0
    And trimmed standard output equals "gh-repoconf 0.1.0"
    And standard error is empty

  Scenario: Print version via subcommand
    Given the "gh-repoconf" command with "version"
    When it runs
    Then it exits with code 0
    And trimmed standard output equals "gh-repoconf 0.1.0"
    And standard error is empty

  Scenario: Reject unknown flag
    Given the "gh-repoconf" command with "--definitely-invalid"
    When it runs
    Then it exits with code 2
    And standard error mentions "unexpected argument"
