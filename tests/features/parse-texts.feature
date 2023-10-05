Feature: parsing texts

  Scenario Outline: parse pipeline text
    Given a <pipeline_id> pipeline text
    When we parse this pipeline text
    Then we have a valid pipeline

    Examples: Pipelines
      | pipeline_id |
      | basic       |
      | advanced    |

  Scenario Outline: parse configuration text
    Given a <pipeline_id> pipeline configuration text
    When we parse this configuration text
    Then we have a valid pipeline configuration

    Examples: Pipelines
      | pipeline_id |
      | basic       |
      | advanced    |

  Scenario Outline: parse run text
    Given a <pipeline_id> pipeline and a <run_id> run text
    When we parse the run text
    Then we have the auto phylo version in the text

    Examples: Pipelines
      | pipeline_id | run_id |
      | basic       | semver |
      | basic       | latest |
      | advanced    | semver |
      | advanced    | latest |

  Scenario Outline: parse a bad pipeline text
    Given a pipeline configuration text with a <pipeline_error_id> error
    When we parse this bad pipeline configuration text
    Then we have all the existent errors identified in the pipeline configuration

    Examples: Pipelines
      | pipeline_error_id     |
      | too_many_params       |
      | not_supported_special |
      | bad_special           |
      | non_integer_special   |
      | invalid_command       |
      | multiple_errors       |

  Scenario Outline: parse a bad configuration text
    Given a configuration text with a <config_error_id> error
    When we parse this bad configuration text
    Then we have all the existent errors identified in the configuration

    Examples: Pipelines
      | config_error_id      |
      | missing_seda         |
      | missing_seda_version |
      | missing_dir          |
      | missing_dir_value    |
      | unsupported_param    |
      | invalid_lines        |
      | multiple_errors      |

  Scenario Outline: parse a bad run text
    Given a run file text with a <run_file_error_id> error
    When we parse this bad run file text
    Then we have all the existent errors identified in the run file

    Examples: Pipelines
      | run_file_error_id |
      | missing_version   |
