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
- look at each SHW space type: `for shw_space_type in shw_and_spaces_dict:`
  - look at each space: `for space_id in shw_and_spaces_dict[shw_space_type]:`
    - get the space using get_component_by_id: `space = get_component_by_id(P_RMD, space_id)`
    - look for the ServiceWaterHeatingUse in the space.  If even one space has a ServiceWaterHeatingUse, continue to rule logic: `if len(space.service_water_heating_uses) > 0: CONTINUE TO RULE LOGIC`
  - if the program reaches this line without going to the rule logic, the project is not applicable for this SHW heating use: `NOT_APPLICABLE`

    ## Rule Logic: 
  - create a boolean to keep track of whether everything matches: `all_match = TRUE`
  - create an error string: `error_str = ""`
  - get a dictionary of all SHW equipment connected to the SHW space type in the baseline model: `b_shw_equipment_dict = get_SHW_equipment_connected_to_use_type(B_RMD)[shw_space_type]`
  - create a variable num_shw_systems = `len(b_shw_equip_dict)["SHWDistribution"]`

    ## Rule Assertion: 
    - Case1: there is exactly one system: PASS: `if num_shw_systems == 1: PASS`
    - Case2: all else, FAIL: `else: FAIL`

  
  **Notes:**
  1.  Are there configurations in which a complete SHW system could exist without SHWDistribution?

**[Back](../_toc.md)**
