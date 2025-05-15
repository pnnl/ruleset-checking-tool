The following is an example of a JSON output file produced by the RCT.

```json
{
  "title": "ASHRAE STD 229P RULESET CHECKING TOOL",
  "purpose": "Project Testing Report",
  "tool_name": "PNNL RCT",
  "tool_version": "0.1.0",
  "ruleset": "ASHRAE 90.1-2019 Performance Rating Method (Appendix G)",
  "date_run": "2022-02-01T18:25:43-05:00",
  "schema_version": "0.29",
  "rpd_files": [
    {
      "ruleset_model_type": "USER",
      "file_name": "user_rmd.json"
    },
    {
      "ruleset_model_type": "PROPOSED",
      "file_name": "proposed_rmd.json"
    },
    {
      "ruleset_model_type": "BASELINE_0",
      "file_name": "baseline_rmd.json"
    },
    {
      "ruleset_model_type": "BASELINE_90",
      "file_name": "baseline_rmd.json"
    },
    {
      "ruleset_model_type": "BASELINE_180",
      "file_name": "baseline_rmd.json"
    },
    {
      "ruleset_model_type": "BASELINE_270",
      "file_name": "baseline_rmd.json"
    }
  ],
  "rules": [
    {
      "rule_id": "5-5",
      "description": "Baseline roof assemblies must match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8.",
      "evaluation_type": "FULL",
      "standard_section": "G3.1.2.2",
      "data_group_names": ["Surface"],
      "evaluations": [
        {
          "data_group_id": "Surface 1",
          "outcome": "PASS",
          "calculated_values": [
            {
              "variable": "roof_u_factor",
              "value": "0.06304743695121398",
              "unit": "Btu/(hr*ft2*R)",
              "source": "Baseline_0"
            },
            {
              "variable": "target_u_factor",
              "value": "0.063",
              "unit": "Btu/(hr*ft2*R)",
              "source": "Ruleset"
            },
            {
              "variable": "target_u_factor_res",
              "value": "None",
              "unit": ""
            },
            {
              "variable": "target_u_factor_nonres",
              "value": "None",
              "unit": ""
            }
          ]
        },
        {
          "data_group_id": "Surface 2",
          "outcome": "FAILED",
          "calculated_values": [
            {
              "variable": "roof_u_factor",
              "value": "0.07277854233600145",
              "unit": "Btu/(hr*ft2*R)",
              "source": "Baseline_0"
            },
            {
              "variable": "target_u_factor",
              "value": "0.063",
              "unit": "Btu/(hr*ft2*R)",
              "source": "Ruleset"
            },
            {
              "variable": "target_u_factor_res",
              "value": "None",
              "unit": ""
            },
            {
              "variable": "target_u_factor_nonres",
              "value": "None",
              "unit": ""
            }
          ]
        }
      ]
    }
  ]
}
```