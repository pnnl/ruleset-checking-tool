# get_dict_of_zones_hvac_sys_serving_specific_floor

**Description:** Returns a dictionary with zone ids as the keys and the associated HVAC system as the values for zones serving a specific floor the applicable RMR i.e. {zone_1.id: [hvac_1.id, hvac_2.id, hvac_3.id], zone_2.id: [hvac_1.id, hvac_2.id, hvac_3.id]}.

**Inputs:**
- **floor_name**: A floor name (string) associated with the RMR to determine the zone ids and hvac systems that are associated with the specific floor.
- **U,P, or B-RMR**: to determine the zone ids and hvac systems associated with a specific floor name in the specified RMR.

**Returns:**
- **dict_of_zones_hvac_sys_serving_specific_floor**: a dictionary with zone ids as the keys and the associated HVAC system as the values for zones serving a specific floor the applicable RMR i.e. {zone_1.id: [hvac_1.id, hvac_2.id, hvac_3.id], zone_2.id: [hvac_1.id, hvac_2.id, hvac_3.id]}.  
 
**Function Call:** 

1. get_list_hvac_systems_associated_with_zone()  

**Logic:**  
- For each zone in the RMR (whichever RMR (U, P, or B) that was input to the function): `For zone_x in RMR...Zone:`
    - If the floor name associated with the zone is equal to floor_name (i.e. the function input floor name) then add it to the dictionary with list of hvac systems: `if zone_x.floor_name = floor_name:`
        - Get list of the hvac systems serving the zone: `list_hvac_x = get_list_hvac_systems_associated_with_zone(RMR,zone_x.id)`
        - Add zone and hvac systems to the dictionary: `dict_of_zones_hvac_sys_serving_specific_floor[zone_x.id] = list_hvac_x`

**Returns** `return dict_of_zones_hvac_sys_serving_specific_floor`  

**[Back](../_toc.md)**