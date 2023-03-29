# is_baseline_system_1  

**Description:** Get either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1 (PTAC), system 1a (system 1 with purchased CHW), system 1b (system 1 with purchased heating), system 1c (system 1 with purchased CHW and purchased HW).  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 in the B_RMD.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_1**: The function returns either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1 (PTAC), system 1a (system 1 with purchased CHW), system 1b (system 1 with purchased heating), system 1c (system 1 with purchased CHW and purchased HW).  
 
**Function Call:** 
1. is_hvac_sys_heating_type_fluid_loop()
2. is_hvac_sys_cooling_type_DX()
3. is_hvac_sys_fan_sys_CV()  
4. is_hvac_sys_fluid_loop_attached_to_boiler()
5. is_hvac_sys_fluid_loop_purchased_heating()
6. is_hvac_sys_fluid_loop_purchased_CHW()
7. is_hvac_sys_cooling_type_fluid_loop()
8. are_all_terminal_heat_sources_none_or_null()  
9. are_all_terminal_cool_sources_none_or_null() 
10. are_all_terminal_fans_null()  
11. does_each_zone_have_only_one_terminal()    
12. does_hvac_system_serve_single_zone()  
13. is_baseline_system_1c()
14. are_all_terminal_types_CAV() 
15. is_baseline_system_1a()  
16. are_all_terminal_supplies_ducted()    
 
## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_1 = Not_Sys_1: `is_baseline_system_1 = "UNMATCHED"`    
- Check that there is no preheat system, if there is none then carry on: `if len(hvac_b.preheat_system) == Null or hvac_b.preheat_system[0].heating_system_type == "NONE" :`    
    - Check if the system is system 1c, else carry on with logic: `if is_baseline_system_1c(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list) == TRUE: is_baseline_system_1 = "SYS-1c"`   
    - Else, carry on: `Else:`     
        - Check if the system is system 1a, else carry on with logic: `if is_baseline_system_1a(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list) == TRUE: is_baseline_system_1 = "SYS-1a"`         
        - Else,. carry on with logic: `Else:`  
            - Check if heatingsystem is a fluid_loop, if it is then carry on: `if is_hvac_sys_heating_type_fluid_loop(B_RMR, hvac_b.id) == TRUE:`     
                - Check if fansystem is constant volume, if yes then carry on: `if is_hvac_sys_fan_sys_CV(B_RMR, hvac_b.id) == TRUE:`  
                    - Check if the hvac system serves a single zone and that the zone only has one terminal unit: `if does_hvac_system_serve_single_zone(B_RMR, zone_id_list) == TRUE AND does_each_zone_have_only_one_terminal(B_RMR,zone_id_list) == TRUE:`     
                        - Check that the data elements associated with the terminal unit align with system 1: `if are_all_terminal_heat_sources_none_or_null(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_none_or_null(B_RMR,terminal_unit_id_list) == TRUE And are_all_terminal_fans_null(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_types_CAV(B_RMR,terminal_unit_id_list) == TRUE:`        
                            - if coolingsystem is DX and the heating fluid loop serves a boiler then SYS-1: `if is_hvac_sys_cooling_type_DX(B_RMR, hvac_b.id) == TRUE AND is_hvac_sys_fluid_loop_attached_to_boiler(B_RMR, hvac_b.id) == TRUE: is_baseline_system_1 = "SYS-1"`
                            - elif coolingsystem is DX and the fluid loop is purchased heating and supply duct is FALSE then SYS-1b: `elif is_hvac_sys_cooling_type_DX(B_RMR, hvac_b.id) == TRUE AND is_hvac_sys_fluid_loop_purchased_heating(B_RMR, hvac_b.id) == TRUE and are_all_terminal_supplies_ducted(B_RMR, terminal_unit_id_list) == FALSE: is_baseline_system_1 = "SYS-1b"`  
                            
**Returns** `is_baseline_system_1`  



**[Back](../../_toc.md)**