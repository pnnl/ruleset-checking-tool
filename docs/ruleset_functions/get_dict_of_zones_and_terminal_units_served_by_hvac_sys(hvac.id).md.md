# get_dict_of_zones_and_terminal_units_served_by_hvac_sys    

**Description:** Returns a dictionary of zones and terminal unit IDs associated with each HVAC system in the RMR.   

**Inputs:**  
- **RMR**: The RMR to evalute (B-RMR or P-RMR or U-RMR).    

**Returns:**  
- **get_dict_of_zones_and_terminal_units_served_by_hvac_sys**: Returns a dictionary of zones and terminal unit IDs associated with each HVAC system in the RMR, {hvac_system_1.id: {"ZONE_LIST": [zone_1.id, zone_2.id, zone_3.id], "Terminal_Unit_List": [terminal_1.id, terminal_2.id, terminal_3.id]}, hvac_system_2.id: {"ZONE_LIST": [zone_4.id, zone_9.id, zone_30.id], "Terminal_Unit_List": [terminal_10.id, terminal_20.id, terminal_30.id]}}
 
**Function Call:**  None

## Logic:   
- For each terminal unit in the RMR: `For terminal_x in RMR...Terminal:`
    - Check if the served_by_heating_ventilation_air_conditioning_system equals to the hvac id input to the function: `if terminal_x.served_by_heating_ventilation_air_conditioning_system = hvac_x.id:`  
        - Add it to the list of terminal units associated with the HVAC system: `get_dict_of_zones_and_terminal_units_served_by_hvac_sys = get_dict_of_zones_and_terminal_units_served_by_hvac_sys.append(terminal_x.id)`  
    - Else, do nothing: `Else:`

**[Back](../_toc.md)**














