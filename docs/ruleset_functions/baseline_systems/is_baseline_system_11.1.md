# is_baseline_system_11.1  

**Description:** Get either Sys-11.1, Sys-11.1a, Sys-11b, Sys-11c, or Not_Sys_11.1 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 11.1 (Single Zone VAV System with Electric Resistance Heating), system 11.1a (system 11.1 with purchased CHW), system 11b (system 11.1 with purchased heating), or system 11c (system 11.1 with purchased CHW and purchased heating).  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as either Sys-11.1, Sys-11.1a, Sys-11b, Sys-11c, or Not_Sys in the B_RMD.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_11.1**: The function returns either Sys-11.1, Sys-11.1a, Sys-11b, Sys-11c, or Not_Sys string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 11.1 (Single Zone VAV System with Electric Resistance Heating), system 11.1a (system 11.1 with purchased CHW), system 11b (system 11.1 with purchased heating), or system 11c (system 11.1 with purchased CHW and purchased heating).     
 
**Function Call:** 
1. does_each_zone_have_only_one_terminal()    
2. does_hvac_system_serve_single_zone()()  
3. is_hvac_sys_cooling_type_fluid_loop()  
4. is_hvac_sys_fluid_loop_purchased_CHW()
5. is_hvac_sys_fluid_loop_attached_to_chiller()
6. is_hvac_sys_fan_sys_VSD()  
7. is_hvac_sys_heating_type_fluid_loop()
8. is_hvac_sys_fluid_loop_purchased_heating()  
9. is_hvac_sys_heating_type_elec_resistance()
10. are_all_terminal_heat_sources_none_or_null()  
11. are_all_terminal_cool_sources_none_or_null() 
12. are_all_terminal_types_VAV()  
13. are_all_terminal_fans_null() 


## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_11.1 = Not_Sys_11.1: `is_baseline_system_11.1 = "Not_Sys_11.1"`    
- Check that there is no preheat system, if there is none then carry on: `if len(hvac_b.preheat_system) == Null or hvac_b.preheat_system.heating_system_type = "NONE" :`   
    - Check if the cooling system type is a fluid loop, if yes then carry on: `if is_hvac_sys_cooling_type_fluid_loop(B_RMR, hvac_b.id) == TRUE:`  
        - Check if fansystem is variable speed drive controlled, if yes then carry on: `if is_hvac_sys_fan_sys_VSD(B_RMR, hvac_b.id) == TRUE:`  
            - Check if the hvac system is single zone and that each zone only has one terminal unit: `if does_hvac_system_serve_single_zone(B_RMR, zone_id_list) == TRUE AND does_each_zone_have_only_one_terminal(B_RMR,zone_id_list) == TRUE:`     
                - Check that the data elements associated with the terminal units align with system 11.1: `if are_all_terminal_cool_sources_none_or_null(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_heat_sources_none_or_null() ==  TRUE AND are_all_terminal_fans_null(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_types_VAV(B_RMR,terminal_unit_id_list) == TRUE:`        
                    - if the hvac sys heating loop is electric resistance and the hvac sys cooling loop is attached to a chiller then Sys-11.1: `if is_hvac_sys_heating_type_elec_resistance(B_RMR, hvac_b.id) == TRUE AND is_hvac_sys_fluid_loop_attached_to_chiller(B_RMR, hvac_b.id) == TRUE: is_baseline_system_11.1 = "Sys-11.1"`
                    - elif the hvac sys heating loop is electric resistance and the hvac sys cooling loop is purchased CHW then Sys-11.1a: `elif is_hvac_sys_heating_type_elec_resistance(B_RMR, hvac_b.id) == TRUE AND  is_hvac_sys_fluid_loop_purchased_CHW(B_RMR, hvac_b.id) == TRUE: is_baseline_system_11.1 = "Sys-11.1a"` 
                    - elif the heating loop is a fluid loop: `elif is_hvac_sys_heating_type_fluid_loop(B_RMR, hvac_b.id) == TRUE:`  
                        - If heating loop is purchased heating: `If is_hvac_sys_fluid_loop_purchased_heating(B_RMR, hvac_b.id) == TRUE:`  
                            - if the cooling loop is attached to a chiller then Sys-11b: `If is_hvac_sys_fluid_loop_attached_to_chiller(B_RMR, hvac_b.id) == TRUE: is_baseline_system_11.1 = "Sys-11b"`
                            - elif the cooling loop is purchased CHW then Sys-11c: `If iis_hvac_sys_fluid_loop_purchased_CHW(B_RMR, hvac_b.id) == TRUE: is_baseline_system_11.1 = "Sys-11c"` 
                                            

**Returns** `is_baseline_system_11.1`  



**[Back](../../_toc.md)**