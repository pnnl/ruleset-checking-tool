# does_each_zone_have_only_one_terminal   

**Description:** Returns TRUE if each zone input to this function only has one terminal unit. It returns FALSE if any zone has more than one terminal unit.   

**Inputs:**  
- **B-RMR**: To evaluate if each zone input to this function only has one terminal unit.   
- **zone_id_list**: List of zones to evaluate.  

**Returns:**  
- **does_each_zone_have_only_one_terminal**: The function returns TRUE if each zone input to this function only has one terminal unit. It returns FALSE if any zone has more than one terminal unit.   
 
**Function Call:**  None    

## Logic: 
- For each zone id in zone_id_list: `For zone_id in zone_id_list:`   
    - Create zone object: `zone = zone_id`
    - Check if there is one terminal unit associated with the zone, if only one then set does_each_zone_have_only_one_terminal to true: `if len(zone.terminals) = 1:does_each_zone_have_only_one_terminal = TRUE`   
    - Else: `Else: does_each_zone_have_only_one_terminal = FALSE`
    - Check if does_each_zone_have_only_one_terminal equals False, if it does then leave the loop: `if does_each_zone_have_only_one_terminal == FALSE:`
        - Leave the loop: `break`
    - Else: continue looping: `Else:`   

**Returns** `return does_each_zone_have_only_one_terminal`  

**[Back](../_toc.md)**