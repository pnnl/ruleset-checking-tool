# get_hvac_systems_5_6_serving_multiple_floors_b

**Description:** Get a dictionary of the system 5, 5a, 5b, 6, 6a, 6b hvac system IDs that are modeled as serving more than one floor in the baseline design model.  The dictionary consists of the hvac system ids as the key and the number of floors served as the value associated with the key.  

**Inputs:**  
- **B-RMD**: To determine if any system type 5, 5a, 5b, 6, 6a, 6bs are modeled as serving more than one floor in the baseline.

**Returns:**  
- **hvac_systems_5_6_serving_multiple_floors_dict_b**: A dictionary that saves all hvac system ids of system types 5, 5a, 5b, 6, 6a, 6b that serve more than 1 floor in the baseline design model and the number of floors served by each.
 
**Function Call:**  

1. get_baseline_system_types()
2. get_hvac_zone_list_w_area_by_rmi_dict()

## Logic:  
- Get dictionary of the baseline hvac system types as keys and lists of applicable hvac system ids as values: `baseline_system_types_dict = get_baseline_system_types(B_RMD)`
- Get dictionary with hvac system id as key and list of associated zones as values: `hvac_zone_list_w_area_dict = get_hvac_zone_list_w_area_by_rmi_dict(B_RMD)`
- Initialize a dictionary to store the applicable hvac system ids as keys and the number of floors served as values: `hvac_systems_5_6_serving_multiple_floors_dict_b = {}`
- For each hvac system in the B_RMD: `for hvac_b in B_RMD...HeatingVentilatingAirConditioningSystem:`
    - If HVAC system is type 5, 5a, 5b, 6, 6a, 6b then the system type is applicable: `if get_baseline_system_types(hvac_b.id) in ["SYS-5", "SYS-5a", "SYS-5b", "SYS-6", "SYS-6a", "SYS-6b"]:`  
        - Get the list of zone ids served by the hvac system from the hvac_zone_list_w_area_dict: `hvac_sys_zone_id_list = hvac_zone_list_w_area_dict[hvac_b["id"]]["zone_list"]`
        - Get the list of zones associated with the zone ids: `hvac_zones_list = find_exactly_one_zone(B_RMD, zone_id) for zone_id in hvac_sys_zone_id_list`
        - Create a set of the unique floor names of zones served by the system: `hvac_floors_served_set = {hvac_zone["floor_name"] for hvac_zone in hvac_zones_list}`
        - Check if the number of unique floor names is greater than 1: `if len(hvac_floors_served_set) > 1:` 
            - Add the system id to the dict of hvac systems serving multiple floors, with the number of floors served as the value: `hvac_systems_5_6_serving_multiple_floors_dict_b [hvac_b.id] = len(hvac_floors_served_set)`  

**Returns** `return hvac_systems_5_6_serving_multiple_floors_dict_b`

**[Back](../_toc.md)**
    
