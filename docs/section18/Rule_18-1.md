# HVAC_SystemZoneAssignment - Rule 18-1  
**Schema Version:** 0.0.22  

**Rule ID:** 18-1  
**Rule Description:** Buildings in CZ 0-3A with predominant HVAC BAT = public assembly, <120,000 ft2 have baseline HVAC system type 4 (PSZ HP)
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 18 HVAC_SystemZoneAssignment  
**Appendix G Section Reference:** Table G3.1.1.3

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. Buildings in CZ 0-3A
2. predominant HVAC BAT = public assembly
3. building area < 120,0000 ft2
4. the zone does not meet one if the G3.1.1.1 exceptions

**Manual Check:** Yes  
**Evaluation Context:** Evaluate whether each Zone is served by the correct HVAC system type  
**Data Lookup:**   
**Function Call:** 

1. get_zone_target_baseline_system()
2. is_hvac_system_of_type()
3. get_list_hvac_systems_associated_with_zone()


**Applicability Checks:**

## Rule Logic:  
- This function uses get_zone_target_baseline_system and looks through the list to find any zones that match the target string for this system.
- The target string is: `target_string = "PUBLIC_ASSEMBLY CZ_0_to_3a < 120,000 ft2"
- get the list of zones, their expected systems and the source string: `zones_expected_system_types = get_zone_target_baseline_system(P-RMD,B-RMD)`

- loop through building segments: `for segment in RMR.building_segments:`
	- loop through zones in the segments: `for zone in segment.zones:`
		- check whether the description string in zones_expected_system_types matches the target_string: `if zones_expected_system_types[zone]["SYSTEM_ORIGIN"] == target_string:`
			- now check whether the system(s) serving this zone match the expected system.  Start by getting the list of HVAC systems that serve the zone: `hvac_systems_serving_zone = get_list_hvac_systems_associated_with_zone(B-RMD)`
			- loop through these systems: `for system in hvac_systems_serving_zone:`
				- create a boolean that indicates whether all systems pass: `all_systems_in_zone_pass = TRUE`
				- now check that system_b is "SYS-4" by using the is_hvac_system_of_type() function: `if is_hvac_system_of_type(B-RMI,system.id,"SYS-4"):`
					- this system passes, no need to do anything (in the python code, the check above can be `not in` instead of `in`)
				- otherwise, this system is not compliant: `else:`
					- set the boolean to false, this zone will fail: `all_systems_in_zone_pass = FALSE`

  **Rule Assertion - Zone:**

  - Case 1: All terminals in the zone are System-4 (there should only be one terminal in the zone, but this rule doesn't check number of terminals):`if all_systems_in_zone_pass == TRUE: PASS`

  - Case 2: Else: `else: FAIL`

**Notes:**

**[Back](../_toc.md)**
