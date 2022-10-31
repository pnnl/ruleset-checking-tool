# HVAC_SystemZoneAssignment - Rule 18-6  
**Schema Version:** 0.0.22  
**Mandatory Rule:** True
**Rule ID:** 18-6
**Rule Description:** Buildings in any CZ with predominant HVAC BAT = Hospital, >150,000 ft2 or >5 floors have baseline HVAC system type 7 (VAV with HW Reheat)
**Rule Assertion:** Options are PASS/FAIL/NOT_APPLICABLE
**Appendix G Section Reference:** Table G3.1.1.3

**Evaluation Context:** Each Zone Data Group
**Data Lookup:**   
**Function Call:** 

1. section_18_rule_test()


**Applicability Checks:**
1. the target string matches, which indicates:
	a. the space type is HOSPITAL
	b. area > 120,000 ft2 OR there are more than 5 floors
	c. none of the G3.1.1 exceptions apply

## Rule Logic:  
- This function uses get_zone_target_baseline_system and looks through the list to find any zones that match the target string for this system.
- The target string is: `target_string = "HOSPITAL > 150,000 ft2 or > 5 floors"`
- the expected system type is "SYS-7": `expected_system_type = "SYS-7"`

- loop through building segments: `for segment in RMR.building_segments:`
	- loop through zones in the segments: `for zone in segment.zones:`
		- use the section_18_rule_test function to determine whether the zone meets the requirements: `zone_result = section_18_rule_test(P-RMD,B-RMD,zone.id,target_string,expected_system_type)`

  **Rule Assertion - Zone:**

  - Case 1: the target strings don't match, so it is not applicable to this zone: `if zone_result == NOT_APPLICABLE: NOT_APPLICABLE`
  - Case 2: All terminals in the zone are System-4 (there should only be one terminal in the zone, but this rule doesn't check number of terminals):`if zone_result == PASS: PASS`

  - Case 3: Else: `else: FAIL`

**Notes:**

**[Back](../_toc.md)**
