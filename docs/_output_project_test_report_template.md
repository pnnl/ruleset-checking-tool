The following is an example of a JSON output file produced by the RCT.

```json
{
    "title": "ASHRAE STD 229P RULESET CHECKING TOOL",
    "purpose": "Project Testing Report",
    "ruleset": "ASHRAE 90.1-2019 Performance Rating Method (Appendix G)",
    "date_run": "2022-02-01T18:25:43-05:00",
    "schema_version": "0.0.0",
    "rmd_files": [
      {
        "ruleset_model_type": "USER",
        "file_name": "user_rmr.json"
      },
      {
        "ruleset_model_type": "PROPOSED",
        "file_name": "proposed_rmr.json"
      },
      {
        "ruleset_model_type": "BASELINE",
        "file_name": "baseline_rmr.json"
      }
    ],
    "rules": [
        {
            "rule_id": "1-1",
            "description": "Description of rule 1-1.",
            "evaluation_type": "Full / Applicability",
            "ruleset_section": "G3.1.2.2",
\           "evaluations": [
                {
                    "evaluated_data_group_id": "wall 1",
                    "evaluation_outcome": "PASS",
                    "messages": ["informative message 1", "informative message 2"],
                    "calculated_values": [
                      {
                        "variable": "calculated_value1",
                        "value": 1.0
                      },
                      {
                        "variable": "calculated_value2",
                        "value": 2.0
                      }
                    ]
                },
                {
                    "evaluated_data_group_id": "wall 2",
                    "evaluation_outcome": "NOT_APPLICABLE",
                    "messages": ["informative message 1"],
                    "calculated_values": [
                        {
                        "variable": "calculated_value1",
                        "value": 1.0
                        }
                    ]
                },
                {
                    "evaluated_data_group_id": "wall 3",
                    "evaluation_outcome": "UNDETERMINED",
                    "messages": ["informative message 1"],
                    "calculated_values": [
                      {
                        "variable": "calculated_value1",
                        "value": 1.0
                      },
                      {
                        "variable": "calculated_value2",
                        "value": 2.0
                      }
                    ]
                },
                {
                    "evaluated_data_group_id": "wall 4",
                    "evaluation_outcome": "FAIL",
                    "messages": ["informative message 1"],
                    "calculated_values": [
                      {
                        "variable": "calculated_value1",
                        "value": 1.0
                      },
                      {
                        "variable": "calculated_value2",
                        "value": 2.0
                      }
                    ]
                }
            ]
        },
        {
            "rule_id": "1-2",
            "description": "Description of rule 1-2.",
            "evaluation_type": "APPLICABILITY",
            "ruleset_section": "G3.1.2.2",
            "evaluations": [
                {
                    "evaluated_data_group_id": "wall 1",
                    "outcome": "UNDETERMINED",
                    "messages": ["informative message 1"],
                    "calculated_values": [
                        {
                          "variable": "calculated_value1",
                          "value": 1.0
                        },
                        {
                          "variable": "calculated_value2",
                          "value": 2.0
                        }
                    ]
                }
            ]
        }
    ]
}
```