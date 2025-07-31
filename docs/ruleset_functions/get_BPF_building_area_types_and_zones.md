# get_BPF_building_area_types_and_zones
**Schema Version:** 0.0.29

**Description:** Get a dictionary of the zone_ids associated with each BPF building area type associated with U_RMD, P_RMD, or B_RMD. Also returns the total floor area of each building area type and the source of the information (BUILDING_AREA_LIGHTING or SPACE_LIGHTING)
- BPF building area type is determined first by looking at the building segment lighting_building_area_type.  If this variable doesn't exist, the function will look at the space lighting type.  Support spaces such as corridors, stairwells and other support spaces will inherit the predominant building area type.
- the entry "CLASSIFICATION_SOURCE" in the **building_area_types_with_total_area_and_zones_dict** passes information about how the BPF_BAT was determined for each building area type.  It can be either "BUILDING_SEGMENT_LIGHTING" or "SPACE_LIGHTING"

**Inputs:**  
- **RMD**: The ruleset model description

**Returns:**  
- **building_area_types_with_total_area_and_zones_dict**: A dict that saves all the BPF building area types and includes a list of all the zone ids associated with area type as well as the total area of each building area type: {MULTIFAMILY: {"zone_id": ["zone_2", "zone_3", "zone_4"], "area": 34567, "classification_source": "BUILDING_SEGMENT_LIGHTING"}, HEALTHCARE_HOSPITAL: {"zone_id": ["zone_1","zone_5","zone_6"], "area": 20381, "classification_source": "SPACE_LIGHTING"}
 
**Function Call:**
- **get_zone_BPF_BAT**

## Logic:  

- create a dictionary to map lighting building area types to BPF building area types: ```building_area_lookup = {
	AUTOMOTIVE_FACILITY: ALL_OTHER,
	CONVENTION_CENTER: ALL_OTHER,
	COURTHOUSE: ALL_OTHER,
	DINING_BAR_LOUNGE_LEISURE: RESTAURANT,  
	DINING_CAFETERIA_FAST_FOOD: RESTAURANT,
	DINING_FAMILY: RESTAURANT,
	DORMITORY: MULTIFAMILY,
	EXERCISE_CENTER: ALL_OTHER,  
	FIRE_STATION: ALL_OTHER,  
	GYMNASIUM: ALL_OTHER,  
	HEALTH_CARE_CLINIC: HEALTHCARE_HOSPITAL,  
	HOSPITAL: HEALTHCARE_HOSPITAL,  
	HOTEL_MOTEL: HOTEL_MOTEL,  
	LIBRARY: ALL_OTHER,  
	MANUFACTURING_FACILITY: ALL_OTHER,  
	MOTION_PICTURE_THEATER: ALL_OTHER,  
	MULTIFAMILY: MULTIFAMILY,
	MUSEUM: ALL_OTHER,  
	OFFICE: OFFICE,  
	PARKING_GARAGE: ALL_OTHER,  
	PENITENTIARY: ALL_OTHER,  
	PERFORMING_ARTS_THEATER: ALL_OTHER,  
	POLICE_STATION: ALL_OTHER,  
	POST_OFFICE: ALL_OTHER,  
	RELIGIOUS_FACILITY: ALL_OTHER,  
	RETAIL: RETAIL,  
	SCHOOL_UNIVERSITY: SCHOOL,  
	SPORTS_ARENA: ALL_OTHER,
	TOWN_HALL: OFFICE,  
	TRANSPORTATION: ALL_OTHER,  
	WAREHOUSE: WAREHOUSE,  
	WORKSHOP: WAREHOUSE,  
	NONE: NONE, 
	}```

- Create a dict to store results`building_area_types_with_total_area_and_zones_dict`: `building_area_types_with_total_area_and_zones_dict = {}`
- For each building segment in RMD: `for building_segment in RMD.building.building_segments:`
	- If the building_segment lighting_building_area_type is defined: `if building_segment.lighting_building_area_type != NULL and building_segment.lighting_building_area_type != NONE`
		- Assign the BPF_BAT to the building_segment_BPF_BAT using the lighting_space_lookup: `building_segment_BPF_BAT = building_area_lookup[building_segment.lighting_building_area_type]`
		- Assign "BUILDING_SEGMENT_LIGHTING" to classification_source: `classification_source = "BUILDING_SEGMENT_LIGHTING"`
	- Else look at each zone, and then each space and determine the building_segment_BPF_BAT using the largest space.lighting_space_type: `else:`
		- Create a dictionary to keep track of the space types and areas: `building_segment_space_types_areas_dict = {}`
		- For each zone in the building segment: `for zone in building_segment.zones:`
			- Create a dictionary for the zone BPF_BAT space types using the function get_zone_BPF_BAT: `zone_BPF_BAT_dict = get_zone_BPF_BAT(B_RMD, zone.id)`
			- For each mapped building area type in the zone_BPF_BAT_dict: `for space_BPF_BAT in zone_BPF_BAT_dict:`
				- If the BAT doesn't exist yet: Add this BAT to the building_segment_space_types_areas_dict with its area: `if space_BPF_BAT not in building_segment_space_types: building_segment_space_types_areas_dict[space_BPF_BAT] = zone_BPF_BAT_dict[space_BPF_BAT]`
				- Else: Add the area: `building_segment_space_types_areas_dict[space_BPF_BAT] += zone_BPF_BAT_dict[space_BPF_BAT]`
		- Get the BPF_BAT with the largest floor area from building_segment_space_types_areas_dict: `building_segment_BPF_BAT = max(building_segment_space_types_areas_dict, key=lambda k: building_segment_space_types_areas_dict[k])`
		- Assign "SPACE_LIGHTING" to classification_source: `classification_source = "SPACE_LIGHTING"`
	- At this point, the building_segment_BPF_BAT has been defined by one of the two approaches. If the BPF_BAT doesn't exist already: add a nested dict for this BPF_BAT to the building_area_types_with_total_area_and_zones_dict : `if building_segment_BPF_BAT not in building_area_types_with_total_area_and_zones_dict: building_area_types_with_total_area_and_zones_dict[building_segment_BPF_BAT] = {"zone_id":[], "area":0, "classification_source": classification_source}`
	- If the BPF_BAT does exist already, and the classification_source is "SPACE_LIGHTING", update the dictionary item classification_source to "SPACE_LIGHTING" so that the recorded value is set to the weakest method used to determine any of the project's BPF_BATs: `elif classification_source == "SPACE_LIGHTING": building_area_types_with_total_area_and_zones_dict[building_segment_BPF_BAT]["classification_source"] = "SPACE_LIGHTING"`
    - For each zone in the building segment: `for zone in building_segment.zones:`
        - Add the zone to the building_area_types_with_total_area_and_zones_dict: `building_area_types_with_total_area_and_zones_dict[building_segment_BPF_BAT]["zone_id"].append(zone.id)`
        - For each space in the zone: `for space in zone.spaces:`
            - Add the space area to the building_area_types_with_total_area_and_zones_dict: `building_area_types_with_total_area_and_zones_dict[building_segment_BPF_BAT]["area"] += space.floor_area`

	 **Returns** `return building_area_types_with_total_area_and_zones_dict`  

**Notes/Questions:**  
1. Mapping scheme from lighting building area types to BPF building area types is replicated from the 90.1 Performance Based Compliance Form
2. Review subroutine 'get_zone_BPF_BAT.md' for mapping scheme from lighting space types to BPF building area types
3. The description of BuildingSegment data group in the schema defines building segments as "large portions of a building that share a building area type".
4. Functions `get_BPF_building_area_types_and_zones()` and `get_zone_BPF_BAT()` are based on similar concept used for determining the HVAC building area types `get_HVAC_building_area_types_and_zones()` and `get_zone_HVAC_BAT()`

**[Back](../_toc.md)**
