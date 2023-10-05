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

  Scenario Outline: generate runs
    Given a <pipeline_id> pipeline configuration and a <run_id> type of version
    When we generate a run text
    Then we have a valid <run_id> run text

    Examples: Pipelines
      | pipeline_id | run_id |
      | basic       | semver |
      | basic       | latest |
      | advanced    | semver |
      | advanced    | latest |
