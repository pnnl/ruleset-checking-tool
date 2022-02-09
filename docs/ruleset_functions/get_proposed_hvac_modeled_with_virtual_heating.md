# get_proposed_hvac_modeled_with_virtual_heating

**Description:** Get the list of HeatingVentilationAirAconditioningSystem in which Appendix G Table G3.1 #10 c is applicable.

**Inputs:**
- **U-RMR**: The U-RMR to determine if an HVAC system has been designed or is existing with heating.
- **P-RMR**: To determine if the same HVAC system has been modeled with heating in the P-RMR.

**Returns:**
- **proposed_hvac_modeled_with_virtual_heating_list_p**: A list that saves all the HVAC systems in which Appendix G Table G3.1 #10 c are applicable (i.e. modeled with virtual heating in the proposed).
 
**Function Call:** 

1. match_data_element()

**Logic:**
- For each building_segment_p in the P_RMR: `for building_segment_p in P_RMR:`
    - Get analogous segment in the U_RMR: `building_segment_u = match_data_element(U_RMR,BuildingSegment,building_segment_p.id)`
    - Get list of hvac systems in the U_RMR: `hvac_list_u = building_segment_u.heating_ventilation_air_conditioning_systems`
    - For each hvac_p in the building_segment_p: `for hvac_p in building_segment_p:`   
        # The line below will indicate a virtual HVAC system was modeled in the proposed
        - Check if the hvac system in the proposed design model is NOT in the U_RMR: `if hvac_p.id not in hvac_list_u:`
            - Reset virtual_heating_modeled_check_p boolean variable: `virtual_heating_modeled_check_p = FALSE`
            # Below checks if a heating system specifically was modeled (could just be cooling for this hvac system). Not checking the preheat coils because if no heating is specified in the design then the proposed should be modeled identically to the baseline and preheat coils are not applicable to any baseline systems.
            - For each heating_system_p in hvac_p: `for heating_system_p in hvac_p:`
                - Check if the heating_system_type != "None": `if heating_system_p.heating_system_type != "None":`
                    - Set virtual_heating_modeled_check_p to true: `virtual_heating_modeled_check_p = TRUE`
            - Check if heating was modeled in the proposed via virtual_heating_modeled_check_p boolean variable (and not in the U_RMR) add hvac system to list: `if virtual_heating_modeled_check_p == TRUE: proposed_hvac_modeled_with_virtual_heating_list_p = proposed_hvac_modeled_with_virtual_heating_list_p.append(hvac_p.id)`
        - Else, the hvac system in the proposed design model is in the U_RMR: `Else:`
            - Reset virtual_heating_modeled_check_p boolean variable: `virtual_heating_modeled_check_p = FALSE`
            # Below compared the heating systems associated with the hvac system across the P_RMR and U_RMR if heating was modeled in the proposed. If heating was modeled in the proposed and in the U_RMR the heating system type is None then this means virtual heating was modeled in the proposed. Not checking the preheat coils because if no heating is specified in the design then the proposed should be modeled identically to the baseline and preheat coils are not applicable to any baseline systems.
            - For each heating_system_p in hvac_p: `for heating_system_p in hvac_p:`
                - Check if "None" is NOT the heating_system_type for heating_system_p, if its not "None" (means heating was modeled) then get the analogous heating system in the U_RMR and check if the heating_system_type is "None" in the U_RMR: `if heating_system_p.heating_system_type != "None":`
                    - Get analogous heating system in U_RMR: `heating_system_u = match_data_element(U_RMR,HeatingSystem,heating_system_p.id)`
                    - Check if the analogous system in the U_RMR has a heating system type equal to "None", if it does then set the virtual_heating_modeled_check_p boolean variable to TRUE : `if heating_system_u.heating_system_type == "None": virtual_heating_modeled_check_p = TRUE`
            - Check if heating was modeled in the proposed via virtual_heating_modeled_check_p boolean variable (and not in the U_RMR) add hvac system to list: `if virtual_heating_modeled_check_p == TRUE: proposed_hvac_modeled_with_virtual_heating_list_p = proposed_hvac_modeled_with_virtual_heating_list_p.append(hvac_p.id)`
 # Below checks if a terminal unit exists in both the P_RMR but not U_RMR. If there is a mismatch then the HVAC system associated with the terminal unit is added to the list of HVAC systems in which virtual heating was modeled in the proposed. If the terminal unit exists in both then it is checked to see if both have heating. If there is a mismatch the HVAC system associated with the terminal unit is added to the list of HVAC systems with virtual heating modeled in the proposed.

- For each zone in P_RMR: `for zone_p in P_RMR...zones:`
    - For each terminal in zone_p: `for terminal_p in zone_p.terminals:` 


 **Returns** `return proposed_hvac_modeled_with_virtual_heating_list_p`  

**[Back](../_toc.md)**