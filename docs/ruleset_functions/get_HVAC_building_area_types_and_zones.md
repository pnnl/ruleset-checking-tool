# get_HVAC_building_area_types_and_zones

**Description:** Get the hvac_ids associated with each building area type associated with U_RMR, P_RMR, or B_RMR. Also returns the total floor area of each building area type
- used to verify the correct type of HVAC baseline system (or systems)

**Inputs:**  
- **U-RMR or P-RMR or B-RMR**: The U-RMR, P-RMR or B-RMR

**Returns:**  
- **list_buildiung_area_types_with_total_area_and_zones**: A dict that saves all the HVAC building area types in the file and includes a list of all the zone ids associated with area type as well as the total area of each building area type
 
**Function Call:** None

## Logic:  
- create lookup table for lighting space types: `lighting_space_lookup = {}`
	- `lighting_space_lookup["AUTOMOTIVE_FACILITY"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["CONVENTION_CENTER"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["COURTHOUSE"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["DINING_BAR_LOUNGE_LEISURE"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["DINING_CAFETERIA_FAST_FOOD"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["DINING_FAMILY"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["DORMITORY"] = "RESIDENTIAL"`
	- `lighting_space_lookup["EXERCISE_CENTER"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["FIRE_STATION"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["GYMNASIUM"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["HEALTH_CARE_CLINIC"] = "HOSPITAL"`
	- `lighting_space_lookup["HOSPITAL"] = "HOSPITAL"`
	- `lighting_space_lookup["HOTEL_MOTEL"] = "RESIDENTIAL"`
	- `lighting_space_lookup["LIBRARY"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["MANUFACTURING_FACILITY"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["MOTION_PICTURE_THEATER"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["MULTIFAMILY"] = "RESIDENTIAL"`
	- `lighting_space_lookup["MUSEUM"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["OFFICE"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["PARKING_GARAGE"] = "HEATED-ONLY_STORAGE"`
	- `lighting_space_lookup["PENITENTIARY"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["PERFORMING_ARTS_THEATER"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["POLICE_STATION"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["POST_OFFICE"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["RELIGIOUS_FACILITY"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["RETAIL"] = "RETAIL"`
	- `lighting_space_lookup["SCHOOL_UNIVERSITY"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["SPORTS_ARENA"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["TOWN_HALL"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["TRANSPORTATION"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["WAREHOUSE"] = "HEATED-ONLY_STORAGE"`
	- `lighting_space_lookup["WORKSHOP"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["NONE"] = "None"`
	- `lighting_space_lookup["ATRIUM_LOW_MEDIUM"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["ATRIUM_HIGH"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["AUDIENCE_SEATING_AREA_AUDITORIUM"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["AUDIENCE_SEATING_AREA_EXERCISE_CENTER"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["AUDIENCE_SEATING_AREA_GYMNASIUM"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["AUDIENCE_SEATING_AREA_MOTION_PICTURE_THEATER"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["AUDIENCE_SEATING_AREA_PENITENTIARY"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["AUDIENCE_SEATING_AREA_PERFORMING_ARTS_THEATER"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["AUDIENCE_SEATING_AREA_RELIGIOUS_FACILITY"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["AUDIENCE_SEATING_AREA_SPORTS_ARENA"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["AUDIENCE_SEATING_AREA_TRANSPORTATION_FACILITY"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["AUDIENCE_SEATING_AREA_ALL_OTHER"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["AUDIENCE_SEATING_AREA_CONVENTION_CENTER"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["BANKING_ACTIVITY_AREA"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["CLASSROOM_LECTURE_HALL_TRAINING_ROOM_PENITENTIARY"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["CONFERENCE_MEETING_MULTIPURPOSE_ROOM"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["CONFINEMENT_CELLS"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["COPY_PRINT_ROOM"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["CORRIDOR_FACILITY_FOR_THE_VISUALLY_IMPAIRED"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["CORRIDOR_HOSPITAL"] = "HOSPITAL"`
	- `lighting_space_lookup["CORRIDOR_MANUFACTURING_FACILITY"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["CORRIDOR_ALL_OTHERS"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["COURT_ROOM"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["COMPUTER_ROOM"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["DINING_AREA_PENITENTIARY"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["DINING_AREA_FACILITY_FOR_THE_VISUALLY_IMPAIRED"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["DINING_AREA_BAR_LOUNGE_OR_LEISURE_DINING"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["DINING_AREA_CAFETERIA_OR_FAST_FOOD_DINING"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["DINING_AREA_FAMILY_DINING"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["DINING_AREA_ALL_OTHERS"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["ELECTRICAL_MECHANICAL_ROOM"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["EMERGENCY_VEHICLE_GARAGE"] = "HEATED-ONLY_STORAGE"`
	- `lighting_space_lookup["FOOD_PREPARATION_AREA"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["GUEST_ROOM"] = "RESIDENTIAL"`
	- `lighting_space_lookup["JUDGES_CHAMBERS"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["DWELLING_UNIT"] = "RESIDENTIAL"`
	- `lighting_space_lookup["LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["LAUNDRY_WASHING_AREA"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["LOADING_DOCK_INTERIOR"] = "HEATED-ONLY_STORAGE"`
	- `lighting_space_lookup["LOBBY_FACILITY_FOR_THE_VISUALLY_IMPAIRED"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["LOBBY_ELEVATOR"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["LOBBY_HOTEL"] = "RESIDENTIAL"`
	- `lighting_space_lookup["LOBBY_MOTION_PICTURE_THEATER"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["LOBBY_PERFORMING_ARTS_THEATER"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["LOBBY_ALL_OTHERS"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["LOCKER_ROOM"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["LOUNGE_BREAKROOM_HEALTH_CARE_FACILITY"] = "HOSPITAL"
	- `lighting_space_lookup["LOUNGE_BREAKROOM_ALL_OTHERS"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["OFFICE_ENCLOSED"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["OFFICE_OPEN_PLAN"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["PARKING_AREA_INTERIOR"] = "HEATED-ONLY_STORAGE"
	- `lighting_space_lookup["PHARMACY_AREA"] = "OTHER_NON_RESIDENTIAL"` # OR RETAIL??? OR HOSPITAL???
	- `lighting_space_lookup["RESTROOM_FACILITY_FOR_THE_VISUALLY_IMPAIRED"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["RESTROOM_ALL_OTHERS"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["SALES_AREA"] = "RETAIL"`
	- `lighting_space_lookup["SEATING_AREA_GENERAL"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["STAIRWELL"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["STORAGE_ROOM_HOSPITAL"] = "HOSPITAL"
	- `lighting_space_lookup["STORAGE_ROOM_SMALL"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["STORAGE_ROOM_LARGE"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["VEHICULAR_MAINTENANCE_AREA"] = "HEATED-ONLY_STORAGE"
	- `lighting_space_lookup["WORKSHOP"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["ASSISTED_LIVING_FACILITY_CHAPEL"] = "RESIDENTIAL"`
	- `lighting_space_lookup["ASSISTED_LIVING_FACILITY_RECREATION_ROOM_COMMON_LIVING_ROOM"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["CONVENTION_CENTER_EXHIBIT_SPACE"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["DORMITORY_LIVING_QUARTERS"] = "RESIDENTIAL"`
	- `lighting_space_lookup["FIRE_STATION_SLEEPING_QUARTERS"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["GYMNASIUM_FITNESS_CENTER_EXERCISE_AREA"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["GYMNASIUM_FITNESS_CENTER_PLAYING_AREA"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["HEALTHCARE_FACILITY_EMERGENCY_ROOM"] = "HOSPITAL"`
	- `lighting_space_lookup["HEALTHCARE_FACILITY_EXAM_TREATMENT_ROOM"] = "HOSPITAL"`
	- `lighting_space_lookup["HEALTHCARE_FACILITY_NURSERY"] = "HOSPITAL"`
	- `lighting_space_lookup["HEALTHCARE_FACILITY_NURSES_STATION"] = "HOSPITAL"`
	- `lighting_space_lookup["HEALTHCARE_FACILITY_OPERATING_ROOM"] = "HOSPITAL"`
	- `lighting_space_lookup["HEALTHCARE_FACILITY_PATIENT_ROOM"] = "HOSPITAL"`
	- `lighting_space_lookup["HEALTHCARE_FACILITY_PHYSICAL_THERAPY_ROOM"] = "HOSPITAL"`
	- `lighting_space_lookup["HEALTHCARE_FACILITY_RECOVERY_ROOM"] = "HOSPITAL"`
	- `lighting_space_lookup["LIBRARY_READING_AREA"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["LIBRARY_STACKS"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["MANUFACTURING_FACILITY_DETAILED_MANUFACTURING_AREA"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["MANUFACTURING_FACILITY_EQUIPMENTROOM"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["MANUFACTURING_FACILITY_EXTRA_HIGH_BAY_AREA"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["MANUFACTURING_FACILITY_HIGH_BAY_AREA"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["MANUFACTURING_FACILITY_LOW_BAY_AREA"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["MUSEUM_GENERAL_EXHIBITION_AREA"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["MUSEUM_RESTORATION_ROOM"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["POST_OFFICE_SORTING_AREA"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["RELIGIOUS_FACILITY_FELLOWSHIP_HALL"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["RELIGIOUS_FACILITY_WORSHIP_PULPIT_CHOIR_AREA"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["RETAIL_FACILITIES_DRESSING_FITTING_ROOM"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["RETAIL_FACILITIES_MALL_CONCOURSE"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["SPORTS_ARENA_PLAYING_AREA_CLASS_I_FACILITY"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["SPORTS_ARENA_PLAYING_AREA_CLASS_II_FACILITY"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["SPORTS_ARENA_PLAYING_AREA_CLASS_III_FACILITY"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["SPORTS_ARENA_PLAYING_AREA_CLASS_IV_FACILITY"] = "PUBLIC_ASSEMBLY"`
	- `lighting_space_lookup["TRANSPORTATION_FACILITY_BAGGAGE_CAROUSEL_AREA"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["TRANSPORTATION_FACILITY_AIRPORT_CONCOURSE"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["TRANSPORTATION_FACILITY_TICKET_COUNTER"] = "OTHER_NON_RESIDENTIAL"`
	- `lighting_space_lookup["WAREHOUSE_STORAGE_AREA_MEDIUM_TO_BULKY_PALLETIZED_ITEMS"] = "HEATED-ONLY_STORAGE"
	- `lighting_space_lookup["WAREHOUSE_STORAGE_AREA_SMALLER_HAND_CARRIED_ITEMS"] = "HEATED-ONLY_STORAGE"

- For each building segment in RMR: `for building_segment in RMR.building.building_segments:`
	- Create list_of_zones for storing zone_ids `list_of_zones = []`
	- For each zone in building_segment: `for zone in building_segment.zones:`
		- add zone_id to list_of_zones: `list_of_zones.append(zone.id)`
		- create space_area_type variable and set equal to "None": `space_area_type = "None"`
		- check if there is an HVAC Building Area Type: `if building_segment.area_type_heating_ventilation_air_conditioning_system != "Null":`
			- set space_area_type equal to HVAC BAT: `space_area_type = building_segment.area_type_heating_ventilation_air_conditioning_system`
		- else:
			- look for a lighting_building_area_type: `if building_segment.lighting_building_area_type != "Null":`
				- set space_area_type based on the lookup table: `space_area_type = lighting_space_lookup[building_segment.lighting_building_area_type`
		- For each space in zone: `for space in zone.spaces:`
			- check if there is a value in space_area_type: `if space_area_type != "None":`
				- add space area: `list_buildiung_area_types_with_total_area_and_zones[space_area_type]["AREA"] += space.floor_area`
			- otherwise, we'll need to map the building area type off of the ligthing category: `else:`
				- set the space area type based on lighting space area: `space_area_type = lighting_space_lookup[space.lighting_space_type]`
				- add space to the area based on space.lighting_space_type: `list_buildiung_area_types_with_total_area_and_zones[space_area_type]["AREA"] += space.floor_area`

	- Append zone_ids to the dict: `list_buildiung_area_types_with_total_area_and_zones[space_area_type]["ZONE_IDS"] = list_of_zones`
	
	 **Returns** `return list_buildiung_area_types_with_total_area_and_zones`  

**Notes/Questions:**  
1. "Heated-Only Storage" was not listed in the schema under HeatingVentilatingAirConditioningBuildingAreaOptions2019ASHRAE901 when this function was written - double check spelling
2. a map was provided for mapping LightingBuildingAreaOptions2019ASHRAE901T951TG38, but not LightingSpaceOptions2019ASHRAE901TG37.  Double check my mapping

**[Back](../_toc.md)**
