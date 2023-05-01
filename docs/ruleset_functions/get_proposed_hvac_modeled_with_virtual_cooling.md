# get_proposed_hvac_modeled_with_virtual_cooling  

**Schema Version:** 0.0.23
**Description:** Get the list of HeatingVentilationAirAconditioningSystem in which Appendix G Table G3.1 #10 d is applicable (i.e. space cooling is modeled in the P_RMI but not the U_RMI).  Table G3.1 #10 d states that "where no cooling system exists or no cooling system has
been submitted with design documents, the cooling system type shall be the same in the proposed as modeled in the baseline building design and shall comply with the requirements of Section 6."   

**Inputs:**  
- **U-RMI**: The U-RMI to determine if an HVAC system has been designed or modeled as existing and with cooling.  
- **P-RMI**: To determine if the same HVAC system has been modeled with cooling in the P-RMI.  

**Returns:**  
- **proposed_hvac_modeled_with_virtual_cooling_list_p**: A list that saves all the HVAC systems in which Appendix G Table G3.1 #10 d are applicable (i.e. modeled with virtual cooling in the proposed).  
 
**Function Call:**   

1. match_data_element()  
2. match_data_element_exist()  

## Logic:  
- For each hvac_p in the P_RMI: `for hvac_p in P_RMI...HeatingVentilatingAirConditioningSystem:`    
    - Reset has_virtual_cooling_p boolean variable: `has_virtual_cooling_p = FALSE`   
    - Check if there are any cooling_systems associated with hvac_p, if not skip indented code in the P_RMI: `if hvac_p.cooling_system != Null:`
        Below compares the cooling systems associated with the hvac system across the P_RMI and U_RMI only if cooling was modeled in the proposed. If cooling was modeled in the proposed and NOT in the U_RMI (the cooling system type is None [or cooling_system = Null] in the U_RMI) then this means virtual cooling was modeled in the proposed. 
        - Check if "None" is NOT the cooling_system_type for cooling_system_p, if its not "None" (means cooling was modeled) then get the analogous cooling system in the U_RMR and check if the cooling_system_type is "None" in the U_RMR: `if cooling_system_p.cooling_system_type != "None":`
          - Check if analogous cooling system exists in the U_RMR: `if match_data_element_exist(U_RMR,CoolingSystem,cooling_system_p.id) == TRUE:`I
            - Get analogous cooling system in U_RMR: `cooling_system_uI= match_data_element(U_RMR,CoolingSIstem,cooling_system_p.id)`
            - Check if analogous cooling system is modeledIwith cooling in the U_RMR: `if cooling_systemIu.cooling_system_type == "None": has_virtual_cooling_p = TRUE`  
          - Else, if analogous cooling system does not exist in the U_RMR then virtual coolIng is being modeled in the proposed: `Else:has_virtual_cooling_p = TRUE`
          I
    - Check if cooling was modeled in the proposed via has_virtual_cooling_p boolean variable (and not in the U_RMI) add hvac system to list: `if has_virtual_cooling_p == TRUE: proposed_hvac_modeled_with_virtual_cooling_list_p = proposed_hvac_modeled_with_virtual_cooling_list_p.append(hvac_p.id)`  

**Returns** `return proposed_hvac_modeled_with_virtual_cooling_list_p`  

**[Back](../_toc.md)**
