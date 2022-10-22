# get_zone_target_baseline_system
**Schema Version:** 0.0.22  

**Description:** Following G3.1.1, determines the baseline system type for each zone in a building

**Inputs:**
- **P-RMD**
- **B-RMD**

**Returns:**  
- **zones_and_systems**: a dictionary with zone / list pairs where the first value in the list is the expected system type (ex "SYS-3") and the second value is the rule used to choose the system, (eg "G3_1_1e"): zones_and_systems[zone] = ["SYS-3", "G3_1_1e"]
 
**Function Call:**
- **get_HVAC_building_area_types_and_zones**
- **zone_meets_G3_1_1b**
- **zone_meets_G3_1_1c**
- **zone_meets_G3_1_1e**
- **zone_meets_G3_1_1f**
- **zone_meets_G3_1_1g**
- **get_predominant_HVAC_building_area_type**
- **get_number_of_floors**
- **expected_system_type_from_Table_G3_1_1**

**Data Lookup**
- **Table G3.1.1**

## Logic:
- get climate zone (not sure this is the correct path): `climate_zone = ASHRAE229.weather.climate_zone`
- create zones_and_systems list: `zones_and_systems = {}`
- pre-fill the list with an empty string:
	- `for building_segment in RMR.building.building_segments:`
		- `for zone in building_segment.zones:`
			- `zones_and_systems[zone] = []`
- get the list of HVAC building area types and zones: `list_building_area_types_and_zones = get_HVAC_building_area_types_and_zones(B-RMR)`
- get the predominant building area type: `predominant_building_area_type = get_predominant_HVAC_building_area_type(list_building_area_types_and_zones)`
- get the total number of floors for the building: `num_floors = get_number_of_floors(B-RMR)`
- first get the expected system type for the predominant building area type.  To do this, we need the total area of the predominant building area type, which includes all BAT's less than 20000 ft2
- set area equal to the area of the predominant building area type: `area = list_building_area_types_and_zones[predominant_building_area_type]["AREA"]`
- loop through the building area types: `for bat in list_building_area_types_and_zones:`
	- if the bat is not equal to the predominant building area type: `if bat != predominant_building_area_type:`
		- and if the area of this bat < 20,000 ft2: `if list_building_area_types_and_zones[bat]["AREA"] <= 20000:`
			- add this area to the area value for determining predominant HVAC system type: `area = area + list_building_area_types_and_zones[bat]["AREA"]`
