//! Core library crate for `gh-repoconf`.
//!
//! At this initial scaffold stage, the crate exposes only the package version
//! read from Cargo manifest metadata and deterministic banner formatting for
//! the standalone CLI.

/// Crate version read from `CARGO_PKG_VERSION` at compile time.
///
/// ```
/// assert!(!gh_repoconf_core::VERSION.is_empty());
/// ```
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Format the version banner printed by the `gh-repoconf` CLI.
///
/// ```
/// let banner = gh_repoconf_core::format_version_banner("gh-repoconf");
/// assert_eq!(banner, format!("gh-repoconf {}", gh_repoconf_core::VERSION));
/// ```
#[must_use]
pub fn format_version_banner(binary: &str) -> String {
    format!("{binary} {VERSION}")
}
