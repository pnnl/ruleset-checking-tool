# is_baseline_system_4  

**Description:** Get either Sys-4 or Not_Sys_4 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 4 (PSZ-HP).  

**Inputs:**  
- **B_RMI**: To evaluate if the hvac system is modeled as Sys-4 in the B_RMR.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.   

**Returns:**  
- **is_baseline_system_4**: The function returns either Sys-4 or Not_Sys_4 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 4 (PSZ-HP).  

**Function Call:**
1. is_hvac_sys_heating_type_heat_pump()
2. is_hvac_sys_cooling_type_DX()
3. is_hvac_sys_fan_sys_CV()  
4. are_all_terminal_heat_sources_none_or_null()  
5. are_all_terminal_cool_sources_none_or_null()
6. are_all_terminal_fans_null()  
7. are_all_terminal_types_CAV()  
8. are_all_terminal_supplies_ducted()  
9. does_each_zone_have_only_one_terminal()   
10. does_hvac_system_serve_single_zone()   


## Logic:    
- Set is_baseline_system_4 = Not_Sys_4: `is_baseline_system_4 = "Not_Sys_4"`
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Check that there is no preheat system, if there is none then carry on: `if hvac_b.preheat_system == "NONE" or hvac_b.preheat_system.heating_system_type == "NONE" :`   
    - Check if heatingsystem is a heat pump, if it is then carry on: `if is_hvac_sys_heating_type_heat_pump(B_RMR, hvac_b.id) == TRUE:`     
        - Check if the coolingsystem is DX, if it is then carry on: `if is_hvac_sys_cooling_type_DX(B_RMR, hvac_b.id) == TRUE:`      
            - Check if fansystem is constant volume, if yes then carry on: `if is_hvac_sys_fan_sys_CV(B_RMR, hvac_b.id) == TRUE:`  
                - Check if the hvac system serves a single zone and that the zone only has one terminal unit: `if does_hvac_system_serve_single_zone(B_RMR, zone_id_list) == TRUE AND does_each_zone_have_only_one_terminal(B_RMR,zone_id_list) == TRUE:`  
                    - Check that the data elements associated with the terminal unit align with system 4: `if are_all_terminal_heat_sources_none_or_null(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_none_or_null(B_RMR,terminal_unit_id_list) == TRUE And are_all_terminal_fans_null(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_supplies_ducted(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_types_CAV(B_RMR,terminal_unit_id_list) == TRUE: is_baseline_system_4 = "Sys-4"`      


**Returns** `is_baseline_system_4`  



**[Back](../../_toc.md)**
