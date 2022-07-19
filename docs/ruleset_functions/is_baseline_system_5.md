# is_baseline_system_5  

**Description:** Get either Sys-5, Sys-5b, or Not_Sys_5 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 5 (Package VAV with Reheat) or system 5b (system 5 with purchased heating).  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as either Sys-5, Sys-5b, or Not_Sys_5 in the B_RMR.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_5**: The function returns either Sys-5, Sys-5b, or Not_Sys_5 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 5 (Package VAV with Reheat) or system 5b (system 5 with purchased heating).   
 
**Function Call:** 
1. is_hvac_sys_heating_type_fluid_loop()
2. is_hvac_sys_cooling_type_DX()
3. is_hvac_sys_fan_sys_VSD()  
5. is_hvac_sys_fluid_loop_purchased_heating()
8. are_all_terminal_heat_sources_hot_water()  
9. are_all_terminal_cool_sources_none_or_null() 
10. are_all_terminal_fans_null()  
11. are_all_terminal_types_VAV()  
12. are_all_terminal_supplies_ducted()  
13. does_each_zone_have_only_one_terminal()    
14. is_hvac_system_multizone()  
 
## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_5 = Not_Sys_5: `is_baseline_system_5 = "Not_Sys_5"`    
- Check that there is one preheat system per G3.1.3.19, if there is then carry on: `if Len(hvac_b.preheat_system) == 1:`   
    - Check if the cooling system type is DX, if yes then carry on: `if is_hvac_sys_cooling_type_DX(B_RMR, hvac_b.id) == TRUE:`  
        - Check if fansystem is variable speed drive controlled, if yes then carry on: `if is_hvac_sys_fan_sys_VSD(B_RMR, hvac_b.id) == TRUE:`  
            - Check if the hvac system is multizone and that the zone only has one terminal unit: `if is_hvac_system_multizone(B_RMR, zone_id_list) == TRUE AND does_each_zone_have_only_one_terminal(B_RMR,zone_id_list) == TRUE:`     
                - Check that the data elements associated with the terminal units align with system 5: `if are_all_terminal_heat_sources_hot_water(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_none_or_null(B_RMR,terminal_unit_id_list) == TRUE And are_all_terminal_fans_null(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_supplies_ducted(B_RMR,terminal_unit_id_list) == TRUE and are_all_terminal_types_VAV(B_RMR,terminal_unit_id_list) == TRUE:`        
                    - if the preheat loop and all terminals are attached to a boiler then SYS-5: `if is_hvac_sys_cooling_type_DX(B_RMR, hvac_b.id) == TRUE AND is_hvac_sys_heating_type_furnace(B_RMR, hvac_b.id) == TRUE: is_baseline_system_5 = "SYS-5"`
                    - elif coolingsystem is DX and the heating type is fluid loop: `elif is_hvac_sys_cooling_type_DX(B_RMR, hvac_b.id) == TRUE and is_hvac_sys_heating_type_fluid_loop(B_RMR, hvac_b.id) == TRUE:`  
                        - Check if fluid loop is purchased heating: `is_hvac_sys_fluid_loop_purchased_heating(B_RMR, hvac_b.id) == TRUE: is_baseline_system_5 = "SYS-5b"`
                    - elif the cooling system is a fluid loop: `elif is_hvac_sys_cooling_type_fluid_loop(B_RMR, hvac_b.id) == TRUE:`   
                        - if the cooling system is purchased CHW and heating type is a furnace then SYS-5a: `if is_hvac_sys_fluid_loop_purchased_CHW(B_RMR, hvac_b.id) == TRUE AND is_hvac_sys_heating_type_furnace(B_RMR, hvac_b.id) == TRUE: is_baseline_system_5 = "SYS-5a"`
                        - elif the cooling system is purchased CHW and heating system is purchased heating then SYS-5c: `if is_hvac_sys_fluid_loop_purchased_CHW(B_RMR, hvac_b.id) == TRUE AND is_hvac_sys_fluid_loop_purchased_heating(B_RMR, hvac_b.id) == TRUE: is_baseline_system_5 = "SYS-5c"`  

**Returns** `is_baseline_system_5`  



**[Back](../_toc.md)**