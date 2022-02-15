# get_proposed_hvac_modeled_with_virtual_cooling  

**Description:** Get the list of HeatingVentilationAirAconditioningSystem in which Appendix G Table G3.1 #10 d is applicable.  

**Inputs:**  
- **U-RMR**: The U-RMR to determine if an HVAC system has been designed or modeled as existing and with cooling.  
- **P-RMR**: To determine if the same HVAC system has been modeled with cooling in the P-RMR.  

**Returns:**  
- **proposed_hvac_modeled_with_virtual_cooling_list_p**: A list that saves all the HVAC systems in which Appendix G Table G3.1 #10 d are applicable (i.e. modeled with virtual cooling in the proposed).  
 
**Function Call:**   

1. match_data_element()  

## Logic:  
- For each building_segment_p in the P_RMR..BuildingSegment: `for building_segment_p in P_RMR...BuildingSegment:`
    - Get analogous segment in the U_RMR: `building_segment_u = match_data_element(U_RMR,BuildingSegment,building_segment_p.id)`
    - Get list of hvac systems in the U_RMR: `hvac_list_u = building_segment_u.cooling_ventilation_air_conditioning_systems`
    - For each hvac_p in the building_segment_p: `for hvac_p in building_segment_p.heating_ventilation_air_conditioning_systems:`    
        The line below will check if a virtual HVAC system was modeled in the proposed. If the hvac_p is not in the U_RMR then its a virtual system.
        - Check if the hvac system in the proposed design model is NOT in the U_RMR: `if hvac_p.id not in hvac_list_u:`
            - Reset virtual_cooling_modeled_check_p boolean variable: `virtual_cooling_modeled_check_p = FALSE`   
            Below checks if a cooling system specifically was modeled (could just be heating for this hvac system) for the vitual system in the proposed. 
            - For each cooling_system_p in hvac_p: `for cooling_system_p in hvac_p.cooling_system:`
                - Check if the cooling_system_type != "None": `if cooling_system_p.cooling_system_type != "None":`
                    - Set virtual_cooling_modeled_check_p to true: `virtual_cooling_modeled_check_p = TRUE`
            - Check if cooling was modeled in the proposed via the virtual_cooling_modeled_check_p boolean variable and add the hvac system to the list with virtual cooling if it was: `if virtual_cooling_modeled_check_p == TRUE: proposed_hvac_modeled_with_virtual_cooling_list_p = proposed_hvac_modeled_with_virtual_cooling_list_p.append(hvac_p.id)`
        - Else, the hvac system in the proposed design model is also in the U_RMR: `Else:`
            - Reset virtual_cooling_modeled_check_p boolean variable: `virtual_cooling_modeled_check_p = FALSE`   
            Below compares the cooling systems associated with the hvac system across the P_RMR and U_RMR only if cooling was modeled in the proposed. If cooling was modeled in the proposed and NOT in the U_RMR (the cooling system type is None in the U_RMR) then this means virtual cooling was modeled in the proposed. 
            - For each cooling_system_p in hvac_p: `for cooling_system_p in hvac_p.cooling_system:`
                - Check if "None" is NOT the cooling_system_type for cooling_system_p, if its not "None" (means cooling was modeled) then get the analogous cooling system in the U_RMR and check if the cooling_system_type is "None" in the U_RMR: `if cooling_system_p.cooling_system_type != "None":`
                    - Get analogous cooling system in U_RMR: `cooling_system_u = match_data_element(U_RMR,CoolingSystem,cooling_system_p.id)`
                    - Check if the analogous system in the U_RMR has a cooling system type equal to "None", if it does then set the virtual_cooling_modeled_check_p boolean variable to TRUE : `if cooling_system_u.cooling_system_type == "None": virtual_cooling_modeled_check_p = TRUE`
            - Check if cooling was modeled in the proposed via virtual_cooling_modeled_check_p boolean variable (and not in the U_RMR) add hvac system to list: `if virtual_cooling_modeled_check_p == TRUE: proposed_hvac_modeled_with_virtual_cooling_list_p = proposed_hvac_modeled_with_virtual_cooling_list_p.append(hvac_p.id)`  

**Returns** `return proposed_hvac_modeled_with_virtual_cooling_list_p`  

**[Back](../_toc.md)**
