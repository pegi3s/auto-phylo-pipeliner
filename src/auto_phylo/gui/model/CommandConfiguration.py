from copy import deepcopy
from typing import Optional, Dict, List

from auto_phylo.gui.model.Command import Command
from auto_phylo.gui.model.SpecialNotSupportedError import SpecialNotSupportedError
from auto_phylo.gui.util.Observable import Observable


class CommandConfiguration(Observable):
    def __init__(self, command: Command,
                 input_dir: Optional[str] = None,
                 output_dir: Optional[str] = None,
                 special: Optional[int] = None,
                 param_values: Optional[Dict[str, str]] = None):
        super().__init__()
        self._command: Command = command
        self._input_dir: Optional[str] = input_dir
        self._output_dir: Optional[str] = output_dir
        self._special: Optional[int] = special
        self._param_values: Dict[str, str] = {} if param_values is None else param_values.copy()

    @property
    def command(self) -> Command:
        return self._command

    @property
    def input_dir(self) -> Optional[str]:
        return self._input_dir

    @input_dir.setter
    def input_dir(self, input_dir: str) -> None:
        if self._input_dir != input_dir:
            self._input_dir = input_dir
            self._notify_observers()

    def has_input_dir(self) -> bool:
        return self._input_dir is not None

    @property
    def output_dir(self) -> Optional[str]:
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_dir: str) -> None:
        if self._output_dir != output_dir:
            self._output_dir = output_dir
            self._notify_observers()

    def has_output_dir(self) -> bool:
        return self._output_dir is not None

    @property
    def special(self) -> Optional[int]:
        if not self.command.supports_special:
            raise SpecialNotSupportedError(self._command)

        return self._special

    @special.setter
    def special(self, special: int) -> None:
        if not self.command.supports_special:
            raise SpecialNotSupportedError(self._command)

        if self._special != special:
            self._special = special
            self._notify_observers()

    def is_special_supported(self) -> bool:
        return self._command.supports_special

    def has_special(self) -> bool:
        return self._special is not None

    def remove_special(self) -> None:
        if not self.command.supports_special:
            raise SpecialNotSupportedError(self._command)

        self._special = None

    @property
    def param_values(self) -> Dict[str, str]:
        return self._param_values.copy()

    def has_param(self, param: str) -> bool:
        return self._command.has_param(param)

    def list_param(self) -> List[str]:
        return self._command.list_params()

    def get_param_value(self, param: str) -> str:
        return self._param_values[param]

    def set_param_value(self, param: str, value: str) -> None:
        if not self._command.has_param(param):
            raise ValueError(f"{param} is not a valid param")

        self._param_values[param] = value

    def remove_param_value(self, param: str) -> None:
        if not self._command.has_param(param):
            raise ValueError(f"{param} is not a valid param")

        del self._param_values[param]

    def has_param_values(self):
        return len(self._param_values) > 0

    def __copy__(self) -> "CommandConfiguration":
        return CommandConfiguration(
            self._command,
            self._input_dir,
            self._output_dir,
            self._special,
            self._param_values
        )

    def __deepcopy__(self, memodict={}) -> "CommandConfiguration":
        return CommandConfiguration(
            self._command,
            self._input_dir,
            self._output_dir,
            self._special,
            deepcopy(self._param_values)
        )
