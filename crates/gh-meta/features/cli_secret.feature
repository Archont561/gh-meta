Feature: Credential redaction through the clifacet seam
  Values that reach clifacet's Secret are rendered as its redaction marker, so a
  credential cannot leave the CLI through rendered output or a failure message.

  Scenario: A classic token renders as the redaction marker
    Given a token value "ghp_live_value"
    When it is rendered through the clifacet seam
    Then the rendered value equals "[redacted]"

  Scenario: A fine-grained token never appears in rendered output
    Given a token value "github_pat_11ABC"
    When it is rendered through the clifacet seam
    Then the rendered value does not contain the token
