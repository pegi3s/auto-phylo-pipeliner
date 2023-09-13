from typing import Dict, Callable, Any, List, Tuple

from behave import fixture
from behave.runner import Context

from auto_phylo.gui.model.Command import Command
from auto_phylo.gui.model.CommandConfiguration import CommandConfiguration
from auto_phylo.gui.model.Pipeline import Pipeline
from auto_phylo.gui.model.PipelineConfiguration import PipelineConfiguration


@fixture(name="fixture.pipeline.basic")
def basic_pipeline(context: Context) -> PipelineConfiguration:
    commands = [
        Command(
            tool="tblaxtx",
            name="tblastx (MP) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/docs/modules_1_blast.html#tblastx",
            supports_special=True,
            params={
                "expect": "0.05"
            }
        ),
        Command(
            tool="disambiguate",
            name="disambiguate (M) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/docs/modules_2_fasta_processing.html#disambiguate",
            supports_special=True,
            params={}
        )
    ]

    pipeline = Pipeline(commands)

    configuration = PipelineConfiguration(
        pipeline,
        [
            CommandConfiguration(commands[0], "a", "b", None, {"expect": "0.01"}),
            CommandConfiguration(commands[1], "b", "c", 10)
        ]
    )

    context.pipeline = configuration

    return configuration


@fixture(name="fixture.pipeline.text.basic")
def basic_pipeline_file(context: Context) -> str:
    pipeline_text = """
        tblaxtx a b
        disambiguate b c Special 10
    """

    context.pipeline_text = pipeline_text

    return pipeline_text


@fixture(name="fixture.config.text.basic")
def basic_config_file(context: Context, seda: str, output_dir: str) -> str:
    config_text = f"""
        # General parameters
        SEDA="{seda}"
        dir={output_dir}

        # Other parameters
        # tblaxtx
        expect=0.01
    """

    context.config_text = config_text

    return config_text


@fixture(name="fixture.pipeline.advanced")
def advanced_pipeline(context: Context) -> PipelineConfiguration:
    commands = [
        Command(
            tool="tblaxtx",
            name="tblastx (MP) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/docs/modules_1_blast.html#tblastx",
            supports_special=True,
            params={
                "expect": "0.05"
            }
        ),
        Command(
            tool="add_taxonomy",
            name="add_taxonomy (MP) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/docs/modules_2_fasta_processing.html#add-taxonomy",
            supports_special=True,
            params={
                "taxonomy": "",
                "category": ""
            }
        ),
        Command(
            tool="CGF_and_CGA_CDS_processing",
            name="CGF_and_CGA_CDS_processing (MP) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/docs/modules_2_fasta_processing.html#cgf-and-cga-cds-processing",
            supports_special=True,
            params={
                "start_codons": "ATG",
                "max_size_difference": "10",
                "reference_file": "",
                "pattern": "\".\"",
                "codon_table": "1",
                "isoform_min_word_length": "",
                "isoform_ref_size": ""
            }
        ),
        Command(
            tool="check_contamination",
            name="check_contamination (MP) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/docs/modules_2_fasta_processing.html#check-contamination",
            supports_special=True,
            params={}
        ),
        Command(
            tool="disambiguate",
            name="disambiguate (M) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/docs/modules_2_fasta_processing.html#disambiguate",
            supports_special=True,
            params={}
        ),
        Command(
            tool="merge",
            name="merge (M) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/docs/modules_2_fasta_processing.html#merge",
            supports_special=False,
            params={}
        ),
        Command(
            tool="prefix",
            name="prefix (M) (FASTA-FASTA)",
            url="http://evolution6.i3s.up.pt/static/auto-phylo/docs/modules_2_fasta_processing.html#prefix",
            supports_special=True,
            params={}
        )
    ]

    pipeline = Pipeline(commands)

    configuration = PipelineConfiguration(
        pipeline,
        [
            CommandConfiguration(commands[0], "a", "b", None, {
                "expect": "0.1"
            }),
            CommandConfiguration(commands[1], "b", "c", 5, {
                "taxonomy": "X",
                "category": "CAT"
            }),
            CommandConfiguration(commands[2], "c", "d", None, {
                "start_codons": "ATG",
                "max_size_difference": "10",
                "reference_file": "",
                "pattern": "\".\"",
                "codon_table": "1",
                "isoform_min_word_length": "",
                "isoform_ref_size": ""
            }),
            CommandConfiguration(commands[3], "b", "e", 20, {}),
            CommandConfiguration(commands[4], "d", "f", None, {}),
            CommandConfiguration(commands[5], "e", "g", None, {}),
            CommandConfiguration(commands[6], "g", "h", 10, {})
        ]
    )

    context.pipeline = configuration

    return configuration


@fixture(name="fixture.pipeline.text.advanced")
def advanced_pipeline_file(context: Context) -> str:
    pipeline_text = """
        tblaxtx a b
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
def advanced_config_file(context: Context, seda: str, output_dir: str) -> str:
    config_text = f"""
        # General parameters
        SEDA="{seda}"
        dir={output_dir}

        # Other parameters
        # tblaxtx
        expect=0.1

        # add_taxonomy
        taxonomy=X
        category=CAT

        # CGF_and_CGA_CDS_processing
        start_codons=ATG
        max_size_difference=10
        reference_file=
        pattern="."
        codon_table=1
        isoform_min_word_length=
        isoform_ref_size=
    """

    context.config_text = config_text

    return config_text


def get_pipeline_registry(*args, **kwargs) -> Dict[str, Tuple[Callable[[Context], Any], Tuple[Any], Dict[str, Any]]]:
    return {
        "fixture.pipeline.basic": (basic_pipeline, args, kwargs),
        "fixture.pipeline.text.basic": (basic_pipeline_file, args, kwargs),
        "fixture.config.text.basic": (basic_config_file, args, kwargs),
        "fixture.pipeline.advanced": (advanced_pipeline, args, kwargs),
        "fixture.pipeline.text.advanced": (advanced_pipeline_file, args, kwargs),
        "fixture.config.text.advanced": (advanced_config_file, args, kwargs)
    }
