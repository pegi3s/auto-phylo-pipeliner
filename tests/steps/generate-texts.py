from behave import *
from behave.fixture import use_fixture_by_tag
from behave.runner import Context
from hamcrest import assert_that, equal_to_ignoring_whitespace

from auto_phylo.gui.io.ConfigurationGenerator import ConfigurationGenerator
from auto_phylo.gui.io.PipelineGenerator import PipelineGenerator
from tests.fixtures.pipelines import fixture_pipelines


@given(u"a {pipeline_id} pipeline configuration")
def step_impl(context: Context, pipeline_id: str) -> None:
    use_fixture_by_tag(f"fixture.pipeline.{pipeline_id}.configured", context, fixture_pipelines)


@when(u"we generate a configuration text")
def step_impl(context: Context) -> None:
    config_generator = ConfigurationGenerator()

    context.generated_config = config_generator.generate(context.pipeline_config)


@when(u"we generate a pipeline text")
def step_impl(context: Context) -> None:
    pipeline_generator = PipelineGenerator()

    context.generated_pipeline = pipeline_generator.generate(context.pipeline_config)


@then(u"we have a valid {pipeline_id} configuration text")
def step_impl(context: Context, pipeline_id: str) -> None:
    use_fixture_by_tag(f"fixture.config.text.{pipeline_id}", context, fixture_pipelines)

    assert_that(context.generated_config, equal_to_ignoring_whitespace(context.config_text))


@then(u"we have a valid {pipeline_id} pipeline text")
def step_impl(context: Context, pipeline_id: str) -> None:
    use_fixture_by_tag(f"fixture.pipeline.text.{pipeline_id}", context, fixture_pipelines)

    assert_that(context.generated_pipeline, equal_to_ignoring_whitespace(context.pipeline_text))
