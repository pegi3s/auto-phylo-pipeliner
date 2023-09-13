Feature: generating a pipeline file

  Scenario Outline: generate pipeline file
    Given a <pipeline> configuration
    When we generate a pipeline file
    Then we have a valid <pipeline_file> pipeline text

    Examples: Pipelines
      | pipeline | pipeline_file |
      | basic    | basic         |
      | advanced | advanced      |
