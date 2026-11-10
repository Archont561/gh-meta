# gh-meta

Standalone CLI and GitHub CLI (`gh`) extension binary crate for
[`gh-meta`](https://github.com/Archont561/gh-meta) — *Your `.github/`
directory, managed as code.*

At this stage the binary is an intentional scaffold exposing `gh-meta
--version`, `-V`, `gh-meta version`, and `--help` before the full interactive
and command workflows are added.

It already depends on [`clifacet`](https://github.com/Archont561/clifacet) 0.5.0
with no frontend features enabled, so credentials route through
`clifacet::secret::Secret` and render as `[redacted]` wherever the CLI builds
output.

## License

Licensed under the [MIT License](LICENSE).
