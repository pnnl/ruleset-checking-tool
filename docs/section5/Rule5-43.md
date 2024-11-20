
# Envelope - Rule 5-43  

**Mandatory Rule:** True
**Rule ID:** 5-43  
**Rule Description:** Automatic fenestration shading devices shall not be modeled in the Baseline.  
**Rule Assertion:** Baseline RMD = expected value  
**Appendix G Section:** Section G3.1-5(f) Building Envelope Modeling Requirements for the Baseline building  

**Manual Check:** None  
**Evaluation Context:** Each Building  
**Function Call:**  


## Applicability Check:  
- look at each zone: `for building in B_RMD.buildings:`
    - look at each zone: `for zone in building...zones:`
        - look at each surface: `for surface in zone.surfaces:`
            - check if the surface is an exterior surface type: `if surface.adjacent_to == "EXTERIOR":`
                - look at each subsurface: `for sub_surface in surface.subsurfaces: CONTINUE TO RULE LOGIC`
    - if the code reaches here without going to the rule logic, the building has no exterior subsurfaces and the rule is not applicable: `NOT APPLICABLE`
    
    ## Rule Logic:  
    - create a list automatic_shades_modeled and initialize it as an empty list: `automatic_shades_modeled = []`
    - look at each zone: `for zone in B_RMD...zones:`
        - look at each surface: `for surface in zone.surfaces:`
            - check if the surface is an exterior surface type: `if surface.adjacent_to == "EXTERIOR":`
                - look at each subsurface: `for sub_surface in surface.subsurfaces:`
                    - check whether the subsurface has the data element has_automatic_shades: `if sub_surface.has_automatic_shades != NULL:`
                        - if the window has automatic shades, append this sub_surface id to the list automatic_shades_modeled: `if sub_surface.has_automatic_shades: automatic_shades_modeled.append(sub_surface.id)`
    - GO TO RULE ASSERTION
    
    **Rule Assertion:**
    - Case 1: If the baseline does not have shading devices, the list automatic_shades_modeled will be empty, PASS: `if len(automatic_shades_modeled) == 0: PASS`
    - Case 2: Otherwise FAIL: `else: FAIL`


**Notes:**


**[Back](../_toc.md)**


