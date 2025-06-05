# is_baseline_system_8  

**Description:** Get either Sys-8, Sys-8a, Sys-8b, Sys-8c, or Not_Sys_8 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 8 (VAV with Parallel Fan-Powered Boxes and Reheat), system 8a (system 8 with purchased CHW), system 8b (system 8 with purchased heating), or 8c (system 8 with purchased heating and purchased chilled water).  

**Inputs:**  
- **B-RMI**: To evaluate if the hvac system is modeled as either Sys-8, Sys-8a, Sys-8b, Sys-8c, or Not_Sys_8 in the B_RMI.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

**Returns:**  
- **is_baseline_system_8**: The function returns either Sys-8, Sys-8a, Sys-8b, Sys-8c, or Not_Sys_8 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 8 (VAV with Parallel Fan-Powered Boxes and Reheat ), system 8a (system 8 with purchased CHW), system 8b (system 8 with purchased heating), or 8c (system 8 with purchased heating and purchased chilled water).   

**Function Call:**
1. does_each_zone_have_only_one_terminal()    
3. is_hvac_sys_cooling_type_fluid_loop()  
4. is_hvac_sys_fluid_loop_purchased_CHW()
5. is_hvac_sys_fluid_loop_attached_to_chiller()
6. is_hvac_sys_fan_sys_VSD()  
7. is_hvac_sys_preheating_type_fluid_loop()
8. is_hvac_sys_preheat_fluid_loop_purchased_heating()  
9. is_hvac_sys_preheating_type_elec_resistance()
10. are_all_terminal_heat_sources_hot_water()  
11. are_all_terminal_heating_loops_purchased_heating()
12. are_all_terminal_heat_sources_electric()
13. are_all_terminal_fan_configs_parallel()
14. do_all_terminals_have_one_fan()
15. are_all_terminal_cool_sources_none_or_null()
16. are_all_terminal_types_VAV()  


## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_8 = Not_Sys_8: `is_baseline_system_8 = "Not_Sys_8"`    
- Check that there is no heating system, if there is none then carry on: `if(hvac_b.heating_system) == Null or hvac_b.heating_system.heating_system_type == "NONE":`  
    - Check that there is preheat system per G3.1.3.19, if there is then carry on: `if(hvac_b.preheat_system) != Null or hvac_b.preheat_system.heating_system_type == "NONE":`   
          - Check if the cooling system type is a fluid loop, if yes then carry on: `if is_hvac_sys_cooling_type_fluid_loop(B_RMI, hvac_b.id) == TRUE:`  
              - Check if fansystem is variable speed drive controlled, if yes then carry on: `if is_hvac_sys_fan_sys_VSD(B_RMI, hvac_b.id) == TRUE:`  
                  - Check that each zone only has one terminal unit: `if does_each_zone_have_only_one_terminal(B_RMI,zone_id_list) == TRUE:`     
                      - Check that the data elements associated with the terminal units align with system 8: `if are_all_terminal_cool_sources_none_or_null(B_RMI,terminal_unit_id_list) == TRUE And do_all_terminals_have_one_fan(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_types_VAV(B_RMI,terminal_unit_id_list) == TRUE AND are_all_terminal_fan_configs_parallel(B_RMI,terminal_unit_id_list) == TRUE:`        
                          - if the hvac sys preheat loop is electric resistance, the terminal units have electric reheat, and the hvac sys cooling loop is attached to a chiller then Sys-8: `if is_hvac_sys_preheating_type_elec_resistance(B_RMI, hvac_b.id) == TRUE AND are_all_terminal_heat_sources_electric(B_RMI,terminal_unit_id_list) == TRUE is_hvac_sys_fluid_loop_attached_to_chiller(B_RMI, hvac_b.id) == TRUE: is_baseline_system_8 = "Sys-8"`
                          - elif the hvac sys preheat loop is electric resistance, the terminal units have electric reheat, and the hvac sys cooling loop is purchased CHW then Sys-8a: `elif is_hvac_sys_preheating_type_elec_resistance(B_RMI, hvac_b.id) == TRUE AND are_all_terminal_heat_sources_electric(B_RMI,terminal_unit_id_list) == TRUE AND is_hvac_sys_fluid_loop_purchased_CHW(B_RMI, hvac_b.id) == TRUE: is_baseline_system_8 = "Sys-8a"`
                          - elif the preheat loop is a fluid loop: `elif is_hvac_sys_preheating_type_fluid_loop(B_RMI, hvac_b.id) == TRUE:`  
                              - If preheat loop is purchased heating, all terminal unit heating is hot_water, and the hvac sys cooling loop is attached to a chiller: `If is_hvac_sys_preheat_fluid_loop_purchased_heating(B_RMI, hvac_b.id) == TRUE AND are_all_terminal_heat_sources_hot_water(B_RMI,terminal_unit_id_list) == TRUE AND is_hvac_sys_fluid_loop_attached_to_chiller(B_RMI, hvac_b.id) == TRUE:`  
                                  - If all terminal hot water loops are purchased heating then Sys-8b: `if are_all_terminal_heating_loops_purchased_heating(B_RMI,terminal_unit_id_list) == TRUE: is_baseline_system_8 = "Sys-8b"`
                              - elif preheat loop is purchased heating, all terminal unit heating is hot_water, and the hvac sys cooling loop is purchased chilled water: `If is_hvac_sys_preheat_fluid_loop_purchased_heating(B_RMI, hvac_b.id) == TRUE AND are_all_terminal_heat_sources_hot_water(B_RMI,terminal_unit_id_list) == TRUE AND is_hvac_sys_fluid_loop_purchased_CHW(B_RMI, hvac_b.id) == TRUE:`  
                                  - If all terminal hot water loops are purchased heating then Sys-8c: `if are_all_terminal_heating_loops_purchased_heating(B_RMI,terminal_unit_id_list) == TRUE: is_baseline_system_8 = "Sys-8c"`

**Returns** `is_baseline_system_8`  

**Notes**  
1. In the current graphical depiction it has electric reheat for when there is purchased heating at the HVAC system level but based on G3.1.1.3.1 it appears that all heating coils should be purchased heating when there is purchased heating in the building providing space heating.  If others disagree I can of course modify this but just wanted to highlight the assumption used in the logic above.


**[Back](../../_toc.md)**
