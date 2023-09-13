from behave import *
from behave.fixture import use_fixture_by_tag
from hamcrest import assert_that, equal_to_ignoring_whitespace

from auto_phylo.gui.io.ConfigurationGenerator import ConfigurationGenerator
from features.fixtures.pipelines import get_pipeline_registry


@given("a {pipeline} configuration with parameters")
def step_impl(context, pipeline):
    use_fixture_by_tag(f"fixture.pipeline.{pipeline}", context, get_pipeline_registry())


@when("we generate a configuration file for {seda} in {output_dir}")
def step_impl(context, seda, output_dir):
    generator = ConfigurationGenerator()

    context.seda = seda
    context.output_dir = output_dir
    context.config_text = generator.generate(seda, output_dir, context.pipeline)


@then("we have a valid {config_file} configuration text")
def step_impl(context, config_file):
    registry = get_pipeline_registry(seda=context.seda, output_dir=context.output_dir)
    use_fixture_by_tag(f"fixture.config.file.{config_file}", context, registry)

    assert_that(context.config_text, equal_to_ignoring_whitespace(context.config_file))
