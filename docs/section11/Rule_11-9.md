# Service_Water_Heating - Rule 11-9
**Schema Version:** 0.0.38  

**Mandatory Rule:** FALSE

**Rule ID:** 11-9

**Rule Description:** "The baseline system must be sized according to Standard 90.1 2019, Section 7.4.1."  

**Rule Assertion:** UNDETERMINED / NOT_APPLICABLE

**Appendix G Section Reference:** Table G3.1 #11, proposed column, a

**Evaluation Context:** B-RMD each SHW BAT
**Data Lookup:**   
**Function Call:** 
- **get_spaces_associated_with_each_SWH_bat**

**Applicability Checks:**
- check that the SHW BAT in the B_RMD has SHW loads

## Applicability Checks:
- only projects with SHW for the SHW space BAT in the baseline model are applicable

- use the function get_spaces_associated_with_each_SWH_bat to get a list of spaces for each SHW BAT: `shw_and_spaces_dict = get_spaces_associated_with_each_SWH_bat(U_RMD)`
- look at each SHW space BAT: `for swh_bat in shw_and_spaces_dict:`
  - create a boolean rule_is_applicable and set it to false: `rule_is_applicable = false`
  - look at each space: `for space_id in shw_and_spaces_dict[swh_bat]:`
    - get the space using get_component_by_id: `space = get_component_by_id(U_RMD, space_id)`
    - look for the ServiceWaterHeatingUse in the space.  If even one space has a ServiceWaterHeatingUse, this rule is applicable: `if len(u.space.service_water_heating_uses) > 0: rule_is_applicable = true`
  ## Rule Assertion:
  - if the boolean rule_is_applicable is equal to true, the rule is applicable, return UNDETERMINED and a note letting the reviewer know what to check: `if rule_is_applicable: UNDETERMINED raise_message: "Check that the baseline Service Water Heating System for Building Area Type " + swh_bat + " is sized according to ASHRAE Standard 90.1 2019, Section 7.4.1."`
  - otherwise, rule is not applicable: `else: NOT_APPLICABLE`

**[Back](../_toc.md)**
