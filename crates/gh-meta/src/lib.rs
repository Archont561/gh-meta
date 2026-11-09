//! Standalone CLI entrypoint library for `gh-meta`.
//!
//! At this initial scaffold stage, the CLI supports version and help queries
//! backed by `gh-meta-core`.

use std::ffi::OsString;

use clap::error::ErrorKind;
use clap::{Arg, ArgAction, Command};

/// Crate version read from `CARGO_PKG_VERSION` at compile time.
///
/// ```
/// assert_eq!(gh_meta::VERSION, gh_meta_core::VERSION);
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

fn build_cli() -> Command {
    Command::new("gh-meta")
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
/// let outcome = gh_meta::run(["gh-meta", "--version"]);
/// assert_eq!(outcome.exit_code, 0);
/// assert_eq!(outcome.stdout.trim(), format!("gh-meta {}", gh_meta::VERSION));
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
                    stdout: format!("{}\n", gh_meta_core::format_version_banner("gh-meta")),
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
    use super::{VERSION, run};

    #[test]
    fn version_matches_core_crate() {
        assert_eq!(VERSION, gh_meta_core::VERSION);
    }

    #[test]
    fn bare_invocation_renders_help_cleanly() {
        let outcome = run(["gh-meta"]);
        assert_eq!(outcome.exit_code, 0);
        assert!(outcome.stdout.contains("Usage: gh-meta"));
        assert_eq!(outcome.stderr, "");
    }

    #[test]
    fn help_flag_exits_zero() {
        let outcome = run(["gh-meta", "--help"]);
        assert_eq!(outcome.exit_code, 0);
        assert!(outcome.stdout.contains("Usage: gh-meta"));
    }

    #[test]
    fn version_subcommand_matches_flag() {
        let sub = run(["gh-meta", "version"]);
        let flag = run(["gh-meta", "--version"]);
        assert_eq!(sub, flag);
    }

    #[test]
    fn unknown_flag_exits_two_on_stderr() {
        let outcome = run(["gh-meta", "--not-a-flag"]);
        assert_eq!(outcome.exit_code, 2);
        assert_eq!(outcome.stdout, "");
        assert_ne!(outcome.stderr, "");
    }
}
