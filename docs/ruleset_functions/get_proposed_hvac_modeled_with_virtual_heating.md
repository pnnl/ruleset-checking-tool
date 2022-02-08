# get_proposed_hvac_modeled_with_virtual_heating

**Description:** Get the list of HeatingVentilationAirAconditioningSystem in which Appendix G Table G3.1 #10 c is applicable.

**Inputs:**
- **U-RMR**: The U-RMR to determine if an HVAC system has been designed or modeled as existing and with heating.
- **P-RMR**: To determine if the same HVAC system has been modeled with heating in the P-RMR.

**Returns:**
- **proposed_hvac_modeled_with_virtual_heating_list_p**: A list that saves all the HVAC systems in which Appendix G Table G3.1 #10 c are applicable (i.e. modeled with virtual heating in the proposed).
 
**Function Call:** 

1. match_data_element()

**Logic:**
- For each building_segment in the U_RMR: `for building_segment_u in U_RMR:`
    - For each hvac_u in building_segment_u: `for hvac_u in building_segment_u:`
        - Reset applicability flag: `rule_applicability_check = FALSE`
        - For each heating_system_u in hvac_u: `for heating_system_u in hvac_u:`
            - Check if the heating_system_type = "None": `if heating_system_u.heating_system_type = "None":`
                - Get analogous heating_system from the P-RMR: `heating_system_p = match_data_element(P_RMR,HeatingSystem,heating_system_u.id)`
                - Check if the analogous heating_system is modeled with heating in the P-RMR: `if heating_system_p.heating_system_type != "None":`
                    - Set applicability applicability_flag to TRUE: `rule_applicability_check = TRUE`
                    - If modeled with heating then get the hvac id: `hvac_p = match_data_element(P_RMR,HeatingVentilationAirConditioningSystem,hvac_u.id)`
                    - If modeled with heating then add to list of hvac systems modeled with virtual heating in the proposed: `proposed_hvac_modeled_with_virtual_heating_list_p = proposed_hvac_modeled_with_virtual_heating_list_p.append(hvac_p.id)`
        - Check if applicability check equal False, if it does then carry on otherwise move to next hvac system: `if rule_applicability_check == FALSE:`
            - For each preheat_system_u in hvac_u: `for preheat_system_u in hvac_u:`
                - Check if the preheat_system_type = "None": `if preheat_system_u.heating_system_type = "None":`
                    - Get analogous preheat_system from the P-RMR: `preheat_system_p = match_data_element(P_RMR,HeatingSystem,preheat_system_u.id)`
                    - Check if the analogous preheat_system is modeled with heating in the P-RMR: `if preheat_system_p.heating_system_type != "None":`
                        - If modeled with preheat then get the hvac id: `hvac_p = match_data_element(P_RMR,HeatingVentilationAirConditioningSystem,hvac_u.id)`
                        - If modeled with preheat then add to list of hvac systems modeled with virtual heating in the proposed: `proposed_hvac_modeled_with_virtual_heating_list_p = proposed_hvac_modeled_with_virtual_heating_list_p.append(hvac_p.id)`
 
 # Duplicates are unlikely unless there are multiple coils modeled for heating and preheating   
 - Convert the list of proposed_hvac_modeled_with_virtual_heating_list_p to a set and the back to a list to eliminate duplicates after looping through all zones:
 `proposed_hvac_modeled_with_virtual_heating_list_p = list(set(proposed_hvac_modeled_with_virtual_heating_list_p))` 

 **Returns** `return proposed_hvac_modeled_with_virtual_heating_list_p`  

**[Back](../_toc.md)**