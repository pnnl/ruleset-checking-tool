# Service_Water_Heating - Rule 11-1
**Schema Version:** 0.0.37  

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
        - if the u_swh_use exists, continue to rule logic as we only need one SWH use to have this rule be applicable: `if(u_swh_use): CONTINUE TO RULE LOGIC #1`
    - if the program reaches this line without going to the rule logic, the project is not applicable for this SWH heating distribution system: `NOT_APPLICABLE`
- we also need to look at the distribution systems in the user model and ensure that all of them have been covered by the above checks.  If any exist (and have SWH use), but do not exist in the proposed model, then there is an issue: `for distribution_id in u_swh_system_and_equip_dict:`
    - check whether there are SWH uses connected to the distribution system: `if len(u_swh_system_and_equip_dict[distribution_id]["USES"]) > ):`
        - if uses exist, continue to rule logic #2: `CONTINUE TO RULE LOGIC #2`
    - if the program reaches this line without going to the rule logic, the project is not applicable for this SWH heating distribution system: `NOT_APPLICABLE`


    ## Rule Logic #1: 
  - create a list that the compare_context_pair function will use to send errors back tot he rule: `errors = []`
  - create the compare context string: `compare_context_str = "AppG 11-1 P_RMD Equals U_RMD"`
  - get a dictionary of all SWH equipment in the proposed model (pumps, distribution, tanks, SWH use, etc): `p_swh_equipment_dict = p_swh_system_and_equip_dict[distribution_id]`
  - get a dictionary of all SWH equipment in the user model (pumps, distribution, tanks, SWH use, etc): `u_swh_equipment_dict = u_swh_system_and_equip_dict[distribution_id]`
  - Compare the distribution in the proposed and user models using the function compare_context_pair.  compare_context_pair is recursive, so by sending the function the distribution systems, it is also checking the tanks and piping that are child objects of the distribution systems.  The boolean all_match is created and set to the result of the function: `all_match = compare_context_pair(distribution_id, distribution_id, $, extra_schema_for_SWH_comparison.json, true, compare_context_str, error_str)`
  - there's equipment that's part of the service water heating distribution system that are not direct child objects of teh distribution system.  We need to check these objects.
  - first, check ServiceWaterHeatingEquipment - when we execute compare_context_pair, this will also check any child objects that exist (SolarThermal and SWH validation point).  Start by checking if there are the same number of objects in the proposed and user models.  We need to do the length check here because it's not checked implicitly as part of compare_context_pair.  For example, if there are more pieces of equipment in the user model than the proposed, comparing each item found in the proposed model could return a false positive: `if len(p_swh_equipment_dict["SWHHeatingEq"]) == len(u_swh_equipment_dict["SWHHeatingEq"]):`
    - look at each SWHEquipment in the proposed model: `for swh_eq_id in p_swh_equipment_dict["SWHHeatingEq"]:`
      - compare the two SWH equipment using compare_context_pair, if the result is false, set all_match equal to false.  We won't exit early if all_match is false as we allow the function to keep running so errors is fully populated and available to the user: `if !compare_context_pair(swh_eq_id, swh_eq_id, $, extra_schema_for_SWH_comparison.json, true, compare_context_str, error_str): all_match = false`
  - next, check Pumps - this will also recursively check PumpOutputValidationPointPumpOutputValidationPoint: `if len(p_swh_equipment_dict["Pumps"]) == len(u_swh_equipment_dict["Pumps"]):`
    - look at each SWHEquipment in the proposed model: `for pump_id in p_swh_equipment_dict["Pumps"]:`
      - compare the two pumps using compare_context_pair, if the result is false, set all_match equal to false.  We won't exit early if all_match is false as we allow the function to keep running so errors is fully populated and available to the user: `if !compare_context_pair(pump_id, pump_id, $, extra_schema_for_SWH_comparison.json, true, compare_context_str, error_str): all_match = false`
     
        
    ## Rule Logic #2: 
  - The equipment exists in the user model, but not in the proposed model, all match is false: `all_match = false`
    

## Rule Assertion: 
- Case1: all elements are equal: PASS: `if all_match: PASS`
- Case2: all elements don't match, FAIL: `if !all_match: FAIL`

  
  **Notes:**
  1.  is there a situation where some of the equipment shouldn't be equal?  Solar hot water, for example? 

**[Back](../_toc.md)**
