use assert_cmd::cargo::cargo_bin_cmd;
use rstest::fixture;
use rstest_bdd_macros::{given, scenario, then, when};

#[derive(Default)]
struct CliWorld {
    binary: String,
    arg: String,
    status: Option<i32>,
    stdout: String,
    stderr: String,
    token: String,
    rendered: String,
}

#[fixture]
fn world() -> CliWorld {
    CliWorld::default()
}

#[given("the \"{binary}\" command with \"{arg}\"")]
fn given_command_with_arg(world: &mut CliWorld, binary: String, arg: String) {
    world.binary = binary;
    world.arg = arg;
}

#[when("it runs")]
fn run_command(world: &mut CliWorld) {
    assert_eq!(world.binary, "gh-meta");
    let output = cargo_bin_cmd!("gh-meta")
        .arg(&world.arg)
        .output()
        .expect("compiled gh-meta binary should execute");
    world.status = output.status.code();
    world.stdout = String::from_utf8(output.stdout).expect("stdout must be UTF-8");
    world.stderr = String::from_utf8(output.stderr).expect("stderr must be UTF-8");
}

#[then("it exits with code {code:i32}")]
fn check_exit_code(world: &CliWorld, code: i32) {
    assert_eq!(world.status, Some(code));
}

#[then("standard output mentions \"{expected}\"")]
fn check_stdout_contains(world: &CliWorld, expected: String) {
    assert!(
        world.stdout.contains(&expected),
        "expected stdout to contain {expected:?}, got {:?}",
        world.stdout
    );
}

#[then("trimmed standard output equals \"{expected}\"")]
fn check_stdout_trimmed(world: &CliWorld, expected: String) {
    assert_eq!(world.stdout.trim(), expected);
}

#[then("standard error is empty")]
fn check_stderr_empty(world: &CliWorld) {
    assert_eq!(world.stderr, "");
}

#[then("standard error mentions \"{expected}\"")]
fn check_stderr_contains(world: &CliWorld, expected: String) {
    assert!(
        world.stderr.contains(&expected),
        "expected stderr to contain {expected:?}, got {:?}",
        world.stderr
    );
}

#[scenario(path = "features/cli_version.feature", name = "Display help via flag")]
fn display_help_flag(world: CliWorld) {
    let _ = world;
}

#[scenario(
    path = "features/cli_version.feature",
    name = "Print version via long flag"
)]
fn print_version_long_flag(world: CliWorld) {
    let _ = world;
}

#[scenario(
    path = "features/cli_version.feature",
    name = "Print version via short flag"
)]
fn print_version_short_flag(world: CliWorld) {
    let _ = world;
}

#[scenario(
    path = "features/cli_version.feature",
    name = "Print version via subcommand"
)]
fn print_version_subcommand(world: CliWorld) {
    let _ = world;
}

#[scenario(path = "features/cli_version.feature", name = "Reject unknown flag")]
fn reject_unknown_flag(world: CliWorld) {
    let _ = world;
}

#[given("a token value \"{token}\"")]
fn given_token_value(world: &mut CliWorld, token: String) {
    world.token = token;
}

#[when("it is rendered through the clifacet seam")]
fn render_through_seam(world: &mut CliWorld) {
    world.rendered = gh_meta::redacted(world.token.clone());
}

#[then("the rendered value equals \"{expected}\"")]
fn check_rendered_equals(world: &CliWorld, expected: String) {
    assert_eq!(world.rendered, expected);
}

#[then("the rendered value does not contain the token")]
fn check_rendered_hides_token(world: &CliWorld) {
    assert!(
        !world.rendered.contains(&world.token),
        "expected the rendered value to hide {:?}, got {:?}",
        world.token,
        world.rendered
    );
}

#[scenario(
    path = "features/cli_secret.feature",
    name = "A classic token renders as the redaction marker"
)]
fn token_renders_as_marker(world: CliWorld) {
    let _ = world;
}

#[scenario(
    path = "features/cli_secret.feature",
    name = "A fine-grained token never appears in rendered output"
)]
fn token_never_appears(world: CliWorld) {
    let _ = world;
}
