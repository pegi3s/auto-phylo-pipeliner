from typing import Callable, Dict, Any, Tuple, Optional

from behave import fixture
from behave.runner import Context


@fixture(name="fixture.pipeline.text.error.too_many_params")
def pipeline_with_too_many_params(context: Context) -> str:
    pipeline_text = """
        tblastx a b
        add_taxonomy b c d
        disambiguate d e Special 10
    """

    context.pipeline_text = pipeline_text.strip()

    return pipeline_text


@fixture(name="fixture.pipeline.text.error.too_many_params.lines")
def pipeline_with_too_many_params_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = tuple([1])

    return context.line_errors


@fixture(name="fixture.pipeline.text.error.not_supported_special")
def pipeline_with_not_supported_special(context: Context) -> str:
    pipeline_text = """
        tblastx a b
        add_taxonomy b c
        disambiguate d e Special 10
        merge e f Special 5
    """

    context.pipeline_text = pipeline_text.strip()

    return pipeline_text


@fixture(name="fixture.pipeline.text.error.not_supported_special.lines")
def pipeline_with_not_supported_special_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = tuple([3])

    return context.line_errors


@fixture(name="fixture.pipeline.text.error.bad_special")
def pipeline_with_bad_special(context: Context) -> str:
    pipeline_text = """
        tblastx a b
        add_taxonomy b c
        disambiguate d e especial 10
    """

    context.pipeline_text = pipeline_text.strip()

    return pipeline_text


@fixture(name="fixture.pipeline.text.error.bad_special.lines")
def pipeline_with_bad_special_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = tuple([2])

    return context.line_errors


@fixture(name="fixture.pipeline.text.error.non_integer_special")
def pipeline_with_non_integer_special(context: Context) -> str:
    pipeline_text = """
        tblastx a b
        add_taxonomy b c
        disambiguate d e Special Ten
    """

    context.pipeline_text = pipeline_text.strip()

    return pipeline_text


@fixture(name="fixture.pipeline.text.error.non_integer_special.lines")
def pipeline_with_non_integer_special_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = tuple([2])

    return context.line_errors


@fixture(name="fixture.pipeline.text.error.invalid_command")
def pipeline_with_invalid_command(context: Context) -> str:
    pipeline_text = """
        blaster a b
        add_taxonomy b c
        disambiguate d e Special 10
    """

    context.pipeline_text = pipeline_text.strip()

    return pipeline_text


@fixture(name="fixture.pipeline.text.error.invalid_command.lines")
def pipeline_with_invalid_command_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = tuple([0])

    return context.line_errors


@fixture(name="fixture.pipeline.text.error.multiple_errors")
def pipeline_with_multiple_errors(context: Context) -> str:
    pipeline_text = """
        # Invalid command
        blaster a b

        # Too many params
        add_taxonomy b c d

        # Invalid special name
        disambiguate d e Especial 10

        # Invalid special value
        check_contamination d e Special Ten
    """

    context.pipeline_text = pipeline_text.strip()

    return pipeline_text


@fixture(name="fixture.pipeline.text.error.multiple_errors.lines")
def pipeline_with_multiple_errors_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = (1, 4, 7, 10)

    return context.line_errors


@fixture(name="fixture.config.text.error.missing_seda")
def configuration_with_missing_seda(context: Context) -> str:
    config_text = f"""
        # General parameters
        dir=advanced_output

        # Other parameters
        # tblastx
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

    context.config_text = config_text.strip()

    return config_text


@fixture(name="fixture.config.text.error.missing_seda.lines")
def configuration_with_missing_seda_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = None

    return context.line_errors


@fixture(name="fixture.config.text.error.missing_seda.general")
def configuration_with_missing_seda_general(context: Context) -> Optional[Tuple[str, ...]]:
    context.general_errors = tuple(["Missing SEDA version"])

    return context.general_errors


@fixture(name="fixture.config.text.error.missing_seda_version")
def configuration_with_missing_seda_version(context: Context) -> str:
    config_text = f"""
        # General parameters
        SEDA=
        dir=advanced_output

        # Other parameters
        # tblastx
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

    context.config_text = config_text.strip()

    return config_text


