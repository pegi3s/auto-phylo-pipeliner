from auto_phylo.gui.model.PipelineConfiguration import PipelineConfiguration


class PipelineGenerator:
    def generate(self, pipeline: PipelineConfiguration) -> str:
        output = ""

        for command in pipeline.pipeline:
            if pipeline.has_command_configuration(command):
                config = pipeline.get_command_configuration(command)

                output += f"{command.tool} {config.input_dir} {config.output_dir}"

                if command.supports_special and config.has_special():
                    output += f" Special {config.special}"

                output += "\n"

        return output
