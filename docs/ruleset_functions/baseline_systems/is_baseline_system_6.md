# is_baseline_system_6  

**Description:** Get either Sys-6, Sys-6b, or Not_Sys_6 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 6 (Package VAV with PFP Boxes) or system 6b (system 6 with purchased heating).  

**Inputs:**  
- **B-RMI**: To evaluate if the hvac system is modeled as either Sys-6, Sys-6b, or Not_Sys_6 in the B_RMI.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_6**: The function returns either Sys-6, Sys-6b, or Not_Sys_6 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 6 (Package VAV with PFP Boxes) or system 6b (system 6 with purchased heating).   

**Function Call:**
1. does_each_zone_have_only_one_terminal()     
3. is_hvac_sys_cooling_type_DX()
4. is_hvac_sys_fan_sys_VSD()  
5. is_hvac_sys_preheating_type_fluid_loop()
6. is_hvac_sys_preheat_fluid_loop_purchased_heating()  
7. is_hvac_sys_preheating_type_elec_resistance()
8. are_all_terminal_heat_sources_hot_water()  
9. are_all_terminal_heating_loops_purchased_heating()
10. are_all_terminal_heat_sources_electric()
11. are_all_terminal_fan_configs_parallel()
12. do_all_terminals_have_one_fan()
13. are_all_terminal_cool_sources_none_or_null()
14. are_all_terminal_types_VAV()  


## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_6 = Not_Sys_6: `is_baseline_system_6 = "Not_Sys_6"`    
- Check that there is no heating system, if there is none then carry on: `if hvac_b.heating_system == "NONE" or hvac_b.heating_system.heating_system_type == "NONE":`
- Check that there is preheat system per G3.1.3.19, if there is then carry on: `if hvac_b.preheat_system != "NONE":`   
    - Check that there is a cooling system: `if hvac_b.cooling_system != Null or hvac_b.cooling_system.cooling_system_type != "NONE":`  
        - Check if the cooling system type is DX, if yes then carry on: `if is_hvac_sys_cooling_type_DX(B_RMI, hvac_b.id) == TRUE:`  
            - Check if fansystem is variable speed drive controlled, if yes then carry on: `if is_hvac_sys_fan_sys_VSD(B_RMI, hvac_b.id) == TRUE:`  
                - Check that each zone only has one terminal unit: `if does_each_zone_have_only_one_terminal(B_RMI,zone_id_list) == TRUE:`     
                    - Check that the data elements associated with the terminal units align with system 6: `if are_all_terminal_cool_sources_none_or_null(B_RMI,terminal_unit_id_list) == TRUE And do_all_terminals_have_one_fan(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_types_VAV(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_fan_configs_parallel(B_RMI,terminal_unit_id_list) == TRUE:`        
                        - if the hvac sys preheat loop is electric resistance and the terminal units have electric reheat then Sys-6: `if is_hvac_sys_preheating_type_elec_resistance(B_RMI, hvac_b.id) == TRUE AND are_all_terminal_heat_sources_electric(B_RMI,terminal_unit_id_list) == TRUE: is_baseline_system_6 = "Sys-6"`
                        - elif the preheat loop is a fluid loop: `elif is_hvac_sys_preheating_type_fluid_loop(B_RMI, hvac_b.id) == TRUE:`  
                            - If preheat loop is purchased heating and all terminal unit heating is hot_water: `If is_hvac_sys_preheat_fluid_loop_purchased_heating(B_RMI, hvac_b.id) == TRUE AND are_all_terminal_heat_sources_hot_water(B_RMI,terminal_unit_id_list) == TRUE:`  
                                - If all terminal hot water loops are purchased heating then Sys-6b: `if are_all_terminal_heating_loops_purchased_heating(B_RMI,terminal_unit_id_list) == TRUE: is_baseline_system_6 = "Sys-6b"`   

**Returns** `is_baseline_system_6`  

**Notes**  
1. In the current graphical depiction it has electric reheat for when there is purchased heating at the HVAC system level but based on G3.1.1.3.1 it appears that all heating coils should be purchased heating when there is purchased heating in the building providing space heating.  If others disagree I can of course modify this but just wanted to highlight the assumption used in the logic above.


**[Back](../../_toc.md)**
