# get_zone_HVAC_BAT
**Schema Version:** 0.0.28  

**Description:** Get a dictionary of the HVAC_BAT and areas for a given zone.
- used to verify the correct type of HVAC baseline system (or systems)
- The function looks at the space lighting type.

**Inputs:**  
- **B-RMI**: The baseline ruleset model instance
- **zone_id**: the id of the zone

**Returns:**  
- **zone_HVAC_BAT_dict**: A dict for the zone that saves the HVAC_BAT as keys and the areas as the values. Example: {OTHER_NON_RESIDENTIAL: 500, PUBLIC_ASSEMBLY: 2000}
 
**Function Call:** 
- None

## Logic:  
- create lookup table for lighting space types: `lighting_space_lookup = {`  
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

- create dict `zone_HVAC_BAT_dict`: `zone_HVAC_BAT_dict = {}`
- get the zone using the function get_object_by_id: `get_object_by_id(B_RMI, zone_id)`
         - look at each space: `for space in zone.spaces:`
                  - look up the HVAC_BAT for the space using the lighting_space_lookup: `space_HVAC_BAT = lighting_space_lookup[space.lighting_space_type]`
                  - add this space type to the zone_HVAC_BAT_dict if it doesn't exist yet: `zone_HVAC_BAT_dict[space_HVAC_BAT] = zone_HVAC_BAT_dict[space_HVAC_BAT] or 0`
                  - add the space area: `zone_HVAC_BAT_dict[space_HVAC_BAT] += space.floor_area`

	 **Returns** `return zone_HVAC_BAT_dict`  

**Notes/Questions:**  
1. a map was provided for mapping LightingBuildingAreaOptions2019ASHRAE901T951TG38, but not LightingSpaceOptions2019ASHRAE901TG37.  Double check my mapping

**[Back](../_toc.md)**