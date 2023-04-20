
# Envelope - Rule 5-39  

**Rule ID:** 5-39  
**Rule Description:** Automatically controlled dynamic glazing may be modeled. Manually controlled dynamic glazing shall use the average of the minimum and maximum SHGC and VT.  
**Rule Assertion:** P-RMR subsurface: dynamic_glazing_type = expected value  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(a)5 Building Envelope Modeling Requirements for the Proposed design   

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** Yes  

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** None

## Rule Logic:  

- For each zone in the Proposed model: `for zone_p in P_RMR...zones:`

  - For each surface in zone: `for surface_p in zone_p.surfaces:`

    - For each subsurface in surface: `for subsurface_p in surface_p.subsurfaces:`

      - Check if subsurface has dynamic glazing, set rule applicability check to True: `if subsurface_p.dynamic_glazing_type != "NOT_DYNAMIC: rule_applicability_check = TRUE`

        - Get matching subsurface from U_RMR: `subsurface_u = match_data_element(U_RMR, Subsurfaces, subsurface_p.id)`

          **Rule Assertion:**  

          - Case 1: For each subsurface that has dynamic glazing, if dynamic glazing type in P-RMR is not equal to that in U-RMR: `if subsurface_p.dynamic_glazing_type != subsurface_u.dynamic_glazing_type: FAIL and raise_warning "SUBSURFACE IN P-RMR IS MODELED WITH DYNAMIC GLAZING BUT THE DYNAMIC GLAZING TYPE IS NOT EQUAL TO U-RMR."`

          - Case 2: Else if dynamic glazing in P-RMR is manually controlled: `if subsurface_p.dynamic_glazing_type == "MANUAL_DYNAMIC": CAUTION and raise_warning "THE PROPOSED DESIGN INCLUDES DYNAMIC GLAZING THAT IS NOT AUTOMATICALLY CONTROLLED. MANUAL CHECK IS REQUIRED TO VERIFY THAT SHGC AND VT WERE MODELED AS THE AVERAGE OF THE MINIMUM AND MAXIMUM SHGC AND VT."`

          - Case 3: Else, dynamic glazing in P-RMR is automatically controlled: `else if subsurface_p.dynamic_glazing_type == "AUTOMATIC_DYNAMIC": PASS`

**Applicability Check:** For each building, if no subsurface in building has dynamic glazing, rule is not applicable: `if NOT rule_applicability_check: is_applicable = FALSE`

**[Back](../_toc.md)**
