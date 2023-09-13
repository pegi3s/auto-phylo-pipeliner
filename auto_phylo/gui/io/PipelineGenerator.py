from auto_phylo.gui.model.PipelineConfiguration import PipelineConfiguration


class PipelineGenerator:
    def generate(self, pipeline: PipelineConfiguration) -> str:
        output = ""

        for command in pipeline.pipeline:
            config = pipeline.get_command_configuration(command)

            output += f"{command.tool} {config.get_input_dir()} {config.get_output_dir()}"

            if command.supports_special and config.has_special():
                output += f" Special {config.get_special()}"

            output += "\n"

        return output
