from copy import copy
from io import StringIO

from behave import *
from behave.fixture import use_fixture_by_tag
from behave.runner import Context
from hamcrest.core import assert_that
from hamcrest.core import is_

from auto_phylo.gui.io.ConfigurationParser import ConfigurationParser
from auto_phylo.gui.io.PipelineParser import PipelineParser
from fixtures.pipelines import fixture_pipelines
from tests.matchers.PipelineConfigurationMatcher import equals_to_pipeline_config


@given(u"a {pipeline_id} pipeline text")
def step_impl(context: Context, pipeline_id: str) -> None:
    use_fixture_by_tag(f"fixture.pipeline.{pipeline_id}", context, fixture_pipelines)
    use_fixture_by_tag(f"fixture.pipeline.text.{pipeline_id}", context, fixture_pipelines)


@when(u"we parse this pipeline text")
def step_impl(context: Context) -> None:
    parser = PipelineParser()
    context.parsed_pipeline = parser.parse(StringIO(context.pipeline_text))


@then(u"we have a valid pipeline")
def step_impl(context: Context) -> None:
    assert_that(context.parsed_pipeline, is_(equals_to_pipeline_config(context.pipeline)))


@given(u"a {pipeline_id} pipeline configuration text")
def step_impl(context: Context, pipeline_id: str) -> None:
    use_fixture_by_tag(f"fixture.pipeline.{pipeline_id}", context, fixture_pipelines)
    use_fixture_by_tag(f"fixture.pipeline.{pipeline_id}.configured", context, fixture_pipelines)
    use_fixture_by_tag(f"fixture.config.text.{pipeline_id}", context, fixture_pipelines)


@when(u"we parse this configuration text")
def step_impl(context: Context) -> None:
    parser = ConfigurationParser()
    context.parsed_pipeline = parser.parse(StringIO(context.config_text), copy(context.pipeline))


@then(u"we have a valid pipeline configuration")
def step_impl(context: Context) -> None:
    assert_that(context.parsed_pipeline, is_(equals_to_pipeline_config(context.pipeline_config)))
