# get_hvac_systems_5_6_serving_multiple_floors_b

**Description:** Get a dictionary of the system 5, 5a, 5b, 6, 6a, 6b hvac system IDs that are modeled as serving more than one floor in the baseline design model.  The dictionary consists of the hvac system ids as the key and the number of floors served as the value associated with the key.  

**Inputs:**  
- **B-RMR**: To determine if any system type 5, 5a, 5b, 6, 6a, 6bs are modeled as serving more than one floor in the baseline.

**Returns:**  
- **hvac_systems_5_6_serving_multiple_floors_dict_b**: A dictionary that saves all hvac system ids of system types 5, 5a, 5b, 6, 6a, 6b that serve more than 1 floor in the baseline design model and the number of floors served by each.
 
**Function Call:**  

1. get_baseline_system_types()
2. get_hvac_zone_list_w_area()

## Logic:  
- For each building_segment in the B_RMR: `for building_segment_b in B_RMR...BuildingSegment:`
    - Reset list of applicable HVAC (HVAC systems that are of type 5, 5a, 5b, 6, 6a, 6b): `applicable_hvac_list_b = ""`
    - For each hvac_b in the building_segment_b: `for hvac_b in building_segment_b.heating_ventilating_air_conditioning_system:`
        - Reset the hvac_system_type_applicable boolean variable (indicates whether the hvac system type is relevant): `hvac_system_type_applicable = FALSE`
        - Reset zones served list: `zone_list_b = []`
        - Get the hvac system type for hvac_b: `hvac_sys_type_b = baseline_hvac_sys_type_ids_dict_b.keys()[list(baseline_hvac_sys_type_ids_dict_b.values()).index(hvac_b.id)]`
        - Check if HVAC system is type 5, 5a, 5b, 6, 6a, 6b, if it is then carry on: `if get_baseline_system_types(hvac_b.id) in ["SYS-5", "SYS-5a", "SYS-5b", "SYS-6", "SYS-6a", "SYS-6b"]:`
            - Add to list of applicable HVAC systems: `applicable_hvac_list_b = applicable_hvac_list_b.Append(hvac_b)`  
    
    Determine the number of floors each applicable hvac system is associated with
    - Get dictionary with hvac system id as key and list of associated zones as values from function: `hvac_zones_served_dict_b = get_hvac_zone_list_w_area(B_RMR)`
    - For each hvac_b in applicable_hvac_list_b: `for hvac_b in applicable_hvac_list_b:`
        - Reset the list of floors: `list_floors_hvac_b = []`
        - Get list of zones associated with the hvac system: `zone_list_b =  hvac_zones_served_dict_b[hvab_.id]["ZONE_LIST"]`
        - for each zone in the list of zones associated with the hvac system add to list of the floor names associated with the HVAC system: `for zone_b in zone_list_b:`
            - Add to list of floors: `list_floors_hvac_b = list_floors_hvac_b.append(zone_b.floor_name)`
        - Get number of unique values (which will equal the number of floors) for the hvac systems (set returns a list of unique items in a list): `num_floors_hvac_b = len(set(list_floors_hvac_b))`
        - Check if the number of unique values is greater than 1, if so then the system serves multiple floors and should be added to the dictionary of hvac systems serving multiple floors with the number of floors as a value: `if num_floors_hvac_b > 1:` 
            - Add to dict of hvac systems serving multiple floors: `hvac_systems_5_6_serving_multiple_floors_dict_b [hvac_b.id] = num_floors_hvac_b`  

**Returns** `return hvac_systems_5_6_serving_multiple_floors_dict_b`

**[Back](../_toc.md)**
    
