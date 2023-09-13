from behave import *
from behave.fixture import use_fixture_by_tag
from hamcrest import assert_that, equal_to_ignoring_whitespace

from auto_phylo.gui.io.PipelineGenerator import PipelineGenerator
from features.fixtures.pipelines import get_pipeline_registry


@given("a {pipeline} configuration")
def step_impl(context, pipeline):
    use_fixture_by_tag(f"fixture.pipeline.{pipeline}", context, get_pipeline_registry())


@when("we generate a pipeline file")
def step_impl(context):
    generator = PipelineGenerator()

    context.pipeline_text = generator.generate(context.pipeline)


@then("we have a valid {pipeline_file} pipeline text")
def step_impl(context, pipeline_file):
    use_fixture_by_tag(f"fixture.pipeline.file.{pipeline_file}", context, get_pipeline_registry())

    assert_that(context.pipeline_text, equal_to_ignoring_whitespace(context.pipeline_file))
