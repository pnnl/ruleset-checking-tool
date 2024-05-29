# Service_Water_Heating - Rule 11-8
**Schema Version:** 0.0.36  

**Mandatory Rule:** TRUE

**Rule ID:** 11-8

**Rule Description:** "One system per building area type shall be modeled in the baseline."

**Rule Assertion:** Options are PASS/FAIL

**Appendix G Section Reference:** Table G3.1 #11, baseline column, a + b

**Evaluation Context:** B-RMD each SHW type
**Data Lookup:**   
**Function Call:** 
- **get_SHW_types_and_spaces**
- **get_SHW_equipment_connected_to_use_type**  

**Applicability Checks:**
- check that the SHW type in the P_RMD has SHW loads - **is P_RMD appropriate for the applicability check, or should it be B_RMD?**  

## Applicability Checks:
- only projects with SHW for the SHW space type in the proposed model are expected to have a SHW system in the baseline model.  If there is no SHW in the proposed model, we assume no SHW system is needed.
- use the function get_SHW_types_and_spaces to get a list of spaces for each SHW type: `shw_and_spaces_dict = get_SHW_types_and_spaces(P_RMD)`
- look at each SHW bat: `for shw_bat in shw_and_spaces_dict:`
  - look at each space: `for space_id in shw_and_spaces_dict[shw_bat]:`
    - get the space using get_component_by_id: `space = get_component_by_id(P_RMD, space_id)`
    - look for the ServiceWaterHeatingUse in the space.  If even one space has a ServiceWaterHeatingUse, continue to rule logic: `if len(space.service_water_heating_uses) > 0: CONTINUE TO RULE LOGIC`
  - if the program reaches this line without going to the rule logic, the project is not applicable for this SHW heating use: `NOT_APPLICABLE`

    ## Rule Logic: 
  - get a dictionary of all SHW equipment connected to the all SHW space bats in the baseline model: `b_shw_equipment_dict = get_SHW_equipment_connected_to_use_type(B_RMD)[shw_bat]`
  - get a dictionary of all SHW equipment connected to the current SHW space bats in the baseline model: `b_shw_equipment_dict_this_use = b_shw_equipment_dict[shw_bat]
  - create a variable num_swh_systems_this_use: `num_swh_systems = len(b_shw_equipment_dict_this_use["SHWDistribution"])`
  - create a boolean is_referenced_in_other_bats and set it to false: `is_referenced_in_other_bats = false`
  
  - if there is exactly one system, check that the system is not used in any of the other BATs: `if num_swh_systems == 1:`
    - create a variable shw_dist_id and set it to the id of the shw distribution equipment for this bat: `shw_dist_id = b_shw_equipment_dict_this_use["SHWDistribution"][0]`
    - loop through each bat: `for other_shw_bat in b_shw_equipment_dict:`
      - if other_shw_bat is not equal to the current shw_bat: `if other_shw_bat != shw_bat:`
        - check whether the shw_dist_id is in the list of SHW Distribution equipment for the other SHW_bat: `if shw_dist_id in? b_shw_equipment_dict[other_shw_bat]["SHWDistribution"]:`
          - set the boolean is_referenced_in_other_bats to true: `is_referenced_in_other_bats = true`

    ## Rule Assertion: 
    - Case1: there is exactly one system AND the system is not referenced by any other shw_bats: PASS: `if num_swh_systems == 1 && is_referenced_in_other_bats = false: PASS`
    - Case2: all else, FAIL: `else: FAIL`

  
  **Notes:**
  1.  Are there configurations in which a complete SHW system could exist without SHWDistribution? - ANSWER: distrbution_system is a required data element, so no.

**[Back](../_toc.md)**
