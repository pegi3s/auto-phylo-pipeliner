from auto_phylo.gui.model.PipelineConfiguration import PipelineConfiguration


class ConfigurationGenerator:
    def generate(self, pipeline: PipelineConfiguration) -> str:
        output = f"""
# General parameters
SEDA={pipeline.seda_version}
dir={pipeline.output_dir}

# Other parameters
"""

        for command in pipeline.pipeline:
            if pipeline.has_command_configuration(command):
                config = pipeline.get_command_configuration(command)

                if config.has_param_values():
                    output += f"# {command.tool}\n"

                    for key, value in config.param_values.items():
                        output += f"{key}={value}\n"

                    output += "\n"

        return output
