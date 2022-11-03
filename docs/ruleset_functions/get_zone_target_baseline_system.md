# get_zone_target_baseline_system
**Schema Version:** 0.0.22  

**Description:** Following G3.1.1, determines the baseline system type for each zone in a building

**Inputs:**
- **P-RMD**
- **B-RMD**

**Returns:**  
- **zones_and_systems**: a dictionary with zone / list pairs where the first value in the list is the expected system type (ex "SYS-3") and the second value is the rule used to choose the system, (eg "G3_1_1e"): zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = "SYS-3"; zones_and_systems[zone]["SYSTEM_ORIGIN"] =  "G3_1_1e"
 
**Function Call:**
- **get_HVAC_building_area_types_and_zones**
- **does_zone_meet_G3_1_1c**
- **does_zone_meet_G3_1_1e**
- **does_zone_meet_G3_1_1f**
- **does_zone_meet_G3_1_1g**
- **get_predominant_HVAC_building_area_type**
- **get_number_of_floors**
- **expected_system_type_from_Table_G3_1_1**

**Data Lookup**
- **Table G3.1.1**

## Logic:
- create zones_and_systems list: `zones_and_systems = {}`
- pre-fill the list with an empty string:
	- `for building_segment in RMR.building.building_segments:`
		- `for zone in building_segment.zones:`
			- `zones_and_systems[zone] = {}`
- get the list of HVAC building area types and zones: `list_building_area_types_and_zones = get_HVAC_building_area_types_and_zones(B-RMR)`
- get the predominant building area type: `predominant_building_area_type = get_predominant_HVAC_building_area_type(list_building_area_types_and_zones)`
- get the total number of floors for the building: `num_floors = get_number_of_floors(B-RMR)`
- first get the expected system type for the predominant building area type.  To do this, we need the total area of the predominant building area type, which includes all BAT's less than 20000 ft2
- set area equal to the area of the predominant building area type: `area = list_building_area_types_and_zones[predominant_building_area_type]["AREA"]`
- loop through the building area types: `for bat in list_building_area_types_and_zones:`
	- if the bat is not equal to the predominant building area type: `if bat != predominant_building_area_type:`
		- and if the area of this bat <= 20,000 ft2: `if list_building_area_types_and_zones[bat]["AREA"] <= 20000:`
			- add this area to the area value for determining predominant HVAC system type: `area = area + list_building_area_types_and_zones[bat]["AREA"]`
- expected_system_type_list = expected_system_type_from_Table_G3_1_1(predominant_building_area_type,num_floors,area)
- fill the zones_and_systems list with the expected system and description string for all zones (we'll overwrite the other zones in the next step): `for zone in zones_and_systems:`
	- set the value to expected_system_type_list: `zones_and_systems[zone] = expected_system_type_list`
	
- now we need to go through each 'exception' to Table_G3_1_1 in order.

- G3.1.1b "Use additional system types for nonpredominant conditions (i.e., residential/nonresidential) if those conditions apply to more than 20,000 ft2 of conditioned floor area." uses the same logic that we just used for the expected_system_type_list, except that we select systems based on non-predominant building area types and the area of these non-predominant conditions
- first check that the building is greater than or equal to 40,000 ft2, otherwise it's impossible to have non-predominant space types.  Create variable total_area: `total_area = 0`
- add the area of all space types: `for bat in list_building_area_types_and_zones:`
	- `total_area += list_building_area_types_and_zones[bat]["AREA"]`
- now check whether the total building area is greater than or equal to 40,000 ft2: `if total_area >= 40000:`
	- check if it is the predominant bat (we have already done this case): `if bat == predominant_building_area_type:`
		- skip this loop using continue: `continue`
	- loop throught the building area types: `for bat in list_building_area_types_and_zones:`
		- look for any bat's that have more than 20000 ft2 area: `if list_building_area_types_and_zones[bat]["AREA"] >=20000:`
			- we select a secondary system type for this bat: `secondary_system_type = expected_system_type_from_Table_G3_1_1(bat,num_floors,list_building_area_types_and_zones[bat]["AREA"])`
			- change the system type for any zone in this bat: `for zone in zones_and_systems:`
				- check if this zone is in the list of zone_ids associated with this bat: `if zone.id in list_building_area_types_and_zones[bat]["ZONE_IDS"]:`
					- change the system type to: [secondary_system_type[0], "G3_1_1b"] - remember that expected_system_type_from_Table_G3_1_1 gives both the expected system type and a string explaining how that system type was chosen.  For the rule testing G3_1_1b, it is only asking whether the system was chosen from Table G3.1.1, not exactly how it got there: `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = secondary_system_type[0]`
					- change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1b"`

- G3.1.1c "If the baseline HVAC system type is 5, 6, 7, 8, 9, 10, 11, 12, or 13 use separate single-zone systems conforming with the requirements of system 3 or system 4 for any HVAC zones that have occupancy, internal gains, or schedules that differ significantly from the rest of the HVAC zones served by the system. The total peak internal gains that differ by 10 Btu/h·ft2 or more from the average of other HVAC zones served by the system, or schedules that differ by more than 40 equivalent full-load hours per week from other spaces served by the system, are considered to differ significantly. Examples where this exception may be applicable include but are not limited to natatoriums and continually occupied security areas. This exception does not apply to computer rooms."
- loop through the zones_and_systems to see if any of the zones meets Ge.1.1.c: `for zone in zones_and_systems:`
	- use the function does_zone_meet_G3_1_1c to determine if this zone meets this requirement: `if does_zone_meet_G3_1_1c(B_RMI,zone,zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] == YES):`
		- change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] + " G3_1_1c"` 
		- the zone meets the G3_1_1c requirements, choose system 3 or 4 based on climate zone: `if is_CZ_0_to_3a():`
			- set the system to "SYS-4": `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = "SYS-4"`
		- else (the climate zone is_CZ_3b_3c_and_4_to_8): `else:`
			- set the system to "SYS-3": `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = "SYS-3"`
				
- G3.1.1d "For laboratory spaces in a building having a total laboratory exhaust rate greater than 15,000 cfm, use a single system of type 5 or 7 serving only those spaces.  The lab exhaust fan shall be modeled as constant horsepower reflecting constantvolume stack discharge with outdoor air bypass."
	- not sure how to apply this one


- G3.1.1e "Thermal zones designed with heating-only systems in the proposed design serving storage rooms, stairwells, vestibules, electrical/mechanical rooms, and restrooms not exhausting or transferring air from mechanically cooled thermal zones in the proposed design shall use system type 9 or 10 in the baseline building design."
- loop through the zones_and_systems to see if any of the zones meets this requirement: `for zone in zones_and_systems:`
	- use the function does_zone_meet_G3_1_1e to determine whether to change the system type (we are using != NO instead of YES, because the function can return MAYBE_VESTIBULE or LIKELY_VESTIBULE.  Here we will assign any "maybe's or "likelies" to the new system type.  The rule itself will deal with the uncertainty of vestibules using the function is_zone_a_vestibule): `if does_zone_meet_G3_1_1e(P-RMR,B-RMR,zone) != NO:`
		- - change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1e"`
		- choose system 9 or 10 based on climate zone: `if is_CZ_0_to_3a():`
			- set the system to "SYS-10"": `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = "SYS-10"`
		- else (the climate zone is_CZ_3b_3c_and_4_to_8): `else:`
			- set the system to "SYS-9": `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = "SYS-9"`


