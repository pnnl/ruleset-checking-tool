# zone_meets_G3_1_1e
**Schema Version:** 0.0.22  

**Description:** determines whether a given zone meets the G3_1_1e exception "Thermal zones designed with heating-only systems in the proposed design serving storage rooms, stairwells, vestibules, electrical/mechanical rooms, and restrooms not exhausting or transferring air from mechanically cooled thermal zones in the proposed design shall use system type 9 or 10 in the baseline building design."

**Inputs:**
- **P-RMR**
- **zone_id**

**Returns:**  
- **result**: a string - either "E" or "No"
 
**Function Call:**
- **is_a_vestibule**

## Logic:
- create list of eligible space types: `eligible_space_types = ["STORAGE_ROOM_HOSPITAL", "STORAGE_ROOM_SMALL", "STORAGE_ROOM_LARGE", "WAREHOUSE_STORAGE_AREA_MEDIUM_TO_BULKY_PALLETIZED_ITEMS", "WAREHOUSE_STORAGE_AREA_SMALLER_HAND_CARRIED_ITEMS", "STAIRWELL", "ELECTRICAL_MECHANICAL_ROOM", "RESTROOM_FACILITY_FOR_THE_VISUALLY_IMPAIRED", "RESTROOM_ALL_OTHERS"]
- set the result variable to "No" - only a positive test can give it a different value: `result = "No"`
- set eligibility boolean to False: `eligible = TRUE`
- For each space in zone: `for space_p in zone.Spaces:`
	- check if the space has an eligible lighting type: `if space_p.lighting_space_type not in eligible_space_types:`
		- set eligibility to False - any non-compliant space type will result in a non-eligible zone: `eligible = FALSE`

- if the zone is not eligible, check if it is a vestibule: `if not eligible:`
	- set variable is_a_vestibule = is_zone_a_vestibule: `is_a_vestibule = is_zone_a_vestibule(zone, B-RMR)`
	- if the result is not equal to no, then it is eligible to be a vestibule: `if is_a_vestibule != "NO":`
		- set eligible to true: `eligible = TRUE`

- if the zone is still eligible: `if eligible:`
	- check if the proposed has a heating-only system
	- get the building_segment_p the zone is in:
	`for building_segment_p in P-RMR.building.building_segments:`
		- check if the zone is in the building_segment:
		`if zone in building_segment.zones:`
			- break - this means the variable "building_segment" is the building_segment that contains the zone:
			`break`
	- create a list of hvac system serving the zone: `hvac_systems_serving_zone = []`
	- loop through the terminals in the zone: `for terminal in zone.terminals:`
		- get the hvac system served by the terminal: `hvac_systems_serving_zone.append(terminal.served_by_heating_ventilating_air_conditioning_system)`
	- loop through each heating system: `for system_p in building_segment.heating_ventilation_air_conditioning_systems:`
		- check if system_p is in the list of hvac systems serving the zone: `if system_p in hvac_systems_serving_zone:`
			- look for a cooling system: `if system_p.cooling_system != "Null":`
				- check to see if the cooling_system_options equals "None": `if system_p.cooling_system.cooling_system_options == "None":`
					- the zone is eligible
				- otherwise: `else:`
					- there is a cooling system and the zone is not eligible: `eligible = FALSE`

- if the zone is still eligible: `if eligible:`
	- set result to "E": `result = "E"`
	- however, if there is transfer air into the space from an air conditioned zone, it is not eligible, so look for transfer air into the space: `if zone.transfer_airflow_rate > 0:`
		- there is no way of knowing where the transfer air is coming from, so for now will give the result the tag "E_T" to signal that there is transfer air.  When the rule is written, "E_T" from this function will trigger an "UNDETERMINED" result and indicate manual checking for transfer air from air-conditioned space: `result = "E_T"


**Returns** `result`


**Notes/Questions:**  
1. the "is_zone_a_vestibule" function gives only "NO" and indeterminite answers.  Is there a way to alert to confirm that the zone is a vestibule?
2. Transfer air does not indicate whether it is transferring from an air conditioned zone or not, therefore cannot do a complete check, only an alert
	221006 - Jason suggests that the schema gets modified to indicate where the transfer air is coming from ("transfer_air_from_zone")
3. does a HeatingVentilationAirConditioningSystem always have a CoolingSystem, or does it return "Null" if there is no cooling system?

**[Back](../_toc.md)**
