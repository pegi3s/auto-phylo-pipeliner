from typing import Callable, Dict, Any, Optional, Tuple

from behave import fixture
from behave.runner import Context


@fixture(name="fixture.run.text.error.missing_version")
def run_file_missing_version(context: Optional[Context] = None) -> str:
    run_text = """
        #!/bin/bash

        # Missing docker run command
    """

    if context is not None:
        context.run_text = run_text.strip()

    return run_text


@fixture(name="fixture.run.text.error.missing_version.lines")
def run_file_missing_version_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = None

    return context.line_errors


@fixture(name="fixture.run.text.error.missing_version.general")
def run_file_missing_version_general(context: Context) -> Optional[Tuple[str, ...]]:
    context.general_errors = tuple(["Missing Auto-phylo version"])

    return context.general_errors


fixture_run_file_errors: Dict[str, Callable[[], Any]] = {
    # Run file text
    "fixture.run.text.error.missing_version": run_file_missing_version,

    # Run file lines
    "fixture.run.text.error.missing_version.general": run_file_missing_version_lines,

    # Run file general errors
    "fixture.run.text.error.missing_version.lines": run_file_missing_version_general,
}
