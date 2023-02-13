# is_baseline_system_7  

**Description:** Get either Sys-7, Sys-7a, Sys-7b, Sys-7c or Not_Sys_7 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 7 (VAV with Reheat), system 7a (system 7 with purchased CHW), system 7b (system 7 with purchased heating), pr system 7c (system 7 with purchased heating and purchased CHW).  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as either Sys-7, Sys-7a, Sys-7b, Sys-7c or Not_Sys_7 in the B_RMR.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_7**: The function returns either Sys-7, Sys-7a, Sys-7b, Sys-7c or Not_Sys_7 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 7 (VAV with Reheat), system 7a (system 7 with purchased CHW), system 7b (system 7 with purchased heating), pr system 7c (system 7 with purchased heating and purchased CHW).   
 
**Function Call:** 
1. does_each_zone_have_only_one_terminal()    
3. is_hvac_sys_fluid_loop_purchased_CHW()
4. is_hvac_sys_cooling_type_fluid_loop()
5. is_hvac_sys_fluid_loop_attached_to_chiller()
6. is_hvac_sys_preheating_type_fluid_loop()
7. is_hvac_sys_preheat_fluid_loop_attached_to_boiler()
8. is_hvac_sys_preheat_fluid_loop_purchased_heating() 
9. is_hvac_sys_fan_sys_VSD()  
10. are_all_terminal_heat_sources_hot_water()  
11. are_all_terminal_heating_loops_attached_to_boiler()  
12. are_all_terminal_heating_loops_purchased_heating()  
13. are_all_terminal_cool_sources_none_or_null() 
14. are_all_terminal_fans_null()  
15. are_all_terminal_types_VAV()  
 
## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_7 = Not_Sys_7: `is_baseline_system_7 = "Not_Sys_7"`    
- Check that there is no heating system, if there is none then carry on: `if hvac_b.heating_system == Null or hvac_b.heating_system.heating_system_type == "NONE":`    
    - Check that there is one preheat system per G3.1.3.19, if there is then carry on: `if hvac_b.preheat_system != Null:`   
        - Check if the preheat system is a fluid loop, if yes then carry on: `if is_hvac_sys_preheating_type_fluid_loop(B_RMR, hvac_b.id) == TRUE:`
            - Check that there is only one cooling system: `if hvac_b.cooling_system == TRUE:` 
                - Check if the cooling system type is a fluid loop, if yes then carry on: `if is_hvac_sys_cooling_type_fluid_loop(B_RMR, hvac_b.id) == TRUE:`  
                    - Check if fansystem is variable speed drive controlled, if yes then carry on: `if is_hvac_sys_fan_sys_VSD(B_RMR, hvac_b.id) == TRUE:`  
                        - Check that each zone only has one terminal unit: `if does_each_zone_have_only_one_terminal(B_RMR,zone_id_list) == TRUE:`     
                            - Check that the data elements associated with the terminal units align with system 7: `if are_all_terminal_heat_sources_hot_water(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_none_or_null(B_RMR,terminal_unit_id_list) == TRUE And are_all_terminal_fans_null(B_RMR,terminal_unit_id_list) == TRUE and are_all_terminal_types_VAV(B_RMR,terminal_unit_id_list) == TRUE:`        
                                - if the preheat loop and all terminals are attached to a boiler and the hvac sys CHW loop is attached to a chiller then Sys-7: `if is_hvac_sys_preheat_fluid_loop_attached_to_boiler(B_RMR, hvac_b.id) == TRUE AND are_all_terminal_heating_loops_attached_to_boiler(B_RMR,terminal_unit_id_list) == TRUE AND is_hvac_sys_fluid_loop_attached_to_chiller(B_RMR, hvac_b.id) == TRUE: is_baseline_system_7 = "Sys-7"`
                                - elif the preheat loop and all terminals are attached to a boiler and the hvac sys CHW loop is purchased cooling then Sys-7a: `elif is_hvac_sys_preheat_fluid_loop_attached_to_boiler(B_RMR, hvac_b.id) == TRUE AND are_all_terminal_heating_loops_attached_to_boiler(B_RMR,terminal_unit_id_list) == TRUE AND is_hvac_sys_fluid_loop_purchased_CHW(B_RMR, hvac_b.id) == TRUE: is_baseline_system_7 = "Sys-7a"`
                                - elif the preheat loop and all terminals are purchased heating and the hvac sys CHW loop is attached to a chiller then Sys-7b: `elif is_hvac_sys_preheat_fluid_loop_purchased_heating(B_RMR, hvac_b.id) == TRUE and are_all_terminal_heating_loops_purchased_heating(B_RMR,terminal_unit_id_list) == TRUE AND is_hvac_sys_fluid_loop_attached_to_chiller(B_RMR, hvac_b.id) == TRUE: is_baseline_system_7 = "Sys-7b"`  
                                - elif the preheat loop and all terminals are purchased heating and the hvac sys CHW loop is purchased cooling then Sys-7c: `elif is_hvac_sys_preheat_fluid_loop_purchased_heating(B_RMR, hvac_b.id) == TRUE and are_all_terminal_heating_loops_purchased_heating(B_RMR,terminal_unit_id_list) == TRUE AND is_hvac_sys_fluid_loop_purchased_CHW(B_RMR, hvac_b.id) == TRUE:is_baseline_system_7 = "Sys-7c"`  
                
**Returns** `is_baseline_system_7`  



**[Back](../../_toc.md)**