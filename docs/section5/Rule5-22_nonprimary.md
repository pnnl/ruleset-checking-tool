# Envelope - Rule 5-22
**Schema Version** 0.0.23  
**Primary Rule:** False
**Rule ID:** 5-22  
**Rule Description:** The baseline fenestration area for an existing building shall equal the existing fenestration area prior to the proposed work.   
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building  

**Applicability Checks:**
  1. The baseline building has existing or altered spaces

**Evaluation Context:**  Each Data Element  
**Data Lookup:** None
**Function Call:**  None  

## Rule Logic:
- create undetermined_zone_list: `undetermined_zone_list = []`

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```

  - For each zone in building segment: ```for zone_b in building_segment_b.zones:``` 

    - For each space in zone: ```for space_b in zone_b.spaces:```

      - Check if space is existing or altered, set rule applicability check to True: ```if ( space_b.status_type == EXISTING ) OR ( space_b.status_type == ALTERED ): rule_applicability_check = TRUE```

        - Add to total number of existing or altered spaces in zone: ```num_space_existing_altered += 1```

        - Add to array of zones with existing or altered spaces if not already saved: ```if NOT zone_b in undetermined_zone_list: undetermined_zone_list.append(zone_b)```

**Rule Assertion - Component:**  

- For each zone, if any space in zone is existing or altered: ```if num_space_existing_altered > 0: outcome = UNDETERMINED"``` 

**Rule Assertion - RMR:**

- Case 1: If any zone in B-RMR is existing or altered, outcome is UNDETERMINED: ```if rule_applicability_check: outcome = UNDETERMINED and raise_message "PART OR ALL OF ZONES LISTED BELOW IS EXISTING OR ALTERED. THE BASELINE VERTICAL FENESTRATION AREA FOR EXISTING ZONES MUST EQUAL TO THE FENESTRATION AREA PRIOR TO THE PROPOSED SCOPE OF WORK. THE BASELINE FENESTRATION AREA IN ZONE MUST BE CHECKED MANUALLY. ${undetermined_zone_list}"```

- Case 2: If no zone in B-RMR is existing or altered, outcome is NOT_APPLICABLE: ```if NOT rule_applicability_check: outcome = NOT_APPLICABLE```

**[Back](../_toc.md)**
