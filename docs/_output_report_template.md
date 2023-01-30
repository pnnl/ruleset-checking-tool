The following is an example of a JSON output file produced by the RCT.

```json
{
    "title": "ASHRAE STD 229P RULESET CHECKING TOOL",
    "purpose": "Project Testing Report",
    "ruleset": "ASHRAE 90.1-2019 Performance Rating Method (Appendix G)",
    "date_run": "2022-02-01T18:25:43-05:00",
    "rmr_files": [
        "user_rmr.json",
        "baseline_rmr.json",
        "proposed_rmr.json"
    ],
    "rules": {
        "rule_name1": {
            "rule_id": 1-1,
            "description": "Description of rule 1-1.",
            "source_value_name": "USER_RMR",
            "expected_value_name": "PROPOSED_RMR",
            "assertion": "EQUALS",
            "primary_rule": "Y",
            "standard_section": "G3.1.2.2",
            "rule_evaluation_outcome": "PASS",
            "evaluations": [
                {
                    "id": 1,
                    "outcome": "PASS",
                    "messages": ["informative message 1", "informative message 2"],
                    "calculated_values": {
                        "calculated_value1": 1.0,
                        "calculated_value2": 0.5,
                        "calculated_value3": 100.0
                    }
                },
                {
                    "id": 2,
                    "outcome": "NOT_APPLICABLE",
                    "messages": ["informative message 1"],
                    "calculated_values": {
                        "calculated_value1": 2.0
                    }
                },
                {
                    "id": 3,
                    "outcome": "UNDETERMINED",
                    "messages": ["informative message 1"],
                    "calculated_values": {
                        "calculated_value1": 3.0,
                        "calculated_value2": 1.0,
                        "calculated_value3": 10000.0
                    }
                },
                {
                    "id": 4,
                    "outcome": "FAIL",
                    "messages": ["informative message 1"],
                    "calculated_values": {
                        "calculated_value1": 4.0,
                        "calculated_value2": 1.5,
                        "calculated_value3": 100000.0
                    }
                }
            ]
        },
        "rule_name2": {
            "rule_id": 1-2,
            "description": "Description of rule 1-2.",
            "ruleset_section_id": "1",
            "source_value_name": "USER_RMR",
            "expected_value_name": "wall_ufactor",
            "assertion": "EQUALS",
            "primary_rule": "Y",
            "standard_section": "G3.1.2.2",
            "rule_evaluation_outcome": "PASS",
            "evalutions": [
                {
                    "id": 1,
                    "outcome": "PASS",
                    "messages": ["informative message 1"],
                    "calculated_values": {
                        "calculated_value1": 15.0,
                        "calculated_value2": 200.0,
                    }
                },
            ]
        }
    }
}
```