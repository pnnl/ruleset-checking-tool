# is_baseline_system_1a  

**Description:** Returns true or false to whether the baseline system type is 1a (system 1 with purchased CHW and HW served by a boiler).  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as System-1a the B_RMD.   
- **hvac_b.id**: The id of the hvac system to evaluate.  
- **terminal_unit_id_list**: list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the is_baseline_system_1 function.
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. TThese are sent to this function from the is_baseline_system_1 function.

**Returns:**  
- **is_baseline_system_1a**: Returns true or false to whether the baseline system type is 1a (system 1 with purchased CHW and HW served by a boiler).
 
**Function Call:** 
1. is_hvac_sys_cooling_type_none()
2. are_all_terminal_heat_sources_hot_water()  
3. are_all_terminal_cool_sources_chilled_water() 
4. do_all_terminals_have_one_fan()    
6. are_all_terminal_types_CAV_With_None_Equal_to_Null()
7. does_each_zone_have_only_one_terminal()    
8. all_terminal_chw_loops_purchased_cooling()
9. are_all_terminal_heating_loops_attached_to_boiler() 
 
## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Set is_baseline_system_1a = FALSE: `is_baseline_system_1a == FALSE`    
- Check that there is no preheat system, if there is none then carry on: `if len(hvac_b.preheat_system) == Null or hvac_b.preheat_system[0].heating_system_type == "NONE" :`    
    - Check that there is no heating system, if there is none then carry on: `if len(hvac_b.heating_system) == Null or hvac_b.heating_system[0].heating_system_type == "NONE":`     
      - Check that there is no fan system, if there is none then carry on: `if len(hvac_b.fan_system) == Null:`
        - Check that there is no cooling system if there is none then carry on: `is_hvac_sys_cooling_type_none(B_RMR, hvac_b.id) == TRUE`  
            - Check if each zone only has one terminal unit: `if does_each_zone_have_only_one_terminal(B_RMR,zone_id_list) == TRUE:`  
                - Check that the data elements associated with the terminal unit align with system 1a, if yes then carry on: `if are_all_terminal_heat_sources_hot_water(B_RMR,terminal_unit_id_list) == TRUE AND are_all_terminal_cool_sources_chilled_water(B_RMR,terminal_unit_id_list) == TRUE And do_all_terminals_have_one_fan( B_RMR,terminal_unit_id_list) == TRUE AND  are_all_terminal_types_CAV_With_None_Equal_to_Null(B_RMR,terminal_unit_id_list) ==  TRUE:`        
                    - Check if all terminal HW loops are served by a boiler: `if are_all_terminal_heating_loops_attached_to_boiler(B_RMR,terminal_unit_id_list) == TRUE:`  
                        - Check if all terminal CHW loop are purchased cooling: `if are_all_terminal_chw_loops_purchased_cooling(B_RMR,terminal_unit_id_list) == TRUE: is_baseline_system_1a == TRUE`  

**Returns** `is_baseline_system_1a`  



**[Back](../../_toc.md)**