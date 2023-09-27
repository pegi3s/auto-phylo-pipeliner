Feature: generating pipeline and config texts

  Scenario Outline: generate texts
    Given a <pipeline_id> pipeline configuration
    When we generate a configuration text
    And we generate a pipeline text
    Then we have a valid <pipeline_id> configuration text
    And we have a valid <pipeline_id> pipeline text

    Examples: Pipelines
      | pipeline_id |
      | basic       |
      | advanced    |
