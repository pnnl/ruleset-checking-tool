# is_baseline_system_1  

**Description:** Get either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1 (PTAC), system 1a (system 1 with purchased CHW), system 1b (system 1 with purchased heating), system 1c (system 1 with purchased CHW and purchased HW).  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 in the B_RMR.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_1**: The function returns either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1 (PTAC), system 1a (system 1 with purchased CHW), system 1b (system 1 with purchased heating), system 1c (system 1 with purchased CHW and purchased HW).  
 
**Function Call:** 
2. is_heating_type_fluid_loop()
3. is_cooling_type_DX()
5. is_fan_CV()  
6. is_fluid_loop_attached_to_boiler()
7. is_fluid_loop_purchased_heating()
8. is_fluid_loop_purchased_CHW()
9. is_cooling_type_fluid_loop()
10. are_all_terminal_heat_sources_none_or_null()  
11. are_all_terminal_cool_sources_none_or_null() 
12. are_all_terminal_fans_null()  
13. are_all_terminal_types_CAV()  
14. are_all_terminal_types_four_pipe()  
15. are_all_terminal_supplies_ducted()  
17. are_all_terminal_heat_sources_hot_water()  
18. are_all_terminal_cool_sources_chilled_water() 
19. does_each_zone_have_only_one_terminal()    

I deleted the first function and didn't think it was crucial to update the subsequent numbering. 
 

## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Get list of terminal units associated with the hvac system from the dictionary input to the function: `terminal_unit_id_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_b.id]["Terminal_Unit_List"]`  
- Get list of zone ids associated with the hvac system from the dictionary input to the function: `zone_id_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_b.id]["Zone_List"]` 
- Check that there is no preheat system (it equals Null), if there is none then carry on: `if Len(hvac_b.preheat_system) == Null:`  
    - Check if heatingsystem is a fluid_loop, if it is then carry on: `if is_heating_type_fluid_loop(B_RMR, hvac_b.id) == TRUE:`     
        - Check if fansystem is constant volume, if yes then carry on: `if is_fan_CV(B_RMR, hvac_b.id) == TRUE:`  
            - Check if the hvac system serves a single zone and that the zone only has one terminal unit: `if len(terminal_unit_id_list) == 1 AND len(zone_id_list) == 1 and does_each_zone_have_only_one_terminal(B_RMR,zone_id_list) == TRUE:`     
                - Check that the data elements associated with the terminal unit align with system 1: `if are_all_terminal_heat_sources_none_or_null(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_none_or_null(B_RMR,terminal_unit_id_list) == TRUE And are_all_terminal_fans_null(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_supplies_ducted(B_RMR,terminal_unit_id_list) == FALSE :`      
                    - if coolingsystem is DX and the heating fluid loop serves a boiler and the terminal type is constant volume then SYS-1: `if is_cooling_type_DX(B_RMR, hvac_b.id) == TRUE AND is_fluid_loop_attached_to_boiler(B_RMR, hvac_b.id) == TRUE AND are_all_terminal_types_CAV(B_RMR,terminal_unit_id_list) == TRUE: is_baseline_system_1 = "SYS-1"`
                    - elif coolingsystem is DX and the fluid loop is purchased heating and the terminal type is constant volume then SYS-1b: `elif is_cooling_type_DX(B_RMR, hvac_b.id) == TRUE AND is_fluid_loop_purchased_heating(B_RMR, hvac_b.id) == TRUE AND are_all_terminal_types_CAV(B_RMR,terminal_unit_id_list) == TRUE: is_baseline_system_1 = "SYS-1b"`
                    - elif the cooling system is a fluid loop and terminal type is four pipe with chilled and hot water coils: `elif is_cooling_type_fluid_loop(B_RMR, hvac_b.id) == TRUE AND are_all_terminal_types_four_pipe(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_heat_sources_hot_water(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_chilled_water(B_RMR,terminal_unit_id_list) == TRUE:`   
                        - if the cooling system is purchased CHW and heating fluid loop serves a boiler then SYS-1a: `if is_fluid_loop_purchased_CHW(B_RMR, hvac_b.id) == TRUE AND is_fluid_loop_attached_to_boiler(B_RMR, hvac_b.id) == TRUE: is_baseline_system_1 = "SYS-1a"`
                        - elif the cooling system is purchased CHW and heating system is purchased heating then SYS-1c: `if is_fluid_loop_purchased_CHW(B_RMR, hvac_b.id) == TRUE AND is_fluid_loop_purchased_heating(B_RMR, hvac_b.id) == TRUE: is_baseline_system_1 = "SYS-1c"`
                        - Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`  
                    - Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`
                - Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`
            - Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`
        - Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`
    - Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`
- Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`


**Returns** `is_baseline_system_1`  



**[Back](../_toc.md)**