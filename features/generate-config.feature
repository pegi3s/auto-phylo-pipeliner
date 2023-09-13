Feature: generating a configuration file

  Scenario Outline: generate config file
    Given a <pipeline> configuration with parameters
    When we generate a configuration file for <seda> in <output_dir>
    Then we have a valid <config_file> configuration text

    Examples: Pipelines
      | pipeline | seda             | output_dir      | config_file |
      | basic    | seda:1.6.0-v2304 | basic_output    | basic       |
      | advanced | seda:1.6.0-v2304 | advanced_output | advanced    |