- G3.1.1f "If the baseline HVAC system type is 9 or 10, use additional system types for all HVAC zones that are mechanically cooled in the proposed design."
- loop through the zones and systems, check only the zones that are SYS-9 or 10: `for zone in zones_and_systems:`
	- check if it is SYS-9 or SYS-10: `if zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] in ["SYS-9", "SYS-10"]:`
		- use the function does_zone_meet_G3_1_1f to see if the zone meets the requirements of G3_1_1f: `if does_zone_meet_G3_1_1f(P-RMR,B-RMR,zone.id) == "F":`
			- change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1f"`
			- the zone meets the G3_1_1f requirements, choose system 3 or 4 based on climate zone: `if is_CZ_0_to_3a():`
				- set the system to "SYS-4": `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = "SYS-4"
			- else (the climate zone is_CZ_3b_3c_and_4_to_8): `else:`
				- set the system to "SYS-3": `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = "SYS-3"

- G3.1.1g is broken down into three parts:
	- part 1: "If the baseline HVAC system serves HVAC zones that includes computer rooms,  baseline system 11 shall be used where the baseline HVAC system type is 7 or 8 and the total computer room peak cooling load is greater than 600,000 BTU/h (175 kW)."
	- part 2: "If the baseline HVAC system serves HVAC zones that includes computer rooms,  Baseline System 11 shall be used for such HVAC zones in buildings with a total computer room peak cooling load >greater than 3,000,000 Btu/h."
	- part 3: "If the baseline HVAC system serves HVAC zones that includes computer rooms,  baseline system 3 or 4 shall be used for all HVAC zones where the computer room peak cooling load is= <600,000 Btu/h"
	- the function `does_zone_meet_G3_1_1g` will return enum G1, G2, G3, or FALSE
- loop through the zones and systems: `for zone in zones_and_systems:`
	- use the function does_zone_meet_G3_1_1g to determine which (if any) of the requirements the zone meets: `does_zone_meet_G =  does_zone_meet_G3_1_1g(B-RMI,zone.id,zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"])`
		- if the zone meets G1: `if does_zone_meet_G == G1:`
			- set the system to "SYS-11" and source to "G3_1_1g_part1": `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = "SYS-11"
			- change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1g_part1"`
		- else if the zone meets G2: `elsif does_zone_meet_G == G2:
			- set the system to "SYS-11" and source to "G3_1_1g_part2": `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = "SYS-11"
			- change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1g_part2"`
		- else if the zone meets G3: `elsif does_zone_meet_G == G3:`
			- - change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1g_part3"`
			- the zone meets the G3_1_1g_part3 requirements, choose system 3 or 4 based on climate zone: `if is_CZ_0_to_3a():`
				- set the system to "SYS-4": `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = "SYS-4"
			- else (the climate zone is_CZ_3b_3c_and_4_to_8): `else:`
				- set the system to "SYS-3": `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = "SYS-3"



**Returns** `zones_and_systems`


**Notes/Questions:**  
1.  Unresolved how to handle G3.1.1d
2.  For G3.1.1f - which system type should be assigned when the zone meets the requirements?
3.  What to do with G3.1.1g???

**[Back](../_toc.md)**
