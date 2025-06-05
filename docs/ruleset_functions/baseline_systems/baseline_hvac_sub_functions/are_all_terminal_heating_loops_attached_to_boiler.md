# are_all_terminal_heating_loops_attached_to_boiler  

**Description:** Returns TRUE if the fluid loop associated with the heating_from_loop associated with each terminal unit is attached to a boiler. Returns FALSE if this is not the case.   

**Inputs:**  
- **B-RMR**: To evaluate if the fluid loop associated with the heating_from_loop associated with each terminal unit is attached to a boiler.   
- **terminal_unit_id_list**: List of terminal units to assess.  

**Returns:**  
- **are_all_terminal_heating_loops_attached_to_boiler**: Returns TRUE if the fluid loop associated with the heating_from_loop associated with each terminal unit is attached to a boiler. Returns FALSE if this is not the case.    
 
**Function Call:** None  

## Logic:   
- Set are_all_terminal_heating_loops_attached_to_boiler equal to TRUE: `are_all_terminal_heating_loops_attached_to_boiler = TRUE`  
- For each boiler in B_RMR, save boiler to loop boiler list: `for boiler_b in B_RMR.RulesetModelInstance.boilers: loop_boiler_list.append(boiler_b)`
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object associate with the heating_from_loop associated with terminal_b: `terminal_fluid_loop_b = terminal_b.heating_from_loop`  
    - Check if the fluid loop type is NOT of type heating OR if the fluid loop id is NOT in the list of keys created above: `if terminal_fluid_loop_b.type != "HEATING" OR terminal_fluid_loop_b.id Not in loop_boiler_list:`
        - Set are_all_terminal_heating_loops_attached_to_boiler = FALSE: `are_all_terminal_heating_loops_attached_to_boiler = FALSE`  
        - Leave the loop: `break`   

**Returns** `are_all_terminal_heating_loops_attached_to_boiler`  


**[Back](../_toc.md)**