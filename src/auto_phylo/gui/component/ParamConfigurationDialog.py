from tkinter import Toplevel, Misc, Entry, StringVar
from tkinter.ttk import Button, Label

from auto_phylo.gui.model.CommandConfiguration import CommandConfiguration


class ParamConfigurationDialog(Toplevel):
    def __init__(self, master: Misc, command_config: CommandConfiguration):
        super().__init__(master)

        self._command_config: CommandConfiguration = command_config

        self.title(f"Configure {command_config.command.name}")

        row = 0
        for param in command_config.command.list_params():
            label = Label(self, text=param)

            sv_entry = StringVar(self)
            if command_config.has_param_value(param):
                sv_entry.set(command_config.get_param_value(param))

            entry = Entry(self, textvariable=sv_entry)
            self._bind_value_change(param, entry)

            label.grid(row=row, column=0, sticky="nsew", padx=(4, 4), pady=(2, 2))
            entry.grid(row=row, column=1, sticky="nsew", padx=(4, 4), pady=(2, 2))

            row += 1

        self._btn_exit: Button = Button(self, text="Close", command=self._on_close)
        self._btn_exit.grid(row=row, column=0, columnspan=2, padx=(4, 4), pady=(2, 2))

    def _bind_value_change(self, param: str, entry: Entry) -> None:
        entry.bind("<FocusOut>", lambda event: self._command_config.set_param_value(param, event.widget.get()))

    def _on_close(self) -> None:
        self.destroy()
