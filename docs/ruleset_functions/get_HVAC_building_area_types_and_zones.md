# get_HVAC_building_area_types_and_zones
**Schema Version:** 0.0.23  

**Description:** Get a dictionary of the zone_ids associated with each building area type associated with U_RMR, P_RMR, or B_RMR. Also returns the total floor area of each building area type and the source of the information (BUILDING_SEGMENT_HVAC_BAT, BUILDING_SEGMENT_LIGHTING or SPACE_LIGHTING)
- used to verify the correct type of HVAC baseline system (or systems)
- HVAC building area type is determined first by looking at the building segment HVAC_BAT.  If this variable does not exist, the function next looks at building segment lighting_building_area_type.  If this variable doesn't exist, the function will look at the space lighting type.  Support spaces such as corridors, stairwells and other support spaces will inherit the predominant building area type EXCEPT in buildings where the predominant HVAC_BAT is residential.  If corridors and stairwells will are not classified by the HVAC_BAT, they will be classified as Other Non-Residential.
- the entry "CLASSIFICATION_SOURCE" in the **building_area_types_with_total_area_and_zones_dict** passes information about how the HVAC_BAT was determined for each segment along

**Inputs:**  
- **B-RMI**: The baseline ruleset model instance

**Returns:**  
- **building_area_types_with_total_area_and_zones_dict**: A dict that saves all the HVAC building area types and includes a list of all the zone ids associated with area type as well as the total area of each building area type: {OTHER_NON_RESIDENTIAL: {"ZONE_IDS": ["zone_1","zone_5"], "AREA": 1234, "CLASSIFICATION_SOURCE": "BUILDING_SEGMENT_HVAC_BAT"}, PUBLIC_ASSEMBLY: {"ZONE_IDS": ["zone_2", "zone_3", "zone_4"], "AREA": 34567, "CLASSIFICATION_SOURCE": "BUILDING_SEGMENT_LIGHTING"}, RESIDENTIAL: {"ZONE_IDS": ["r1","r2","r3"], "AREA": 20381, "CLASSIFICATION_SOURCE": "SPACE_LIGHTING"}
 
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
	`AUDIENCE_SEATING_AREA_EXERCISE_CENTER: OTHER_NON_RESIDENTIAL` - **PLEASE REVIEW**  
	`AUDIENCE_SEATING_AREA_GYMNASIUM: PUBLIC_ASSEMBLY` - **PLEASE REVIEW**  
	`AUDIENCE_SEATING_AREA_MOTION_PICTURE_THEATER: PUBLIC_ASSEMBLY`  
	`AUDIENCE_SEATING_AREA_PENITENTIARY: OTHER_NON_RESIDENTIAL` - **PLEASE REVIEW**  
	`AUDIENCE_SEATING_AREA_PERFORMING_ARTS_THEATER: PUBLIC_ASSEMBLY`  
	`AUDIENCE_SEATING_AREA_RELIGIOUS_FACILITY: PUBLIC_ASSEMBLY`  
	`AUDIENCE_SEATING_AREA_SPORTS_ARENA: PUBLIC_ASSEMBLY`  
	`AUDIENCE_SEATING_AREA_TRANSPORTATION_FACILITY: OTHER_NON_RESIDENTIAL` - **PLEASE REVIEW** (when would there be audience seating in a transportation center?)  
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
	`PHARMACY_AREA: OTHER_NON_RESIDENTIAL` **OR RETAIL??? OR HOSPITAL???**  
	`RESTROOM_FACILITY_FOR_THE_VISUALLY_IMPAIRED: OTHER_UNDETERMINED`  
	`RESTROOM_ALL_OTHERS: OTHER_UNDETERMINED`  
	`SALES_AREA: RETAIL`  
	`SEATING_AREA_GENERAL: PUBLIC_ASSEMBLY` - ??? **PLEASE CHECK**  
	`STAIRWELL: OTHER_UNDETERMINED`  
	`STORAGE_ROOM_HOSPITAL: HOSPITAL`  
	`STORAGE_ROOM_SMALL: OTHER_UNDETERMINED`  
	`STORAGE_ROOM_LARGE: OTHER_UNDETERMINED` - **?? OR HEATED_ONLY_STORAGE??**  
	`VEHICULAR_MAINTENANCE_AREA: HEATED_ONLY_STORAGE`  
	`WORKSHOP: OTHER_NON_RESIDENTIAL`  
	`ASSISTED_LIVING_FACILITY_CHAPEL: PUBLIC_ASSEMBLY`  
	`ASSISTED_LIVING_FACILITY_RECREATION_ROOM_COMMON_LIVING_ROOM: OTHER_NON_RESIDENTIAL`  
	`CONVENTION_CENTER_EXHIBIT_SPACE: PUBLIC_ASSEMBLY`  
	`DORMITORY_LIVING_QUARTERS: RESIDENTIAL`  
	`FIRE_STATION_SLEEPING_QUARTERS: RESIDENTIAL` - **?? PLEASE CHECK**  
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
	- if the building segment has a HVAC_BAT assigned, assign all zones in that building segment to the HVAC_BAT: `if building_segment.area_type_heating_ventilating_air_conditioning_system != NULL:`
		- assign the HVAC_BAT to be the building_segment_HVAC_BAT: `building_segment_HVAC_BAT = building_segment.area_type_heating_ventilating_air_conditioning_system`
		- assign "BUILDING_SEGMENT_HVAC_BAT" to classification_source: `classification_source = "BUILDING_SEGMENT_HVAC_BAT"`
	- else if there is no HVAC_BAT assigned, look in the building_segment lighting_building_area_type: `elif building_segment.lighting_building_area_type != NULL`
		- assign the HVAC_BAT to the building_segment_HVAC_BAT using the lighting_space_lookup: `building_segment_HVAC_BAT = lighting_space_lookup[building_segment.lighting_building_area_type]`
		- assign "BUILDING_SEGMENT_LIGHTING" to classification_source: `classification_source = "BUILDING_SEGMENT_LIGHTING"`
	- else look at each zone, and then each space and determine the building_segment_HVAC_BAT using the largest space.lighting_space_type: `else:`
		- create a dictionary to keep track of the space types and areas: `building_segment_space_types_areas_dict = {}`
		- look at each zone: `for zone in building_segment.zones:`
			- look at each space: `for space in zone.spaces:`
				- look up the HVAC_BAT for the space using the lighting_space_lookup: `space_HVAC_BAT = lighting_space_lookup[space.lighting_space_type]`
				- add this space type to the building_segment_space_types_areas_dict if it doesn't exist yet: `building_segment_space_types_areas_dict[space_HVAC_BAT] = building_segment_space_types_areas_dict[space_HVAC_BAT] or 0`
				- add the space area: `building_segment_space_types_areas_dict[space_HVAC_BAT] += space.floor_area`
		- get the HVAC_BAT with the largest floor area from building_segment_space_types_areas_dict: `building_segment_HVAC_BAT = max(building_segment_space_types_areas_dict, key=building_segment_space_types_areas_dict.get)`
		- assign "SPACE_LIGHTING" to classification_source: `classification_source = "SPACE_LIGHTING"`
	- at this point, the building_segment_HVAC_BAT has been defined by one of the three approaches, add a list for this type of HVAC_BAT to the building_area_types_with_total_area_and_zones_dict if it doesn't exist already: `building_area_types_with_total_area_and_zones_dict[building_segment_HVAC_BAT] = building_area_types_with_total_area_and_zones_dict[building_segment_HVAC_BAT] or {"ZONE_IDS":[], "AREA":0, "CLASSIFICATION_SOURCE": classification_source}`
	- loop through each zone: `for zone in building_segment.zones:`
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
