# is_baseline_system_9b  

**Description:** Returns true or false to whether the baseline system type is 9b (system 9 with purchased HW).  

**Inputs:**  
- **B-RMI**: To evaluate if the hvac system is modeled as either Sys-9bin the B_RMI.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the is_baseline_system_1 function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. TThese are sent to this function from the is_baseline_system_1 function.

**Returns:**  
- **is_baseline_system_9b**: Returns true or false to whether the baseline system type is 9b (system 9 with purchased HW).

**Function Call:**
1. is_hvac_sys_cooling_type_none_or_non_mechanical()
2. are_all_terminal_heat_sources_hot_water()  
3. do_all_terminals_have_one_fan()  
4. are_all_terminal_types_cav_with_none_equal_to_null ()
5. does_each_zone_have_only_one_terminal()    


## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_9b = FALSE: `is_baseline_system_9b == FALSE`    
- Check that there is no preheat system, if there is none then carry on: `if(hvac_b.preheat_system) == Null or hvac_b.preheat_system.heating_system_type == "NONE" :`    
    - Check that there is no heating system, if there is none then carry on: `if(hvac_b.heating_system) == Null or hvac_b.heating_system[0].heating_system_type == "NONE":`     
        - Check that there is no cooling system if there is none then carry on: `is_hvac_sys_cooling_type_none_or_non_mechanical(B_RMI, hvac_b.id) == TRUE`  
        - Check that there is no fan system, if there is none then carry on: `if(hvac_b.fan_system) == Null:`     
            - Check if the zone(s) only have one terminal unit: `if does_each_zone_have_only_one_terminal(B_RMI,zone_id_list) == TRUE:`  
                - Check that the data elements associated with the terminal unit align with system 9b, if yes then carry on: `if are_all_terminal_heat_sources_hot_water(B_RMI,terminal_unit_id_list) == TRUE AND do_all_terminals_have_one_fan(B_RMI,terminal_unit_id_list) == TRUE AND  are_all_terminal_types_cav_with_none_equal_to_null(B_RMI,terminal_unit_id_list) ==  TRUE:`        
                    - Check if all terminal HW loops are purchased heating: `if are_all_terminal_heating_loops_purchased_heating(B_RMI, hvac_b.id) == TRUE:` 
                        - Check if all terminal cooling sources are NOT chilled water and all terminal chw loops are NOT puchased chilled water: `if are_all_terminal_cool_sources_chilled_water(B_RMI,terminal_unit_id_list) == False and are_all_terminal_chw_loops_purchased_cooling(B_RMI,terminal_unit_id_list) == False: is_baseline_system_9b == TRUE`   

**Returns** `is_baseline_system_9b`  

**[Back](../../_toc.md)**
