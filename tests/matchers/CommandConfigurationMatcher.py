from auto_phylo.pipeliner.model.CommandConfiguration import CommandConfiguration
from matchers.EntityMatcher import EntityMatcher
from tests.matchers.CommandMatcher import CommandMatcher


class CommandConfigurationMatcher(EntityMatcher[CommandConfiguration]):
    def __init__(self, command_config: CommandConfiguration):
        super().__init__(command_config)

    def _match_entity(self, actual_entity: CommandConfiguration) -> None:
        self._expect_that(actual_entity) \
            .has_same("command", CommandMatcher) \
            .and_has_same("input_dir") \
            .and_has_same("output_dir") \
            .and_is_true(lambda e, a: e.is_special_supported() == a.is_special_supported()
                 and (not e.is_special_supported() or e.special == a.special),
                 f"Different special support or value"
            ) \
            .and_has_same_dict("param_values")


def equal_to_command_config(command_config: CommandConfiguration) -> "CommandConfigurationMatcher":
    return CommandConfigurationMatcher(command_config)
