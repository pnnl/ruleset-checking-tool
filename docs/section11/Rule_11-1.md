# Service_Water_Heating - Rule 11-1
**Schema Version:** 0.0.36  

**Mandatory Rule:** TRUE

**Rule ID:** 11-1

**Rule Description:** "Where a complete service water-heating system exists, the proposed design shall reflect the actual system type. Where a service water-heating system has been designed the service waterheating type shall be consistent with design documents."

**Rule Assertion:** Options are PASS/FAIL

**Appendix G Section Reference:** Table G3.1 #11, proposed column, a & b

**Evaluation Context:** P-RMD each SWH Distribution
**Data Lookup:**   
**Function Call:** 
- **get_component_by_id**
- **compare_context_pair** - there is no RDS for this function, but it is a function developed for Rule 1-6 that compares two elements
- **get_SWH_equipment_associated_with_each_swh_distribution_system**  

**Applicability Checks:**
- check that the U_RMD has SWH Uses with loads

## Applicability Checks:
- only projects with SWH in the user model are expected to have a SWH system in the proposed model.  If there is no SWH in the user model, we assume there is no SWH system designed, and instead rule 11-3 Applies and P_RMD matches B_RMD.
- use the function get_SWH_equipment_associated_with_each_swh_distribution_system to get a dictionary of SWH equipment associated with each Distribution System for the Proposed model (pumps, tanks, SWH use, distribution system, etc): `p_swh_system_and_equip_dict = get_SWH_equipment_associated_with_each_swh_distribution_system(P_RMD)`
- use the function get_SWH_equipment_associated_with_each_swh_distribution_system to get a dictionary of SWH equipment associated with each Distribution System for the User model (pumps, tanks, SWH use, distribution system, etc): `u_swh_system_and_equip_dict = get_SWH_equipment_associated_with_each_swh_distribution_system(U_RMD)`
- for each distribution system: `for distribution_id in p_swh_system_and_equip_dict:`
    - get the distribution system: `p_distribution = get_component_by_id(P_RMD, distribution_id)`
    - for each swh use in the dictionary, check to see that the swh use exists in the user model: `for swh_use_id in p_swh_system_and_equip_dict[distribution_id]["USES"]:`
        - get the user swh_use: `u_swh_use = get_component_by_id(U_RMD, swh_use_id)`
        - if the u_swh_use exists, continue to rule logic as we only need one SWH use to have this rule be applicable: `if(u_swh_use): CONTINUE TO RULE LOGIC`
    - if the program reaches this line without going to the rule logic, the project is not applicable for this SWH heating distribution system: `NOT_APPLICABLE`

    ## Rule Logic: 
  - create a boolean to keep track of whether everything matches: `all_match = TRUE`
  - create an error string: `error_str = ""`
  - create the compare context string: `compare_context_str = "AppG 11-1 P_RMD Equals U_RMD"`
  - get a dictionary of all SWH equipment in the proposed model (pumps, distribution, tanks, SWH use, etc): `p_shw_equipment_dict = p_swh_system_and_equip_dict[distribution_id]`
  - get a dictionary of all SWH equipment in the user model (pumps, distribution, tanks, SWH use, etc): `u_shw_equipment_dict = u_swh_system_and_equip_dict[distribution_id]`
  - check if the u_shw_equipment exists: `if(u_swh_equipment_dict):`
    - Compare the distribution in the proposed and user models.  This check relies on the understanding that the RCT team has a method for comparing all elements within an object match (compare_context_pair): `if !compare_context_pair(distribution_id, distribution_id, $, extra_schema_for_SWH_comparison.json, true, compare_context_str, error_str): all_match = FALSE`
  - otherwise, the distribution equipment doesn't exist in the user model, set all_match to false: `all_match = FALSE; error_str += distribution_id + " not found in the user model"`
  - continue if all_match is still true: `if all_match`
    - create a list of all of the SWH equipment types that exist in both the proposed and user models: `shw_equipment_types = set(p_shw_equipment_dict.keys()) | set(u_shw_equipment_dict.keys())`
    - loop through each of the equipment types: `for shw_equipment_type in shw_equipment_types:`
      - continue if all_match is still true: `if all_match:`
        - check if this equipment type matches between the proposed and user models.  First check whether there are the same number equipment: `if len(p_shw_equipment_dict[shw_equipment_type]) == len(u_shw_equipment_dict[shw_equipment_type]):`
            - look at each equipment type system in the proposed model and see if there is one that is the same in the user model.  This check relies on the understanding that the RCT team has a method for comparing all elements within an object match (compare_context_pair): `for p_SWH_equip_id in p_shw_equipment_dict[shw_equipment_type]:`
                - if this system is in U_RMD.service_water_heating_distribution_systems, compare the systems: `if p_SWH_equip_id in u_shw_equipment_dict[shw_equipment_type]:`
                    - use compare_context_pair to compare systems and set all_match to FALSE if the systems don't compare: `if !compare_context_pair(p_SWH_equip_id, p_SWH_equip_id, $, extra_schema_for_SWH_comparison.json, true, compare_context_str, error_str): all_match = FALSE`
                - otherwise, set all_match to false: `else: all_match = FALSE`
        - otherwise, all_match is false: `all_match = FALSE`

## Rule Assertion: 
- Case1: all elements are equal: PASS: `if all_match: PASS`
- Case2: all elements don't match, FAIL: if !all_match: FAIL`

  
  **Notes:**
  1.  using compare_context_pair might not be the correct approach - this function requires data elements in the extra schema to have a tag "AppG P_RMD Equals U_RMD" - is it possible to pass in a custom json created for this rule which identifies which elements need to be equal?
  2.  is there a situation where some of the equipment shouldn't be equal?  Solar hot water, for example? 

**[Back](../_toc.md)**