@fixture(name="fixture.config.text.error.missing_seda_version.lines")
def configuration_with_missing_seda_version_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = tuple([1])

    return context.line_errors


@fixture(name="fixture.config.text.error.missing_seda_version.general")
def configuration_with_missing_seda_version_general(context: Context) -> Optional[Tuple[str, ...]]:
    context.general_errors = tuple(["Missing SEDA version"])

    return context.general_errors


@fixture(name="fixture.config.text.error.missing_dir")
def configuration_with_missing_dir(context: Context) -> str:
    config_text = f"""
        # General parameters
        SEDA="seda:1.6.0-v2304"

        # Other parameters
        # tblastx
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

    context.config_text = config_text.strip()

    return config_text


@fixture(name="fixture.config.text.error.missing_dir.lines")
def configuration_with_missing_dir_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = None

    return context.line_errors


@fixture(name="fixture.config.text.error.missing_dir.general")
def configuration_with_missing_dir_general(context: Context) -> Optional[Tuple[str, ...]]:
    context.general_errors = tuple(["Missing working directory (dir)"])

    return context.general_errors


@fixture(name="fixture.config.text.error.missing_dir_value")
def configuration_with_missing_dir_value(context: Context) -> str:
    config_text = f"""
        # General parameters
        SEDA="seda:1.6.0-v2304"
        dir=

        # Other parameters
        # tblastx
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

    context.config_text = config_text.strip()

    return config_text


@fixture(name="fixture.config.text.error.missing_dir_value.lines")
def configuration_with_missing_dir_value_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = tuple([2])

    return context.line_errors


@fixture(name="fixture.config.text.error.missing_dir_value.general")
def configuration_with_missing_dir_value_general(context: Context) -> Optional[Tuple[str, ...]]:
    context.general_errors = tuple(["Missing working directory (dir)"])

    return context.general_errors


