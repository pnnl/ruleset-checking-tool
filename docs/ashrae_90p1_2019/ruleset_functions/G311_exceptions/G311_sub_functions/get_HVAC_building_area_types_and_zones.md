# get_HVAC_building_area_types_and_zones
**Schema Version:** 0.0.28  

**Description:** Get a dictionary of the zone_ids associated with each building area type associated with U_RMR, P_RMR, or B_RMR. Also returns the total floor area of each building area type and the source of the information (BUILDING_SEGMENT_HVAC_BAT, BUILDING_SEGMENT_LIGHTING or SPACE_LIGHTING)
- used to verify the correct type of HVAC baseline system (or systems)
- HVAC building area type is determined first by looking at the building segment HVAC_BAT.  If this variable does not exist, the function next looks at building segment lighting_building_area_type.  If this variable doesn't exist, the function will look at the space lighting type.  Support spaces such as corridors, stairwells and other support spaces will inherit the predominant building area type EXCEPT in buildings where the predominant HVAC_BAT is residential.  If corridors and stairwells will are not classified by the HVAC_BAT, they will be classified as Other Non-Residential.
- the entry "CLASSIFICATION_SOURCE" in the **building_area_types_with_total_area_and_zones_dict** passes information about how the HVAC_BAT was determined for each segment along

**Inputs:**  
- **B-RMI**: The baseline ruleset model instance

