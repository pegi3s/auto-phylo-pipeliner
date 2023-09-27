from matchers.EntityMatcher import EntityMatcher
from auto_phylo.gui.model.Command import Command


class CommandMatcher(EntityMatcher[Command]):
    def __init__(self, command: Command):
        super().__init__(command)

    def _match_entity(self, actual_entity: Command) -> None:
        self._expect_that(actual_entity) \
            .has_same("name") \
            .and_has_same("url") \
            .and_has_same("supports_special") \
            .and_has_same_dict("params")


def equals_to_command(command: Command) -> "CommandMatcher":
    return CommandMatcher(command)
