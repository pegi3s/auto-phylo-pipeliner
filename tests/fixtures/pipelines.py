from copy import deepcopy
from typing import Callable, Dict, Any, Optional

from behave import fixture
from behave.runner import Context

from src.auto_phylo.pipeliner.model.Command import Command
from src.auto_phylo.pipeliner.model.CommandConfiguration import CommandConfiguration
from src.auto_phylo.pipeliner.model.Pipeline import Pipeline
from src.auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration


@fixture(name="fixture.pipeline.basic")
def basic_pipeline(context: Optional[Context] = None) -> PipelineConfiguration:
    commands = [
        Command(
            tool="tblastx",
            name="tblastx (MP) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/v2/docs/modules_1_blast.html#tblastx",
            supports_special=True,
            params={
                "tblastx_query": "",
                "tblastx_expect": "0.05"
            }
        ),
        Command(
            tool="disambiguate",
            name="disambiguate (M) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/v2/docs/modules_2_fasta_processing.html#disambiguate",
            supports_special=True,
            params={}
        )
    ]

    configuration = PipelineConfiguration(Pipeline(commands), command_configs=[
        CommandConfiguration(commands[0], "a", "b"),
        CommandConfiguration(commands[1], "b", "c", 10)
    ])

    if context is not None:
        context.pipeline = configuration

    return configuration


@fixture(name="fixture.pipeline.basic.configured")
def basic_configured_pipeline(context: Optional[Context] = None) -> PipelineConfiguration:
    configuration = deepcopy(basic_pipeline(context))

    commands = configuration.pipeline.commands

    configuration.seda_version = "\"seda:1.6.0-v2304\""
    configuration.output_dir = "basic_output"
    configuration.set_command_configuration(0, CommandConfiguration(commands[0], "a", "b", None,
                                                                    {"tblastx_expect": "0.01"}))
    configuration.set_command_configuration(1, CommandConfiguration(commands[1], "b", "c", 10))

    if context is not None:
        context.pipeline_config = configuration

    return configuration


@fixture(name="fixture.pipeline.text.basic")
def basic_pipeline_file(context: Context) -> str:
    pipeline_text = """
        tblastx a b
        disambiguate b c Special 10
    """

    context.pipeline_text = pipeline_text

    return pipeline_text


@fixture(name="fixture.config.text.basic")
def basic_config_file(context: Context) -> str:
    config_text = f"""
        # General parameters
        SEDA="seda:1.6.0-v2304"
        dir=basic_output

        # Other parameters
        # tblastx
        tblastx_expect=0.01
    """

    context.config_text = config_text

    return config_text


@fixture(name="fixture.pipeline.advanced")
def advanced_pipeline(context: Optional[Context] = None) -> PipelineConfiguration:
    commands = [
        Command(
            tool="tblastx",
            name="tblastx (MP) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/v2/docs/modules_1_blast.html#tblastx",
            supports_special=True,
            params={
                "tblastx_query": "",
                "tblastx_expect": "0.05"
            }
        ),
        Command(
            tool="add_taxonomy",
            name="add_taxonomy (MP) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/v2/docs/modules_2_fasta_processing.html#add-taxonomy",
            supports_special=True,
            params={
                "add_tax_taxonomy_header": ""
            }
        ),
        Command(
            tool="CGF_and_CGA_CDS_processing",
            name="CGF_and_CGA_CDS_processing (MP) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/v2/docs/modules_2_fasta_processing.html#cgf-and-cga-cds-processing",
            supports_special=True,
            params={
                "cgf_cga_start_codon": "ATG",
                "cgf_cga_max_size_difference": "10",
                "cgf_cga_reference_file": "",
                "cgf_cga_pattern": "\".\"",
                "cgf_cga_codon_table": "1",
                "cgf_cga_isoform_min_word_length": "",
                "cgf_cga_isoform_ref_size": ""
            }
        ),
        Command(
            tool="check_contamination",
            name="check_contamination (MP) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/v2/docs/modules_2_fasta_processing.html#check-contamination",
            supports_special=True,
            params={
                "check_cont_taxonomy": "",
                "check_cont_category": ""
            }
        ),
        Command(
            tool="disambiguate",
            name="disambiguate (M) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/v2/docs/modules_2_fasta_processing.html#disambiguate",
            supports_special=True,
            params={}
        ),
        Command(
            tool="merge",
            name="merge (M) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/v2/docs/modules_2_fasta_processing.html#merge",
            supports_special=False,
            params={}
        ),
        Command(
            tool="prefix",
            name="prefix (M) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/v2/docs/modules_2_fasta_processing.html#prefix",
            supports_special=True,
            params={}
        )
    ]

    configuration = PipelineConfiguration(Pipeline(commands), command_configs=[
        CommandConfiguration(commands[0], "a", "b"),
        CommandConfiguration(commands[1], "b", "c", 5),
        CommandConfiguration(commands[2], "c", "d"),
        CommandConfiguration(commands[3], "b", "e", 20),
        CommandConfiguration(commands[4], "d", "f"),
        CommandConfiguration(commands[5], "e", "g"),
        CommandConfiguration(commands[6], "g", "h", 10)
    ])

    if context is not None:
        context.pipeline = configuration

    return configuration


