import webbrowser
from tkinter import Widget, StringVar, Event, BooleanVar
from tkinter.constants import NORMAL, DISABLED
from tkinter.ttk import Frame, OptionMenu, Entry, Spinbox, Button, Checkbutton
from typing import Optional, Dict, Any, List, Final, Tuple

from auto_phylo.gui import load_commands
from auto_phylo.gui.component.ParamConfigurationDialog import ParamConfigurationDialog
from auto_phylo.gui.model.Command import Command
from auto_phylo.gui.model.CommandConfiguration import CommandConfiguration
from auto_phylo.gui.model.CommandConfigurationEvent import CommandConfigurationEvent
from auto_phylo.gui.model.Commands import Commands
from auto_phylo.gui.model.Pipeline import Pipeline
from auto_phylo.gui.model.PipelineChangeEvent import PipelineChangeEvent
from auto_phylo.gui.model.PipelineChangeType import PipelineChangeType
from auto_phylo.gui.model.PipelineConfiguration import PipelineConfiguration
from auto_phylo.gui.model.PipelineConfigurationChangeEvent import PipelineConfigurationChangeEvent


class _CommandConfigFormMediator:
    def __init__(self, master: Frame,
                 index: int,
                 pipeline_config: PipelineConfiguration,
                 commands: Commands,
                 **kwargs):
        self._master: Frame = master
        self._index: int = index
        self._command_config: CommandConfiguration = pipeline_config.get_command_configuration(index)
        self._pipeline_config: PipelineConfiguration = pipeline_config
        self._commands: Commands = commands
        self._grid_kwargs: Dict[str, Any] = kwargs

        self._btn_up = Button(master, text="↑", width=2)
        self._btn_down = Button(master, text="↓", width=2)

        self._sv_om_commands = StringVar(master)
        self._om_commands = OptionMenu(master, self._sv_om_commands, *commands.list_names())

        self._e_input = Entry(master, width=10)
        self._e_output = Entry(master, width=10)

        self._bv_chk_special = BooleanVar(master)
        self._chk_special = Checkbutton(master, text="Special", variable=self._bv_chk_special)
        self._sb_special = Spinbox(master, from_=1, to=100, increment=1, width=3)

        self._btn_params = Button(master, text="Params")
        self._btn_info = Button(master, text="Info")
        self._btn_remove = Button(master, text="X", width=2)

        self._update_position()
        self._update_command()
        self._update_input_dir()
        self._update_output_dir()
        self._update_special()

        self._e_input.bind("<FocusOut>", self._on_input_change)
        self._e_output.bind("<FocusOut>", self._on_output_change)

        self._sv_om_commands.trace_add("write", self._on_command_change)
        self._chk_special.configure(command=self._on_special_activation_change)
        self._sb_special.configure(command=self._on_special_change)
        self._sb_special.bind("<FocusOut>", self._on_special_change)

        self._btn_down.configure(command=self._on_down_command)
        self._btn_up.configure(command=self._on_up_command)
        self._btn_params.configure(command=self._on_params_command)
        self._btn_info.configure(command=self._on_info_command)
        self._btn_remove.configure(command=self._on_remove_command)

        self._command_config.add_callback(self._on_command_config_change)
        self._pipeline_config.pipeline.add_callback(self._on_pipeline_change)

    def _locate_components(self):
        self._btn_up.grid(row=self._index, column=0, **self._grid_kwargs)
        self._btn_down.grid(row=self._index, column=1, sticky="nsew", **self._grid_kwargs)
        self._om_commands.grid(row=self._index, column=2, sticky="nsew", **self._grid_kwargs)
        self._e_input.grid(row=self._index, column=3, sticky="nsew", **self._grid_kwargs)
        self._e_output.grid(row=self._index, column=4, sticky="nsew", **self._grid_kwargs)
        self._chk_special.grid(row=self._index, column=5, sticky="nsew", **self._grid_kwargs)
        self._sb_special.grid(row=self._index, column=6, sticky="nsew", **self._grid_kwargs)
        self._btn_params.grid(row=self._index, column=7, sticky="nsew", **self._grid_kwargs)
        self._btn_info.grid(row=self._index, column=8, sticky="nsew", **self._grid_kwargs)
        self._btn_remove.grid(row=self._index, column=9, **self._grid_kwargs)

    def _remove_components(self):
        self._btn_up.destroy()
        self._btn_down.destroy()
        self._om_commands.destroy()
        self._e_input.destroy()
        self._e_output.destroy()
        self._chk_special.destroy()
        self._sb_special.destroy()
        self._btn_params.destroy()
        self._btn_info.destroy()
        self._btn_remove.destroy()

        self._command_config.remove_callback(self._on_command_config_change)
        self._pipeline_config.pipeline.remove_callback(self._on_pipeline_change)

    def _get_special_value(self) -> Optional[int]:
        try:
            return int(self._sb_special.get())
        except ValueError:
            return None

    def _on_command_config_change(self, _: CommandConfiguration, event: CommandConfigurationEvent) -> None:
        if event.attribute == CommandConfiguration.command.fget.__name__:  # type: ignore
            self._update_command()
        elif event.attribute == CommandConfiguration.input_dir.fget.__name__:  # type: ignore
            self._update_input_dir()
        elif event.attribute == CommandConfiguration.output_dir.fget.__name__:  # type: ignore
            self._update_output_dir()
        elif event.attribute == CommandConfiguration.special.fget.__name__:  # type: ignore
            self._update_special()

    def _on_pipeline_change(self, _: Pipeline, event: PipelineChangeEvent) -> None:
        if event.action == PipelineChangeType.ADD or event.action == PipelineChangeType.INSERT:
            if self._index >= event.index:
                self._index += 1
                self._update_position()
            else:
                self._update_arrows()
        elif event.action == PipelineChangeType.REMOVE:
            if self._index == event.index:
                self._remove_components()
            elif self._index > event.index:
                self._index -= 1
                self._update_position()
        elif event.action == PipelineChangeType.SWAP:
            if self._index == event.index_a:
                self._index = event.index_b  # type: ignore
                self._update_position()
            elif self._index == event.index_b:
                self._index = event.index_a
                self._update_position()

    def _on_command_change(self, variable: str, _, action: str):
        if self._command_config.command.name != self._sv_om_commands.get():
            new_command = self._commands.find_by_name(self._sv_om_commands.get())
            new_configuration = CommandConfiguration(new_command)

            self._command_config.copy_to(new_configuration)

            self._pipeline_config.replace_command_configuration(self._index, new_configuration)

    def _on_input_change(self, event: Event) -> None:
        self._command_config.input_dir = event.widget.get()

    def _on_output_change(self, event: Event) -> None:
        self._command_config.output_dir = event.widget.get()

    def _on_special_activation_change(self) -> None:
        if self._bv_chk_special.get():
            self._sb_special.configure(state=NORMAL)
            self._command_config.special = self._get_special_value()
        else:
            self._command_config.special = None
            self._sb_special.configure(state=DISABLED)

    def _on_special_change(self, _: Optional[Event] = None) -> None:
        self._command_config.special = self._get_special_value()

    def _on_down_command(self) -> None:
        self._pipeline_config.pipeline.swap_command_position(self._index, self._index + 1)

    def _on_up_command(self) -> None:
        self._pipeline_config.pipeline.swap_command_position(self._index, self._index - 1)

    def _on_remove_command(self) -> None:
        self._pipeline_config.pipeline.remove_command(self._index)

    def _on_params_command(self) -> None:
        dialog = ParamConfigurationDialog(self._master, self._command_config)
        dialog.wait_visibility()
        dialog.grab_set()

    def _on_info_command(self) -> None:
        webbrowser.open(self._command_config.command.url)

    def _update_position(self):
        self._update_arrows()

        self._locate_components()

    def _update_arrows(self):
        self._btn_up.config(state=DISABLED if self._index == 0 else NORMAL)
        self._btn_down.config(state=DISABLED if self._index == len(self._pipeline_config.pipeline) - 1 else NORMAL)

    def _update_command(self) -> None:
        self._sv_om_commands.set(self._command_config.command.name)

        if self._command_config.command.supports_special:
            if self._command_config.has_special():
                self._bv_chk_special.set(True)
                self._sb_special.set(self._command_config.special)
            else:
                self._bv_chk_special.set(False)
                self._sb_special.set("")

            self._sb_special.configure(state=NORMAL)
            self._chk_special.configure(state=NORMAL)
        else:
            self._sb_special.set("")
            self._bv_chk_special.set(False)
            self._sb_special.configure(state=DISABLED)
            self._chk_special.configure(state=DISABLED)

        if self._command_config.command.has_params():
            self._btn_params.configure(state=NORMAL)
        else:
            self._btn_params.configure(state=DISABLED)

    def _update_input_dir(self) -> None:
        self._e_input.delete(0, len(self._e_input.get()))
        if self._command_config.has_input_dir():
            self._e_input.insert(0, self._command_config.input_dir)  # type: ignore

    def _update_output_dir(self) -> None:
        self._e_output.delete(0, len(self._e_output.get()))
        if self._command_config.has_output_dir():
            self._e_output.insert(0, self._command_config.output_dir)  # type: ignore

    def _update_special(self) -> None:
        if not self._command_config.is_special_supported():
            self._chk_special.config(state=DISABLED)
            self._sb_special.config(state=DISABLED)  # type: ignore
        else:
            if self._command_config.has_special():
                self._bv_chk_special.set(True)
                self._sb_special.config(state=NORMAL)  # type: ignore
                self._sb_special.set(self._command_config.special)
            else:
                self._bv_chk_special.set(False)
                self._sb_special.config(state=DISABLED)  # type: ignore


