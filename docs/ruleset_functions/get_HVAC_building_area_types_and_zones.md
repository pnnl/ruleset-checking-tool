# get_HVAC_building_area_types_and_zones
**Scheme Version:** 0.0.23  

**Description:** Get the hvac_ids associated with each building area type associated with U_RMR, P_RMR, or B_RMR. Also returns the total floor area of each building area type
- used to verify the correct type of HVAC baseline system (or systems)
- HVAC building area type is determined first by looking at the space lighting type and then by looking at the building segment HVAC building area type.  Support spaces such as corridors, stairwells and other support spaces will inherit the predominant building area type EXCEPT in buildings where the predominant HVAC_BAT is residential.  In residential buildings, support spaces such as corridors and stairwells will be classified as Other Non-Residential.

**Inputs:**  
- **B-RMI**: The baseline ruleset model instance

**Returns:**  
- **building_area_types_with_total_area_and_zones_dict**: A dict that saves all the HVAC building area types in the file and includes a list of all the zone ids associated with area type as well as the total area of each building area type
 
**Function Call:** None

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
	`ATRIUM_LOW_MEDIUM: OTHER_UNDETERMINED`
	`ATRIUM_HIGH: OTHER_UNDETERMINED`
	`AUDIENCE_SEATING_AREA_AUDITORIUM: PUBLIC_ASSEMBLY`
	`AUDIENCE_SEATING_AREA_EXERCISE_CENTER: OTHER_NON_RESIDENTIAL` - PLEASE REVIEW
	`AUDIENCE_SEATING_AREA_GYMNASIUM: PUBLIC_ASSEMBLY` - PLEASE REVIEW
	`AUDIENCE_SEATING_AREA_MOTION_PICTURE_THEATER: PUBLIC_ASSEMBLY`
	`AUDIENCE_SEATING_AREA_PENITENTIARY: OTHER_NON_RESIDENTIAL` - PLEASE REVIEW
	`AUDIENCE_SEATING_AREA_PERFORMING_ARTS_THEATER: PUBLIC_ASSEMBLY`
	`AUDIENCE_SEATING_AREA_RELIGIOUS_FACILITY: PUBLIC_ASSEMBLY`
	`AUDIENCE_SEATING_AREA_SPORTS_ARENA: PUBLIC_ASSEMBLY`
	`AUDIENCE_SEATING_AREA_TRANSPORTATION_FACILITY: OTHER_NON_RESIDENTIAL` - PLEASE REVIEW (when would there be audience seating in a transportation center?)
	`AUDIENCE_SEATING_AREA_ALL_OTHER: PUBLIC_ASSEMBLY`
	`AUDIENCE_SEATING_AREA_CONVENTION_CENTER: PUBLIC_ASSEMBLY`
	`BANKING_ACTIVITY_AREA: OTHER_NON_RESIDENTIAL`
	`CLASSROOM_LECTURE_HALL_TRAINING_ROOM_PENITENTIARY: OTHER_NON_RESIDENTIAL`
	`CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL: OTHER_NON_RESIDENTIAL`
	`CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER: OTHER_NON_RESIDENTIAL`
	`CONFERENCE_MEETING_MULTIPURPOSE_ROOM: OTHER_NON_RESIDENTIAL`
	`CONFINEMENT_CELLS: OTHER_NON_RESIDENTIAL`
	`COPY_PRINT_ROOM: OTHER_UNDETERMINED`
	`CORRIDOR_FACILITY_FOR_THE_VISUALLY_IMPAIRED: OTHER_UNDETERMINED`
	`CORRIDOR_HOSPITAL: HOSPITAL`
	`CORRIDOR_MANUFACTURING_FACILITY: OTHER_NON_RESIDENTIAL`
	`CORRIDOR_ALL_OTHERS: OTHER_UNDETERMINED`
	`COURT_ROOM: OTHER_NON_RESIDENTIAL`
	`COMPUTER_ROOM: OTHER_UNDETERMINED`
	`DINING_AREA_PENITENTIARY: OTHER_NON_RESIDENTIAL`
	`DINING_AREA_FACILITY_FOR_THE_VISUALLY_IMPAIRED: OTHER_NON_RESIDENTIAL`
	`DINING_AREA_BAR_LOUNGE_OR_LEISURE_DINING: OTHER_NON_RESIDENTIAL`
	`DINING_AREA_CAFETERIA_OR_FAST_FOOD_DINING: OTHER_NON_RESIDENTIAL`
	`DINING_AREA_FAMILY_DINING: OTHER_NON_RESIDENTIAL`
	`DINING_AREA_ALL_OTHERS: OTHER_NON_RESIDENTIAL`
	`ELECTRICAL_MECHANICAL_ROOM: OTHER_UNDETERMINED`
	`EMERGENCY_VEHICLE_GARAGE: HEATED-ONLY_STORAGE`
	`FOOD_PREPARATION_AREA: OTHER_NON_RESIDENTIAL`
	`GUEST_ROOM: RESIDENTIAL`
	`JUDGES_CHAMBERS: OTHER_NON_RESIDENTIAL`
	`DWELLING_UNIT: RESIDENTIAL`
	`LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM: OTHER_NON_RESIDENTIAL`
	`LAUNDRY_WASHING_AREA: OTHER_NON_RESIDENTIAL`
	`LOADING_DOCK_INTERIOR: HEATED-ONLY_STORAGE`
	`LOBBY_FACILITY_FOR_THE_VISUALLY_IMPAIRED: OTHER_NON_RESIDENTIAL`
	`LOBBY_ELEVATOR: OTHER_UNDETERMINED`
	`LOBBY_HOTEL: OTHER_NON_RESIDENTIAL`
	`LOBBY_MOTION_PICTURE_THEATER: PUBLIC_ASSEMBLY`
	`LOBBY_PERFORMING_ARTS_THEATER: PUBLIC_ASSEMBLY`
	`LOBBY_ALL_OTHERS: OTHER_UNDETERMINED`
	`LOCKER_ROOM: OTHER_UNDETERMINED`
	`LOUNGE_BREAKROOM_HEALTH_CARE_FACILITY: HOSPITAL`
	`LOUNGE_BREAKROOM_ALL_OTHERS: OTHER_NON_RESIDENTIAL`
	`OFFICE_ENCLOSED: OTHER_NON_RESIDENTIAL`
	`OFFICE_OPEN_PLAN: OTHER_NON_RESIDENTIAL`
	`PARKING_AREA_INTERIOR: HEATED-ONLY_STORAGE`
	`PHARMACY_AREA: OTHER_NON_RESIDENTIAL` # OR RETAIL??? OR HOSPITAL???
	`RESTROOM_FACILITY_FOR_THE_VISUALLY_IMPAIRED: OTHER_UNDETERMINED`
	`RESTROOM_ALL_OTHERS: OTHER_UNDETERMINED`
	`SALES_AREA: RETAIL`
	`SEATING_AREA_GENERAL: PUBLIC_ASSEMBLY` - ??? PLEASE CHECK
	`STAIRWELL: OTHER_UNDETERMINED`
	`STORAGE_ROOM_HOSPITAL: HOSPITAL`
	`STORAGE_ROOM_SMALL: OTHER_UNDETERMINED`
	`STORAGE_ROOM_LARGE: OTHER_UNDETERMINED` - ?? OR HEATED_ONLY_STORAGE??
	`VEHICULAR_MAINTENANCE_AREA: HEATED_ONLY_STORAGE`
	`WORKSHOP: OTHER_NON_RESIDENTIAL`
	`ASSISTED_LIVING_FACILITY_CHAPEL: PUBLIC_ASSEMBLY`
	`ASSISTED_LIVING_FACILITY_RECREATION_ROOM_COMMON_LIVING_ROOM: OTHER_NON_RESIDENTIAL`
	`CONVENTION_CENTER_EXHIBIT_SPACE: PUBLIC_ASSEMBLY`
	`DORMITORY_LIVING_QUARTERS: RESIDENTIAL`
	`FIRE_STATION_SLEEPING_QUARTERS: RESIDENTIAL` - ?? PLEASE CHECK
	`GYMNASIUM_FITNESS_CENTER_EXERCISE_AREA: PUBLIC_ASSEMBLY`
	`GYMNASIUM_FITNESS_CENTER_PLAYING_AREA: PUBLIC_ASSEMBLY`
	`HEALTHCARE_FACILITY_EMERGENCY_ROOM: HOSPITAL`
	`HEALTHCARE_FACILITY_EXAM_TREATMENT_ROOM: HOSPITAL`
	`HEALTHCARE_FACILITY_NURSERY: HOSPITAL`
	`HEALTHCARE_FACILITY_NURSES_STATION: HOSPITAL`
	`HEALTHCARE_FACILITY_OPERATING_ROOM: HOSPITAL`
	`HEALTHCARE_FACILITY_PATIENT_ROOM: HOSPITAL`
	`HEALTHCARE_FACILITY_PHYSICAL_THERAPY_ROOM: HOSPITAL`
	`HEALTHCARE_FACILITY_RECOVERY_ROOM: HOSPITAL`
	`LIBRARY_READING_AREA: OTHER_NON_RESIDENTIAL`
	`LIBRARY_STACKS: OTHER_NON_RESIDENTIAL`
	`MANUFACTURING_FACILITY_DETAILED_MANUFACTURING_AREA: OTHER_NON_RESIDENTIAL`
	`MANUFACTURING_FACILITY_EQUIPMENTROOM: OTHER_NON_RESIDENTIAL`
	`MANUFACTURING_FACILITY_EXTRA_HIGH_BAY_AREA: OTHER_NON_RESIDENTIAL`
	`MANUFACTURING_FACILITY_HIGH_BAY_AREA: OTHER_NON_RESIDENTIAL`
	`MANUFACTURING_FACILITY_LOW_BAY_AREA: OTHER_NON_RESIDENTIAL`
	`MUSEUM_GENERAL_EXHIBITION_AREA: PUBLIC_ASSEMBLY`
	`MUSEUM_RESTORATION_ROOM: PUBLIC_ASSEMBLY`
	`POST_OFFICE_SORTING_AREA: OTHER_NON_RESIDENTIAL`
	`RELIGIOUS_FACILITY_FELLOWSHIP_HALL: PUBLIC_ASSEMBLY`
	`RELIGIOUS_FACILITY_WORSHIP_PULPIT_CHOIR_AREA: PUBLIC_ASSEMBLY`
	`RETAIL_FACILITIES_DRESSING_FITTING_ROOM: RETAIL`
	`RETAIL_FACILITIES_MALL_CONCOURSE: RETAIL`
	`SPORTS_ARENA_PLAYING_AREA_CLASS_I_FACILITY: PUBLIC_ASSEMBLY`
	`SPORTS_ARENA_PLAYING_AREA_CLASS_II_FACILITY: PUBLIC_ASSEMBLY`
	`SPORTS_ARENA_PLAYING_AREA_CLASS_III_FACILITY: PUBLIC_ASSEMBLY`
	`SPORTS_ARENA_PLAYING_AREA_CLASS_IV_FACILITY: PUBLIC_ASSEMBLY`
	`TRANSPORTATION_FACILITY_BAGGAGE_CAROUSEL_AREA: OTHER_NON_RESIDENTIAL`
	`TRANSPORTATION_FACILITY_AIRPORT_CONCOURSE: OTHER_NON_RESIDENTIAL`
	`TRANSPORTATION_FACILITY_TICKET_COUNTER: OTHER_NON_RESIDENTIAL`
	`WAREHOUSE_STORAGE_AREA_MEDIUM_TO_BULKY_PALLETIZED_ITEMS: HEATED_ONLY_STORAGE`
	`WAREHOUSE_STORAGE_AREA_SMALLER_HAND_CARRIED_ITEMS: HEATED_ONLY_STORAGE`
	`NONE: NONE`
	
	`}`

