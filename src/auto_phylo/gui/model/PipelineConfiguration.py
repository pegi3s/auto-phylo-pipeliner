from typing import List, Optional

from auto_phylo.gui.model.Command import Command
from auto_phylo.gui.model.CommandConfiguration import CommandConfiguration
from auto_phylo.gui.model.Pipeline import Pipeline
from auto_phylo.gui.util.Observable import Observable


class PipelineConfiguration(Observable):
    def __init__(self, pipeline: Pipeline, configurations: Optional[List[CommandConfiguration]] = None):
        super().__init__()
        self._pipeline: Pipeline = pipeline
        self._command_configs: List[CommandConfiguration] = [] if configurations is None else configurations.copy()

    @property
    def pipeline(self) -> Pipeline:
        return self._pipeline

    def add_command_configuration(self, command_config: CommandConfiguration) -> None:
        self._command_configs.append(command_config)
        self._notify_observers()

    def remove_command_configuration(self, command_config: CommandConfiguration) -> None:
        self._command_configs.remove(command_config)
        self._notify_observers()

    def get_command_configuration(self, command: Command) -> CommandConfiguration:
        return next(config for config in self._command_configs if config.command == command)
