# does_zone_meet_G3_1_1f
**Schema Version:** 0.0.22

**Description:** determines whether a given zone meets the G3_1_1f exception "If the baseline HVAC system type is 9 or 10, use additional system types for all HVAC zones that are mechanically cooled in the proposed design."

**Inputs:**
- **P-RMI** - the proposed building
- **B-RMI** - the baseline building
- **zone_id** - the zone in the proposed building

**Returns:**  
- **result**: an enum - either YES or NO
 
**Function Call:**
- **get_HVAC_building_area_types_and_zones**
- **is_baseline_system_9**
- **is_baseline_system_10**

## Logic:
- set the result variable to NO - only a positive test can give it a different value: `result = NO`
- set eligibility boolean to False: `eligible = FALSE`

- the expected baseline system will be 9 or 10 under one of the two following conditions:
	1. the building area type is "heated-only storage"
	2. there is more than 20,000 ft2 in the building of "heated-only storage"
- get the list of HVAC building area types and zones: `hvac_building_area_types_and_zones = get_HVAC_building_area_types_and_zones(B-RMR)`
- get the predominant building area type: `predominant_type = get_predominant_HVAC_building_area_type(hvac_building_area_types_and_zones)`
- if the predominant building area type is "HEATING-ONLY_STORAGE": `if predominant_type == "HEATING-ONLY_STORAGE":`
	- the baseline system type should be either system 9 or 10, set eligible to TRUE: `eligible = TRUE`
- otherwise, check if the zone is in a non-predominant type "HEATING-ONLY_STORAGE" & greater than 20,000 ft2: `else:`
	- check if hvac_building_area_types_and_zones["HEATING-ONLY_STORAGE"]["AREA"] > 20000: `if hvac_building_area_types_and_zones["HEATING-ONLY_STORAGE"]["AREA"] > 20000:`
		- now check if the zone is in the list of zones for "HEATING-ONLY_STORAGE": `if zone_id in hvac_building_area_types_and_zones["hvac_building_area_types_and_zones"]["ZONE_IDS"]:`
			- the baseline system type should be either system 9 or 10, set eligible to TRUE: `eligibile = TRUE`

- continue only if eligible is still true: `if eligibile == TRUE:`
	- reset eligibile to false: `eligibile = FALSE`
	- get the proposed zone and building segment by looping through proposed building segments: `for building_segment_p in P-RMR.building_segments:`
		- loop through the zone in this building segment looking for the zone_id: `for zone_p in building_segment_p:`
			- if the zone_p.id == zone_id, this is the zone: `if zone_p.id == zone_id:`
				- break - this means the variable "building_segment_p" is the building_segment that contains the zone, and zone_p is the zone in the proposed:
				`break`
	- check if the proposed cooling
	- loop through each heating system: `for system_p in building_segment.heating_ventilation_air_conditioning_systems:`
		- look for a cooling system: `if system_p.cooling_system != "Null":`
			- check to see if the cooling_system_options equals "None": `if system_p.cooling_system.cooling_system_options == "None":`
				- the zone is not eligible: `eligible = FALSE`
			- otherwise: `else:`
				- there is a cooling system and the zone is eligible: `eligible = TRUE`
				- set result to YES: `result = YES`

**Returns** `result`


**Notes/Questions:**  
1. for exception e - zones in the proposed design that receive transfer air from an air conditioned zone are considered air conditioned.  There's no mention here, but I assume it's the same???
2. Transfer air does not indicate whether it is transferring from an air conditioned zone or not, therefore cannot do a complete check, only an alert
	221006 - Jason suggests that the schema gets modified to indicate where the transfer air is coming from
3. does a HeatingVentilationAirConditioningSystem always have a CoolingSystem, or does it return "Null" if there is no cooling system?
