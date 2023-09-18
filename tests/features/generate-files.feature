Feature: generating pipeline and config texts

  Scenario Outline: generate texts
    Given a <pipeline_id> configuration
    When we generate a configuration text for <seda> in <output_dir>
      And we generate a pipeline text
    Then we have a valid <config_text_id> configuration
      And we have a valid <pipeline_text_id> pipeline

    Examples: Pipelines
      | pipeline_id | seda             | output_dir      | config_text_id | pipeline_text_id |
      | basic       | seda:1.6.0-v2304 | basic_output    | basic          | basic            |
      | advanced    | seda:1.6.0-v2304 | advanced_output | advanced       | advanced         |