class PipelineDesigner(Frame):
    _PAD_X: Final[Tuple[int, int]] = (4, 4)
    _PAD_Y: Final[Tuple[int, int]] = (2, 2)

    def __init__(self, pipeline_config: PipelineConfiguration, commands: Commands = load_commands(),
                 master: Optional[Widget] = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._commands: Commands = commands
        self._pipeline_config: PipelineConfiguration = pipeline_config

        self._mediators: List[_CommandConfigFormMediator] = []
        for index in range(0, len(self._pipeline_config.pipeline)):
            self._mediators.append(_CommandConfigFormMediator(self, index, self._pipeline_config, self._commands,
                                                              padx=PipelineDesigner._PAD_X,
                                                              pady=PipelineDesigner._PAD_Y))

        self._btn_new: Button = Button(self, text="Add command", command=self._on_add_command)
        self._btn_new.grid(row=len(self._mediators), column=0, columnspan=10, padx=PipelineDesigner._PAD_X,
                           pady=PipelineDesigner._PAD_Y)

        self._pipeline_config.add_callback(self._on_pipeline_config_change)

    def _get_first_unselected_command(self) -> Command:
        for command in self._commands:
            if not self._pipeline_config.pipeline.has_command(command):
                return command

        return self._commands.commands[0]

    def _on_pipeline_config_change(self, _: PipelineConfiguration, event: PipelineConfigurationChangeEvent) -> None:
        if event.attribute == "command_configs" and event.old_value is None:
            index = event.new_value[0]  # type: ignore

            self._add_command_config_form(index)

    def _on_add_command(self) -> None:
        index = self._pipeline_config.pipeline.add_command(self._get_first_unselected_command())

        self._add_command_config_form(index)

    def _add_command_config_form(self, index):
        self._mediators.append(_CommandConfigFormMediator(self, index, self._pipeline_config, self._commands,
                                                          padx=PipelineDesigner._PAD_X,
                                                          pady=PipelineDesigner._PAD_Y))
        self._btn_new.grid(row=len(self._mediators), column=0, columnspan=10,
                           padx=PipelineDesigner._PAD_X, pady=PipelineDesigner._PAD_Y)
