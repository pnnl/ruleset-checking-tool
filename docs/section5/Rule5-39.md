
# Envelope - Rule 5-39  

**Rule ID:** 5-39  
**Rule Description:** Automatically controlled dynamic glazing may be modeled. Manually controlled dynamic glazing shall use the average of the minimum and maximum SHGC and VT.  
**Rule Assertion:** P-RMR subsurface: dynamic_glazing_type = expected value  
**Appendix G Section:** Section G3.1-5(a)5 Building Envelope Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** None

## Rule Logic:  

- For each building segment in the Proposed model: `for building_segment_p in P_RMR.building.building_segments:`

  - For each thermal block in building segment: `for thermal_block_p in building_segment_p.thermal_blocks:`

    - For each zone in thermal block: `for zone_p in thermal_block_p.zones:`

      - For each surface in zone: `for surface_p in zone_p.surfaces:`

        - For each subsurface in surface: `for subsurface_p in surface_p.subsurfaces:`

          **Rule Assertion:**  

          - Case 1: If subsurface does not have dynamic glazing: `if subsurface_p.dynamic_glazing_type == "NOT_DYNAMIC": rule_not_applicable`

          - Case 2: If subsurface has dynamic glazing and it is manually controlled: `if subsurface_p.dynamic_glazing_type == "MANUAL_DYNAMIC": CAUTION and raise_warning "THE PROPOSED DESIGN INCLUDES DYNAMIC GLAZING THAT IS NOT AUTOMATICALLY CONTROLLED. MANUAL CHECK IS REQUIRED TO VERIFY THAT SHGC AND VT WERE MODELED AS THE AVERAGE OF THE MINIMUM AND MAXIMUM SHGC AND VT."`

          - Case 3: Else if subsurface has dynamic glazing, and it is automatically controlled: `else if subsurface_p.dynamic_glazing_type == "AUTOMATIC_DYNAMIC": PASS`

**[Back](../_toc.md)**
