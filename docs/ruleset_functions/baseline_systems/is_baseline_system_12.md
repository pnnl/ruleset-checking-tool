# is_baseline_system_12  

**Description:** Get either Sys-12, Sys-12a, Sys-12b, Sys-12c, or Not_Sys_12 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 12 (Single Zone Constant Volume System with CHW and HW), system 12a (system 12 with purchased CHW), system 12b (system 12 with purchased heating), system 12c (system 12 with purchased CHW and purchased HW).  

**Inputs:**  
- **B-RMI**: To evaluate if the hvac system is modeled as either Sys-12, Sys-12a, Sys-12b, Sys-12c, or Not_Sys_12 in the B_RMI.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_12**: The function returns either Sys-12, Sys-12a, Sys-12b, Sys-12c, or Not_Sys_12 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 12 (Single Zone Constant Volume System with CHW and HW), system 12a (system 12 with purchased CHW), system 12b (system 12 with purchased heating), system 12c (system 12 with purchased CHW and purchased HW).

**Function Call:**
1. is_hvac_sys_heating_type_fluid_loop()
2. is_hvac_sys_fluid_loop_attached_to_boiler()
3. is_hvac_sys_fluid_loop_purchased_heating()
4. is_hvac_sys_fluid_loop_purchased_CHW()
5. is_hvac_sys_cooling_type_fluid_loop()
6. is_hvac_sys_fluid_loop_attached_to_chiller()
7. is_hvac_sys_fan_sys_CV()  
8. are_all_terminal_heat_sources_none_or_null()  
9. are_all_terminal_cool_sources_none_or_null()
10. are_all_terminal_fans_null()  
11. are_all_terminal_types_CAV()   
12. does_each_zone_have_only_one_terminal()    
13. does_hvac_system_serve_single_zone()  

## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_12 = Not_Sys_12: `is_baseline_system_12 = "Not_Sys_12"`    
- Check that there is no preheat system, if there is none then carry on: `if hvac_b.preheat_system == "NONE" or hvac_b.preheat_system.heating_system_type = "NONE" :`    
    - Check if heatingsystem is a fluid_loop, if it is then carry on: `if is_hvac_sys_heating_type_fluid_loop(B_RMI, hvac_b.id) == TRUE:`     
        - Check if coolingsystem is a fluid_loop, if it is then carry on: `if is_hvac_sys_cooling_type_fluid_loop(B_RMI, hvac_b.id) == TRUE:`  
            - Check if fansystem is constant volume, if yes then carry on: `if is_hvac_sys_fan_sys_CV(B_RMI, hvac_b.id) == TRUE:`  
                - Check if the hvac system serves a single zone and that the zone only has one terminal unit: `if does_hvac_system_serve_single_zone(B_RMI, zone_id_list) == TRUE AND does_each_zone_have_only_one_terminal(B_RMI,zone_id_list) == TRUE:`     
                    - Check that the data elements associated with the terminal unit align with system 12: `if are_all_terminal_heat_sources_none_or_null(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_none_or_null(B_RMI,terminal_unit_id_list) == TRUE And are_all_terminal_fans_null(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_types_CAV(B_RMI,terminal_unit_id_list) == TRUE:`        
                        - if coolingsystem is attached to a chiller and the heating fluid loop is served by a boiler then system 12: `if is_hvac_sys_fluid_loop_attached_to_chiller(B_RMI, hvac_b.id) == TRUE AND is_hvac_sys_fluid_loop_attached_to_boiler(B_RMI, hvac_b.id) == TRUE: is_baseline_system_12 = "Sys-12"`
                        - elif coolingsystem is purchased CHW and the heating fluid loop is served by a boiler then Sys-12a: `elif is_hvac_sys_fluid_loop_purchased_CHW(B_RMI, hvac_b.id) == TRUE AND is_hvac_sys_fluid_loop_attached_to_boiler(B_RMI, hvac_b.id) == TRUE: is_baseline_system_12 = "Sys-12a"`
                        - elif the coolingsystem is attached to a chiller and the heating system is purchased heating then Sys-12b: `elif is_hvac_sys_fluid_loop_attached_to_chiller(B_RMI, hvac_b.id) == TRUE AND is_hvac_sys_fluid_loop_purchased_heating(B_RMI, hvac_b.id) == TRUE: is_baseline_system_12 = "Sys-12b"`  


**Returns** `is_baseline_system_12`  



**[Back](../../_toc.md)**
