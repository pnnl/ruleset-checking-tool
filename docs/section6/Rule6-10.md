
# Lighting - Rule 6-10  

**Rule ID:** 6-10   
**Rule Description:** Where retail display lighting is included in the proposed building design in accordance with Section 9.5.2.2(b), the baseline building design retail display lighting additional power shall be equal to the limits established by Section 9.5.2.2(b) or same as proposed, whichever is less.  
**Rule Assertion:** Baseline RMD = expected value  
**Appendix G Section:** G3.1 #6 Baseline column  

**Mandatory Rule:** True  
**Evaluation Context:** Each Space  
**Function Call:**  

- get_component_by_id()

## Applicability Check:  
- look at each building segment: `for building_segment in P_RMD.building_segments:`
    - get the building segment lighting type: `building_segment_lighting_type = building_segment.lighting_building_area_type`
    - look at each space: `for space in building_segment...spaces:`
        - set a boolean called applicable to false: `applicable = false`
        - set lighting_space_type equal to the space.lighting_space_type: `lighting_space_type = space.lighting_space_type`
        - if the lighting_space_type is NULL, set the lighting_space_type equal to the building_segment_lighting_type: `if lighting_space_type == NULL: lighting_space_type = building_segment_lighting_type`
        - if the lighting space type is one of the retail space types, look at each InteriorLighting object in the model: `if lighting_space_type == "SALES AREA":`
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
                - get the equivalent space in the baseline model: `space_b = get_component_by_id(space.id, B_RMD);`
                - calculate to total baseline interior display lighting power for this space - initialize at 0: `baseline_interior_display_W = 0`
                - look at each lighting in the space: `for interior_lighting in space_b.interior_lighting:`
                    - if the interior lighting purpose_type is RETAIL_DISPLAY, add the lighting wattage to baseline_interior_display_W: `if interior_lighting.purpose_type == "RETAIL_DISPLAY": baseline_interior_display_W = baseline_interior_display_W + interior_lighting.power_per_area * space_b.floor_area`

                **Rule Assertion:**
                - Case 1: If the proposed_interior_display_W is less than or equal to the minimum AND the baseline_interior_display_W is equal to the proposed, then PASS: `if((proposed_interior_display_W <= minimum_retail_display_W) and (baseline_interior_display_W == proposed_interior_display_W)): PASS`
                - Case 2: Otherwise, if the baseline_interior_display_W is greater than the minimum of proposed_interior_display_W and maximum_retail_display_W, then FAIL: `elif baseline_interior_display_W > min(proposed_interior_display_W,maximum_retail_display_W): FAIL`
                - Case 3: All other cases UNDETERMINED and provide note: `else: UNDETERMINED; note = "It could not be determined whether the baseline retail display lighting power is modeled correctly as the minimum of the proposed retail display lighting power and the allowance calculated according to the formulas in ASHRAE 90.1 Section 9.5.2.2(b)."`


**Notes:**
1.  Is the lighting space type check necessary because we are checking the interior_lighting.purpose_type to be RETAIL_DISPLAY?

**[Back](../_toc.md)**


