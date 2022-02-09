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
        - Reset U_RMR cooling is designed boolean to FALSE, equals true if cooling is designed: `cooling_designed_check_u = FALSE`
        - Reset P_RMR cooling is modeled boolean to FALSE, equals true if cooling is modeled: `cooling_modeled_check_p = FALSE`
        - For each cooling_system_u in hvac_u: `for cooling_system_u in hvac_u:`
            - Check if the cooling_system_type does not equal "None": `if cooling_system_u.cooling_system_type != "None":`
                - Set cooling_designed_check_u to true: `cooling_designed_check_u = TRUE`
        - Check if cooling is NOT designed for the hvac system in the U_RMR, cooling_designed_check_u = FALSE: `if cooling_designed_check_u == FALSE:`        
            - Get the analogous hvac id for the P_RMR: `hvac_p = match_data_element(P_RMR,HeatingVentilationAirConditioningSystem,hvac_u.id)`
                - For each cooling_system_p in hvac_p: `for cooling_system_p in hvac_p:`
                    - Check if the cooling_system_type does not equal "None": `if cooling_system_p.cooling_system_type != "None":`
                        - Set cooling_modeled_check_p to true: `cooling_modeled_check_p = TRUE`
                - If modeled with cooling in the P_RMR then add to list of hvac systems modeled with virtual cooling in the proposed: `if cooling_modeled_check_p == TRUE: proposed_hvac_modeled_with_virtual_cooling_list_p = proposed_hvac_modeled_with_virtual_cooling_list_p.append(hvac_p.id)`
    
**Returns** `return proposed_hvac_modeled_with_virtual_cooling_list_p`  

**[Back](../_toc.md)**
