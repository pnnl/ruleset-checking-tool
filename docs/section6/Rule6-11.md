
# Lighting - Rule 6-11  

**Rule ID:** 6-11   
**Rule Description:**Where retail display lighting is included in the proposed building design the display lighting additional power shall be less than or equal to the limits established by Section 9.5.2.2(b)  
**Rule Assertion:** Proposed RMD = expected value  
**Appendix G Section:** G1.2.1b.1 and the methodology described in Table 9.5.2.2(b)

**Mandatory Rule:** True  
**Evaluation Context:** Each Space  
**Function Call:**  

- get_component_by_id()

## Applicability Check:  
- look at each building segment: `for building_segment in P_RMD.building_segments:`
    - look at each space: `for space in building_segment...spaces:`
        - set a boolean called applicable to false: `applicable = false`
        - set lighting_space_type equal to the space.lighting_space_type: `lighting_space_type = space.lighting_space_type`
        - if the lighting space type is a Sales Area, look at each InteriorLighting object in the model: `if lighting_space_type == "SALES AREA":`
            - look at each interior lighting: `for interior_lighting in space.interior_lighting:`
                - if the interior lighting purpose_type is RETAIL_DISPLAY, set applicable to true - we don't go to the rule logic for each interior lighting because the evaluation context is at the space level: `if interior_lighting.purpose_type == "RETAIL_DISPLAY": applicable = true`
        - if the boolean applicable is true, continue to rule logic: `if applicable: CONTINUE TO RULE LOGIC`
        - otherwise, rule is not applicable: `else: RULE NOT APPLICABLE`
     
            ## Rule Logic:
                - 9.5.2.2(b) gives a formula (750 W + (Retail Area 1 × 0.40 W/ft2) + (Retail Area 2 × 0.40 W/ft2) + (Retail Area 3 × 0.70 W/ft2) + (Retail Area 4 × 1.00 W/ft2)) for retail display lighting that is based on four area categories.  We don't have access to these four area categories in the schema, so we will calculate the maximum and minimum values possible based on this function.  The maximum is calculated based on 100% of the space floor area being type 4: `maximum_retail_display_W = 750 + space.floor_area * (1)`
                - the minimum is calculated based on none of the floor area being a retail area: `minimum_retail_display_W = 750`
                - now calculate the total proposed interior display lighting power for this space - initialize at 0: `proposed_interior_display_W = 0`
                - look at each lighting in the space: `for interior_lighting in space.interior_lighting:`
                    - if the interior lighting purpose_type is RETAIL_DISPLAY, add the lighting wattage to proposed_interior_display_W: `if interior_lighting.purpose_type == "RETAIL_DISPLAY": proposed_interior_display_W = proposed_interior_display_W + interior_lighting.power_per_area * space.floor_area`

                **Rule Assertion:**
                - Case 1: If the proposed_interior_display_W is less than the minimum, then PASS: `if(proposed_interior_display_W < minimum_retail_display_W): PASS`
                - Case 2: Otherwise, if the proposed_interior_display_W is greater than maximum_retail_display_W, then FAIL: `elif proposed_interior_display_W > maximum_retail_display_W: FAIL`
                - Case 3: All other cases UNDETERMINED and provide note: `else: UNDETERMINED; note = "It could not be determined whether the proposed retail display lighting power is less than or equal to the allowance calculated according to the formulas in ASHRAE 90.1 Section 9.5.2.2(b)."

`


**Notes:**
1.  Is the lighting space type check necessary because we are checking the interior_lighting.purpose_type to be RETAIL_DISPLAY?

**[Back](../_toc.md)**


