# Service_Water_Heating - Rule 11-9
**Schema Version:** 0.0.38  

**Mandatory Rule:** FALSE

**Rule ID:** 11-9

**Rule Description:** "The baseline system must be sized according to Standard 90.1 2019, Section 7.4.1."  

**Rule Assertion:** Applicable / not applicable

**Appendix G Section Reference:** Table G3.1 #11, proposed column, a & b

**Evaluation Context:** B-RMD each SHW type
**Data Lookup:**   
**Function Call:** 
- **get_SHW_types_and_spaces**

**Applicability Checks:**
- check that the SHW type in the B_RMD has SHW loads

## Applicability Checks:
- only projects with SHW for the SHW space type in the baseline model are applicable
- use the function get_SHW_types_and_spaces to get a list of spaces for each SHW type: `shw_and_spaces_dict = get_SHW_types_and_spaces(U_RMD)`
- look at each SHW space type: `for shw_space_type in shw_and_spaces_dict:`
  - look at each space: `for space_id in shw_and_spaces_dict[shw_space_type]:`
    - get the space using get_component_by_id: `space = get_component_by_id(U_RMD, space_id)`
    - look for the ServiceWaterHeatingUse in the space.  If even one space has a ServiceWaterHeatingUse, this rule is applicable: `if len(u.space.service_water_heating_uses) > 0: APPLICABLE`
  - if the program reaches this line without going to the rule logic, the project is not applicable for this SHW heating use: `NOT_APPLICABLE`

**[Back](../_toc.md)**
