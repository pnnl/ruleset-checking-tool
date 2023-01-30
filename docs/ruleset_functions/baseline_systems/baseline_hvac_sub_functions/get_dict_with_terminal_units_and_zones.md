# get_dict_with_terminal_units_and_zones    

**Description:** Returns a dictionary of zone IDs associated with each terminal unit in the RMD.   

**Inputs:**  
- **RMR**: The RMR to evalute (B-RMR or P-RMR or U-RMR).    

**Returns:**  
- **get_dict_with_terminal_units_and_zones**: Returns a dictionary of zones associated with each terminal unit in the RMR, {terminal_unit_1.id: [zone_1.id, zone_2.id, zone_3.id], terminal_unit_2.id: [zone_4.id, zone_9.id, zone_30.id]}
 
**Function Call:**  None

## Logic:   
- For each terminal unit in the RMR: `for terminal in RMR...Terminal:`  
    - For each zone in RMR: `for zone in RMR...Zone:`
        - Check if terminal is in zone.terminals.id (terminal is a terminal id and zone.terminals appears to be a list of terminal objects, leaving it up to the RCT team to decide how to determine if terminal is an ID associated with the list of terminal objects): `if terminal in list(zone.terminals.id):`    
            - Get zone ID: `zone_id = zone.id`
            - Add zone id to the terminal unit dictionary for this terminal unit: `get_dict_with_terminal_units_and_zones[terminal].append(zone_id)`    

**Returns**  `return get_dict_with_terminal_units_and_zones`

**[Back](../../../_toc.md)**








