from copy import deepcopy
from typing import List, Iterable, Iterator, Sized

from auto_phylo.pipeliner.model.Command import Command


class CommandsIterator(Iterator[Command]):
    def __init__(self, commands: "Commands"):
        self._commands: Commands = commands
        self._index: int = 0

    def __next__(self) -> Command:
        if self._index == len(self._commands.commands):
            raise StopIteration
        else:
            item = self._commands.commands[self._index]
            self._index += 1

            return item


class Commands(Iterable[Command], Sized):
    def __init__(self, version: str, commands: Iterable[Command]):
        self._version: str = version
        self._commands: List[Command] = list(commands)

    @property
    def version(self) -> str:
        return self._version

    @property
    def commands(self) -> List[Command]:
        return self._commands.copy()

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

    def __iter__(self) -> Iterator[Command]:
        return CommandsIterator(self)

    def __len__(self) -> int:
        return len(self._commands)

    def __copy__(self) -> "Commands":
        return Commands(self._version, self._commands)

    def __deepcopy__(self, memodict={}) -> "Commands":
        return Commands(self._version, deepcopy(self._commands))