@fixture(name="fixture.pipeline.advanced.configured")
def advanced_configured_pipeline(context: Optional[Context] = None) -> PipelineConfiguration:
    configuration = deepcopy(advanced_pipeline(context))

    commands = configuration.pipeline.commands

    configuration.seda_version = "\"seda:1.6.0-v2304\""
    configuration.output_dir = "advanced_output"
    configuration.set_command_configuration(0, CommandConfiguration(commands[0], "a", "b", None, {
        "tblastx_expect": "0.1"
    }))
    configuration.set_command_configuration(1, CommandConfiguration(commands[1], "b", "c", 5, {
        "add_tax_taxonomy_header": "X"
    }))
    configuration.set_command_configuration(2, CommandConfiguration(commands[2], "c", "d", None, {
        "cgf_cga_start_codon": "ATG",
        "cgf_cga_max_size_difference": "10",
        "cgf_cga_reference_file": "",
        "cgf_cga_pattern": "\".\"",
        "cgf_cga_codon_table": "1",
        "cgf_cga_isoform_min_word_length": "",
        "cgf_cga_isoform_ref_size": ""
    }))
    configuration.set_command_configuration(3, CommandConfiguration(commands[3], "b", "e", 20, {}))
    configuration.set_command_configuration(4, CommandConfiguration(commands[4], "d", "f", None, {}))
    configuration.set_command_configuration(5, CommandConfiguration(commands[5], "e", "g", None, {}))
    configuration.set_command_configuration(6, CommandConfiguration(commands[6], "g", "h", 10, {}))

    if context is not None:
        context.pipeline_config = configuration

    return configuration


@fixture(name="fixture.pipeline.text.advanced")
def advanced_pipeline_file(context: Context) -> str:
    pipeline_text = """
        tblastx a b
        add_taxonomy b c Special 5
        CGF_and_CGA_CDS_processing c d
        check_contamination b e Special 20
        disambiguate d f
        merge e g
        prefix g h Special 10
    """

    context.pipeline_text = pipeline_text

    return pipeline_text


@fixture(name="fixture.config.text.advanced")
def advanced_config_file(context: Context) -> str:
    config_text = f"""
        # General parameters
        SEDA="seda:1.6.0-v2304"
        dir=advanced_output

        # Other parameters
        # tblastx
        tblastx_expect=0.1

        # add_taxonomy
        add_tax_taxonomy_header=X

        # CGF_and_CGA_CDS_processing
        cgf_cga_start_codon=ATG
        cgf_cga_max_size_difference=10
        cgf_cga_reference_file=
        cgf_cga_pattern="."
        cgf_cga_codon_table=1
        cgf_cga_isoform_min_word_length=
        cgf_cga_isoform_ref_size=
    """

    context.config_text = config_text

    return config_text


fixture_pipelines: Dict[str, Callable[[], Any]] = {
    "fixture.pipeline.basic": basic_pipeline,
    "fixture.pipeline.basic.configured": basic_configured_pipeline,
    "fixture.pipeline.text.basic": basic_pipeline_file,
    "fixture.config.text.basic": basic_config_file,
    "fixture.pipeline.advanced": advanced_pipeline,
    "fixture.pipeline.advanced.configured": advanced_configured_pipeline,
    "fixture.pipeline.text.advanced": advanced_pipeline_file,
    "fixture.config.text.advanced": advanced_config_file
}
