# HVAC_SystemZoneAssignment - Rule 18-5
**Schema Version:** 0.0.22  

**Rule ID:** 18-5 
**Rule Description:** Buildings in any CZ with predominant HVAC BAT = Hospital, <=150,000 ft2 or <=5 floors have baseline HVAC system type 5(P-VAV with HW Reheat)
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 18 HVAC_SystemZoneAssignment  
**Appendix G Section Reference:** Table G3.1.1.3

**Applicability:** All required data elements exist for B_RMR  

**Manual Check:** Yes  
**Evaluation Context:** Evaluate whether each Zone is served by the correct HVAC system type  
**Data Lookup:**   
**Function Call:** 

1. section_18_rule_test()


**Applicability Checks:**
1. the target string matches, which indicates:
	a. predominant HVAC BAT = HOSPITAL
	b. building area <= 150,0000 ft2 AND building has fewer than 5 floors
	c. none of the G3.1.1 exceptions apply

## Rule Logic:  
- This function uses get_zone_target_baseline_system and looks through the list to find any zones that match the target string for this system.
- The target string is: `target_string = "HOSPITAL All Other"`
- the expected system type is "SYS-5": `expected_system_type = "SYS-5"`

- loop through building segments: `for segment in RMR.building_segments:`
	- loop through zones in the segments: `for zone in segment.zones:`
		- use the section_18_rule_test function to determine whether the zone meets the requirements: `zone_result = section_18_rule_test(P-RMD,B-RMD,zone.id,target_string,expected_system_type)`

  **Rule Assertion - Zone:**

  - Case 1: the target strings don't match, so it is not applicable to this zone: `if zone_result == NOT_APPLICABLE: NOT_APPLICABLE`
  - Case 2: All terminals in the zone are System-4 (there should only be one terminal in the zone, but this rule doesn't check number of terminals):`if zone_result == PASS: PASS`

  - Case 3: Else: `else: FAIL`

**Notes:**

**[Back](../_toc.md)**
