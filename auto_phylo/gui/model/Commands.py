from typing import List, Iterable

from auto_phylo.gui.model.Command import Command


class Commands:
    def __init__(self, commands: Iterable[Command]):
        self._commands: List[Command] = list(commands)

    def list_names(self) -> List[str]:
        return [command.name for command in self._commands]

    def find_by_tool(self, tool: str) -> Command:
        command = next(filter(lambda cmd: cmd.tool == tool, self._commands), None)

        if command is None:
            raise LookupError("command not found")

        return command

    def find_by_name(self, name: str) -> Command:
        command = next(filter(lambda cmd: cmd.name == name, self._commands), None)

        if command is None:
            raise LookupError("command not found")

        return command
