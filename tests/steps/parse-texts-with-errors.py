from io import StringIO

from behave import *
from behave.fixture import use_fixture_by_tag
from behave.runner import Context
from hamcrest.core import assert_that

from auto_phylo.gui.io.ConfigurationParser import ConfigurationParser
from auto_phylo.gui.io.ParseError import ParseError
from auto_phylo.gui.io.PipelineParser import PipelineParser
from fixtures.pipeline_errors import fixture_pipeline_errors
from fixtures.pipelines import fixture_pipelines
from tests.matchers.ParseErrorGeneralErrorsMatcher import has_general_errors, does_not_have_any_general_error
from tests.matchers.ParseErrorLinesMatcher import has_errors_in_lines, does_not_have_any_line_error


@given(u"a pipeline configuration text with a {pipeline_error_id} error")
def step_impl(context: Context, pipeline_error_id: str) -> None:
    use_fixture_by_tag(f"fixture.pipeline.text.error.{pipeline_error_id}", context, fixture_pipeline_errors)
    use_fixture_by_tag(f"fixture.pipeline.text.error.{pipeline_error_id}.lines", context, fixture_pipeline_errors)


@when(u"we parse this bad pipeline configuration text")
def step_impl(context: Context) -> None:
    parser = PipelineParser()

    try:
        parser.parse(StringIO(context.pipeline_text))
    except ParseError as pe:
        context.parse_error = pe


@then(u"we have all the existent errors identified in the pipeline configuration")
def step_impl(context: Context) -> None:
    assert_that(context.parse_error, has_errors_in_lines(context.line_errors))


@given(u"a configuration text with a {config_error_id} error")
def step_impl(context: Context, config_error_id: str) -> None:
    use_fixture_by_tag(f"fixture.pipeline.advanced", context, fixture_pipelines)
    use_fixture_by_tag(f"fixture.config.text.error.{config_error_id}", context, fixture_pipeline_errors)
    use_fixture_by_tag(f"fixture.config.text.error.{config_error_id}.lines", context, fixture_pipeline_errors)
    use_fixture_by_tag(f"fixture.config.text.error.{config_error_id}.general", context, fixture_pipeline_errors)


@when(u"we parse this bad configuration text")
def step_impl(context: Context) -> None:
    parser = ConfigurationParser()

    try:
        parser.parse(StringIO(context.config_text), context.pipeline)
    except ParseError as pe:
        context.parse_error = pe


@then(u"we have all the existent errors identified in the configuration")
def step_impl(context: Context) -> None:
    if context.line_errors is None:
        assert_that(context.parse_error, does_not_have_any_line_error())
    else:
        assert_that(context.parse_error, has_errors_in_lines(context.line_errors))

    if context.general_errors is None:
        assert_that(context.parse_error, does_not_have_any_general_error())
    else:
        assert_that(context.parse_error, has_general_errors(context.general_errors))
