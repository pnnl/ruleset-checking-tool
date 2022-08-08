# is_baseline_system_1c  

**Description:** Returns true or false to whether the baseline system type is 1c (system 1 with purchased CHW and purchased HW).  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as either Sys-1cin the B_RMR.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the is_baseline_system_1 function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. TThese are sent to this function from the is_baseline_system_1 function.

**Returns:**  
- **is_baseline_system_1c**: Returns true or false to whether the baseline system type is 1c (system 1 with purchased CHW and purchased HW).
 
**Function Call:** 
1. is_hvac_sys_cooling_type_none()
8. are_all_terminal_heat_sources_hot_water()  
9. are_all_terminal_cool_sources_chilled_water() 
10. do_all_terminals_have_one_fan()  
11. are_all_terminal_supplies_ducted()  
are_all_terminal_types_four_pipe()
are_all_terminal_types_CAV()
12. does_each_zone_have_only_one_terminal()    
13. does_hvac_system_serve_single_zone()  
 
## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_1c = FALSE: `is_baseline_system_1c == FALSE`    
- Check that there is no preheat system, if there is none then carry on: `if len(hvac_b.preheat_system) == Null or hvac_b.preheat_system[0].heating_system_type == "NONE" :`    
    - Check that there is no heating system, if there is none then carry on: `if len(hvac_b.heating_system) == Null or hvac_b.heating_system[0].heating_system_type == "NONE":`     
        - Check that there is no cooling system if there is none then carry on: `is_hvac_sys_cooling_type_none(B_RMR, hvac_b.id) == TRUE`  
        - Check that there is no fan system, if there is none then carry on: `if len(hvac_b.fan_system) == Null:`     
            - Check if the hvac system serves a single zone and that the zone only has one terminal unit: `if does_hvac_system_serve_single_zone(B_RMR, zone_id_list) == TRUE AND does_each_zone_have_only_one_terminal(B_RMR,zone_id_list) == TRUE:`  
                - Check that the data elements associated with the terminal unit align with system 1c, if yes then carry on: `if are_all_terminal_heat_sources_hot_water(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_chilled_water(B_RMR,terminal_unit_id_list) == TRUE And do_all_terminals_have_one_fan( B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_supplies_ducted(B_RMR,terminal_unit_id_list) == FALSE AND  (are_all_terminal_types_four_pipe(B_RMR,terminal_unit_id_list) == TRUE OR are_all_terminal_types_CAV(B_RMR,terminal_unit_id_list) ==  TRUE):`        
                    - Check if all terminal HW loops are purchased heating: `if are_all_terminal_heating_loops_purchased_heating(B_RMR, hvac_b.id) == TRUE:`  
                        - Check if all termina CHW loop are purchased cooling: 

**Returns** `is_baseline_system_1c`  



**[Back](../_toc.md)**