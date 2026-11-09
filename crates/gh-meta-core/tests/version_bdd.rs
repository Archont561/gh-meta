use gh_meta_core::{VERSION, format_version_banner};
use rstest::fixture;
use rstest_bdd_macros::{given, scenario, then, when};

#[derive(Default)]
struct CoreWorld {
    crate_name: String,
    tool_name: String,
    observed: String,
}

#[fixture]
fn world() -> CoreWorld {
    CoreWorld::default()
}

#[given("the \"{crate_name}\" crate metadata version")]
fn given_crate_metadata(world: &mut CoreWorld, crate_name: String) {
    assert_eq!(crate_name, env!("CARGO_PKG_NAME"));
    world.crate_name = crate_name;
}

#[given("the tool name \"{tool_name}\"")]
fn given_tool_name(world: &mut CoreWorld, tool_name: String) {
    world.tool_name = tool_name;
}

#[when("a caller reads the core VERSION constant")]
fn read_version(world: &mut CoreWorld) {
    assert_eq!(world.crate_name, env!("CARGO_PKG_NAME"));
    VERSION.clone_into(&mut world.observed);
}

#[when("a caller formats the version banner")]
fn format_banner(world: &mut CoreWorld) {
    world.observed = format_version_banner(&world.tool_name);
}

#[then("the constant equals \"{expected}\"")]
fn check_constant(world: &CoreWorld, expected: String) {
    assert_eq!(world.observed, expected);
}

#[then("the banner equals \"{expected}\"")]
fn check_banner(world: &CoreWorld, expected: String) {
    assert_eq!(world.observed, expected);
}

#[scenario(
    path = "features/core_version.feature",
    name = "Core version matches the crate manifest"
)]
fn expose_version_matches_metadata(world: CoreWorld) {
    let _ = world;
}

#[scenario(
    path = "features/core_version.feature",
    name = "Banner includes the package name and version"
)]
fn format_banner_with_core_version(world: CoreWorld) {
    let _ = world;
}
