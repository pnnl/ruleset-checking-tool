The following is an example of a JSON output file produced by the RCT software testing workflow.

```json
{
	"title": "RULESET CHECKING TOOL",
	"purpose": "RCT Ruleset Software Testing Report",
	"ruleset": "ASHRAE 90.1-2019 Performance Rating Method (Appendix G)",
	"date_run": "2023-03-16T14:45:33-05:00",
	"schema_version": "0.0.23",
	"rule_tests":{
		"5-5-a": {
			"rule_id": "5-5",
			"test_id": "a",
			"test_description": "Building is located in climate zone 4A and includes a space that has residential occupancy type and is conditioned based on heating capacity of the HVAC system that servies the parent zone. The baseline roof U-factor for the space is established correctly.",
			"ruleset_section": "Table G3.1(5) Baseline Building Performance (b)",
			"ruleset_section_title": "Envelope",
            "evaluation": "Full / Applicability",
            "rule_unit_test_outcome_agreement": false,
            "expected_rule_unit_test_evaluation_outcome": "PASS",
            "actual_rule_unit_test_evaluation_outcome": "UNDETERMINED",
			"rule_unit_test_evaluation": [
				{
					"id": "Surface 1",
					"messages": "message",
                    "evaluation_outcome": "PASS",
					"calculated_values": {
						"roof_u_factor": "0.063 Btu/(hr*ft2*R)",
						"target_u_factor": "0.063 Btu/(hr*ft2*R)",
						"taregt_u_factor_nonres": null,
						"target_u_factor_res": null
					}
				},
				{
					"id": "Surface 2",
					"evaluation_outcome": "FAILED",
					"messages": "message",
					"calculated_values": {
						"roof_u_factor": "0.056 Btu/(hr*ft2*R)",
						"target_u_factor": "0.063 Btu/(hr*ft2*R)",
						"taregt_u_factor_nonres": null,
						"target_u_factor_res": null
					}
				},
				{
					"id": "Surface 3",
					"expected_test_outcome": "NOT_APPLICABLE",
					"test_outcome": "NOT_APPLICABLE",
					"messages": "message"
				},
				{
					"id": "Surface 4",
					"expected_test_outcome": "UNDETERMINED",
					"test_outcome": "UNDETERMINED",
					"messages": "message"
				}
			]
		}
	}
}
```
