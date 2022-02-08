# get_proposed_hvac_modeled_with_virtual_cooling

**Description:** Get the list of HeatingVentilationAirAconditioningSystem in which Appendix G Table G3.1 #10 d is applicable.

**Inputs:**
- **U-RMR**: The U-RMR to determine if an HVAC system has been designed or modeled as existing and with cooling.
- **P-RMR**: To determine if the same HVAC system has been modeled with cooling in the P-RMR.

**Returns:**
- **proposed_hvac_modeled_with_virtual_cooling_list_p**: A list that saves all the HVAC systems in which Appendix G Table G3.1 #10 d are applicable (i.e. modeled with virtual cooling in the proposed).
 
**Function Call:** 

1. match_data_element()

**Logic:**
- For each building_segment in the U_RMR: `for building_segment_u in U_RMR:`
    - For each hvac_u in building_segment_u: `for hvac_u in building_segment_u:`
        - For each cooling_system_u in hvac_u: `for cooling_system_u in hvac_u:`
            - Check if the cooling_system_type = "None": `if cooling_system_u.cooling_system_type = "None":`
                - Get analogous cooling_system from the P-RMR: `cooling_system_p = match_data_element(P_RMR,CoolingSystem,cooling_system_u.id)`
                - Check if the analogous cooling_system is modeled with cooling in the P-RMR: `if cooling_system_p.cooling_system_type != "None":`
                    - If modeled with cooling then get the hvac id: `hvac_p = match_data_element(P_RMR,HeatingVentilationAirConditioningSystem,hvac_u.id)`
                    - If modeled with cooling then add to list of hvac systems modeled with virtual cooling in the proposed: `proposed_hvac_modeled_with_virtual_cooling_list_p = proposed_hvac_modeled_with_virtual_cooling_list_p.append(hvac_p.id)`
 
 - Convert the list of proposed_hvac_modeled_with_virtual_cooling_list_p to a set and the back to a list to eliminate duplicates after looping through all zones:
 `proposed_hvac_modeled_with_virtual_cooling_list_p = list(set(proposed_hvac_modeled_with_virtual_cooling_list_p))` 

 **Returns** `return proposed_hvac_modeled_with_virtual_cooling_list_p`  

**[Back](../_toc.md)**
