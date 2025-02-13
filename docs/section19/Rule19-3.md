# Section 19 - Rule 19-3     
**Schema Version:** 0.1.3  
**Mandatory Rule:** True    
**Rule ID:** 19-3     
**Rule Description:** Weather conditions used in sizing runs to determine baseline equipment capacities shall be based on design days developed using 99.6% heating design temperatures and 1% dry-bulb and 1% wet-bulb cooling design temperatures.    
**Rule Assertion:** Options are Pass/Fail     
**Appendix G Section:** G3.1.2.2.1      
**90.1 Section Reference:** None  

**Data Lookup:** None  

**Evaluation Context:** Each RulesetProjectDescription

**Applicability Checks:** None  

**Function Calls:**  None

## Rule Logic:
- Get the weather for the ruleset project description: `weather = RulesetProjectDescription.weather`

- **Rule Assertion:**
- Case 1: If the correct design day options are populated in the RMD then pass: `if weather.cooling_dry_bulb_temp_design_day_type == "COOLING_1_0" and weather.heating_dry_bulb_temp_design_day_type == "HEATING_99_6" and weather.cooling_wet_bulb_temp_design_day_type == "COOLING_1_0": PASS`
- Case 2: else then FAIL: `else: FAIL`



**Notes/Questions:**  
1. This logic assumes the suggestion in Issue #327 will be implemented in the schema.

**[Back](_toc.md)**