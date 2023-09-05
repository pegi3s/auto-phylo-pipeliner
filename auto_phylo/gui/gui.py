import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import font
import webbrowser
import os
import subprocess
import json
from typing import List

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
        self.__working_directory_var = tk.StringVar(top_frame)
        self.__working_directory_btn = tk.Button(top_frame, text="Working Directory",
                                                 command=lambda: self.__select_working_directory(
                                                     self.__working_directory_var))
        self.__working_directory_btn.grid(row=0, column=0)

        # Module Selection
        self.__module_selection_var = tk.StringVar(top_frame)
        self.__module_selection_var.set("Choose a module")  # Default value
        module_selection_btn = tk.OptionMenu(top_frame, self.__module_selection_var, *self._commands.list_names())
        module_selection_btn.grid(row=0, column=1)

        # Information button
        label_font = font.Font(slant="italic", size=9)
        info_btn = tk.Button(top_frame, text="info", font=label_font, command=self.__open_web_address)
        info_btn.grid(row=0, column=2)

        # Special Number Selection
        self.__special_var = tk.IntVar(top_frame)
        self.__special_var.set(0)  # Default value

        # Label for Special Number Selection
        label_special = tk.Label(top_frame, text="Special value:")
        label_special.grid(row=1, column=0)
        special_btn = tk.Scale(top_frame, variable=self.__special_var, from_=0, to=50, orient=tk.HORIZONTAL)
        special_btn.grid(row=1, column=1)

        # Special Information button
        label_font = font.Font(slant="italic", size=9)
        info1_btn = tk.Button(top_frame, text="info", font=label_font, command=self.__open_web_address1)
        info1_btn.grid(row=1, column=2)

        # Label for Input Directory
        label_input = tk.Label(top_frame, text="Input Directory:")
        label_input.grid(row=2, column=0)

        # Text field for Input Directory
        self.__input_dir = tk.Text(top_frame, height=1, width=40)
        self.__input_dir.grid(row=2, column=1)

        # Label for Output Directory
        label_output = tk.Label(top_frame, text="Output Directory:")
        label_output.grid(row=3, column=0)

        # Text field for Output Directory
        self.__output_dir = tk.Text(top_frame, height=1, width=40)
        self.__output_dir.grid(row=3, column=1)

        # Label for Config
        label_config = tk.Label(middle_frame, text="Config file:")
        label_config.grid(row=0, column=0)

        # Text field for Config
        self.__config_text = scrolledtext.ScrolledText(middle_frame, height=10)
        self.__config_text.grid(row=0, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        # Label for Pipeline
        label_pipeline = tk.Label(middle_frame, text="Pipeline file:")
        label_pipeline.grid(row=1, column=0)

        # Text field for Pipeline
        self.__pipeline_text = scrolledtext.ScrolledText(middle_frame, height=10)
        self.__pipeline_text.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        # Update Button
        self.__next_btn = tk.Button(bottom_frame, text="Update", command=self.__update_files)
        self.__next_btn.grid(row=0, column=0)

        # Run Button
        self.__next_btn = tk.Button(bottom_frame, text="Run", command=self.__run)
        self.__next_btn.grid(row=0, column=2)

    def __open_web_address(self):
        input_string = self.__module_selection_var.get()
        split_parts = input_string.split(' ')
        selection = split_parts[0]

        web_address = self._commands.find_by_tool(selection).url

        if web_address:
            webbrowser.open(web_address)

    def __save_config(self):
        working_directory = self.__working_directory_var.get()
        config_file_path = os.path.join(working_directory, "config")
        input_string = self.__module_selection_var.get()
        split_parts = input_string.split(' ')
        selected_option = split_parts[0]

        command = self._commands.find_by_tool(selected_option)

        for param in command.list_params():
            search_word = param + "="
            with open(config_file_path, "r") as config_file:
                is_absent = search_word not in config_file.read()

            if is_absent:
                with open(config_file_path, "a") as config_file:
                    default_value = command.get_default_param_value(param)
                    config_file.write(f"{search_word}{default_value}\n")

    def __save_pipeline(self):
        working_directory = self.__working_directory_var.get()
        pipeline_file_path = os.path.join(working_directory, "pipeline")
        input_var = self.__input_dir.get("1.0", "end-1c")
        output_var = self.__output_dir.get("1.0", "end-1c")
        input_string = self.__module_selection_var.get()
        split_parts = input_string.split(' ')
        content_to_extract = split_parts[0]
        with open(pipeline_file_path, "a") as pipeline_file:
            pipeline_file.write(content_to_extract + " " + input_var + " " + output_var + " ")
            if self.__special_var.get() == 0:
                pipeline_file.write(f"\n")
            else:
                command = self._commands.find_by_tool(content_to_extract)
                if command.supports_special:
                    pipeline_file.write(f"Special {self.__special_var.get()}\n")

        self.__rm_blanks_from_pipeline()

    def __open_web_address1(self):
        web_address = "http://evolution6.i3s.up.pt/static/auto-phylo/docs/modules_6_special.html#special"
        webbrowser.open(web_address)

    def __select_working_directory(self, button_var):
        selected_directory = filedialog.askdirectory()
        button_var.set(selected_directory)
        # Create files
        working_directory = self.__working_directory_var.get()
        config_file_path = os.path.join(working_directory, "config")
        pipeline_file_path = os.path.join(working_directory, "pipeline")
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
        self.__load_config()
        self.__load_pipeline()
        self.__working_directory_btn.config(state=tk.DISABLED)

    def __load_config(self):
        working_directory = self.__working_directory_var.get()
        config_file_path = os.path.join(working_directory, "config")
        with open(config_file_path, "r") as config_file:
            content = config_file.read()
            self.__config_text.delete("1.0", tk.END)
            self.__config_text.insert(tk.END, content)

    def __load_pipeline(self):
        working_directory = self.__working_directory_var.get()
        pipeline_file_path = os.path.join(working_directory, "pipeline")
        with open(pipeline_file_path, "r") as pipeline_file:
            content = pipeline_file.read()
            self.__pipeline_text.delete("1.0", tk.END)
            self.__pipeline_text.insert(tk.END, content)

    def __edit_config(self):
        working_directory = self.__working_directory_var.get()
        config_file_path = os.path.join(working_directory, "config")
        config_content = self.__config_text.get("1.0", tk.END)
        with open(config_file_path, "w") as file:
            file.write(config_content)

    def __edit_pipeline(self):
        working_directory = self.__working_directory_var.get()
        pipeline_file_path = os.path.join(working_directory, "pipeline")
        pipeline_content = self.__pipeline_text.get("1.0", tk.END)
        with open(pipeline_file_path, "w") as pipeline_file:
            pipeline_file.write(pipeline_content)
        self.__rm_blanks_from_pipeline()

    def __rm_blanks_from_pipeline(self):
        working_directory = self.__working_directory_var.get()
        pipeline_file_path = os.path.join(working_directory, "pipeline")
        with open(pipeline_file_path, "r+") as pipeline_file:
            lines = pipeline_file.readlines()
            pipeline_file.seek(0)
            pipeline_file.truncate()
            for line in lines:
                if line.strip():
                    pipeline_file.write(line)

    def __set_default_values(self):
        input_var = self.__output_dir.get("1.0", "end-1c")
        self.__input_dir.delete(1.0, "end")
        self.__input_dir.insert("1.0", input_var)
        self.__output_dir.delete(1.0, "end")
        self.__output_dir.insert("1.0", "")
        self.__module_selection_var.set("Choose a module")
        self.__special_var.set(0)

    def __update_files(self):
        input_var = self.__input_dir.get("1.0", "end-1c")
        output_var = self.__output_dir.get("1.0", "end-1c")
        if ((self.__working_directory_var.get() != "") and (input_var != "") and (output_var != "")):
            if self.__module_selection_var.get() != "Choose a module":
                self.__save_config()
                self.__load_config()
                self.__save_pipeline()
                self.__load_pipeline()
        self.__edit_config()
        self.__edit_pipeline()
        self.__load_pipeline()
        if ((self.__working_directory_var.get() != "") and (
            self.__module_selection_var.get() != "Choose a module") and (input_var != "") and (output_var != "")):
            self.__set_default_values()

    def __run(self):
        if self.__working_directory_var.get() != "":
            working_directory = self.__working_directory_var.get()
            pipeline_file_path = os.path.join(working_directory, "pipeline")
            with open(pipeline_file_path, 'r') as file:
                first_line = file.readline().strip()
                fields = first_line.split()
                data_dir = fields[1]
                data_dir_input = os.path.join(working_directory, data_dir)
            if os.path.exists(data_dir_input) and os.path.isdir(data_dir_input):
                file_names = ["config", "pipeline"]
                all_files_exist = all(
                    os.path.exists(os.path.join(working_directory, file_name)) for file_name in file_names)
                if all_files_exist:
                    bash_command = "docker run --rm -v" + self.__working_directory_var.get() + ":/data -v /var/run/docker.sock:/var/run/docker.sock pegi3s/auto-phylo"
                    print("Running " + bash_command)
                    command = bash_command
                    subprocess.run(command, shell=True)
                    self.__next_btn.config(state=tk.DISABLED)
                    self.__next_btn.config(text="Done")
                    self.__next_btn.config(fg="black")
                    self.__next_btn.config(bg="red")
                    print("Done")


def launch():
    with open("commands.json", "r") as file:
        commands = json.load(file)
    designer = AutoPhyloDesigner(Commands(Command(**data) for data in commands))
    designer.mainloop()


if __name__ == "__main__":
    launch()
