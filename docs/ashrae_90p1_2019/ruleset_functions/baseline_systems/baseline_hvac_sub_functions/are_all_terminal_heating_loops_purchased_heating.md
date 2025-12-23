# are_all_terminal_heating_loops_purchased_heating  

**Description:** Returns TRUE if the fluid loop associated with the heating_from_loop associated with each terminal unit is purchased heating. Returns FALSE if this is not the case.   

**Inputs:**  
- **B-RMR**: To evaluate if the fluid loop associated with the heating_from_loop associated with each terminal unit is purchased heating.   
- **terminal_unit_id_list**: List of terminal units to assess.  

**Returns:**  
- **are_all_terminal_heating_loops_purchased_heating**: Returns TRUE if the fluid loop associated with the heating_from_loop associated with each terminal unit is purchased heating. Returns FALSE if this is not the case.    
 
**Function Call:** None  

## Logic:   
- Set are_all_terminal_heating_loops_purchased_heating equal to TRUE: `are_all_terminal_heating_loops_purchased_heating = TRUE`  
- Check if RMR is not modeled with external fluid source: `if RMR.RuleModelInstance.external_fluid_source != Null:`  
    - For each external fluid source in RMR: `for external_fluid_source.id in RMR.RuleModelInstance.external_fluid_source:`  
        - Check if external fluid source is heating type: `if external_fluid_source.id.type == "HOT_WATER" OR external_fluid_source.id.type == "STEAM":`    
            - Add the associated loop to the purchased_heating_loop_list_b list: `purchased_heating_loop_list_b = purchased_heating_loop_list_b.append (external_fluid_source.id.loop.id)`   
    - For each terminal unit in terminal_unit_id_list: `For terminal_b_ID in terminal_unit_id_list:`  
        - Create an object for the terminal unit based on ID (however the RCT decides to do this): `terminal_b = terminal_b_ID`  
        - Create an object associate with the heating_from_loop associated with terminal_b: `terminal_fluid_loop_b = terminal_b.heating_from_loop`  
        - Check if the fluid loop type is NOT of type heating OR if the fluid loop id is NOT in the list of keys created above: `if terminal_fluid_loop_b.type != "HEATING" OR terminal_fluid_loop_b.id Not in purchased_heating_loop_list_b:`
            - Set are_all_terminal_heating_loops_purchased_heating = FALSE: `are_all_terminal_heating_loops_purchased_heating = FALSE`  
            - Leave the loop: `break`

**Returns** `are_all_terminal_heating_loops_purchased_heating`  


**[Back](../../../_toc.md)**
