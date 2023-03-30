# Envelope - Rule 5-22
**Schema Version** 0.0.23  
**Primary Rule:** False
**Rule ID:** 5-22  
**Rule Description:** The baseline fenestration area for an existing building shall equal the existing fenestration area prior to the proposed work.   
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building  

**Applicability Checks:**
  1. The baseline zone contains existing or altered spaces

**Evaluation Context:**  Each Data Element  
**Data Lookup:** None
**Function Call:**  None  

## Rule Logic:

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```

  - For each zone in building segment: ```for zone_b in building_segment_b.zones:``` 
    
    - Initialize zone as not applicable (no existing or altered spaces): ``` applicable = False```
  
    - For each space in zone: ```for space_b in zone_b.spaces:```

      - If any space is existing or altered, iteration can end, rule is applicable to this zone: ```if ( space_b.status_type == EXISTING ) OR ( space_b.status_type == ALTERED ): applicable = True```
    
    **Rule Assertion**
    
    - Case 1: At least one space in the zone is existing or altered, outcome is UNDETERMINED: ``` if applicable: outcome = UNDETERMINED and raise_message "PART OR ALL OF ZONE [zone.id] IS EXISTING OR ALTERED. THE BASELINE VERTICAL FENESTRATION AREA FOR EXISTING ZONES MUST EQUAL TO THE FENESTRATION AREA PRIOR TO THE PROPOSED SCOPE OF WORK. THE BASELINE FENESTRATION AREA IN ZONE MUST BE CHECKED MANUALLY.```
    
    - Case 2: There are no existing or altered spaces in the zone, outcome is NOT_APPLICABLE: ```else: outcome = NOT_APPLICABLE```

**[Back](../_toc.md)**
