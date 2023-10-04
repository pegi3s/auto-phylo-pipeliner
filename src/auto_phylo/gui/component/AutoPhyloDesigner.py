from tkinter import Tk, Widget, filedialog, StringVar, Misc, Text
from tkinter.constants import BOTH, X, TOP, INSERT, END
from tkinter.ttk import Notebook, Frame, Label, Button
from typing import List, Optional

import sv_ttk

from auto_phylo.gui import load_commands
from auto_phylo.gui.component.PipelineDesigner import PipelineDesigner
from auto_phylo.gui.io.ConfigurationGenerator import ConfigurationGenerator
from auto_phylo.gui.io.PipelineGenerator import PipelineGenerator
from auto_phylo.gui.model.Commands import Commands
from auto_phylo.gui.model.Pipeline import Pipeline
from auto_phylo.gui.model.PipelineConfiguration import PipelineConfiguration
from auto_phylo.gui.model.PipelineConfigurationChangeEvent import PipelineConfigurationChangeEvent


class AutoPhyloDesigner(Tk):
    def __init__(self,
                 pipeline_config: Optional[PipelineConfiguration] = None,
                 commands: Commands = load_commands(), *args, **kwargs):
        super().__init__(*args, *kwargs)

        self._commands: Commands = commands
        self._pipeline_config: PipelineConfiguration = \
            PipelineConfiguration(Pipeline()) if pipeline_config is None else pipeline_config

        self.title("auto-phylo designer")
        sv_ttk.set_theme("light")

        self._tab_control: Notebook = Notebook(self)

        designer_frame = self._build_designer_tab(self._tab_control)
        pipeline_frame = self._build_pipeline_tab(self._tab_control)
        config_frame = self._build_configuration_tab(self._tab_control)
        status_bar = self._build_status_bar(self)

        self._tab_control.add(designer_frame, text="Designer")
        self._tab_control.add(pipeline_frame, text="Pipeline")
        self._tab_control.add(config_frame, text="Configuration")
        self._tab_control.pack(expand=1, fill=BOTH)
        status_bar.pack(fill=X)

        self._pipeline_config.add_callback(self._on_pipeline_change)

    def _on_pipeline_change(self, _: PipelineConfiguration, __: PipelineConfigurationChangeEvent) -> None:
        if self._pipeline_config.is_valid():
            self._sb_lbl_status.set("Pipeline configuration: OK")
        else:
            self._sb_lbl_status.set("Pipeline configuration: not valid")

        self._update_pipeline_text()
        self._update_configuration_text()

    def _has_working_dir(self) -> bool:
        return self._pipeline_config.output_dir is not None

    def _build_designer_tab(self, root: Widget) -> Frame:
        frame = Frame(root)

        top_frame = self._build_designer_tab_top(frame)
        center_frame = self._build_designer_tab_center(frame)
        top_frame.pack(side=TOP)
        center_frame.pack(side=TOP)

        return frame

    def _build_designer_tab_top(self, frame: Frame) -> Frame:
        top_frame = Frame(frame)

        self._sv_btn_working_dir = StringVar()
        btn_working_dir = Button(top_frame, textvariable=self._sv_btn_working_dir,
                                 command=self._on_select_working_directory)
        self._sv_lbl_working_dir = StringVar()
        lbl_working_dir = Label(top_frame, textvariable=self._sv_lbl_working_dir)
        if self._has_working_dir():
            self._sv_btn_working_dir.set("Change")
            if self._pipeline_config.output_dir is None:
                self._sv_lbl_working_dir.set("")
            else:
                self._sv_lbl_working_dir.set(self._pipeline_config.output_dir)
        else:
            self._sv_btn_working_dir.set("Select")
            self._sv_lbl_working_dir.set("<No working directory selected>")
        btn_working_dir.grid(row=0, column=0)
        lbl_working_dir.grid(row=0, column=1)

        return top_frame

    def _build_designer_tab_center(self, frame: Frame) -> Frame:
        return PipelineDesigner(self._pipeline_config, master=frame)

    def _get_used_directories(self, prefix: str) -> List[str]:
        return [word for word in ["input", "output"] if word.startswith(prefix)]

    def _build_pipeline_tab(self, root: Widget) -> Frame:
        frame = Frame(root)

        self._txt_pipeline = Text(frame)
        self._txt_pipeline.pack(expand=True, fill=BOTH)
        self._update_pipeline_text()

        return frame

    def _build_configuration_tab(self, root: Widget) -> Frame:
        frame = Frame(root)

        self._txt_config = Text(frame)
        self._txt_config.pack(expand=True, fill=BOTH)
        self._update_configuration_text()

        return frame

    def _update_pipeline_text(self) -> None:
        self._txt_pipeline.delete("1.0", END)

        if self._pipeline_config.is_valid():
            generator = PipelineGenerator()
            self._txt_pipeline.insert(INSERT, generator.generate(self._pipeline_config))
        else:
            self._txt_pipeline.insert(INSERT, "Pipeline is not valid")

    def _update_configuration_text(self) -> None:
        self._txt_config.delete("1.0", END)

        if self._pipeline_config.is_valid():
            generator = ConfigurationGenerator()
            self._txt_config.insert(INSERT, generator.generate(self._pipeline_config))
        else:
            self._txt_config.insert(INSERT, "Pipeline is not valid")

    def _on_select_working_directory(self) -> None:
        selected_directory = filedialog.askdirectory(initialdir=self._pipeline_config.output_dir)

        self._sv_lbl_working_dir.set(selected_directory)
        self._sv_btn_working_dir.set("Change")

    def _build_status_bar(self, root: Misc) -> Widget:
        self._sb_lbl_status = StringVar()
        self._sb_lbl_status.set("Welcome to Auto-Phylo Designer")
        self._lbl_status = Label(root, textvariable=self._sb_lbl_status)

        return self._lbl_status
