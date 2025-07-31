# is_baseline_system_3  

**Description:** Get either Sys-3, Sys-3a, Sys-3b, Sys-3c, or Not_Sys_3 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 3 (PSZ), system 3a (system 3 with purchased CHW), system 3b (system 3 with purchased heating), system 3c (system 3 with purchased CHW and purchased HW).  

**Inputs:**  
- **B-RMI**: To evaluate if the hvac system is modeled as either Sys-3, Sys-3a, Sys-3b, Sys-3c, or Not_Sys_3 in the B_RMI.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_3**: The function returns either Sys-3, Sys-3a, Sys-3b, Sys-3c, or Not_Sys_3 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 3 (PSZ), system 3a (system 3 with purchased CHW), system 3b (system 3 with purchased heating), system 3c (system 3 with purchased CHW and purchased HW).   

**Function Call:**
1. is_hvac_sys_heating_type_fluid_loop()
2. is_hvac_sys_cooling_type_DX()
3. is_hvac_sys_fan_sys_CV()  
4. is_hvac_sys_heating_type_furnace()
5. is_hvac_sys_fluid_loop_purchased_heating()
6. is_hvac_sys_fluid_loop_purchased_CHW()
7. is_hvac_sys_cooling_type_fluid_loop()
8. are_all_terminal_heat_sources_none_or_null()  
9. are_all_terminal_cool_sources_none_or_null()
10. are_all_terminal_fans_null()  
11. are_all_terminal_types_CAV()  
12. are_all_terminal_supplies_ducted()
13. does_each_zone_have_only_one_terminal()    
14. does_hvac_system_serve_single_zone()  

## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_3 = Not_Sys_3: `is_baseline_system_3 = "Not_Sys_3"`    
- Check that there is no preheat system, if there is none then carry on: `if hvac_b.preheat_system == "NONE" or hvac_b.preheat_system.heating_system_type == "NONE" :`     
    - Check if fansystem is constant volume, if yes then carry on: `if is_hvac_sys_fan_sys_CV(B_RMI, hvac_b.id) == TRUE:`  
        - Check if the hvac system serves a single zone and that the zone only has one terminal unit: `if does_hvac_system_serve_single_zone(B_RMI, zone_id_list) == TRUE AND does_each_zone_have_only_one_terminal(B_RMI,zone_id_list) == TRUE:`     
            - Check that the data elements associated with the terminal unit align with system 3: `if are_all_terminal_heat_sources_none_or_null(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_none_or_null(B_RMI,terminal_unit_id_list) == TRUE And are_all_terminal_fans_null(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_types_CAV(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_supplies_ducted(B_RMI, terminal_unit_id_list) == TRUE:`        
                - if coolingsystem is DX and the heating type is a furnace then SYS-3: `if is_hvac_sys_cooling_type_DX(B_RMI, hvac_b.id) == TRUE AND is_hvac_sys_heating_type_furnace(B_RMI, hvac_b.id) == TRUE: is_baseline_system_3 = "SYS-3"`
                - elif coolingsystem is DX and the heating type is fluid loop: `elif is_hvac_sys_cooling_type_DX(B_RMI, hvac_b.id) == TRUE and is_hvac_sys_heating_type_fluid_loop(B_RMI, hvac_b.id) == TRUE:`  
                    - Check if fluid loop is purchased heating: `is_hvac_sys_fluid_loop_purchased_heating(B_RMI, hvac_b.id) == TRUE: is_baseline_system_3 = "SYS-3b"`
                - elif the cooling system is a fluid loop: `elif is_hvac_sys_cooling_type_fluid_loop(B_RMI, hvac_b.id) == TRUE:`   
                    - if the cooling system is purchased CHW and heating type is a furnace then SYS-3a: `if is_hvac_sys_fluid_loop_purchased_CHW(B_RMI, hvac_b.id) == TRUE AND is_hvac_sys_heating_type_furnace(B_RMI, hvac_b.id) == TRUE: is_baseline_system_3 = "SYS-3a"`
                    - elif the cooling system is purchased CHW and heating system is purchased heating then SYS-3c: `if is_hvac_sys_fluid_loop_purchased_CHW(B_RMI, hvac_b.id) == TRUE AND is_hvac_sys_fluid_loop_purchased_heating(B_RMI, hvac_b.id) == TRUE: is_baseline_system_3 = "SYS-3c"`  

**Returns** `is_baseline_system_3`  



**[Back](../../_toc.md)**
