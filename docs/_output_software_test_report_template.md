The following is an example of a JSON output file produced by the RCT software testing workflow.

```json
{
  "title": "RULESET CHECKING TOOL",
  "purpose": "RCT Ruleset Software Testing Report", 
  "tool_name": "PNNL RCT",
  "tool_version": "0.1.0",
  "ruleset": "ASHRAE 90.1-2019 Performance Rating Method (Appendix G)",
  "date_run": "2023-03-16T14:45:33-05:00",
  "schema_version": "0.0.29",
  "rule_tests":[
    {
      "rule_id": "5-5",
      "test_id": "a",
      "test_description": "Building is located in climate zone 4A and includes a space that has residential occupancy type and is conditioned based on heating capacity of the HVAC system that servies the parent zone. The baseline roof U-factor for the space is established correctly.",
      "ruleset_section": "Table G3.1(5) Baseline Building Performance (b)",
      "ruleset_section_title": "Envelope",
      "evaluation_type": "FULL",
      "rule_unit_test_outcome_agreement": true,
      "expected_rule_unit_test_evaluation_outcome": "PASS",
      "actual_rule_unit_test_evaluation_outcome": "PASS",
      "rule_unit_test_evaluations": [
        {
          "data_group_id": "Surface 1",
          "messages": "message",
          "evaluation_outcome": "PASS",
          "calculated_values": [
            {
              "variable": "roof_u_factor",
              "value": "0.063",
              "unit": "Btu/(hr*ft2*R)",
              "source": "Test Case"
            },
            {
              "variable": "target_u_factor",
              "value": "0.063",
              "unit": "Btu/(hr*ft2*R)",
              "source": "Standard"
            }
          ]
        }
      ]
    },
    {
      "rule_id": "5-5",
      "test_id": "b",
      "test_description": "Building is located in climate zone 4A and includes a space that has residential occupancy type and is conditioned based on heating capacity of the HVAC system that servies the parent zone. The baseline roof U-factor for the space is established incorrectly.",
      "ruleset_section": "Table G3.1(5) Baseline Building Performance (b)",
      "ruleset_section_title": "Envelope",
      "evaluation_type": "FULL",
      "rule_unit_test_outcome_agreement": true,
      "expected_rule_unit_test_evaluation_outcome": "FAILED",
      "actual_rule_unit_test_evaluation_outcome": "FAILED",
      "rule_unit_test_evaluations": [
        {
          "data_group_id": "Surface 1",
          "messages": "message",
          "evaluation_outcome": "FAILED",
          "calculated_values": [
            {
              "variable": "roof_u_factor",
              "value": "0.075",
              "unit": "Btu/(hr*ft2*R)",
              "source": "Test Case"
            },
            {
              "variable": "target_u_factor",
              "value": "0.063",
              "unit": "Btu/(hr*ft2*R)",
              "source": "Standard"
            }
          ]
        }
      ]
    }
  ]
}
```
