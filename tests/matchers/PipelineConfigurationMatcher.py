from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration
from matchers.EntityMatcher import EntityMatcher
from tests.matchers.CommandConfigurationMatcher import CommandConfigurationMatcher
from tests.matchers.PipelineMatcher import PipelineMatcher


class PipelineConfigurationMatcher(EntityMatcher[PipelineConfiguration]):
    def __init__(self, pipeline_config: PipelineConfiguration):
        super().__init__(pipeline_config)

    def _match_entity(self, actual_entity: PipelineConfiguration) -> None:
        self._expect_that(actual_entity) \
            .has_same("seda_version") \
            .and_has_same("output_dir") \
            .and_has_same("pipeline", PipelineMatcher) \
            .and_has_same_list("command_configs", CommandConfigurationMatcher)


def equal_to_pipeline_config(pipeline_config: PipelineConfiguration) -> "PipelineConfigurationMatcher":
    return PipelineConfigurationMatcher(pipeline_config)
