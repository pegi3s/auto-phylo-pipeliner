import json
import os
import subprocess
import tkinter as tk
import webbrowser
from tkinter import filedialog
from tkinter import font
from tkinter import scrolledtext

from auto_phylo.gui.model.Command import Command
from auto_phylo.gui.model.Commands import Commands


class AutoPhyloDesigner(tk.Tk):
    def __init__(self, commands: Commands, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self._commands: Commands = commands

        self.title("auto-phylo GUI")

        top_frame = tk.Frame(self)
        middle_frame = tk.Frame(self)
        bottom_frame = tk.Frame(self)

        top_frame.pack(side=tk.TOP)
        middle_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=10, padx=10)
        bottom_frame.pack(side=tk.TOP)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        middle_frame.columnconfigure(0, weight=0)
        middle_frame.columnconfigure(1, weight=1)

        # Working Directory
        self._working_directory_var = tk.StringVar(top_frame)
        self._working_directory_btn = tk.Button(top_frame, text="Working Directory",
                                                command=self._on_select_working_directory)
        self._working_directory_btn.grid(row=0, column=0)

        # Module Selection
        self._module_selection_var = tk.StringVar(top_frame)
        self._module_selection_var.set("Choose a module")  # Default value
        module_selection_btn = tk.OptionMenu(top_frame, self._module_selection_var, *self._commands.list_names())
        module_selection_btn.grid(row=0, column=1)

        # Information button
        label_font = font.Font(slant="italic", size=9)
        info_btn = tk.Button(top_frame, text="info", font=label_font, command=self._on_open_command_help)
        info_btn.grid(row=0, column=2)

        # Special Number Selection
        self._special_var = tk.IntVar(top_frame)
        self._special_var.set(0)  # Default value

        # Label for Special Number Selection
        label_special = tk.Label(top_frame, text="Special value:")
        label_special.grid(row=1, column=0)
        special_btn = tk.Scale(top_frame, variable=self._special_var, from_=0, to=50, orient=tk.HORIZONTAL)
        special_btn.grid(row=1, column=1)

        # Special Information button
        label_font = font.Font(slant="italic", size=9)
        info1_btn = tk.Button(top_frame, text="info", font=label_font, command=self._on_open_special_help)
        info1_btn.grid(row=1, column=2)

        # Label for Input Directory
        label_input = tk.Label(top_frame, text="Input Directory:")
        label_input.grid(row=2, column=0)

        # Text field for Input Directory
        self._input_dir = tk.Text(top_frame, height=1, width=40)
        self._input_dir.grid(row=2, column=1)

        # Label for Output Directory
        label_output = tk.Label(top_frame, text="Output Directory:")
        label_output.grid(row=3, column=0)

        # Text field for Output Directory
        self._output_dir = tk.Text(top_frame, height=1, width=40)
        self._output_dir.grid(row=3, column=1)

        # Label for Config
        label_config = tk.Label(middle_frame, text="Config file:")
        label_config.grid(row=0, column=0)

        # Text field for Config
        self._config_text = scrolledtext.ScrolledText(middle_frame, height=10)
        self._config_text.grid(row=0, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        # Label for Pipeline
        label_pipeline = tk.Label(middle_frame, text="Pipeline file:")
        label_pipeline.grid(row=1, column=0)

        # Text field for Pipeline
        self._pipeline_text = scrolledtext.ScrolledText(middle_frame, height=10)
        self._pipeline_text.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        # Update Button
        self._update_btn = tk.Button(bottom_frame, text="Update", command=self._on_update_files)
        self._update_btn.grid(row=0, column=0)

        # Run Button
        self._run_btn = tk.Button(bottom_frame, text="Run", command=self._on_run_pipeline)
        self._run_btn.grid(row=0, column=2)

    def _get_selected_command(self) -> Command:
        return self._commands.find_by_name(self._module_selection_var.get())

    def _get_working_directory(self):
        return self._working_directory_var.get()

    def _get_config_path(self):
        return os.path.join(self._get_working_directory(), "config")

    def _get_pipeline_path(self):
        return os.path.join(self._get_working_directory(), "pipeline")

    def _has_special(self):
        return self._special_var.get() > 0

    def _has_working_directory(self):
        return self._get_working_directory() != ""

    def _has_command_selected(self):
        return self._get_selected_command() != "Choose a module"

    def _save_config(self):
        config_file_path = self._get_config_path()
        command = self._get_selected_command()

        for param in command.list_params():
            search_word = param + "="
            with open(config_file_path, "r") as config_file:
                is_absent = search_word not in config_file.read()

            if is_absent:
                with open(config_file_path, "a") as config_file:
                    default_value = command.get_default_param_value(param)
                    config_file.write(f"{search_word}{default_value}\n")

    def _save_pipeline(self):
        pipeline_file_path = self._get_pipeline_path()
        input_var = self._input_dir.get("1.0", "end-1c")
        output_var = self._output_dir.get("1.0", "end-1c")

        command = self._get_selected_command()
        with open(pipeline_file_path, "a") as pipeline_file:
            pipeline_file.write(command.tool + " " + input_var + " " + output_var + " ")
            if self._has_special():
                if command.supports_special:
                    pipeline_file.write(f"Special {self._special_var.get()}\n")
            else:
                pipeline_file.write("\n")

        self._remove_blanks_from_pipeline()

    def _load_config(self):
        config_file_path = self._get_config_path()
        with open(config_file_path, "r") as config_file:
            content = config_file.read()
            self._config_text.delete("1.0", tk.END)
            self._config_text.insert(tk.END, content)

    def _load_pipeline(self):
        pipeline_file_path = self._get_pipeline_path()
        with open(pipeline_file_path, "r") as pipeline_file:
            content = pipeline_file.read()
            self._pipeline_text.delete("1.0", tk.END)
            self._pipeline_text.insert(tk.END, content)

    def _edit_config(self):
        config_file_path = self._get_config_path()
        config_content = self._config_text.get("1.0", tk.END)
        with open(config_file_path, "w") as file:
            file.write(config_content)

    def _edit_pipeline(self):
        pipeline_file_path = self._get_pipeline_path()
        pipeline_content = self._pipeline_text.get("1.0", tk.END)
        with open(pipeline_file_path, "w") as pipeline_file:
            pipeline_file.write(pipeline_content)
        self._remove_blanks_from_pipeline()

    def _remove_blanks_from_pipeline(self):
        pipeline_file_path = self._get_pipeline_path()
        with open(pipeline_file_path, "r+") as pipeline_file:
            lines = pipeline_file.readlines()
            pipeline_file.seek(0)
            pipeline_file.truncate()
            for line in lines:
                if line.strip():
                    pipeline_file.write(line)

    def _set_default_values(self):
        input_var = self._output_dir.get("1.0", "end-1c")
        self._input_dir.delete(1.0, "end")
        self._input_dir.insert("1.0", input_var)
        self._output_dir.delete(1.0, "end")
        self._output_dir.insert("1.0", "")
        self._module_selection_var.set("Choose a module")
        self._special_var.set(0)

    def _on_open_command_help(self):
        command = self._get_selected_command()

        web_address = command.url

        if web_address:
            webbrowser.open(web_address)

    def _on_open_special_help(self):
        web_address = "http://evolution6.i3s.up.pt/static/auto-phylo/docs/modules_6_special.html#special"
        webbrowser.open(web_address)

    def _on_select_working_directory(self):
        button_var = self._working_directory_var
        selected_directory = filedialog.askdirectory()
        button_var.set(selected_directory)
        # Create files
        working_directory = self._get_working_directory()
        config_file_path = self._get_config_path()
        pipeline_file_path = self._get_pipeline_path()
        with open(pipeline_file_path, "a") as pipeline_file:
            pipeline_file.write("")
        with open(config_file_path, "a") as config_file:
            config_file.write("")
        search_word = "SEDA="
        with open(config_file_path, "r") as config_file:
            is_absent = search_word not in config_file.read()
        if is_absent:
            with open(config_file_path, "a") as config_file:
                config_file.write("#General parameters\n")
                config_file.write("SEDA=\"seda:1.6.0-v2304\"\n")
                config_file.write("dir=" + working_directory + "\n")
                config_file.write("\n#Other parameters\n")
        self._load_config()
        self._load_pipeline()
        self._working_directory_btn.config(state=tk.DISABLED)

    def _on_update_files(self):
        input_var = self._input_dir.get("1.0", "end-1c")
        output_var = self._output_dir.get("1.0", "end-1c")
        if (self._has_working_directory()) and (input_var != "") and (output_var != ""):
            if self._has_command_selected():
                self._save_config()
                self._load_config()
                self._save_pipeline()
                self._load_pipeline()
        self._edit_config()
        self._edit_pipeline()
        self._load_pipeline()
        if (self._has_working_directory()) and (self._has_command_selected()) and (input_var != "") and (
            output_var != ""):
            self._set_default_values()

    def _on_run_pipeline(self):
        if self._has_working_directory():
            working_directory = self._get_working_directory()
            pipeline_file_path = self._get_pipeline_path()

            with open(pipeline_file_path, "r") as file:
                first_line = file.readline().strip()
                fields = first_line.split()
                data_dir = fields[1]
                data_dir_input = os.path.join(working_directory, data_dir)

            if os.path.exists(data_dir_input) and os.path.isdir(data_dir_input):
                file_names = ["config", "pipeline"]
                all_files_exist = all(
                    os.path.exists(os.path.join(working_directory, file_name)) for file_name in file_names)
                if all_files_exist:
                    bash_command = f"""
                        docker run --rm \\
                            -v {working_directory}:/data \\
                            -v /var/run/docker.sock:/var/run/docker.sock pegi3s/auto-phylo
                    """
                    print("Running " + bash_command)
                    command = bash_command
                    subprocess.run(command, shell=True)
                    self._update_btn.config(state=tk.DISABLED)
                    self._update_btn.config(text="Done")
                    self._update_btn.config(fg="black")
                    self._update_btn.config(bg="red")
                    print("Done")


def launch():
    with open("commands.json", "r") as file:
        commands = json.load(file)
    designer = AutoPhyloDesigner(Commands(Command(**data) for data in commands))
    designer.mainloop()


if __name__ == "__main__":
    launch()
