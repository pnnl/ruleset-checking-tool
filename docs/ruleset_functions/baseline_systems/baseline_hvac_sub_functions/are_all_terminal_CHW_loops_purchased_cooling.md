# are_all_terminal_CHW_loops_purchased_cooling  

**Description:** Returns TRUE if the fluid loop associated with the cooling_from_loop associated with each terminal unit is purchased CHW. Returns FALSE if this is not the case.   

**Inputs:**  
- **B-RMR**: To evaluate if the fluid loop associated with the cooling_from_loop associated with each terminal unit is purchased CHW.   
- **terminal_unit_id_list**: List of terminal units to assess.  

**Returns:**  
- **are_all_terminal_CHW_loops_purchased_cooling**: Returns TRUE if the fluid loop associated with the cooling_from_loop associated with each terminal unit is purchased CHW. Returns FALSE if this is not the case.    
 
**Function Call:** None  

## Logic:   
- Set are_all_terminal_CHW_loops_purchased_cooling equal to TRUE: `are_all_terminal_CHW_loops_purchased_cooling = TRUE`  
- Check if RMR is modeled with external fluid source: `if RMR.RuleModelInstance.external_fluid_source != Null:`  
    - For each external fluid source in RMR: `for external_fluid_source.id in RMR.RuleModelInstance.external_fluid_source:`  
        - Check if external fluid source is CHW: `if external_fluid_source.id.type == "CHILLED_WATER":`    
            - Add the associated loop to the purchased_cooling_loop_list_b list: `purchased_cooling_loop_list_b = purchased_cooling_loop_list_b.append (external_fluid_source.id.loop.id)`   
    - For each terminal unit in terminal_unit_id_list: `For terminal_b_ID in terminal_unit_id_list:`  
        - Create an object for the terminal unit based on ID (however the RCT decides to do this): `terminal_b = terminal_b_ID`  
        - Create an object associate with the cooling_from_loop associated with terminal_b: `terminal_fluid_loop_b = terminal_b.cooling_from_loop`  
        - Check if the fluid loop type is NOT of type cooling OR if the fluid loop id is NOT in the list created above: `if terminal_fluid_loop_b.type != "COOLING" OR terminal_fluid_loop_b.id Not in purchased_cooling_loop_list_b:`
            - Set are_all_terminal_CHW_loops_purchased_cooling = FALSE: `are_all_terminal_CHW_loops_purchased_cooling = FALSE`  
            - Leave the loop: `break`   

**Returns** `are_all_terminal_CHW_loops_purchased_cooling`  


**[Back](../../../_toc.md)**
