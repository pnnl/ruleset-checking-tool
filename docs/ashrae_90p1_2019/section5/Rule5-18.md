# Envelope - Rule 5-18  
**Schema Version** 0.0.23  
**Primary Rule:** False
**Rule ID:** 5-18  
**Rule Description:** Manually controlled dynamic glazing shall use the average of the minimum and maximum SHGC and VT.
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(a)5 Building Envelope Modeling Requirements for the Proposed design   

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**
  1. The proposed building uses manually controlled dynamic glazing

**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** None

## Rule Logic:
- For each building segment in the Proposed model: ```for building_segment_p in P_RMR.building.building_segments:```

  - For each zone in building segment: ```for zone_p in building_segment_p.zones:```

    - For each surface in zone: ```for surface_p in zone_p.surfaces:```

      - For each subsurface in surface: ```for subsurface_p in surface_p.subsurfaces:```
        
      **Rule Assertion:**
      - Case 1: If subsurface has manual dynamic glazing, outcome is UNDETERMINED: ```if subsurface_p.dynamic_glazing_type == "MANUAL_DYNAMIC: outcome = UNDETERMINED and raise_message "SUBSURFACE ${subsurface_p} INCLUDES MANUALLY CONTROLLED DYNAMIC GLAZING IN THE PROPOSED DESIGN. VERIFY THAT SHGC AND VT WERE MODELED AS THE AVERAGE OF THE MINIMUM AND MAXIMUM SHGC AND VT."```
      - Case 2: Else, outcome is NOT_APPLICABLE: ```else: outcome = NOT_APPLICABLE```

**Notes:**

1. Update Rule ID from 5-39 to 5-29 on 10/26/2023
2. Update Rule ID from 5-29 to 5-18 on 12/22/2023

**[Back](../_toc.md)**