- expected_system_type_list = expected_system_type_from_Table_G3_1_1(predominant_building_area_type,num_floors,area,climate_zone)
- fill the zones_and_systems list with the expected system and description string for all zones (we'll overwrite the other zones in the next step): `for zone in zones_and_systems:`
	- set the value to expected_system_type_list: `zones_and_systems[zone] = expected_system_type_list`
	
- now we need to go through each 'exception' to Table_G3_1_1 in order.

- G3.1.1b "Use additional system types for nonpredominant conditions (i.e., residential/nonresidential) if those conditions apply to more than 20,000 ft2 of conditioned floor area." uses the same logic that we just used for the expected_system_type_list, except that we select systems based on non-predominant building area types and the area of these non-predominant conditions
- loop throught the building area types: `for bat in list_building_area_types_and_zones:`
	- look for any bat's that have more than 20000 ft2 area: `if list_building_area_types_and_zones[bat]["AREA"] >=20000:`
		- we select a secondary system type for this bat: `secondary_system_type = expected_system_type_from_Table_G3_1_1(bat,num_floors,list_building_area_types_and_zones[bat]["AREA"],climate_zone)`
		- change the system type for any zone in this bat: `for zone in zones_and_systems:`
			- check if this zone is in the list of zone_ids associated with this bat: `if zone.id in list_building_area_types_and_zones[bat]["ZONE_IDS"]:`
				- change the system type to: [secondary_system_type[0], "G3_1_1b"] - remember that expected_system_type_from_Table_G3_1_1 gives both the expected system type and a string explaining how that system type was chosen.  For the rule testing G3_1_1b, it is only asking whether the system was chosen from Table G3.1.1, not exactly how it got there: `zones_and_systems[zone] = [secondary_system_type[0], "G3_1_1b"]`

- G3.1.1c "If the baseline HVAC system type is 5, 6, 7, 8, 9, 10, 11, 12, or 13 use separate single-zone systems conforming with the requirements of system 3 or system 4 for any HVAC zones that have occupancy, internal gains, or schedules that differ significantly from the rest of the HVAC zones served by the system. The total peak internal gains that differ by 10 Btu/h·ft2 or more from the average of other HVAC zones served by the system, or schedules that differ by more than 40 equivalent full-load hours per week from other spaces served by the system, are considered to differ significantly. Examples where this exception may be applicable include but are not limited to natatoriums and continually occupied security areas. This exception does not apply to computer rooms."
- create a list of the baseline system types specified in G3.1.1c: `c_system_types = ["SYS-5","SYS-6","SYS-7","SYS-8","SYS-9","SYS-10","SYS-11","SYS-12","SYS-13"]
- loop through the zones_and_systems to see if any of the zones have one of the above systems: `for zone in zones_and_systems:`
	- check to see if the expected system type is one of the above: `if zones_and_systems[zone][0] in c_system_types:`
		- use the function zone_meets_G3_1_1c to see if the zone meets the requirements: `if zone_meets_G3_1_1c(B-RMR,zone) == "C":`
			- the zone meets the G3_1_1c requirements, choose system 3 or 4 based on climate zone: `if is_CZ_0_to_3a(climate_zone):`
				- set the system to "SYS-3" and source to "G3_1_1c": `zones_and_systems[zone] = ["SYS-3","G3_1_1c"]`
			- else if the climate zone is_CZ_3b_3c_and_4_to_8: `elsif is_CZ_3b_3c_and_4_to_8(climate_zone):`
				- set the system to "SYS-4" and source to "G3_1_1c": `zones_and_systems[zone] = ["SYS-4","G3_1_1c"]`
				
- G3.1.1d "For laboratory spaces in a building having a total laboratory exhaust rate greater than 15,000 cfm, use a single system of type 5 or 7 serving only those spaces.  The lab exhaust fan shall be modeled as constant horsepower reflecting constantvolume stack discharge with outdoor air bypass."
- not sure how to apply this one


- G3.1.1e "Thermal zones designed with heating-only systems in the proposed design serving storage rooms, stairwells, vestibules, electrical/mechanical rooms, and restrooms not exhausting or transferring air from mechanically cooled thermal zones in the proposed design shall use system type 9 or 10 in the baseline building design."
	- loop through the zones_and_systems to see if any of the zones meets this requirement: `for zone in zones_and_systems:`
		- use the function zone_meets_G3_1_1e to determine whether to change the system type.  Note that this function can return "E" - meaning it mees the requirements of G3.1.1e, or "UNDEFINED" or "E_T" - which indicates that there is transfer air in the zone.  For assigning expected systems, only "E" will be used.  The other cases will be picked up in the rules related to G3.1.1e: `if zone_meets_G3_1_1e(P-RMR,B-RMR,zone) == "E":`
			- choose system 9 or 10 based on climate zone: `if is_CZ_0_to_3a(climate_zone):`
				- set the system to "SYS-9" and source to "G3_1_1e": `zones_and_systems[zone] = ["SYS-9","G3_1_1e"]`
			- else if the climate zone is_CZ_3b_3c_and_4_to_8: `elsif is_CZ_3b_3c_and_4_to_8(climate_zone):`
				- set the system to "SYS-10" and source to "G3_1_1e": `zones_and_systems[zone] = ["SYS-10","G3_1_1e"]`



- G3.1.1f "If the baseline HVAC system type is 9 or 10, use additional system types for all HVAC zones that are mechanically cooled in the proposed design."
	- loop through the zones and systems, check only the zones that are SYS-9 or 10: `for zone in zones_and_systems:`
		- check if it is SYS-9 or SYS-10: `if zones_and_systems[zone][0] in ["SYS-9", "SYS-10"]:`
			- use the function zone_meets_G3_1_1f to see if the zone meets the requirements of G3_1_1f: `if zone_meets_G3_1_1f(P-RMR,B-RMR,zone.id) == "F":`
				- the zone meets the G3_1_1f requirements, choose system 3 or 4 based on climate zone: `if is_CZ_0_to_3a(climate_zone):`
					- set the system to "SYS-3" and source to "G3_1_1f": `zones_and_systems[zone] = ["SYS-3","G3_1_1f"]`
				- else if the climate zone is_CZ_3b_3c_and_4_to_8: `elsif is_CZ_3b_3c_and_4_to_8(climate_zone):`
					- set the system to "SYS-4" and source to "G3_1_1f": `zones_and_systems[zone] = ["SYS-4","G3_1_1f"]`


**Returns** `zones_and_systems`


**Notes/Questions:**  
1.  Unresolved how to handle G3.1.1d
2.  For G3.1.1f - which system type should be assigned when the zone meets the requirements?
3.  What to do with G3.1.1g???

**[Back](../_toc.md)**