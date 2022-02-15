# get_list_of_zones_per_hvac_sys_b

**Description:** Get a dictionary with each HVAC system id as a key and a list of zones that each hvac system is associated with as values for the B-RMR.  

**Inputs:**  
- **B-RMR**: To create a dictionary with each HVAC system id as a key and a list of zones that each hvac system is associated with as values for the B-RMR.  

**Returns:**  
- **hvac_id_zones_dict_b**: A dictionary with each HVAC system id as a key and a list of zones that each hvac system is associated with as values for the B-RMR.   
 
**Function Call:** None  


## Logic:  
- For each building_segment in the B_RMR: `for building_segment_b in B_RMR..BuildingSegment:`
    - For each hvac_b in the building_segment_b: `for hvac_b in building_segment_b.heating_ventilation_air_conditioning_system:`
        - Reset zones served list: `zone_list_b = []`
        - For each zone_b in the building_segment_b: `for zone_b in building_segment_b:`
            - For each terminal unit associated with each zone: `for terminal_b in zone_b:`
                - Get the served_by_heating_ventilation_air_conditioning_systems for each terminal: `heating_ventilation_air_conditioning_systems_b = terminal_b.served_by_heating_ventilation_air_conditioning_systems`
                - Add to list of heating_ventilation_air_conditioning_systems_list_b as the code loops through the terminal units: `heating_ventilation_air_conditioning_systems_list_b = heating_ventilation_air_conditioning_systems_list_b.append(heating_ventilation_air_conditioning_systems_b)`                
            - Convert the list of heating_ventilation_air_conditioning_systems_list_b associated with the zone to a set and the back to a list to eliminate duplicates after looping through terminal units: `heating_ventilation_air_conditioning_systems_list_b = list(set(heating_ventilation_air_conditioning_systems_list_b))`
            - For each hvac_zone_b in heating_ventilation_air_conditioning_systems_list_b (i.e. list of hvac units associated with zone): `for hvac_zone_b in heating_ventilation_air_conditioning_systems_list_b:` 
                - Check if hvac_zone_b equals hvac_b and if it does then add zone to list of zones for that hvac system: `if hvac_zone_b.id == hvac_b.id: zone_list_b = zone_list_b.append(zone_b.id)`
        - Add to dictionary with hvac_b.id as key and a list of zones served as values, start with empty list: `hvac_id_zones_dict_b[hvac_b.id] = list()`
        - Add to dictionary with hvac_b.id as key and a list of zones served as values: `hvac_id_zones_dict_b[hvac_b.id].extend(zone_list_b)`
            

**Returns** `return hvac_id_zones_dict_b`

**[Back](../_toc.md)**