**Returns:**  
- **building_area_types_with_total_area_and_zones_dict**: A dict that saves all the HVAC building area types and includes a list of all the zone ids associated with area type as well as the total area of each building area type: {OTHER_NON_RESIDENTIAL: {"ZONE_IDS": ["zone_1","zone_5"], "AREA": 1234, "CLASSIFICATION_SOURCE": "BUILDING_SEGMENT_HVAC_BAT"}, PUBLIC_ASSEMBLY: {"ZONE_IDS": ["zone_2", "zone_3", "zone_4"], "AREA": 34567, "CLASSIFICATION_SOURCE": "BUILDING_SEGMENT_LIGHTING"}, RESIDENTIAL: {"ZONE_IDS": ["r1","r2","r3"], "AREA": 20381, "CLASSIFICATION_SOURCE": "SPACE_LIGHTING"}
 
**Function Call:** 
- **get_zone_conditioning_category**
- **get_zone_HVAC_BAT**

## Logic:  
- create lookup table for lighting space types: `lighting_space_lookup = {`  
	`AUTOMOTIVE_FACILITY: = OTHER_NON_RESIDENTIAL`  
	`CONVENTION_CENTER: PUBLIC_ASSEMBLY`  
	`COURTHOUSE: OTHER_NON_RESIDENTIAL`  
	`DINING_BAR_LOUNGE_LEISURE: OTHER_NON_RESIDENTIAL`  
	`DINING_CAFETERIA_FAST_FOOD: OTHER_NON_RESIDENTIAL`  
	`DINING_FAMILY: OTHER_NON_RESIDENTIAL`  
	`DORMITORY: RESIDENTIAL`  
	`EXERCISE_CENTER: OTHER_NON_RESIDENTIAL`  
	`FIRE_STATION: OTHER_NON_RESIDENTIAL`  
	`GYMNASIUM: PUBLIC_ASSEMBLY`  
	`HEALTH_CARE_CLINIC: HOSPITAL`  
	`HOSPITAL: HOSPITAL`  
	`HOTEL_MOTEL: RESIDENTIAL`  
	`LIBRARY: OTHER_NON_RESIDENTIAL`  
	`MANUFACTURING_FACILITY: OTHER_NON_RESIDENTIAL`  
	`MOTION_PICTURE_THEATER: PUBLIC_ASSEMBLY`  
	`MULTIFAMILY: RESIDENTIAL`  
	`MUSEUM: PUBLIC_ASSEMBLY`  
	`OFFICE: OTHER_NON_RESIDENTIAL`  
	`PARKING_GARAGE: HEATED-ONLY_STORAGE`  
	`PENITENTIARY: OTHER_NON_RESIDENTIAL`  
	`PERFORMING_ARTS_THEATER: PUBLIC_ASSEMBLY`  
	`POLICE_STATION: OTHER_NON_RESIDENTIAL`  
	`POST_OFFICE: OTHER_NON_RESIDENTIAL`  
	`RELIGIOUS_FACILITY: PUBLIC_ASSEMBLY`  
	`RETAIL: RETAIL`  
	`SCHOOL_UNIVERSITY: OTHER_NON_RESIDENTIAL`  
	`SPORTS_ARENA: PUBLIC_ASSEMBLY`  
	`TOWN_HALL: OTHER_NON_RESIDENTIAL`  
	`TRANSPORTATION: OTHER_NON_RESIDENTIAL`  
	`WAREHOUSE: HEATED-ONLY_STORAGE`  
	`WORKSHOP: OTHER_NON_RESIDENTIAL`  
	`NONE: NONE`  
	
	`}`  

- use the function get_zone_conditioning_category to get a dictionary of zone id's and their conditioning category - we will only include conditioned zones in the building_area_types_with_total_area_and_zones_dict: `zone_conditioning_category_dict = get_zone_conditioning_category(RMI)`
- create dict `building_area_types_with_total_area_and_zones_dict`: `building_area_types_with_total_area_and_zones_dict = {}`
- For each building segment in RMR: `for building_segment in RMR.building.building_segments:`
	- if the building segment has a HVAC_BAT assigned, assign all zones in that building segment to the HVAC_BAT: `if building_segment.area_type_heating_ventilating_air_conditioning_system != NULL:`
		- assign the HVAC_BAT to be the building_segment_HVAC_BAT: `building_segment_HVAC_BAT = building_segment.area_type_heating_ventilating_air_conditioning_system`
		- assign "BUILDING_SEGMENT_HVAC_BAT" to classification_source: `classification_source = "BUILDING_SEGMENT_HVAC_BAT"`
	- else if there is no HVAC_BAT assigned, look in the building_segment lighting_building_area_type: `elif building_segment.lighting_building_area_type != NULL`
		- assign the HVAC_BAT to the building_segment_HVAC_BAT using the lighting_space_lookup: `building_segment_HVAC_BAT = lighting_space_lookup[building_segment.lighting_building_area_type]`
		- assign "BUILDING_SEGMENT_LIGHTING" to classification_source: `classification_source = "BUILDING_SEGMENT_LIGHTING"`
	- else look at each zone, and then each space and determine the building_segment_HVAC_BAT using the largest space.lighting_space_type: `else:`
		- create a dictionary to keep track of the space types and areas: `building_segment_space_types_areas_dict = {}`
		- look at each zone: `for zone in building_segment.zones:`
			- create a dictionary for the zone HVAC_BAT space types using the function get_zone_HVAC_BAT: zone_HVAC_BAT_dict = get_zone_HVAC_BAT(B_RMI, zone.id)`
			- loop through the zone_HVAC_BAT_dict: `for space_HVAC_BAT in zone_HVAC_BAT_dict:`
				- add this space type to the building_segment_space_types_areas_dict if it doesn't exist yet: `building_segment_space_types_areas_dict[space_HVAC_BAT] = building_segment_space_types_areas_dict[space_HVAC_BAT] or 0`
				- add the space area: `building_segment_space_types_areas_dict[space_HVAC_BAT] += zone_HVAC_BAT_dict[space_HVAC_BAT]`
		- get the HVAC_BAT with the largest floor area from building_segment_space_types_areas_dict: `building_segment_HVAC_BAT = max(building_segment_space_types_areas_dict, key=building_segment_space_types_areas_dict.get)`
		- assign "SPACE_LIGHTING" to classification_source: `classification_source = "SPACE_LIGHTING"`
	- at this point, the building_segment_HVAC_BAT has been defined by one of the three approaches, add a list for this type of HVAC_BAT to the building_area_types_with_total_area_and_zones_dict if it doesn't exist already: `building_area_types_with_total_area_and_zones_dict[building_segment_HVAC_BAT] = building_area_types_with_total_area_and_zones_dict[building_segment_HVAC_BAT] or {"ZONE_IDS":[], "AREA":0, "CLASSIFICATION_SOURCE": classification_source}`
	- loop through each zone: `for zone in building_segment.zones:`
		- using zone_conditioning_category_dict, check if the zone is conditioned. `if zone_conditioning_category_dict[zone.id] == "CONDITIONED RESIDENTIAL" || zone_conditioning_category_dict[zone.id] == "CONDITIONED NON-RESIDENTIAL" || zone_conditioning_category_dict[zone.id] == "CONDITIONED MIXED"`:
			- add the zone to the building_area_types_with_total_area_and_zones_dict: `building_area_types_with_total_area_and_zones_dict[building_segment_HVAC_BAT]["ZONE_IDS"].append(zone.id)`
				- loop through each space: `for space in zone.spaces:`
					- add the space area to the building_area_types_with_total_area_and_zones_dict: `building_area_types_with_total_area_and_zones_dict[building_segment_HVAC_BAT]["AREA"] += space.floor_area`
- we still need to deal with the possibility that there are spaces classified as OTHER_UNDETERMINED: `if OTHER_UNDETERMINED in building_area_types_with_total_area_and_zones_dict:`
	- determine what the largest space type is: `predominate_HVAC_BAT = sorted(building_area_types_with_total_area_and_zones_dict.items(), key=lambda x: x[1]["AREA"], reverse = True)[0][0]`
	- if RESIDENTIAL or OTHER_UNDETERMINED is the largest space area: `if predominate_HVAC_BAT == OTHER_UNDETERMINED or predominate_HVAC_BAT == RESIDENTIAL:`
		- we re-classify all OTHER_UNDETERMINED spaces as OTHER_NON_RESIDENTIAL: `building_area_types_with_total_area_and_zones_dict[OTHER_NON_RESIDENTIAL] = building_area_types_with_total_area_and_zones_dict[OTHER_NON_RESIDENTIAL] or {"ZONE_IDS":[], "AREA":0, "CLASSIFICATION_SOURCE": building_area_types_with_total_area_and_zones_dict[OTHER_NON_RESIDENTIAL]["CLASSIFICATION_SOURCE"]}`
		- add the zones from the OTHER_UNDETERMINED list to the OTHER_NON_RESIDENTIAL list: `building_area_types_with_total_area_and_zones_dict[OTHER_NON_RESIDENTIAL]["ZONE_IDS"] += building_area_types_with_total_area_and_zones_dict[OTHER_UNDETERMINED]["ZONE_IDS"]`
		- add the area from the OTHER_UNDETERMIEND list to the OTHER_NON_RESIDENTIAL area: `building_area_types_with_total_area_and_zones_dict[OTHER_NON_RESIDENTIAL]["AREA"] += building_area_types_with_total_area_and_zones_dict[OTHER_UNDETERMINED]["AREA"]
	- otherwise, we can add the are and zones from OTHER_UNDETERMINED to the predominate_HVAC_BAT: `else:`
		- add the zones from the OTHER_UNDETERMINED list to the predominate_HVAC_BAT list: `building_area_types_with_total_area_and_zones_dict[predominate_HVAC_BAT]["ZONE_IDS"] += building_area_types_with_total_area_and_zones_dict[OTHER_UNDETERMINED]["ZONE_IDS"]`
		- add the area from the OTHER_UNDETERMIEND list to the predominate_HVAC_BAT area: `building_area_types_with_total_area_and_zones_dict[predominate_HVAC_BAT]["AREA"] += building_area_types_with_total_area_and_zones_dict[OTHER_UNDETERMINED]["AREA"]
	- remove the key OTHER_UNDETERMINED from building_area_types_with_total_area_and_zones_dict: `del building_area_types_with_total_area_and_zones_dict[OTHER_UNDETERMINED]`

	 **Returns** `return building_area_types_with_total_area_and_zones_dict`  

**Notes/Questions:**  
1. "Heated-Only Storage" was not listed in the schema under HeatingVentilatingAirConditioningBuildingAreaOptions2019ASHRAE901 when this function was written - double check spelling
2. a map was provided for mapping LightingBuildingAreaOptions2019ASHRAE901T951TG38, but not LightingSpaceOptions2019ASHRAE901TG37.  Double check my mapping

**[Back](../_toc.md)**
