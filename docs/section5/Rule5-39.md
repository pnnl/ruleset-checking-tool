
# Envelope - Rule 5-39  

**Rule ID:** 5-39  
**Rule Description:** Automatically controlled dynamic glazing may be modeled. Manually controlled dynamic glazing shall use the average of the minimum and maximum SHGC and VT.  
**Rule Assertion:** P-RMR subsurface: is_dynamic_glazing = expected value  
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

          - Check if subsurface is window and has dynamic glazing: `if subsurface_p.classification == "WINDOW":`

            **Rule Assertion:**  

            If window has dynamic glazing, request manual check: `if subsurface_p.is_dynamic_glazing: CAUTION and raise_warning "THE PROPOSED DESIGN INCLUDES DYNAMIC GLAZING. MANUAL CHECK IS REQUIRED TO VERIFY THAT SHGC AND VT WERE MODELED AS REQUIRED. MANUALLY CONTROLLED DYNAMIC GLAZING SHALL USE THE AVERAGE OF THE MINIMUM AND MAXIMUM SHGC AND VT."`

**[Back](../_toc.md)**

**Notes:**

1. Can subsurface.is_dynamic_glazing be applied to skylight and glass door as well? Right now it seems to be a property for window only in the schema. 

subsurface.is_dynamic_glazing:

Description: "Identifies whether the window subsurface can change it's performance properties"
Data Type: "Boolean"
