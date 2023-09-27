from copy import deepcopy
from typing import List, Optional, Iterable

from auto_phylo.gui.model.Command import Command
from auto_phylo.gui.model.CommandConfiguration import CommandConfiguration
from auto_phylo.gui.model.Pipeline import Pipeline
from auto_phylo.gui.util.Observable import Observable


class PipelineConfiguration(Observable):
    def __init__(self,
                 pipeline: Pipeline,
                 seda_version: Optional[str] = None,
                 output_dir: Optional[str] = None,
                 command_configs: Optional[List[CommandConfiguration]] = None):
        super().__init__()
        self._pipeline: Pipeline = pipeline
        self._seda_version: Optional[str] = seda_version
        self._output_dir: Optional[str] = output_dir
        self._command_configs: List[CommandConfiguration] = [] if command_configs is None else command_configs.copy()

    @property
    def pipeline(self) -> Pipeline:
        return self._pipeline

    @property
    def seda_version(self) -> Optional[str]:
        return self._seda_version

    @seda_version.setter
    def seda_version(self, seda_version: str) -> None:
        if self._seda_version != seda_version:
            self._seda_version = seda_version
            self._notify_observers()

    @property
    def output_dir(self) -> Optional[str]:
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_dir: str) -> None:
        if self._output_dir != output_dir:
            self._output_dir = output_dir
            self._notify_observers()

    @property
    def command_configs(self) -> List[CommandConfiguration]:
        return self._command_configs.copy()

    def add_command_configuration(self, command_config: CommandConfiguration) -> None:
        self._command_configs.append(command_config)
        self._notify_observers()

    def add_commands_configurations(self, command_configs: Iterable[CommandConfiguration]) -> None:
        for command_config in command_configs:
            self._command_configs.append(command_config)
        self._notify_observers()

    def remove_command_configuration(self, command_config: CommandConfiguration) -> None:
        self._command_configs.remove(command_config)
        self._notify_observers()

    def clear_command_configurations(self):
        self._command_configs.clear()

    def get_command_configuration(self, command: Command) -> CommandConfiguration:
        return next(config for config in self._command_configs if config.command == command)

    def has_command_configuration(self, command: Command) -> bool:
        return any(config for config in self._command_configs if config.command == command)

    def __copy__(self) -> "PipelineConfiguration":
        return PipelineConfiguration(
            self._pipeline,
            self._seda_version,
            self._output_dir,
            self._command_configs
        )

    def __deepcopy__(self, memodict={}) -> "PipelineConfiguration":
        return PipelineConfiguration(
            deepcopy(self._pipeline),
            self._seda_version,
            self._output_dir,
            deepcopy(self._command_configs)
        )
