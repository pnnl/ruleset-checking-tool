
# Envelope - Rule 5-43  

**Mandatory Rule:** True
**Rule ID:** 5-43  
**Rule Description:** Automatic fenestration shading devices shall not be modeled in the Baseline.  
**Rule Assertion:** Baseline RMD = expected value  
**Appendix G Section:** Section G3.1-5(f) Building Envelope Modeling Requirements for the Baseline building  

**Manual Check:** None  
**Evaluation Context:** Each SubSurface  
**Function Call:**  

NONE

## Applicability Check:  
- look at each zone: `for zone in B_RMD...zones:`
    - look at each surface: `for surface in zone.surfaces:`
        - look at each subsurface: `for sub_surface in surface.subsurfaces: CONTINUE TO RULE LOGIC`

            ## Rule Logic:  
            - create a variable automatic_shades_modeled and set it to false: `automatic_shades_modeled = false`
            - check whether the subsurface has the data element has_automatic_shades: `if sub_surface.has_automatic_shades != NULL:`
                - set automatic_shades_modeled to sub_surface.has_atomatic_shades: `automatic_shades_modeled = sub_surface.has_automatic_shades`

            **Rule Assertion:**
            - Case 1: If the baseline subsurface does not have shading devices, then pass: `if not automatic_shades_modeled: PASS`
            - Case 2: If the baseline subsurface has shading devices, then fail: `if automatic_shades_modeled: FAIL`


**Notes:**


**[Back](../_toc.md)**


