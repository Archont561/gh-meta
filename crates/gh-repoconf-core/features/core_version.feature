Feature: Core crate version constant
  The core crate exports the shared package version and banner helper
  before any command handlers or domain types exist.

  Scenario: Core version matches the crate manifest
    Given the "gh-repoconf-core" crate metadata version
    When a caller reads the core VERSION constant
    Then the constant equals "0.1.0"

  Scenario: Banner includes the package name and version
    Given the tool name "gh-repoconf-core"
    When a caller formats the version banner
    Then the banner equals "gh-repoconf-core 0.1.0"