- create dict `building_area_types_with_total_area_and_zones_dict`: `building_area_types_with_total_area_and_zones_dict = {}`
- For each building segment in RMR: `for building_segment in RMR.building.building_segments:`
	- Create list_of_zones for storing zone_ids `list_of_zones = []`
	- For each zone in building_segment: `for zone in building_segment.zones:`
		- add zone_id to list_of_zones: `list_of_zones.append(zone.id)`
		- create space_area_type variable and set equal to "None": `space_area_type = NONE`
		- we need to look at all the spaces, map lighting space types to HVAC building area types, and find the largest floor area.  The zone will get assigned the HVAC_BAT associated with the largest floor area.
		- create a dict of space area types: `zone_space_area_types = {}`
		- create a variable for the total floor area of the zone: `zone_total_floor_area = 0`
		- loop through the spaces: `for space in zone.spaces:`
			- add the space floor area to the zone total floor area: `zone_total_floor_area += space.floor_area
			- look up the area type using `lighting_space_lookup`: `area_type = lighting_space_lookup[space.lighting_space_type]`
			- create the integer for this space area type if it doesn't exist yet: `zone_space_area_types[area_type] = zone_space_area_types[area_type] or 0`
			- add the space area to the dict under `area_type`: `zone_space_area_types[area_type] = zone_space_area_types[area_type] + space.floor_area`
		- assign the key with the maximum floor area to `space_area_type`: `space_area_type = max(zone_space_area_types, key = zone_space_area_types.get)`
		- if the space_area_type is NONE, we look at the building_segment.area_type_heating_ventilating_air_conditioning_system: `space_area_type = building_segment.area_type_heating_ventilating_air_conditioning_system`
		
		- now we need to add the data about the zone to the building_area_types_with_total_area_and_zones_dict.  If this is the first time we are seeing the space area type, we need to create the dictionary entries for this space area type.  Create the sub-dictionary: `building_area_types_with_total_area_and_zones_dict[space_area_type = {}`
		- create the integer for `building_area_types_with_total_area_and_zones_dict[space_area_type]["AREA"]` if it doesn't yet exist: `building_area_types_with_total_area_and_zones_dict[space_area_type]["AREA"] = building_area_types_with_total_area_and_zones_dict[space_area_type]["AREA"] or 0`
		- create the list for `building_area_types_with_total_area_and_zones_dict[space_area_type]["ZONE_IDS"]` if it doesn't already exist: `building_area_types_with_total_area_and_zones_dict[space_area_type]["ZONE_IDS"] = building_area_types_with_total_area_and_zones_dict[space_area_type]["ZONE_IDS"] or []`
		- add zone area: `building_area_types_with_total_area_and_zones_dict[space_area_type]["AREA"] += zone_total_floor_area`

		- Append zone_id to the dict: `building_area_types_with_total_area_and_zones_dict[space_area_type]["ZONE_IDS"].append(zone.id)`

- now we need to reclasify any spaces that we clasified as OTHER_UNDETERMINED and remove OTHER_UNDETERMINED from the dict.  Check if OTHER_UNDETERMINED is in the dict: `if OTHER_UNDETERMINED in building_area_types_with_total_area_and_zones_dict:`
	- check if the dict has a length of 1, this means that there are ONLY OTHER_UDETERMINED spaces in the RMI: `if len(building_area_types_with_total_area_and_zones_dict) == 1:`
		- change the key from OTHER_UNDETERMINED to OTHER_NON_RESIDENTIAL: `building_area_types_with_total_area_and_zones_dict[OTHER_NON_RESIDENTIAL] = building_area_types_with_total_area_and_zones_dict.pop(OTHER_UNDETERMINED)`
	- otherwise, we need to reclassify the undetermined zones as part of the largest space area type in the building: `else:`
		- create a variable to hold list of OTHER_UNDETERMINED zones: `other_undetermined_zones_list = building_area_types_with_total_area_and_zones_dict[OTHER_UNDETERMINED]["ZONE_IDS"]
		- create a variable to hold the area of OTHER_UNDETERMINED zones: `other_undetermined_zones_area = building_area_types_with_total_area_and_zones_dict[OTHER_UNDETERMINED]["AREA"]`
		- now remove OTHER_UNDETERMINED from  building_area_types_with_total_area_and_zones_dict: `building_area_types_with_total_area_and_zones_dict.pop(OTHER_UNDETERMINED)`
		
		- now that we have saved the information about OTHER_UNDETERMINED zones, and we have removed it from the dict, we determine the predominant building area type based on the remaining information.  We start by sorting the dict into a sorted list: sorted_list = sorted(building_area_types_with_total_area_and_zones_dict.items(), key=lambda x: x[1]["AREA"], reverse = True)
		- the first item in the list will be the predominant building area type: `predominant_HVAC_building_area_type = sorted_list[0][0]`
		- if the predominant_HVAC_building_area_type is RESIDENTIAL, the OTHER_UNDETERMINED zones will be added to the next largest building area type if it exists: `if predominant_HVAC_building_area_type == RESIDENTIAL:`
			- check if there is another building area type, by checking the length of building_area_types_with_total_area_and_zones_dict: `if len(sorted_list) > 1:`
				- set predominant_HVAC_building_area_type to the second item in the sorted_list: `predominant_HVAC_building_area_type = sorted_list[1][0]`
		- add the zone ids from OTHER_UNDETERMINED to the predominant_HVAC_building_area_type: `building_area_types_with_total_area_and_zones_dict[predominant_HVAC_building_area_type]["ZONE_IDS"].append(other_undetermined_zones_list)`
		- add the area from OTHER_UNDETERMINED to the predominant_HVAC_building_area_type: `building_area_types_with_total_area_and_zones_dict[predominant_HVAC_building_area_type]["AREA"] += other_undetermined_zones_area`


	 **Returns** `return buildiung_area_types_with_total_area_and_zones_dict`  

**Notes/Questions:**  
1. "Heated-Only Storage" was not listed in the schema under HeatingVentilatingAirConditioningBuildingAreaOptions2019ASHRAE901 when this function was written - double check spelling
2. a map was provided for mapping LightingBuildingAreaOptions2019ASHRAE901T951TG38, but not LightingSpaceOptions2019ASHRAE901TG37.  Double check my mapping

**[Back](../_toc.md)**
