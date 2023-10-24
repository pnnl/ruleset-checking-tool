# is_baseline_system_10  

**Description:** Get either Sys-10 or Not_Sys_10 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 10 (Heating and Ventilation with electric heating).  

**Inputs:**  
- **B-RMI**: To evaluate if the hvac system is modeled as either Sys-10 or Not_Sys_10 in the B_RMI.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_10**: The function returns either Sys-10 or Not_Sys_10 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 10 (Heating and Ventilation with electric heating).  

**Function Call:**
1. is_hvac_sys_cooling_type_none_or_non_mechanical()
2. are_all_terminal_heat_sources_electric()  
3. are_all_terminal_cool_sources_none_or_null()
4. do_all_terminals_have_one_fan()    
6. are_all_terminal_types_cav_with_none_equal_to_null()
7. does_each_zone_have_only_one_terminal()    
8. does_hvac_system_serve_single_zone()  
9. is_hvac_sys_fan_sys_CV()  
10. is_hvac_sys_heating_type_elec_resistance()
11. are_all_terminal_heat_sources_none_or_null()  
12. are_all_terminal_cool_sources_none_or_null()
13. are_all_terminal_fans_null()  
14. are_all_terminal_types_CAV()   
15. does_each_zone_have_only_one_terminal()    
16. does_hvac_system_serve_single_zone()  


## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_10 = Not_Sys_10: `is_baseline_system_10 = "Not_Sys_10"`    
- Check that there is no preheat system, if there is none then carry on: `if hvac_b.preheat_system == "NONE" or hvac_b.preheat_system.heating_system_type == "NONE" :`    
    - Check that there is no heating system, if there is none then carry on: `if hvac_b.heating_system == "NONE" or hvac_b.heating_system.heating_system_type == "NONE":`     
        - Check that there is no cooling system if there is none then carry on: `is_hvac_sys_cooling_type_none_or_non_mechanical(B_RMI, hvac_b.id) == TRUE`  
            - Check that there is no fan system, if there is none then carry on: `if len(hvac_b.fan_system) == Null:`     
                - Check if the zone only has one terminal unit: `if does_each_zone_have_only_one_terminal(B_RMI,zone_id_list) == TRUE:`   
                    - Check that the data elements associated with the terminal unit align with system 10: `if are_all_terminal_heat_sources_electric(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_none_or_null(B_RMI,terminal_unit_id_list) == TRUE And do_all_terminals_have_one_fan(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_types_cav_with_none_equal_to_null(B_RMI,terminal_unit_id_list) == TRUE: is_baseline_system_10 = "Sys-10"`      
- Check if is_baseline_system_10 equals "Not_Sys_10", if it does then perform logic below: `if is_baseline_system_10 == "Not_Sys_10:"`  
    - Check that there is a heating system, if there is then carry on: `if hvac_b.heating_system != Null and hvac_b.heating_system.heating_system_type != "NONE":`   
        - Check that there is no preheat system, if there is none then carry on: `if len(hvac_b.preheat_system) == Null or hvac_b.preheat_system.heating_system_type == "NONE" :`    
            - Check if fansystem is constant volume, if yes then carry on: `if is_hvac_sys_fan_sys_CV(B_RMI, hvac_b.id) == TRUE:`  
                - Check if the hvac system serves a single zone and that the zone only has one terminal unit: `if does_hvac_system_serve_single_zone(B_RMI, zone_id_list) == TRUE AND does_each_zone_have_only_one_terminal(B_RMI,zone_id_list) == TRUE:`     
                    - Check that the data elements associated with the terminal unit align with system 10: `if are_all_terminal_heat_sources_none_or_null(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_none_or_null(B_RMI,terminal_unit_id_list) == TRUE And are_all_terminal_fans_null(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_types_CAV(B_RMI,terminal_unit_id_list) == TRUE:`        
                        - if coolingsystem is None and the heating type is a electric then Sys-10: `if is_hvac_sys_cooling_type_none_or_non_mechanical(B_RMI, hvac_b.id) == TRUE AND is_hvac_sys_heating_type_elec_resistance(B_RMI, hvac_b.id) == TRUE: is_baseline_system_10 = "Sys-10"`  


**Returns** `is_baseline_system_10`  



**[Back](../../_toc.md)**