@fixture(name="fixture.config.text.error.unsupported_param")
def configuration_with_unsupported_param(context: Context) -> str:
    config_text = f"""
        # General parameters
        SEDA="seda:1.6.0-v2304"
        dir=advanced_output

        # Other parameters
        # tblastx
        expectation=0.1

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

    context.config_text = config_text.strip()

    return config_text


@fixture(name="fixture.config.text.error.unsupported_param.lines")
def configuration_with_unsupported_param_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = tuple([6])

    return context.line_errors


@fixture(name="fixture.config.text.error.unsupported_param.general")
def configuration_with_unsupported_param_general(context: Context) -> Optional[Tuple[str, ...]]:
    context.general_errors = None

    return context.general_errors


@fixture(name="fixture.config.text.error.invalid_lines")
def configuration_with_invalid_lines(context: Context) -> str:
    config_text = f"""
        # General parameters
        SEDA="seda:1.6.0-v2304"
        dir=advanced_output

        # Other parameters
        # tblastx
        expect=0.1
        invalid line 1

        # add_taxonomy
        taxonomy=X
        category=CAT

        # CGF_and_CGA_CDS_processing
        start_codons=ATG
        max_size_difference=10
        reference_file=
        invalid_line=2=not_valid
        pattern="."
        codon_table=1
        isoform_min_word_length=
        isoform_ref_size=
        =not_valid
    """

    context.config_text = config_text.strip()

    return config_text


@fixture(name="fixture.config.text.error.invalid_lines.lines")
def configuration_with_invalid_lines_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = tuple([7, 17, 22])

    return context.line_errors


@fixture(name="fixture.config.text.error.invalid_lines.general")
def configuration_with_invalid_lines_general(context: Context) -> Optional[Tuple[str, ...]]:
    context.general_errors = None

    return context.general_errors


@fixture(name="fixture.config.text.error.multiple_errors")
def configuration_with_multiple_errors(context: Context) -> str:
    config_text = f"""
        # General parameters
        dir=

        # Other parameters
        # tblastx
        expect=0.1
        expectation
        invalid line 1

        # add_taxonomy
        taxonomy=X
        category=CAT

        # CGF_and_CGA_CDS_processing
        start_codons=ATG
        max_size_difference=10
        reference_file=
        invalid_line=2=not_valid
        pattern="."
        codon_table=1
        isoform_min_word_length=
        isoform_ref_size=
        =not_valid
    """

    context.config_text = config_text.strip()

    return config_text


@fixture(name="fixture.config.text.error.multiple_errors.lines")
def configuration_with_multiple_errors_lines(context: Context) -> Optional[Tuple[int, ...]]:
    context.line_errors = (1, 6, 7, 17, 22)

    return context.line_errors


@fixture(name="fixture.config.text.error.multiple_errors.general")
def configuration_with_multiple_errors_general(context: Context) -> Optional[Tuple[str, ...]]:
    context.general_errors = tuple([
        "Missing SEDA version",
        "Missing working directory (dir)"
    ])

    return context.general_errors


fixture_pipeline_errors: Dict[str, Callable[[], Any]] = {
    # Pipeline
    "fixture.pipeline.text.error.too_many_params": pipeline_with_too_many_params,
    "fixture.pipeline.text.error.not_supported_special": pipeline_with_not_supported_special,
    "fixture.pipeline.text.error.bad_special": pipeline_with_bad_special,
    "fixture.pipeline.text.error.non_integer_special": pipeline_with_non_integer_special,
    "fixture.pipeline.text.error.invalid_command": pipeline_with_invalid_command,
    "fixture.pipeline.text.error.multiple_errors": pipeline_with_multiple_errors,

    # Pipeline lines
    "fixture.pipeline.text.error.too_many_params.lines": pipeline_with_too_many_params_lines,
    "fixture.pipeline.text.error.not_supported_special.lines": pipeline_with_not_supported_special_lines,
    "fixture.pipeline.text.error.bad_special.lines": pipeline_with_bad_special_lines,
    "fixture.pipeline.text.error.non_integer_special.lines": pipeline_with_non_integer_special_lines,
    "fixture.pipeline.text.error.invalid_command.lines": pipeline_with_invalid_command_lines,
    "fixture.pipeline.text.error.multiple_errors.lines": pipeline_with_multiple_errors_lines,

    # Configuration
    "fixture.config.text.error.missing_seda": configuration_with_missing_seda,
    "fixture.config.text.error.missing_seda_version": configuration_with_missing_seda_version,
    "fixture.config.text.error.missing_dir": configuration_with_missing_dir,
    "fixture.config.text.error.missing_dir_value": configuration_with_missing_dir_value,
    "fixture.config.text.error.unsupported_param": configuration_with_unsupported_param,
    "fixture.config.text.error.invalid_lines": configuration_with_invalid_lines,
    "fixture.config.text.error.multiple_errors": configuration_with_multiple_errors,

    # Configuration lines
    "fixture.config.text.error.missing_seda.lines": configuration_with_missing_seda_lines,
    "fixture.config.text.error.missing_seda_version.lines": configuration_with_missing_seda_version_lines,
    "fixture.config.text.error.missing_dir.lines": configuration_with_missing_dir_lines,
    "fixture.config.text.error.missing_dir_value.lines": configuration_with_missing_dir_value_lines,
    "fixture.config.text.error.unsupported_param.lines": configuration_with_unsupported_param_lines,
    "fixture.config.text.error.invalid_lines.lines": configuration_with_invalid_lines_lines,
    "fixture.config.text.error.multiple_errors.lines": configuration_with_multiple_errors_lines,

    # Configuration general errors
    "fixture.config.text.error.missing_seda.general": configuration_with_missing_seda_general,
    "fixture.config.text.error.missing_seda_version.general": configuration_with_missing_seda_version_general,
    "fixture.config.text.error.missing_dir.general": configuration_with_missing_dir_general,
    "fixture.config.text.error.missing_dir_value.general": configuration_with_missing_dir_value_general,
    "fixture.config.text.error.unsupported_param.general": configuration_with_unsupported_param_general,
    "fixture.config.text.error.invalid_lines.general": configuration_with_invalid_lines_general,
    "fixture.config.text.error.multiple_errors.general": configuration_with_multiple_errors_general
}
