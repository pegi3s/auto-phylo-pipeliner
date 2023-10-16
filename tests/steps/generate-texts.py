from behave import *
from behave.fixture import use_fixture_by_tag
from behave.runner import Context
from hamcrest import assert_that, equal_to_ignoring_whitespace, is_

from auto_phylo.pipeliner.io.ConfigurationGenerator import ConfigurationGenerator
from auto_phylo.pipeliner.io.PipelineGenerator import PipelineGenerator
from auto_phylo.pipeliner.io.RunFileGenerator import RunFileGenerator
from fixtures.run_files import fixture_runs
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

    assert_that(context.generated_config, is_(equal_to_ignoring_whitespace(context.config_text)))


@then(u"we have a valid {pipeline_id} pipeline text")
def step_impl(context: Context, pipeline_id: str) -> None:
    use_fixture_by_tag(f"fixture.pipeline.text.{pipeline_id}", context, fixture_pipelines)

    assert_that(context.generated_pipeline, is_(equal_to_ignoring_whitespace(context.pipeline_text)))


@given(u"a {pipeline_id} pipeline configuration and a {run_id} type of version")
def step_impl(context: Context, pipeline_id: str, run_id: str) -> None:
    context.pipeline_id = pipeline_id
    use_fixture_by_tag(f"fixture.run.{pipeline_id}.{run_id}.version", context, fixture_runs)
    use_fixture_by_tag(f"fixture.pipeline.{pipeline_id}.configured", context, fixture_pipelines)


@when(u"we generate a run text")
def step_impl(context: Context) -> None:
    run_file_generator = RunFileGenerator()

    context.generated_run = run_file_generator.generate(context.pipeline_config, context.run_version)


@then(u"we have a valid {run_id} run text")
def step_impl(context: Context, run_id: str) -> None:
    use_fixture_by_tag(f"fixture.run.{context.pipeline_id}.{run_id}.text", context, fixture_runs)

    assert_that(context.generated_run, is_(equal_to_ignoring_whitespace(context.run_text)))
