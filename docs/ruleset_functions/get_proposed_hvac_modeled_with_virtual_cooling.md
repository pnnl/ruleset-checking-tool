# get_proposed_hvac_modeled_with_virtual_cooling  

**Description:** Get the list of HeatingVentilationAirAconditioningSystem in which Appendix G Table G3.1 #10 d is applicable (i.e. space cooling is modeled in the P_RMR but not the U_RMR).  Table G3.1 #10 d states that "where no cooling system exists or no cooling system has
been submitted with design documents, the cooling system type shall be the same in the proposed as modeled in the baseline building design and shall comply with the requirements of Section 6."   

**Inputs:**  
- **U-RMR**: The U-RMR to determine if an HVAC system has been designed or modeled as existing and with cooling.  
- **P-RMR**: To determine if the same HVAC system has been modeled with cooling in the P-RMR.  

**Returns:**  
- **proposed_hvac_modeled_with_virtual_cooling_list_p**: A list that saves all the HVAC systems in which Appendix G Table G3.1 #10 d are applicable (i.e. modeled with virtual cooling in the proposed).  
 
**Function Call:**   

1. match_data_element()  
2. match_data_element_exist()  

## Logic:  
- For each building_segment_p in the P_RMR...BuildingSegment: `for building_segment_p in P_RMR...BuildingSegment:`
    - Get analogous segment in the U_RMR: `building_segment_u = match_data_element(U_RMR,BuildingSegment,building_segment_p.id)`
    - Get list of hvac systems in the U_RMR: `hvac_list_u = building_segment_u.cooling_ventilation_air_conditioning_system`
    - For each hvac_p in the building_segment_p: `for hvac_p in building_segment_p.heating_ventilation_air_conditioning_system:`    
        - Reset has_virtual_cooling_p boolean variable: `has_virtual_cooling_p = FALSE`   
        - Check if there are any cooling_systems associated with hvac_p, if not skip indented code: `if hvac_p.cooling_system != Null:`
            Below compares the cooling systems associated with the hvac system across the P_RMR and U_RMR only if cooling was modeled in the proposed. If cooling was modeled in the proposed and NOT in the U_RMR (the cooling system type is None in the U_RMR) then this means virtual cooling was modeled in the proposed. 
            - For each cooling_system_p in hvac_p: `for cooling_system_p in hvac_p.cooling_system:`
                - Check if "None" is NOT the cooling_system_type for cooling_system_p, if its not "None" (means cooling was modeled) then get the analogous cooling system in the U_RMR and check if the cooling_system_type is "None" in the U_RMR: `if cooling_system_p.cooling_system_type != "None":`
                    - Check if analogous cooling system exists in the U_RMR: `if match_data_element_exist(U_RMR,CoolingSystem,cooling_system_p.id) == TRUE:` 
                        - Get analogous cooling system in U_RMR: `cooling_system_u = match_data_element(U_RMR,CoolingSystem,cooling_system_p.id)`
                        - Check if analogous cooling system is modeled with cooling in the U_RMR: `if cooling_system_u.cooling_system_type == "None": has_virtual_cooling_p = TRUE`  
                    - Else, if analogous cooling system does not exist in the U_RMR then virtual cooling is being modeled in the proposed: `Else:has_virtual_cooling_p = TRUE`
                    
        - Check if cooling was modeled in the proposed via has_virtual_cooling_p boolean variable (and not in the U_RMR) add hvac system to list: `if has_virtual_cooling_p == TRUE: proposed_hvac_modeled_with_virtual_cooling_list_p = proposed_hvac_modeled_with_virtual_cooling_list_p.append(hvac_p.id)`  

**Returns** `return proposed_hvac_modeled_with_virtual_cooling_list_p`  

**[Back](../_toc.md)**
