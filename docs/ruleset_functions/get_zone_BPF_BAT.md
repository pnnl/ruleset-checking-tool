# get_zone_BPF_BAT
**Schema Version:** 0.0.29

**Description:** Get a dictionary of the BPF_BAT and areas for a given zone.
- The function looks at the space lighting type to guess a building area type for a BuildingSegment whose lighting_building_area_type is NONE. The schema note suggests that lighting building area type always be populated - even when the space-by-space lighting method is used. This function ideally would not be used but is included as a backup.

**Inputs:**  
- **RMD**: The ruleset model instance
- **zone_id**: The id of the zone

**Returns:**  
- **zone_BPF_BAT_dict**: A dict for the zone that saves the BPF_BAT as keys and the areas as the values. Example: {SCHOOL: 50000, UNDETERMINED: 2000}
 
**Function Call:** 
- None

## Logic:  

- create a dictionary to map lighting space types to BPF building area types: ```building_area_lookup = { 
	ATRIUM_LOW_MEDIUM: UNDETERMINED,						
	ATRIUM_HIGH: UNDETERMINED,
	AUDIENCE_SEATING_AREA_AUDITORIUM: UNDETERMINED,
	AUDIENCE_SEATING_AREA_CONVENTION_CENTER: ALL_OTHER,
	AUDIENCE_SEATING_AREA_EXERCISE_CENTER: UNDETERMINED,
	AUDIENCE_SEATING_AREA_GYMNASIUM: UNDETERMINED,
	AUDIENCE_SEATING_AREA_MOTION_PICTURE_THEATER: ALL_OTHER,
	AUDIENCE_SEATING_AREA_PENITENTIARY: ALL_OTHER,
	AUDIENCE_SEATING_AREA_PERFORMING_ARTS_THEATER: UNDETERMINED,
	AUDIENCE_SEATING_AREA_RELIGIOUS_FACILITY: UNDETERMINED,
	AUDIENCE_SEATING_AREA_SPORTS_ARENA: UNDETERMINED,
	AUDIENCE_SEATING_AREA_TRANSPORTATION_FACILITY: ALL_OTHER,
	AUDIENCE_SEATING_AREA_ALL_OTHER: UNDETERMINED,
	BANKING_ACTIVITY_AREA: UNDETERMINED,
	CLASSROOM_LECTURE_HALL_TRAINING_ROOM_PENITENTIARY: ALL_OTHER,
	CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL: SCHOOL,
	CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER:	UNDETERMINED,
	CONFERENCE_MEETING_MULTIPURPOSE_ROOM: UNDETERMINED,
	CONFINEMENT_CELLS: ALL_OTHER,
	COPY_PRINT_ROOM: UNDETERMINED,
	CORRIDOR_FACILITY_FOR_THE_VISUALLY_IMPAIRED: UNDETERMINED,
	CORRIDOR_HOSPITAL: HEALTHCARE_HOSPITAL,
	CORRIDOR_MANUFACTURING_FACILITY: ALL_OTHER,
	CORRIDOR_ALL_OTHERS: UNDETERMINED,
	COURT_ROOM:	OFFICE,
	COMPUTER_ROOM: UNDETERMINED,
	DINING_AREA_PENITENTIARY: ALL_OTHER,
	DINING_AREA_FACILITY_FOR_THE_VISUALLY_IMPAIRED: UNDETERMINED,
	DINING_AREA_BAR_LOUNGE_OR_LEISURE_DINING: RESTAURANT,
	DINING_AREA_CAFETERIA_OR_FAST_FOOD_DINING: RESTAURANT,
	DINING_AREA_FAMILY_DINING: RESTAURANT,
	DINING_AREA_ALL_OTHERS: RESTAURANT,
	ELECTRICAL_MECHANICAL_ROOM: UNDETERMINED,
	EMERGENCY_VEHICLE_GARAGE: UNDETERMINED,
	FOOD_PREPARATION_AREA: UNDETERMINED,
	GUEST_ROOM: HOTEL_MOTEL,
	JUDGES_CHAMBERS: OFFICE,
	DWELLING_UNIT: MULTIFAMILY,
	LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM: ALL_OTHER,
	LAUNDRY_WASHING_AREA: UNDETERMINED,
	LOADING_DOCK_INTERIOR: UNDETERMINED,
	LOBBY_FACILITY_FOR_THE_VISUALLY_IMPAIRED: UNDETERMINED,
	LOBBY_ELEVATOR: UNDETERMINED,
	LOBBY_HOTEL: HOTEL_MOTEL,
	LOBBY_MOTION_PICTURE_THEATER: ALL_OTHER,
	LOBBY_PERFORMING_ARTS_THEATER: ALL_OTHER,
	LOBBY_ALL_OTHERS: UNDETERMINED,
	LOCKER_ROOM: UNDETERMINED,
	LOUNGE_BREAKROOM_HEALTH_CARE_FACILITY: HEALTHCARE_HOSPITAL,
	LOUNGE_BREAKROOM_ALL_OTHERS: UNDETERMINED,
	OFFICE_ENCLOSED: OFFICE,
	OFFICE_OPEN_PLAN: OFFICE,
	PARKING_AREA_INTERIOR: UNDETERMINED,
	PHARMACY_AREA: UNDETERMINED,
	RESTROOM_FACILITY_FOR_THE_VISUALLY_IMPAIRED: UNDETERMINED,
	RESTROOM_ALL_OTHERS: UNDETERMINED,
	SALES_AREA: RETAIL,
	SEATING_AREA_GENERAL: UNDETERMINED,
	STAIRWELL: UNDETERMINED,
	STORAGE_ROOM_HOSPITAL: HEALTHCARE_HOSPITAL,
	STORAGE_ROOM_SMALL: UNDETERMINED,
	STORAGE_ROOM_LARGE: UNDETERMINED,
	VEHICULAR_MAINTENANCE_AREA: ALL_OTHER,
	WORKSHOP: UNDETERMINED,
	ASSISTED_LIVING_FACILITY_CHAPEL: UNDETERMINED,
	ASSISTED_LIVING_FACILITY_RECREATION_ROOM_COMMON_LIVING_ROOM: UNDETERMINED,
	CONVENTION_CENTER_EXHIBIT_SPACE: ALL_OTHER,
	DORMITORY_LIVING_QUARTERS: MULTIFAMILY,  
	FIRE_STATION_SLEEPING_QUARTERS: UNDETERMINED,
	GYMNASIUM_FITNESS_CENTER_EXERCISE_AREA: UNDETERMINED,
	GYMNASIUM_FITNESS_CENTER_PLAYING_AREA: UNDETERMINED,
	HEALTHCARE_FACILITY_EMERGENCY_ROOM: HEALTHCARE_HOSPITAL,
	HEALTHCARE_FACILITY_EXAM_TREATMENT_ROOM: HEALTHCARE_HOSPITAL,
    HEALTHCARE_FACILITY_MEDICAL_SUPPLY_ROOM: HEALTHCARE_HOSPITAL,
	HEALTHCARE_FACILITY_NURSERY: HEALTHCARE_HOSPITAL,
	HEALTHCARE_FACILITY_NURSES_STATION: HEALTHCARE_HOSPITAL,
	HEALTHCARE_FACILITY_OPERATING_ROOM: HEALTHCARE_HOSPITAL,
	HEALTHCARE_FACILITY_PATIENT_ROOM: HEALTHCARE_HOSPITAL,
	HEALTHCARE_FACILITY_PHYSICAL_THERAPY_ROOM: HEALTHCARE_HOSPITAL,
	HEALTHCARE_FACILITY_RECOVERY_ROOM: HEALTHCARE_HOSPITAL,
	LIBRARY_READING_AREA: UNDETERMINED,
	LIBRARY_STACKS: UNDETERMINED,
	MANUFACTURING_FACILITY_DETAILED_MANUFACTURING_AREA: ALL_OTHER,
	MANUFACTURING_FACILITY_EQUIPMENTROOM: ALL_OTHER,
	MANUFACTURING_FACILITY_EXTRA_HIGH_BAY_AREA: ALL_OTHER,
	MANUFACTURING_FACILITY_HIGH_BAY_AREA: ALL_OTHER,
	MANUFACTURING_FACILITY_LOW_BAY_AREA: ALL_OTHER,
	MUSEUM_GENERAL_EXHIBITION_AREA: ALL_OTHER,
	MUSEUM_RESTORATION_ROOM: ALL_OTHER,
	POST_OFFICE_SORTING_AREA: ALL_OTHER,
	RELIGIOUS_FACILITY_FELLOWSHIP_HALL: ALL_OTHER,
	RELIGIOUS_FACILITY_WORSHIP_PULPIT_CHOIR_AREA: ALL_OTHER,
	RETAIL_FACILITIES_DRESSING_FITTING_ROOM: RETAIL,
	RETAIL_FACILITIES_MALL_CONCOURSE: RETAIL,
	SPORTS_ARENA_PLAYING_AREA_CLASS_I_FACILITY: ALL_OTHER,
	SPORTS_ARENA_PLAYING_AREA_CLASS_II_FACILITY: ALL_OTHER,
	SPORTS_ARENA_PLAYING_AREA_CLASS_III_FACILITY: ALL_OTHER,
	SPORTS_ARENA_PLAYING_AREA_CLASS_IV_FACILITY: UNDETERMINED,
	TRANSPORTATION_FACILITY_BAGGAGE_CAROUSEL_AREA: ALL_OTHER,
	TRANSPORTATION_FACILITY_AIRPORT_CONCOURSE: ALL_OTHER,
	TRANSPORTATION_FACILITY_TICKET_COUNTER: ALL_OTHER,
	WAREHOUSE_STORAGE_AREA_MEDIUM_TO_BULKY_PALLETIZED_ITEMS: WAREHOUSE,
	WAREHOUSE_STORAGE_AREA_SMALLER_HAND_CARRIED_ITEMS: WAREHOUSE
	}```

