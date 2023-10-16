from pathlib import Path
from typing import Callable, Dict, Any, Optional

from behave import fixture
from behave.runner import Context

from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration
from fixtures.pipelines import basic_configured_pipeline, advanced_configured_pipeline


@fixture(name="fixture.run.basic.semver.text")
def run_basic_semver_text(context: Optional[Context] = None) -> str:
    run = _build_file(basic_configured_pipeline(), run_basic_semver_version())

    if context is not None:
        context.run_text = run

    return run


@fixture(name="fixture.run.basic.semver.version")
def run_basic_semver_version(context: Optional[Context] = None) -> str:
    if context is not None:
        context.run_version = "1.0.0"

    return "1.0.0"


@fixture(name="fixture.run.basic.latest.text")
def run_basic_latest_text(context: Optional[Context] = None) -> str:
    run = _build_file(basic_configured_pipeline(), run_basic_latest_version())

    if context is not None:
        context.run_text = run

    return run


@fixture(name="fixture.run.basic.latest.version")
def run_basic_latest_version(context: Optional[Context] = None) -> str:
    if context is not None:
        context.run_version = "latest"

    return "latest"


@fixture(name="fixture.run.advanced.semver.text")
def run_advanced_semver_text(context: Optional[Context] = None) -> str:
    run = _build_file(advanced_configured_pipeline(), run_advanced_semver_version())

    if context is not None:
        context.run_text = run

    return run


@fixture(name="fixture.run.advanced.semver.version")
def run_advanced_semver_version(context: Optional[Context] = None) -> str:
    if context is not None:
        context.run_version = "1.0.0"

    return "1.0.0"


@fixture(name="fixture.run.advanced.latest.text")
def run_advanced_latest_text(context: Optional[Context] = None) -> str:
    run = _build_file(advanced_configured_pipeline(), run_advanced_latest_version())

    if context is not None:
        context.run_text = run

    return run


@fixture(name="fixture.run.advanced.latest.version")
def run_advanced_latest_version(context: Optional[Context] = None) -> str:
    if context is not None:
        context.run_version = "latest"

    return "latest"


def _build_file(pipeline: PipelineConfiguration, version: str) -> str:
    path = Path(pipeline.output_dir).absolute()

    return f"""
        #!/bin/bash

        docker run --rm -v "{path}":/data -v /var/run/docker.sock:/var/run/docker.sock pegi3s/auto-phylo:{version}
    """.strip()


fixture_runs: Dict[str, Callable[[], Any]] = {
    "fixture.run.basic.semver.text": run_basic_semver_text,
    "fixture.run.basic.semver.version": run_basic_semver_version,
    "fixture.run.basic.latest.text": run_basic_latest_text,
    "fixture.run.basic.latest.version": run_basic_latest_version,
    "fixture.run.advanced.semver.text": run_advanced_semver_text,
    "fixture.run.advanced.semver.version": run_advanced_semver_version,
    "fixture.run.advanced.latest.text": run_advanced_latest_text,
    "fixture.run.advanced.latest.version": run_advanced_latest_version
}
