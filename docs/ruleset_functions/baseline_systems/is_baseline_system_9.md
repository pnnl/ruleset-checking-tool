# is_baseline_system_9  

**Description:** Get either Sys-9, Sys-9b, or Not_Sys_9 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 9 (Heating and Ventilation) or system 9b (system 9 with purchased heating).  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as either Sys-9, Sys-9b, or Not_Sys_9 in the B_RMR.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_9**: The function returns either Sys-9, Sys-9b, or Not_Sys_9 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 9 (Heating and Ventilation) or system 9b (system 9 with purchased heating).   
 
**Function Call:** 
1. is_hvac_sys_heating_type_fluid_loop()
2. is_hvac_sys_cooling_type_none()
3. is_hvac_sys_fan_sys_CV()  
4. is_hvac_sys_heating_type_furnace()
5. is_hvac_sys_fluid_loop_purchased_heating()
6. are_all_terminal_heat_sources_none_or_null()  
7. are_all_terminal_cool_sources_none_or_null() 
8. are_all_terminal_fans_null()  
9. are_all_terminal_types_CAV()   
10. does_each_zone_have_only_one_terminal()    
11. does_hvac_system_serve_single_zone()  
12. is_there_only_one_hvac_sys_heating_system ()  
13. is_baseline_system_9b()  

 
## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_9 = Not_Sys_9: `is_baseline_system_9 = "Not_Sys_9"`    
- Check if the system is system 9b, else carry on with logic: `if is_baseline_system_9b(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list) == TRUE: is_baseline_system_9 = "SYS-9b"` 
- Else: `Else:`    
    - Check that there is one heating system, if there is then carry on: `if is_there_only_one_hvac_sys_heating_system(B_RMR, hvac_b.id) == TRUE:`   
        - Check that there is no preheat system, if there is none then carry on: `if len(hvac_b.preheat_system) == Null or hvac_b.preheat_system[0].heating_system_type = "NONE" :`     
            - Check if fansystem is constant volume, if yes then carry on: `if is_hvac_sys_fan_sys_CV(B_RMR, hvac_b.id) == TRUE:`  
                - Check if the hvac system serves a single zone and that the zone only has one terminal unit: `if does_hvac_system_serve_single_zone(B_RMR, zone_id_list) == TRUE AND does_each_zone_have_only_one_terminal(B_RMR,zone_id_list) == TRUE:`     
                    - Check that the data elements associated with the terminal unit align with system 9: `if are_all_terminal_heat_sources_none_or_null(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_none_or_null(B_RMR,terminal_unit_id_list) == TRUE And are_all_terminal_fans_null(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_types_CAV(B_RMR,terminal_unit_id_list) == TRUE:`        
                        - if coolingsystem is None and the heating type is a furnace then Sys-9: `if is_hvac_sys_cooling_type_none(B_RMR, hvac_b.id) == TRUE AND is_hvac_sys_heating_type_furnace(B_RMR, hvac_b.id) == TRUE: is_baseline_system_9 = "Sys-9"`   

**Returns** `is_baseline_system_9`  



**[Back](../../_toc.md)**