# get_proposed_hvac_modeled_with_virtual_heating

**Description:** Get the list of HeatingVentilationAirAconditioningSystem in which Appendix G Table G3.1 #10 c is applicable (i.e. space heating is modeled in the P_RMR but not the U_RMR).  Table G3.1 #10 c states that "where no heating system exists or no heating system has been submitted with design documents, the system type shall be the same system as modeled in the baseline building design and shall comply with but not exceed the requirements of Section 6."   

**Inputs:**  
- **U-RMR**: The U-RMR to determine if an HVAC system has been designed or is existing with heating.  
- **P-RMR**: To determine if the same HVAC system has been modeled with heating in the P-RMR.  

**Returns:**  
- **proposed_hvac_modeled_with_virtual_heating_list_p**: A list that saves all the HVAC systems in which Appendix G Table G3.1 #10 c are applicable (i.e. modeled with virtual heating in the proposed).  
 
**Function Call:**   

1. match_data_element()  
2. match_data_element_exist()

## Logic:  
- For each hvac_p in the the P_RMR: `for hvac_p in P_RMR...HeatingVentilationAirConditioningSystem:`       
    - Reset has_virtual_heating_p boolean variable: `has_virtual_heating_p = FALSE`   
        Below compares the heating systems associated with the hvac system across the P_RMR and U_RMR only if heating was modeled in the proposed. If heating was modeled in the proposed and NOT in the U_RMR (the heating system type is None [or heating_system = Null] in the U_RMR) then this means virtual heating was modeled in the proposed. We are checking the preheat coils because baseline systems 5 through 8 have preheat coils. 
    - Check if there are any heating_system associated with hvac_p, if not skip to preheat check: `if hvac_p.heating_system != Null:`
        - For each heating_system_p in hvac_p: `for heating_system_p in hvac_p.heating_system:`
            - Check if "None" is NOT the heating_system_type for heating_system_p, if its not "None" (means heating was modeled) then get the analogous heating system in the U_RMR (if it exists) and check if the heating_system_type is "None" in the U_RMR: `if heating_system_p.heating_system_type != "None":`
                - Check if analogous heating system exists in the U_RMR: `if match_data_element_exist(U_RMR,HeatingSystem,heating_system_p.id) == TRUE:` 
                    - Get analogous heating system in U_RMR: `heating_system_u = match_data_element(U_RMR,HeatingSystem,heating_system_p.id)`
                    - Check if the analogous system in the U_RMR has a heating system type equal to "None", if it does then set the has_virtual_heating_p boolean variable to TRUE: `if heating_system_u.heating_system_type == "None": has_virtual_heating_p = TRUE`
                - Else, if the analogous heating system does not exist in the U_RMR, then set has_virtual_heating_p boolean variable to TRUE: `Else: has_virtual_heating_p = TRUE`
    - Check if has_virtual_heating_p = false, if it equals true then skip indented logic: `if has_virtual_heating_p == False:`
        - Check if there are any preheat_system associated with hvac_p, if not skip indented code: `if hvac_p.preheat_system != Null:`
            - For each preheat_system_p in hvac_p: `for preheat_system_p in hvac_p.preheat_system:`
                - Check if "None" is NOT the preheat_system_type for preheat_system_p, if its not "None" (means preheat was modeled) then get the analogous preheat system in the U_RMR (if it exists) and check if the preheat_system_type is "None" in the U_RMR: `if preheat_system_p.preheat_system_type != "None":`
                    - Check if analogous preheat system exists in the U_RMR: `if match_data_element_exist(U_RMR,HeatingSystem,preheat_system_p.id) == TRUE:` 
                        - Get analogous preheat system in U_RMR: `preheat_system_u = match_data_element(U_RMR,HeatingSystem,preheat_system_p.id)`
                        - Check if the analogous system in the U_RMR has a preheat system type equal to "None", if it does then set the has_virtual_preheat_p boolean variable to TRUE : `if preheat_system_u.preheat_system_type == "None": has_virtual_heating_p = TRUE`            
                    - Else, if the analogous preheat system does not exist in the U_RMR, then set has_virtual_heating_p boolean variable to TRUE: `Else: has_virtual_heating_p = TRUE`
    - Check if heating was modeled in the proposed via has_virtual_heating_p boolean variable (and not in the U_RMR) add hvac system to list: `if has_virtual_heating_p == TRUE: proposed_hvac_modeled_with_virtual_heating_list_p = proposed_hvac_modeled_with_virtual_heating_list_p.append(hvac_p.id)`   

 **Returns** `return proposed_hvac_modeled_with_virtual_heating_list_p`  

**[Back](../_toc.md)**