# get_zone_target_baseline_system
**Schema Version:** 0.0.22  

**Description:** Following G3.1.1, determines the baseline system type for each zone in a building

**Inputs:**
- **P-RMD**
- **B-RMD**
- **B-CLIMATEZONE** 

**Returns:**  
- **zones_and_systems**: a dictionary with zone / list pairs where the first value in the list is the expected system type (ex SYS_3) and the second value is the rule used to choose the system, (eg "G3_1_1e"): zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = SYS_3; zones_and_systems[zone]["SYSTEM_ORIGIN"] =  "G3_1_1e"
 
**Function Call:**
- **get_HVAC_building_area_types_and_zones**
- **does_zone_meet_G3_1_1c**
- **does_zone_meet_G3_1_1d**
- **does_zone_meet_G3_1_1e**
- **does_zone_meet_G3_1_1f**
- **does_zone_meet_G3_1_1g**
- **get_predominant_HVAC_building_area_type**
- **get_number_of_floors**
- **expected_system_type_from_Table_G3_1_1**
- **get_zone_conditioning_category**
- **get_zone_HVAC_BAT**

**Data Lookup**
- **Table G3.1.1**

## Logic:
- use the function get_zone_conditioning_category to get a dictionary of zone id's and their conditioning category - we will only include conditioned zones in the building_area_types_with_total_area_and_zones_dict: `zone_conditioning_category_dict = get_zone_conditioning_category(RMD)`
- create zones_and_systems list: `zones_and_systems = {}`
- pre-fill the list with an empty string:
	- `for building_segment in RMR.building.building_segments:`
		- `for zone in building_segment.zones:`
			- using zone_conditioning_category_dict, check if the zone is conditioned. `if zone_conditioning_category_dict[zone.id] == "CONDITIONED RESIDENTIAL" || zone_conditioning_category_dict[zone.id] == "CONDITIONED NON-RESIDENTIAL" || zone_conditioning_category_dict[zone.id] == "CONDITIONED MIXED"`:
				- add all zones that are conditioned: `zones_and_systems[zone] = {}`
- get the list of HVAC building area types and zones: `list_building_area_types_and_zones = get_HVAC_building_area_types_and_zones(B-CLIMATEZONE, B-RMD)`
- get the predominant building area type: `predominant_building_area_type = get_predominant_HVAC_building_area_type(B-CLIMATEZONE, B-RMD)`
- get the total number of floors for the building: `num_floors = get_number_of_floors(B-CLIMATEZONE, B-RMD)`
- first get the expected system type for the predominant building area type.
- loop through the building area types: `for bat in list_building_area_types_and_zones:`
	- add this area to the area value for determining predominant HVAC system type: `area += list_building_area_types_and_zones[bat]["AREA"]`
