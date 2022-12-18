# is_baseline_system_5  

**Description:** Get either Sys-5, Sys-5b, or Not_Sys_5 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 5 (Package VAV with Reheat) or system 5b (system 5 with purchased heating).  

**Inputs:**  
- **B-RMI**: To evaluate if the hvac system is modeled as either Sys-5, Sys-5b, or Not_Sys_5 in the B_RMI.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_5**: The function returns either Sys-5, Sys-5b, or Not_Sys_5 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 5 (Package VAV with Reheat) or system 5b (system 5 with purchased heating).   

**Function Call:**
1. does_each_zone_have_only_one_terminal()    
3. is_hvac_sys_cooling_type_DX()
4. is_hvac_sys_fan_sys_VSD()  
5. is_hvac_sys_preheating_type_fluid_loop()
6. is_hvac_sys_preheat_fluid_loop_attached_to_boiler()
7. is_hvac_sys_preheat_fluid_loop_purchased_heating()  
8. are_all_terminal_heat_sources_hot_water()  
9. are_all_terminal_heating_loops_attached_to_boiler()  
10. are_all_terminal_heating_loops_purchased_heating()  
11. are_all_terminal_cool_sources_none_or_null()
12. are_all_terminal_fans_null()  
13. are_all_terminal_types_VAV()


## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_5 = Not_Sys_5: `is_baseline_system_5 = "Not_Sys_5"`    
- Check that there is no heating system, if there is none then carry on: `if hvac_b.heating_system == "NONE" or hvac_b.heating_system.heating_system_type == "NONE":`    
    - Check that there is preheat system per G3.1.3.19, if there is then carry on: `if hvac_b.preheat_system is not "NONE":`   
        - Check if the preheat system is a fluid loop, if yes then carry on: `if is_hvac_sys_preheating_type_fluid_loop(B_RMI, hvac_b.id) == TRUE:`
            - Check that there is a cooling system: `if hvac_b.cooling_system != Null or hvac_b.cooling_system.cooling_system_type != "NONE":`  
                - Check if the cooling system type is DX, if yes then carry on: `if is_hvac_sys_cooling_type_DX(B_RMI, hvac_b.id) == TRUE:`  
                    - Check if fansystem is variable speed drive controlled, if yes then carry on: `if is_hvac_sys_fan_sys_VSD(B_RMI, hvac_b.id) == TRUE:`  
                        - Check that each zone only has one terminal unit: `if does_each_zone_have_only_one_terminal(B_RMI,zone_id_list) == TRUE:`     
                            - Check that the data elements associated with the terminal units align with system 5: `if are_all_terminal_heat_sources_hot_water(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_none_or_null(B_RMI,terminal_unit_id_list) == TRUE And are_all_terminal_fans_null(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_types_VAV(B_RMI,terminal_unit_id_list) == TRUE:`        
                                - if the preheat loop and all terminals are attached to a boiler then SYS-5: `if is_hvac_sys_preheat_fluid_loop_attached_to_boiler(B_RMI, hvac_b.id) == TRUE AND are_all_terminal_heating_loops_attached_to_boiler(B_RMI,terminal_unit_id_list) == TRUE: is_baseline_system_5 = "SYS-5"`
                                - elif the preheat loop and all terminals are purchased heating then SYS-5b: `elif is_hvac_sys_preheat_fluid_loop_purchased_heating(B_RMI, hvac_b.id) == TRUE and are_all_terminal_heating_loops_purchased_heating(B_RMI,terminal_unit_id_list) == TRUE:is_baseline_system_5 = "SYS-5b"`  


**Returns** `is_baseline_system_5`  



**[Back](../../_toc.md)**
