
# Envelope - Rule 5-39  

**Rule ID:** 5-39  
**Rule Description:** Automatically controlled dynamic glazing may be modeled. Manually controlled dynamic glazing shall use the average of the minimum and maximum SHGC and VT.  
**Rule Assertion:** P-RMR subsurface: dynamic_glazing_type = expected value  
**Appendix G Section:** Section G3.1-5(a)5 Building Envelope Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

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

        **Rule Assertion:**  

        - Case 1: For each subsurface that has dynamic glazing, if it is manually controlled: `if subsurface_p.dynamic_glazing_type == "MANUAL_DYNAMIC": CAUTION and raise_warning "THE PROPOSED DESIGN INCLUDES DYNAMIC GLAZING THAT IS NOT AUTOMATICALLY CONTROLLED. MANUAL CHECK IS REQUIRED TO VERIFY THAT SHGC AND VT WERE MODELED AS THE AVERAGE OF THE MINIMUM AND MAXIMUM SHGC AND VT."`

        - Case 2: Else if it is automatically controlled: `else if subsurface_p.dynamic_glazing_type == "AUTOMATIC_DYNAMIC": PASS`

**Applicability Check:** For each building, if no subsurface in building has dynamic glazing, rule is not applicable: `if NOT rule_applicability_check: is_applicable = FALSE`

**[Back](../_toc.md)**
