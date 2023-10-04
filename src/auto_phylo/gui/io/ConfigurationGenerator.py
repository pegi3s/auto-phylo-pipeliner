from typing import Dict

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
            param_values: Dict[str, str] = pipeline.get_command_parameters(command)

            if len(param_values) > 0:
                output += f"# {command.tool}\n"

                for key, value in param_values.items():
                    output += f"{key}={value}\n"

                output += "\n"

        return output.strip()
