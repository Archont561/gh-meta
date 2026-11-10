//! Standalone CLI entrypoint library for `gh-repoconf`.
//!
//! At this scaffold stage, the CLI supports version and help queries backed by
//! `gh-repoconf-core`, plus the `clifacet` command seam that later interactive
//! workflows build on (decision-2). No frontend feature is enabled yet.

use std::ffi::OsString;

use clap::error::ErrorKind;
use clap::{Arg, ArgAction, Command};

/// Crate version read from `CARGO_PKG_VERSION` at compile time.
///
/// ```
/// assert_eq!(gh_repoconf::VERSION, gh_repoconf_core::VERSION);
/// ```
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Outcome returned by invoking the CLI parser and dispatcher.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CliOutcome {
    /// Process exit code (`0` for success, `2` for usage errors).
    pub exit_code: u8,
    /// Content written to standard output.
    pub stdout: String,
    /// Content written to standard error.
    pub stderr: String,
}

/// Render `value` the way `clifacet` renders a secret, for anywhere output is built.
///
/// Later commands take credentials (a GitHub token) as command input. `clifacet`'s
/// `Secret` redacts itself in both `Display` and `Debug`, so routing a value through
/// this function is what keeps it out of rendered output and test failure messages.
///
/// ```
/// let token = gh_repoconf::redacted("ghp_live_value");
/// assert_eq!(token, "[redacted]");
/// assert!(!token.contains("ghp_live_value"));
/// ```
#[must_use]
pub fn redacted(value: &str) -> String {
    clifacet::secret::Secret::new(value.to_owned()).to_string()
}

fn build_cli() -> Command {
    Command::new("gh-repoconf")
        .about("Your .github/ directory, managed as code.")
        .version(VERSION)
        .disable_version_flag(true)
        .arg(
            Arg::new("version")
                .short('V')
                .long("version")
                .action(ArgAction::SetTrue)
                .help("Print version information"),
        )
        .subcommand(Command::new("version").about("Print version information"))
}

/// Parse arguments and produce the CLI stdout, stderr, and exit code without exiting the process.
///
/// ```
/// let outcome = gh_repoconf::run(["gh-repoconf", "--version"]);
/// assert_eq!(outcome.exit_code, 0);
/// assert_eq!(outcome.stdout.trim(), format!("gh-repoconf {}", gh_repoconf::VERSION));
/// ```
#[must_use]
pub fn run<I, T>(args: I) -> CliOutcome
where
    I: IntoIterator<Item = T>,
    T: Into<OsString> + Clone,
{
    let mut cmd = build_cli();
    match cmd.try_get_matches_from_mut(args) {
        Ok(matches) => {
            if matches.get_flag("version") || matches.subcommand_name() == Some("version") {
                return CliOutcome {
                    exit_code: 0,
                    stdout: format!(
                        "{}\n",
                        gh_repoconf_core::format_version_banner("gh-repoconf")
                    ),
                    stderr: String::new(),
                };
            }
            CliOutcome {
                exit_code: 0,
                stdout: cmd.render_help().to_string(),
                stderr: String::new(),
            }
        }
        Err(error) => {
            let exit_code = match error.kind() {
                ErrorKind::DisplayHelp | ErrorKind::DisplayVersion => 0,
                _ => 2,
            };
            let rendered = error.render().to_string();
            if exit_code == 0 {
                CliOutcome {
                    exit_code: 0,
                    stdout: rendered,
                    stderr: String::new(),
                }
            } else {
                CliOutcome {
                    exit_code,
                    stdout: String::new(),
                    stderr: rendered,
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{VERSION, redacted, run};

    #[test]
    fn version_matches_core_crate() {
        assert_eq!(VERSION, gh_repoconf_core::VERSION);
    }

    #[test]
    fn bare_invocation_renders_help_cleanly() {
        let outcome = run(["gh-repoconf"]);
        assert_eq!(outcome.exit_code, 0);
        assert!(outcome.stdout.contains("Usage: gh-repoconf"));
        assert_eq!(outcome.stderr, "");
    }

    #[test]
    fn help_flag_exits_zero() {
        let outcome = run(["gh-repoconf", "--help"]);
        assert_eq!(outcome.exit_code, 0);
        assert!(outcome.stdout.contains("Usage: gh-repoconf"));
    }

    #[test]
    fn version_subcommand_matches_flag() {
        let sub = run(["gh-repoconf", "version"]);
        let flag = run(["gh-repoconf", "--version"]);
        assert_eq!(sub, flag);
    }

    #[test]
    fn credentials_never_reach_rendered_output() {
        let rendered = redacted("ghp_live_value");
        assert_eq!(rendered, clifacet::secret::REDACTED);
        assert!(!rendered.contains("ghp_live_value"));
    }

    #[test]
    fn unknown_flag_exits_two_on_stderr() {
        let outcome = run(["gh-repoconf", "--not-a-flag"]);
        assert_eq!(outcome.exit_code, 2);
        assert_eq!(outcome.stdout, "");
        assert_ne!(outcome.stderr, "");
    }
}