- create variable expected_system_type_dict, which is the dictionary returned by expected_system_type_from_Table_G3_1_1: `expected_system_type_dict = expected_system_type_from_Table_G3_1_1(predominant_building_area_type,B_CLIMATEZONE,num_floors,area)`
- fill the zones_and_systems list with the expected system and description string for all zones (we'll overwrite the other zones in the next step): `for zone in zones_and_systems:`
	- set the value to expected_system_type_dict: `zones_and_systems[zone] = expected_system_type_dict`
	
- now we need to go through each 'exception' to Table_G3_1_1 in order.

- G3.1.1b "Use additional system types for nonpredominant conditions (i.e., residential/nonresidential) if those conditions apply to more than 20,000 ft2 of conditioned floor area." uses the same logic that we just used for the expected_system_type_dict, except that we select systems based on non-predominant building area types and the area of the entire building
- first check that the building is greater than or equal to 40,000 ft2, otherwise it's impossible to have non-predominant space types: `if area >= 40000:`
	- check if it is the predominant bat (we have already done this case): `if bat == predominant_building_area_type:`
		- skip this loop using continue: `continue`
	- loop throught the building area types: `for bat in list_building_area_types_and_zones:`
		- look for any bat's that have more than 20000 ft2 area: `if list_building_area_types_and_zones[bat]["AREA"] >=20000:`
			- we select a secondary system type for this bat: `secondary_system_type = expected_system_type_from_Table_G3_1_1(bat,B-CLIMATEZONE,num_floors,area)`
			- change the system type for any zone in this bat: `for zone in zones_and_systems:`
				- check if this zone is in the list of zone_ids associated with this bat: `if zone.id in list_building_area_types_and_zones[bat]["ZONE_IDS"]:`
					- change the system type to: [secondary_system_type[0], "G3_1_1b"] - remember that expected_system_type_from_Table_G3_1_1 gives both the expected system type and a string explaining how that system type was chosen.  For the rule testing G3_1_1b, it is only asking whether the system was chosen from Table G3.1.1, not exactly how it got there: `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = secondary_system_type["expected_system_type"]`
					- change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1b"`

- G3.1.1c "If the baseline HVAC system type is 5, 6, 7 or 8 use separate single-zone systems conforming with the requirements of system 3 or system 4 for any HVAC zones that have occupancy, internal gains, or schedules that differ significantly from the rest of the HVAC zones served by the system. The total peak internal gains that differ by 10 Btu/h·ft2 or more from the average of other HVAC zones served by the system, or schedules that differ by more than 40 equivalent full-load hours per week from other spaces served by the system, are considered to differ significantly. Examples where this exception may be applicable include but are not limited to natatoriums and continually occupied security areas. This exception does not apply to computer rooms."
- create a list of zones that meet G3.1.1c - we can't change the system type assignment as we go, otherwise we'll be calculating the peak load average with a diminishing list of zones: `zones_that_meetG3_1_1c_list = []`
- loop through the zones_and_systems to see if any of the zones meets G3.1.1.c: `for zone in zones_and_systems:`
	- use the function does_zone_meet_G3_1_1c to determine if this zone meets this requirement: `if does_zone_meet_G3_1_1c(B_RMD,zone.id,leap_year, zones_and_systems):`
		- append the zone_id to the zones_that_meetG3_1_1c_list: `zones_that_meetG3_1_1c_list.append(zone)`
- loop through zones_that_meetG3_1_1c_list and change the expected system type and origin for the zones that meet G3.1.1c: `for zone in zones_that_meetG3_1_1c_list:`
	- change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1c"` 
	- the zone meets the G3_1_1c requirements, choose system 3 or 4 based on climate zone: `if is_CZ_0_to_3a(B-CLIMATEZONE):`
		- set the system to SYS_4: `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = SYS_4`
	- else (the climate zone is_CZ_3b_3c_and_4_to_8): `else:`
		- set the system to SYS_3: `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = SYS_3`
				
- G3.1.1d "For laboratory spaces in a building having a total laboratory exhaust rate greater than 15,000 cfm, use a single system of type 5 or 7 serving only those spaces.  The lab exhaust fan shall be modeled as constant horsepower reflecting constant volume stack discharge with outdoor air bypass."
- select assigned system type based on total building area and number of floors - for less than 5 floors and less than 150,000 sf we use system 5, anything else is system 7.
- if the building is less than 6 floors, and < 150,000 sf: `if( num_floors < 6 && area < 150000 ):`
	- then the system type is SYS-5: `G3_1_1d_expected_system_type = SYS_5`
- all other cases: `else:`
	- the system type is SYS-7: `G3_1_1d_expected_system_type = SYS_7`
- loop through the zones_and_systems to see if any of the zones meets G3.1.1.d: `for zone in zones_and_systems:`
	- use the function does_zone_meet_G3_1_1d to determine if this zone meets this requirement: `if does_zone_meet_G3_1_1d(B_RMD,zone.id):`
		- change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1d"` 
		- set the system to SYS_5 or SYS_7: `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = G3_1_1d_expected_system_type`

- G3.1.1e "Thermal zones designed with heating-only systems in the proposed design serving storage rooms, stairwells, vestibules, electrical/mechanical rooms, and restrooms not exhausting or transferring air from mechanically cooled thermal zones in the proposed design shall use system type 9 or 10 in the baseline building design."
- loop through the zones_and_systems to see if any of the zones meets this requirement: `for zone in zones_and_systems:`
	- use the function does_zone_meet_G3_1_1e to determine whether to change the system type: `if does_zone_meet_G3_1_1e(P-RMD,B-RMD,zone.id):`
        - change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1e"`
        - choose system 9 or 10 based on climate zone: `if is_CZ_0_to_3a(B-CLIMATEZONE):`
            - set the system to SYS_10: `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = SYS_10`
        - else (the climate zone is_CZ_3b_3c_and_4_to_8): `else:`
            - set the system to SYS_9: `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = SYS_9`


- G3.1.1f "If the baseline HVAC system type is 9 or 10, use additional system types for all HVAC zones that are mechanically cooled in the proposed design."
- loop through the zones and systems, check only the zones that are SYS-9 or 10: `for zone in zones_and_systems:`
	- check if it is SYS-9 or SYS-10: `if zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] in [SYS_9, SYS_10]:`
		- use the function does_zone_meet_G3_1_1f to see if the zone meets the requirements of G3_1_1f: `if does_zone_meet_G3_1_1f(B-RMD,zone.id):`
			- change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1f"`
			- now determine the baseline system type using the zone HVAC building area type, the total building area and the total building number of floors.  First by get the bat by using the function get_zone_HVAC_BAT: `bat = get_zone_HVAC_BAT(B_RMD, zone.id)` 			
            - set the system to the system type selected by the function expected_system_type_from_Table_G3_1_1: `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = expected_system_type_from_Table_G3_1_1(bat,num_floors,area)`

- G3.1.1g is broken down into three parts:
	- part 1: "If the baseline HVAC system serves HVAC zones that includes computer rooms,  baseline system 11 shall be used where the baseline HVAC system type is 7 or 8 and the total computer room peak cooling load is greater than 600,000 BTU/h (175 kW)."
	- part 2: "If the baseline HVAC system serves HVAC zones that includes computer rooms,  Baseline System 11 shall be used for such HVAC zones in buildings with a total computer room peak cooling load >greater than 3,000,000 Btu/h."
	- part 3: "If the baseline HVAC system serves HVAC zones that includes computer rooms,  baseline system 3 or 4 shall be used for all other conditions where the HVAC system serves computer room zones"
	- the function `does_zone_meet_G3_1_1g` will return true or false.
- loop through the zones and systems: `for zone in zones_and_systems:`
	- use the function does_zone_meet_G3_1_1g to determine which (if any) of the requirements the zone meets: `does_zone_meet_G =  does_zone_meet_G3_1_1g(B-RMD,zone.id)`
        - if the zone meets g3_1_1g: `if does_zone_meet_G:`
        - calculate the total_computer_zones_peak_cooling_load: `total_computer_zones_peak_cooling_load = get_computer_zones_peak_cooling_load(B-RMD)`
        - if total_computer_zones_peak_cooling_load is greater than 3,000,000 btu/hr: `if total_computer_zones_peak_cooling_load > 3000000`
            - set the system to SYS_11 and source to "G3_1_1g_part2": `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = SYS_11`
            - change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1g_part2"`
        - else if zone's original expected system type is SYS-7 or SYS-8: `elsif zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] in [HVAC.SYS_7, HVAC.SYS_8]:`
            - if total_computer_zones_peak_cooling_load is greater than 600,000 but/hr: `if total_computer_zones_peak_cooling_load > 600000`
              - set the system to SYS_11 and source to "G3_1_1g_part1": `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = SYS_11`
              - change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1g_part1"`
            - else: `else:`
              - change the system origin string: `zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1g_part3"`
                - the zone meets the G3_1_1g_part3 requirements, choose system 3 or 4 based on climate zone: `if is_CZ_0_to_3a(B-CLIMATEZONE):`
                    - set the system to SYS_4: `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = SYS_4`
                - else (the climate zone is_CZ_3b_3c_and_4_to_8): `else:`
                    - set the system to SYS_3: `zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = SYS_3`



**Returns** `zones_and_systems`


**Notes/Questions:**  

**[Back](../_toc.md)**
