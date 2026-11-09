Feature: Workspace version synchronization tool

  The bump-version script keeps Cargo, Pixi, the Conda recipe, and package.json
  at the same semantic version and ensures every crate inherits the workspace
  version from the root manifest.

  Scenario: Live repository manifests match the workspace version
    Given the live gh-meta repository workspace
    When the version checker inspects all workspace manifests
    Then the version check exits with code 0
    And all manifest version sites record the same version

  Scenario: Detect version drift in the Conda recipe
    Given a temporary workspace at version "0.1.0"
    And the temporary Conda recipe context version is changed to "0.9.9"
    When the version checker inspects the temporary workspace
    Then the version check exits with code 1
    And the version checker reports drift in "crates/gh-meta/recipe/recipe.yaml"

  Scenario: Refuse a workspace crate that pins its own version
    Given a temporary workspace at version "0.1.0"
    And crate "gh-meta" pins explicit version "0.1.0" instead of inheriting
    When the version checker inspects the temporary workspace
    Then the version check exits with code 1
    And the version checker reports an explicit crate version pin

  Scenario: Bump all version sites cleanly across manifests
    Given a temporary workspace at version "0.1.0"
    When the bump tool updates the temporary workspace to "0.2.0"
    Then the bump tool exits with code 0
    And the version checker on the temporary workspace reports "0.2.0" across all manifests
