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
            "evalutions": [
                {
                    "id": 1,
                    "calculated_calculated_values": {
                        "calculated_value1": 1,
                        "calculated_value2": 0.5,
                        "calculated_value3": 100.0
                    },
                    "result": "PASS",

                },
                {
                    "id": 2,
                    "calculated_values": {
                        "calculated_value1": 2,
                        "calculated_value2": 0.75,
                        "calculated_value3": 1000.0
                    },
                    "result": "NOT_APPLICABLE",
                },
                {
                    "id": 3,
                    "calculated_values": {
                        "calculated_value1": 3,
                        "calculated_value2": 1.0,
                        "calculated_value3": 10000.0
                    },
                    "result": "UNDETERMINED",
                },
                {
                    "id": 4,
                    "calculated_values": {
                        "calculated_value1": 4,
                        "calculated_value2": 1.5,
                        "calculated_value3": 100000.0
                    },
                    "result": "FAIL",
                }
            ]
        },
        "rule_name2": {
            "evalutions": [
                {
                    "id": 1,
                    "calculated_calculated_values": {
                        "calculated_value1": 15.0,
                        "calculated_value2": 200.0,
                    },
                    "result": "PASS",

                },
            ]
        }
    }
}
```