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
        - Reset U_RMR heating is designed boolean to FALSE, equals true if heating is designed: `heating_designed_check_u = FALSE`
        - Reset P_RMR heating is modeled boolean to FALSE, equals true if heating is modeled: `heating_modeled_check_p = FALSE`
        - For each heating_system_u in hvac_u: `for heating_system_u in hvac_u:`
            - Check if the heating_system_type != "None": `if heating_system_u.heating_system_type != "None":`
                - Set heating_designed_check_u to true: `heating_designed_check_u = TRUE`
        - Check if heating_designed_check_u = FALSE: `if heating_designed_check_u == FALSE:`
            - For each preheat_system_u in hvac_u: `for preheat_system_u in hvac_u:`
                - Check if the preheat_system_type != "None": `if preheat_system_u.heating_system_type != "None":`  
                    - Set heating_designed_check_u to true: `heating_designed_check_u = TRUE`
        - Check if heating is NOT designed for the hvac system in the U_RMR, heating_designed_check_u = FALSE: `if heating_designed_check_u == FALSE:`        
            - Get the analogous hvac id for the P_RMR: `hvac_p = match_data_element(P_RMR,HeatingVentilationAirConditioningSystem,hvac_u.id)`
            - For each heating_system_p in hvac_p: `for heating_system_p in hvac_p:`
                - Check if the heating_system_type != "None": `if heating_system_p.heating_system_type != "None":`
                    - Set heating_modeled_check_p to true: `heating_modeled_check_p = TRUE`
            - Check if heating_modeled_check_p = FALSE: `if heating_modeled_check_p == FALSE:`
                - For each preheat_system_p in hvac_p: `for preheat_system_p in hvac_p:`
                    - Check if the preheat_system_type != "None": `if preheat_system_p.heating_system_type != "None":`  
                        - Set heating_modeled_check_p to true: `heating_modeled_check_p = TRUE`
                - Check if heating_modeled_check_p equals true then add to list of hvac systems if it does: `if heating_modeled_check_p == TRUE: proposed_hvac_modeled_with_virtual_heating_list_p = proposed_hvac_modeled_with_virtual_heating_list_p.append(hvac_p.id)`
 
 **Returns** `return proposed_hvac_modeled_with_virtual_heating_list_p`  

**[Back](../_toc.md)**