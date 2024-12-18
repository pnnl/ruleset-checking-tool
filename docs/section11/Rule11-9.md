# Service_Water_Heating - Rule 11-9
**Schema Version:** 0.0.38  

**Mandatory Rule:** FALSE

**Rule ID:** 11-9

**Rule Description:** The baseline system must be sized according to Standard 90.1 2019, Section 7.4.1.  

**Rule Assertion:** UNDETERMINED / NOT_APPLICABLE

**Appendix G Section Reference:** Table G3.1 #11, baseline column, a

**Evaluation Context:** B-RMD each SHW BAT  
**Data Lookup:**   
**Function Call:** 
- **get_SWH_bats_and_SWH_use**

**Applicability Checks:**
- check that the SHW BAT in the B_RMD has SHW loads

## Applicability Checks:
- only projects with SHW use for the SHW space BAT in the baseline model are applicable
- create boolean rule_is_applicable and set it to false: `rule_is_applicable = FALSE`
- use the function get_SWH_bats_and_SWH_use to get a list of SWH uses for each BAT: `shw_bat_uses_dict = get_SWH_bats_and_SWH_use(B_RMD)`
- look at each SHW BAT: `for swh_bat in shw_bat_uses_dict:`
  - look at the uses in this swh bat: `for swh_use_id in shw_bat_uses_dict[swh_bat]:`
    - get the swh use: `swh_use = get_component_by_id(B_RMD, ServiceWaterHeatingUse)`
    - if even one use is greater than zero, go to rule assertion: `if swh_use.use > 0: `
      - set rule_is_applicable to true and go to the rule assertion: `rule_is_applicable = TRUE`
      - `GO TO RULE ASSERTION`
- if we reach here without finding a swh use, go to rule assertion: `GO TO RULE ASSERTION`
      
  ## Rule Assertion:
  - if the boolean rule_is_applicable is equal to true, the rule is applicable, return UNDETERMINED and a note letting the reviewer know what to check: `if rule_is_applicable: UNDETERMINED raise_message: "Check that the baseline Service Water Heating System for Building Area Type " + swh_bat + " is sized according to ASHRAE Standard 90.1 2019, Section 7.4.1."`
  - otherwise, rule is not applicable: `else: NOT_APPLICABLE`

**[Back](../_toc.md)**
