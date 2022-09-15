# does_each_terminal_serve_only_one_zone   

**Description:** Returns TRUE if each terminal unit only serves one zone. It returns FALSE if any terminal unit serves no zones or more than one zone.   
   

**Inputs:**  
- **B-RMR**: To evaluate if each terminal unit only serves one zone.   
- **terminal_unit_id_list**: List of terminal units to assess. 


**Returns:**  
- **does_each_terminal_serve_only_one_zone**: The function returns TRUE if each terminal unit only serves one zone. It returns FALSE if any terminal unit serves no zones or more than one zone.   
 
**Function Call:**  None  

## Logic: 
- Set does_each_terminal_serve_only_one_zone = TRUE: `does_each_terminal_serve_only_one_zone = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Reset the counter variable: `counter = 0`  
    - For each zone in the B_RMR: `For zone_b in B_RMR...Zone:` 
        - Check if terminal_b is in zone_b.terminals.id (terminal_b is a terminal id and zone.terminals appears to be a list of terminal objects, leaving it up to the RCT team to decide how to determine if terminal_b is an ID associated with the list of terminal objects): `if terminal_b in list(zone_b.terminals.id):`  
        - Increase counter by 1: `counter = counter + 1`  
        - Check if counter is greater than 1: `if counter > 1:` 
        - Set does_each_terminal_serve_only_one_zone equal to false: `does_each_terminal_serve_only_one_zone = FALSE`  
        - Leave the loop: `break`
    - Check if counter does not equal 1: `if counter != 1:` 
        - Set does_each_terminal_serve_only_one_zone equal to false: `does_each_terminal_serve_only_one_zone = FALSE`  
        - Leave the loop: `break`

**Returns** `return does_each_terminal_serve_only_one_zone`  

**[Back](../../../_toc.md)**
