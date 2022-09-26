# get_HVAC_building_area_types_and_zones

**Description:** Get the hvac_ids associated with each building area type associated with U_RMR, P_RMR, or B_RMR. Also returns the total floor area of each building area type
- used to verify the correct type of HVAC baseline system (or systems)

**Inputs:**  
- **U-RMR or P-RMR or B-RMR**: The U-RMR, P-RMR or B-RMR

**Returns:**  
- **list_buildiung_area_types_with_total_area_and_zones**: A dict that saves all the HVAC building area types in the file and includes a list of all the zone ids associated with area type as well as the total area of each building area type
 
**Function Call:** None

## Logic:  

- For each building segment in RMR: `for building_segment in RMR.building.building_segments:`
	- Create list_of_zones for storing zone_ids `list_of_zones = []`
	- For each zone in building_segment: `for zone in building_segment.zones:`
		- add zone_id to list_of_zones: `list_of_zones.append(zone.id)`
		- For each space in zone: `for space in zone.spaces:`
			- add space area: `list_buildiung_area_types_with_total_area_and_zones[building_segment.area_type_heating_ventilation_air_conditioning_system]["AREA"] += space.floor_area`
	- Append zone_ids to the dict: `list_buildiung_area_types_with_total_area_and_zones[building_segment.area_type_heating_ventilation_air_conditioning_system]["ZONE_IDS"] = list_of_zones
	
	 **Returns** `return list_buildiung_area_types_with_total_area_and_zones`  

**[Back](../_toc.md)**
