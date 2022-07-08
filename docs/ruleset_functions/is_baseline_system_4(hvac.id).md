# is_baseline_system_4  

**Description:** Get either Sys-4 or Not_Sys_4 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 4 (PSZ-HP).  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as Sys-4 in the B_RMR.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_baseline_system_4**: The function returns either Sys-4 or Not_Sys_4 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 4 (PSZ-HP).  
 
**Function Call:** 
1. is_heating_type_heat_pump()
2. is_cooling_type_DX()
3. serves_single_zone()  
4. is_fan_CV()  
5. is_terminal_heat_source_none()  
6. is_terminal_cool_source_none()  
7. is_terminal_fan_null()  
8. is_terminal_type_CAV()  
9. is_terminal_supply_ducted()  
9. get_terminal_unit_for_SZ_baseline_HVAC()  


## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Check that there is no preheat system (it equals Null), if there is none then carry on: `if Len(hvac_b.preheat_system) == Null:`  
    - Check if heatingsystem is a heat pump, if it is then carry on: `if is_heating_type_heat_pump(B_RMR, hvac_b.id) == TRUE:`     
        - Check if the coolingsystem is DX, if it is then carry on: `if is_cooling_type_DX(B_RMR, hvac_b.id) == TRUE:`      
            - Check if fansystem is constant volume, if yes then carry on: `if is_fan_CV(B_RMR, hvac_b.id) == TRUE:`  
                - Check if the hvac system serves a single zone, if yes carry on: `if serves_single_zone(B_RMR, hvac_b.id) == TRUE:`   
                    - Get and create an object for the terminal unit associated with the zone: `terminal_b = get_terminal_unit_for_SZ_baseline_HVAC(B_RMR,hvac_b.id)`  
                    - Check that the terminal unit object does not equal Null: `if terminal_b != Null:`  
                        - Check that the data elements associated with the terminal unit align with system 4: `if is_terminal_heat_source_none(B_RMR,terminal_b.id) ==  TRUE AND is_terminal_cool_source_none(B_RMR,terminal_b.id) == TRUE And is_terminal_fan_null(B_RMR,terminal_b.id) == TRUE AND is_terminal_supply_ducted(B_RMR,terminal_b.id) == TRUE AND is_terminal_type_CAV(B_RMR, terminal_b.id) == TRUE:`
                            - Set is_baseline_system_4 equal to Sys-4: `is_baseline_system_4 = Sys-4`      
                        - Else, is_baseline_system_4 = "Not_Sys_4": `is_baseline_system_4 = Not_Sys_4`  
                    - Else, is_baseline_system_4 = "Not_Sys_4": `is_baseline_system_4 = Not_Sys_4`  
                - Else, is_baseline_system_4 = "Not_Sys_4": `is_baseline_system_4 = Not_Sys_4`
            - Else, is_baseline_system_4 = "Not_Sys_4": `is_baseline_system_4 = Not_Sys_4`
        - Else, is_baseline_system_4 = "Not_Sys_4": `is_baseline_system_4 = Not_Sys_4`
    - Else, is_baseline_system_4 = "Not_Sys_4": `is_baseline_system_4 = Not_Sys_4`
- Else, is_baseline_system_4 = "Not_Sys_4": `is_baseline_system_4 = Not_Sys_4`


**Returns** `is_baseline_system_4`  



**[Back](../_toc.md)**