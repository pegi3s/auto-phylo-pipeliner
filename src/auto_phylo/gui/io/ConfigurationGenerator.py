from auto_phylo.gui.model.PipelineConfiguration import PipelineConfiguration


class ConfigurationGenerator:
    def generate(self, seda_version: str, output_dir: str, pipeline: PipelineConfiguration) -> str:
        output = f"""
# General parameters
SEDA="{seda_version}"
dir={output_dir}

# Other parameters
"""

        for command in pipeline.pipeline:
            config = pipeline.get_command_configuration(command)

            if config.has_param_values():
                output += f"# {command.tool}\n"

                for key, value in config.get_param_values().items():
                    output += f"{key}={value}\n"

                output += "\n"

        return output