- create dictionary to store the sum of space area assigned to each mapped BPF building area type `zone_BPF_BAT_dict`: `zone_BPF_BAT_dict = {}`
- get the zone using the function get_object_by_id: `get_object_by_id(B_RMD, zone_id)`
- iterate through each space in the zone: `for space in zone.spaces:`
  - get the lighting space type: `lighting_space_type = space.get(lighting_space_type, None)`
  - map from the lighting space type to the BPF building area type: `space_BPF_BAT = "UNDETERMINED" if lighting_space_type is None else BUILDING_AREA_LOOKUP[lighting_space_type]`
  - add the space area if it exists: `if space_BPF_BAT in zone_BPF_BAT_dict: zone_BPF_BAT_dict[space_BPF_BAT] += space.floor_area`
  - otherwise just add this space type to the zone_BPF_BAT_dict if it doesn't exist yet: `zone_BPF_BAT_dict[space_BPF_BAT] = space.floor_area`

       **Returns** `return zone_BPF_BAT_dict`  

**Notes/Questions:** 
1. at the time of writing this RDS, bpf_building_area_type is not yet a part of the schema.
2. Check Mapping Scheme:
   - Scheme Overview:
   - UNDETERMINED = Space type could exist in more than one of the BPF Building Area Types. Lean towards UNDETERMINED in uncertainty because misinterpretation by this function could cause false FAIL outcomes
   - [MULTIFAMILY, HEALTHCARE_HOSPITAL, OFFICE, RESTAURANT, RETAIL, SCHOOL, WAREHOUSE] = Space type is most likely to exist in one of these building area types
   - ALL_OTHER = Space type is not likely to exist in any of [MULTIFAMILY, HEALTHCARE_HOSPITAL, OFFICE, RESTAURANT, RETAIL, SCHOOL, WAREHOUSE] building area types

**[Back](../_toc.md)**
