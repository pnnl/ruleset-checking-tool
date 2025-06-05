# is_baseline_system_13  

**Description:** Get either Sys-13, Sys-13a, or Not_Sys_13 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 13 (Single Zone Constant Volume System with CHW and Electric Resistance) or system 13a (system 13 with purchased CHW).  

**Inputs:**  
- **B-RMI**: To evaluate if the hvac system is modeled as either Sys-13, Sys-13a,or Not_Sys_13 in the B_RMI.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_13**: The function returns either Sys-13, Sys-13a, or Not_Sys_13 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 13 (Single Zone Constant Volume System with CHW and Electric Resistance) or system 13a (system 13 with purchased CHW).

**Function Call:**
1. is_hvac_sys_heating_type_elec_resistance()
2. is_hvac_sys_fluid_loop_purchased_CHW()
3. is_hvac_sys_cooling_type_fluid_loop()
4. is_hvac_sys_fluid_loop_attached_to_chiller()
5. is_hvac_sys_fan_sys_CV()  
6. are_all_terminal_heat_sources_none_or_null()  
7. are_all_terminal_cool_sources_none_or_null()
8. are_all_terminal_fans_null()  
9. are_all_terminal_types_CAV()  
10. does_each_zone_have_only_one_terminal()    
11. does_hvac_system_serve_single_zone()  

## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_13 = Not_Sys_13: `is_baseline_system_13 = "Not_Sys_13"`    
- Check that there is no preheat system, if there is none then carry on: `if hvac_b.preheat_system == "NONE" or hvac_b.preheat_system.heating_system_type = "NONE" :`    
    - Check if heatingsystem is a electric resistance, if it is then carry on: `if is_hvac_sys_heating_type_elec_resistance(B_RMI, hvac_b.id) == TRUE:`     
        - Check if coolingsystem is a fluid_loop, if it is then carry on: `if is_hvac_sys_cooling_type_fluid_loop(B_RMI, hvac_b.id) == TRUE:`  
            - Check if fansystem is constant volume, if yes then carry on: `if is_hvac_sys_fan_sys_CV(B_RMI, hvac_b.id) == TRUE:`  
                - Check if the hvac system serves a single zone and that the zone only has one terminal unit: `if does_hvac_system_serve_single_zone(B_RMI, zone_id_list) == TRUE AND does_each_zone_have_only_one_terminal(B_RMI,zone_id_list) == TRUE:`     
                    - Check that the data elements associated with the terminal unit align with system 13: `if are_all_terminal_heat_sources_none_or_null(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_none_or_null(B_RMI,terminal_unit_id_list) == TRUE And are_all_terminal_fans_null(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_types_CAV(B_RMI,terminal_unit_id_list) == TRUE:`        
                        - if coolingsystem is attached to a chiller then system 13: `if is_hvac_sys_fluid_loop_attached_to_chiller(B_RMI, hvac_b.id) == TRUE: is_baseline_system_13 = "Sys-13"`
                        - elif coolingsystem is purchased CHW then Sys-13a: `elif is_hvac_sys_fluid_loop_purchased_CHW(B_RMI, hvac_b.id) == TRUE: is_baseline_system_13 = "Sys-13a"`

**Returns** `is_baseline_system_13`  



**[Back](../../_toc.md)**
