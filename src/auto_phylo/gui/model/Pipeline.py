from copy import deepcopy
from typing import List, Optional, Iterable, Iterator, Sized

from auto_phylo.gui.model.Command import Command
from auto_phylo.gui.util.Observable import Observable


class PipelineIterator(Iterator[Command]):
    def __init__(self, pipeline: "Pipeline"):
        self._pipeline: Pipeline = pipeline
        self._index: int = 0

    def __next__(self) -> Command:
        if self._index == len(self._pipeline.commands):
            raise StopIteration
        else:
            item = self._pipeline.commands[self._index]
            self._index += 1

            return item


class Pipeline(Observable, Iterable[Command], Sized):
    def __init__(self, commands: Optional[List[Command]] = None):
        super().__init__()
        self._commands: List[Command] = [] if commands is None else commands.copy()

    @property
    def commands(self) -> List[Command]:
        return self._commands.copy()

    def add_command(self, command: Command) -> None:
        self._commands.append(command)
        self._notify_observers()

    def remove_command(self, index: int) -> None:
        self._commands.pop(index)
        self._notify_observers()

    def get_command_indexes(self, command: Command) -> List[int]:
        return [index for index, value in enumerate(self._commands) if value == command]

    def find_command_with_param(self, param: str) -> Command:
        try:
            return next(command for command in self._commands if command.has_param(param))
        except StopIteration:
            raise ValueError(f"Unknown parameter {param}")

    def __len__(self) -> int:
        return len(self._commands)

    def __iter__(self) -> Iterator[Command]:
        return PipelineIterator(self)

    def __copy__(self) -> "Pipeline":
        return Pipeline(self._commands)

    def __deepcopy__(self, memodict={}) -> "Pipeline":
        return Pipeline(deepcopy(self._commands))
