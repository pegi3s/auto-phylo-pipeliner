from typing import List

from auto_phylo.gui.model.Pipeline import Pipeline
from matchers.EntityMatcher import EntityMatcher
from tests.matchers.CommandMatcher import CommandMatcher


class PipelineMatcher(EntityMatcher[Pipeline]):
    def __init__(self, pipeline: Pipeline):
        super().__init__(pipeline)
        self._pipeline: Pipeline = pipeline
        self._matcher: List[CommandMatcher] = [CommandMatcher(command) for command in pipeline]

    def _match_entity(self, actual_entity: Pipeline) -> None:
        self._expect_that(actual_entity) \
            .has_same_list("commands", CommandMatcher)


def equals_to_pipeline(pipeline: Pipeline) -> "PipelineMatcher":
    return PipelineMatcher(pipeline)
