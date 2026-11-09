//! Core library crate for `gh-meta`.
//!
//! At this initial scaffold stage, the crate exposes only the package version
//! read from Cargo manifest metadata and deterministic banner formatting for
//! the standalone CLI.

/// Crate version read from `CARGO_PKG_VERSION` at compile time.
///
/// ```
/// assert!(!gh_meta_core::VERSION.is_empty());
/// ```
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Format the version banner printed by the `gh-meta` CLI.
///
/// ```
/// let banner = gh_meta_core::format_version_banner("gh-meta");
/// assert_eq!(banner, format!("gh-meta {}", gh_meta_core::VERSION));
/// ```
#[must_use]
pub fn format_version_banner(binary: &str) -> String {
    format!("{binary} {VERSION}")
}
