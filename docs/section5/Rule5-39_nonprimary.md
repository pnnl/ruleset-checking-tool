# Envelope - Rule 5-39  
**Schema Version** 0.0.23  
**Primary Rule:** False
**Rule ID:** 5-39  
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
- Create undetermined_subsurface_list: `undetermined_subsurface_list = []`

- For each building segment in the Proposed model: ```for building_segment_p in P_RMR.building.building_segments:```

  - For each zone in building segment: ```for zone_p in building_segment_p.zones:```

    - For each space in zone: ```for space_p in zone_p.spaces:```
    
      - For each surface in space: ```for surface_p in space_p.surfaces:```

        - For each subsurface in surface: ```for subsurface_p in surface_p.subsurfaces:```

          - Check if subsurface has manual dynamic glazing, set rule applicability check to True: ```if subsurface_p.dynamic_glazing_type == "MANUAL_DYNAMIC: rule_applicability_check = TRUE```

            - Add to array of subsurfaces with manual dynamic glazing if not already saved: ```if NOT subsurface_p in undetermined_subsurface_list: undetermined_subsurface_list.append(subsurface_p)```

              **Rule Assertion:**

              - Case 1: If dynamic glazing in P-RMR is manually controlled, outcome is UNDETERMINED: ```if rule_applicability_check: outcome = UNDETERMINED and raise_warning "THE SUBSURFACES LISTED BELOW INCLUDE MANUALLY CONTROLLED DYNAMIC GLAZING IN THE PROPOSED DESIGN. VERIFY THAT SHGC AND VT WERE MODELED AS THE AVERAGE OF THE MINIMUM AND MAXIMUM SHGC AND VT. ${undetermined_subsurface_list}"```

              - Case 2: For each building, if no subsurface in building has dynamic glazing, outcome is NOT_APPLICABLE: ```if NOT rule_applicability_check: outcome = NOT_APPLICABLE```

**[Back](../_toc.md)**
