# get_BPF_building_area_types_and_zones
**Schema Version:** 0.0.29

**Description:** Get a dictionary of the zone_ids associated with each BPF building area type associated with U_RMR, P_RMR, or B_RMR. Also returns the total floor area of each building area type and the source of the information (BUILDING_SEGMENT_BPF_BAT, BUILDING_AREA_LIGHTING or SPACE_LIGHTING)
- used to verify the correct type of BPF baseline system (or systems)
- BPF building area type is determined first by looking at the building segment BPF_BAT.  If this variable does not exist, the function next looks at building segment lighting_building_area_type.  If this variable doesn't exist, the function will look at the space lighting type.  Support spaces such as corridors, stairwells and other support spaces will inherit the predominant building area type.
- the entry "CLASSIFICATION_SOURCE" in the **building_area_types_with_total_area_and_zones_dict** passes information about how the BPF_BAT was determined for each segment along

**Inputs:**  
- **RMD**: The ruleset model description

**Returns:**  
- **building_area_types_with_total_area_and_zones_dict**: A dict that saves all the BPF building area types and includes a list of all the zone ids associated with area type as well as the total area of each building area type: {SCHOOL: {"ZONE_IDS": ["zone_1","zone_5"], "AREA": 50000, "CLASSIFICATION_SOURCE": "BUILDING_SEGMENT_BPF_BAT"}, MULTIFAMILY: {"ZONE_IDS": ["zone_2", "zone_3", "zone_4"], "AREA": 34567, "CLASSIFICATION_SOURCE": "BUILDING_SEGMENT_LIGHTING"}, HEALTHCARE_HOSPITAL: {"ZONE_IDS": ["r1","r2","r3"], "AREA": 20381, "CLASSIFICATION_SOURCE": "SPACE_LIGHTING"}
 
**Function Call:** 
- **get_zone_conditioning_category**
- **get_zone_BPF_BAT**

## Logic:  

- create a dictionary to map lighting building area types to BPF building area types: ```building_area_lookup = {
	AUTOMOTIVE_FACILITY: 			ALL_OTHER,
	CONVENTION_CENTER: 				ALL_OTHER,
	COURTHOUSE: 					ALL_OTHER,
	DINING_BAR_LOUNGE_LEISURE: 		RESTAURANT,  
	DINING_CAFETERIA_FAST_FOOD: 	RESTAURANT,
	DINING_FAMILY: 					RESTAURANT,
	DORMITORY: 						MULTIFAMILY,
	EXERCISE_CENTER: 				ALL_OTHER,  
	FIRE_STATION: 					ALL_OTHER,  
	GYMNASIUM: 						ALL_OTHER,  
	HEALTH_CARE_CLINIC: 			HEALTHCARE_HOSPITAL,  
	HOSPITAL: 						HEALTHCARE_HOSPITAL,  
	HOTEL_MOTEL: 					HOTEL_MOTEL,  
	LIBRARY: 						ALL_OTHER,  
	MANUFACTURING_FACILITY: 		ALL_OTHER,  
	MOTION_PICTURE_THEATER: 		ALL_OTHER,  
	MULTIFAMILY: 					MULTIFAMILY,
	MUSEUM: 						ALL_OTHER,  
	OFFICE: 						OFFICE,  
	PARKING_GARAGE: 				ALL_OTHER,  
	PENITENTIARY: 					ALL_OTHER,  
	PERFORMING_ARTS_THEATER: 		ALL_OTHER,  
	POLICE_STATION: 				ALL_OTHER,  
	POST_OFFICE: 					ALL_OTHER,  
	RELIGIOUS_FACILITY: 			ALL_OTHER,  
	RETAIL: 						RETAIL,  
	SCHOOL_UNIVERSITY: 				SCHOOL,  
	SPORTS_ARENA: 					ALL_OTHER,
	TOWN_HALL: 						OFFICE,  
	TRANSPORTATION: 				ALL_OTHER,  
	WAREHOUSE: 						HEATED-ONLY_STORAGE,  
	WORKSHOP: 						WAREHOUSE,  
	NONE: 							NONE, 
	}```

- use the function get_zone_conditioning_category to get a dictionary of zone id's and their conditioning category - we will only include conditioned zones in the building_area_types_with_total_area_and_zones_dict: `zone_conditioning_category_dict = get_zone_conditioning_category(RMD)`
- create dict `building_area_types_with_total_area_and_zones_dict`: `building_area_types_with_total_area_and_zones_dict = {}`
- For each building segment in RMD: `for building_segment in RMR.building.building_segments:`
	- if the building segment has a BPF_BAT assigned, assign all zones in that building segment to the BPF_BAT: `if building_segment.bpf_building_area_type != NULL:`
		- assign the BPF_BAT to be the building_segment_BPF_BAT: `building_segment_BPF_BAT = building_segment.bpf_building_area_type`
		- assign "BUILDING_SEGMENT_BPF_BAT" to classification_source: `classification_source = "BUILDING_SEGMENT_BPF_BAT"`
	- else if there is no BPF_BAT assigned, look in the building_segment lighting_building_area_type: `elif building_segment.lighting_building_area_type != NULL and building_segment.lighting_building_area_type != NONE`
		- assign the BPF_BAT to the building_segment_BPF_BAT using the lighting_space_lookup: `building_segment_BPF_BAT = building_area_lookup[building_segment.lighting_building_area_type]`
		- assign "BUILDING_SEGMENT_LIGHTING" to classification_source: `classification_source = "BUILDING_SEGMENT_LIGHTING"`
	- else look at each zone, and then each space and determine the building_segment_BPF_BAT using the largest space.lighting_space_type: `else:`
		- create a dictionary to keep track of the space types and areas: `building_segment_space_types_areas_dict = {}`
		- loop through each zone: `for zone in building_segment.zones:`
			- create a dictionary for the zone BPF_BAT space types using the function get_zone_BPF_BAT: `zone_BPF_BAT_dict = get_zone_BPF_BAT(B_RMI, zone.id)`
			- loop through the zone_BPF_BAT_dict: `for space_BPF_BAT in zone_BPF_BAT_dict:`
				- add this space type to the building_segment_space_types_areas_dict if it doesn't exist yet: `building_segment_space_types_areas_dict[space_BPF_BAT] = building_segment_space_types_areas_dict[space_BPF_BAT] or 0`
				- add the space area: `building_segment_space_types_areas_dict[space_BPF_BAT] += zone_BPF_BAT_dict[space_BPF_BAT]`
		- get the BPF_BAT with the largest floor area from building_segment_space_types_areas_dict: `building_segment_BPF_BAT = max(building_segment_space_types_areas_dict, key=lambda k: building_segment_space_types_areas_dict[k])`
		- assign "SPACE_LIGHTING" to classification_source: `classification_source = "SPACE_LIGHTING"`
	- at this point, the building_segment_BPF_BAT has been defined by one of the three approaches, add a nested dict for this type of BPF_BAT to the building_area_types_with_total_area_and_zones_dict if it doesn't exist already: `if building_segment_BPF_BAT not in building_area_types_with_total_area_and_zones_dict: building_area_types_with_total_area_and_zones_dict[building_segment_BPF_BAT] = {"ZONE_IDS":[], "AREA":0, "CLASSIFICATION_SOURCE": classification_source}`
	- loop through each zone: `for zone in building_segment.zones:`
		- using zone_conditioning_category_dict, check if the zone is conditioned. `if zone_conditioning_category_dict[zone.id] in ["CONDITIONED RESIDENTIAL", "CONDITIONED NON-RESIDENTIAL", "CONDITIONED MIXED"]`:
			- add the zone to the building_area_types_with_total_area_and_zones_dict: `building_area_types_with_total_area_and_zones_dict[building_segment_BPF_BAT]["ZONE_IDS"].append(zone.id)`
				- loop through each space: `for space in zone.spaces:`
					- add the space area to the building_area_types_with_total_area_and_zones_dict: `building_area_types_with_total_area_and_zones_dict[building_segment_BPF_BAT]["AREA"] += space.floor_area`

	 **Returns** `return building_area_types_with_total_area_and_zones_dict`  

**Notes/Questions:**  
1. Mapping scheme from lighting building area types to BPF building area types is replicated from the 90.1 Performance Based Compliance Form
2. Review subroutine 'get_zone_BPF_BAT.md' for mapping scheme from lighting space types to BPF building area types

**[Back](../_toc.md)**
