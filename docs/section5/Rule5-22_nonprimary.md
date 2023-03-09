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

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```

  - For each zone in building segment: ```for zone_b in building_segment_b.zones:``` 

    - For each space in zone: ```for space_b in zone_b.spaces:```
      
      **Rule Assertion**
    
      - Case 1: Check if space is existing or altered, outcome is UNDETERMINED: ```if ( space_b.status_type == EXISTING ) OR ( space_b.status_type == ALTERED ): outcome = UNDETERMINED```
    
      - Case 2: Else, outcome is NOT_APPLICABLE: ```else: outcome = NOT_APPLICABLE```

**[Back](../_toc.md)**
