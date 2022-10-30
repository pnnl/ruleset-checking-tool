# HVAC_SystemZoneAssignment - Rule 18-2 
**Schema Version:** 0.0.22  

**Rule ID:** 18-2
**Rule Description:** Buildings in CZ 0-3A with  predominant HVAC BAT = public assembly, >=120,000 ft2 have baseline HVAC system type 13 (SZ-CV-ER)
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 18 HVAC_SystemZoneAssignment  
**Appendix G Section Reference:** Table G3.1.1.3

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. the target string matches, which indicates:
	a. the space type is PUBLIC_ASSEMBLY
	b. climate zone CZ_0_to_3a
	c. area >= 120,000 ft2
	d. none of the G3.1.1 exceptions apply

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
- The target string is: `target_string = "PUBLIC_ASSEMBLY CZ_0_to_3a >= 120,000 ft2"`
- the expected system type is "SYS-13": `expected_system_type = "SYS-13"`

- loop through building segments: `for segment in RMR.building_segments:`
	- loop through zones in the segments: `for zone in segment.zones:`
		- use the section_18_rule_test function to determine whether the zone meets the requirements: `zone_result = section_18_rule_test(P-RMD,B-RMD,zone.id,target_string,expected_system_type)`

  **Rule Assertion - Zone:**

  - Case 1: the target strings don't match, so it is not applicable to this zone: `if zone_result == NOT_APPLICABLE: NOT_APPLICABLE`
  - Case 2: All terminals in the zone are System-4 (there should only be one terminal in the zone, but this rule doesn't check number of terminals):`if zone_result == PASS: PASS`

  - Case 3: Else: `else: FAIL`
**Notes:**

**[Back](../_toc.md)**
