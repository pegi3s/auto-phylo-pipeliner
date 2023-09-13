from behave import *
from behave.fixture import use_fixture_by_tag
from behave.runner import Context
from hamcrest import assert_that, equal_to_ignoring_whitespace

from auto_phylo.gui.io.ConfigurationGenerator import ConfigurationGenerator
from auto_phylo.gui.io.PipelineGenerator import PipelineGenerator
from features.fixtures.pipelines import get_pipeline_registry


@given(u"a {pipeline_id} configuration")
def step_impl(context: Context, pipeline_id: str) -> None:
    use_fixture_by_tag(f"fixture.pipeline.{pipeline_id}", context, get_pipeline_registry())


@when(u"we generate a configuration text for {seda} in {output_dir}")
def step_impl(context: Context, seda: str, output_dir: str) -> None:
    config_generator = ConfigurationGenerator()

    context.seda = seda
    context.output_dir = output_dir
    context.generated_config = config_generator.generate(seda, output_dir, context.pipeline)


@when(u"we generate a pipeline text")
def step_impl(context: Context) -> None:
    pipeline_generator = PipelineGenerator()

    context.generated_pipeline = pipeline_generator.generate(context.pipeline)


@then(u"we have a valid {config_text_id} configuration")
def step_impl(context: Context, config_text_id: str) -> None:
    registry = get_pipeline_registry(seda=context.seda, output_dir=context.output_dir)
    use_fixture_by_tag(f"fixture.config.text.{config_text_id}", context, registry)

    assert_that(context.generated_config, equal_to_ignoring_whitespace(context.config_text))


@then(u"we have a valid {pipeline_text_id} pipeline")
def step_impl(context: Context, pipeline_text_id: str) -> None:
    use_fixture_by_tag(f"fixture.pipeline.text.{pipeline_text_id}", context, get_pipeline_registry())

    assert_that(context.generated_pipeline, equal_to_ignoring_whitespace(context.pipeline_text))
