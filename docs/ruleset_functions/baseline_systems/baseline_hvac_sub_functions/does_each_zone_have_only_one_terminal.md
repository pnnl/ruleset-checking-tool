# does_each_zone_have_only_one_terminal   

**Description:** Returns TRUE if each zone input to this function only has one terminal unit. It returns FALSE if any zone has more than one terminal unit.   

**Inputs:**  
- **B-RMR**: To evaluate if each zone input to this function only has one terminal unit.   
- **zone_id_list**: List of zones to evaluate.  

**Returns:**  
- **does_each_zone_have_only_one_terminal**: The function returns TRUE if each zone input to this function only has one terminal unit. It returns FALSE if any zone has more than one terminal or no terminal units.   
 
**Function Call:**  None    

## Logic: 
- Set does_each_zone_have_only_one_terminal = TRUE: `does_each_zone_have_only_one_terminal = TRUE`  
- For each zone id in zone_id_list: `For zone_id in zone_id_list:`   
    - Create zone object: `zone = zone_id`
    - check if there is more than one terminal or no terminal units associated with the zone: `if len(zone.terminals) != 1:`     
        - Set does_each_zone_have_only_one_terminal = FALSE: `does_each_zone_have_only_one_terminal = FALSE`  
        - Leave the loop: `break`  

**Returns** `return does_each_zone_have_only_one_terminal`  

**[Back](../../../_toc.md)**