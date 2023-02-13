# get_dict_of_zones_and_terminal_units_served_by_hvac_sys    

**Schema Version:** 0.0.23
**Description:** Returns a dictionary of zones and terminal unit IDs associated with each HVAC system in the RMD.   

**Inputs:**  
- **RMR**: The RMR to evalute (B-RMR or P-RMR or U-RMR).    

**Returns:**  
- **get_dict_of_zones_and_terminal_units_served_by_hvac_sys**: Returns a dictionary of zones and terminal unit IDs associated with each HVAC system in the RMR, {hvac_system_1.id: {"ZONE_LIST": [zone_1.id, zone_2.id, zone_3.id], "Terminal_Unit_List": [terminal_1.id, terminal_2.id, terminal_3.id]}, hvac_system_2.id: {"ZONE_LIST": [zone_4.id, zone_9.id, zone_30.id], "Terminal_Unit_List": [terminal_10.id, terminal_20.id, terminal_30.id]}}
 
**Function Call:**  None

## Logic:   
- For each zone in RMR: `for zone in RMR...Zone:`
    - Check if the zone is connected to any terminals (i.e., does not equal null): `if len(zone.terminals) != Null:`  
        - Get zone ID: `zone_id = zone.id`
        - For each terminal unit serving the zone: `for terminal in zone.terminals:`
            - Get terminal ID: `terminal_id = terminal.id`  
            - Get HVAC system connected to the terminal: `hvac_sys_id = terminal.served_by_heating_ventilating_air_conditioning_system`
            - Check if the zone is not already saved in HVAC system dictionary: `if NOT zone_id in dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_sys_id]["ZONE_LIST"]:`
                - Add zone id to the HVAC system dictionary: `dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_sys_id]["ZONE_LIST"].append(zone_id)`
            - Add the terminal id to the HVAC system dictionary: `dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_sys_id]["Terminal_Unit_LIST"].append(terminal_id)`  

**Returns**  `return dict_of_zones_and_terminal_units_served_by_hvac_sys`

**[Back](../_toc.md)**














