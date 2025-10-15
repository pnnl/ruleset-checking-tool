                                          
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
    - look at each space: `for space in building_segment...spaces:`
        - if the space has any retail display lighting then the rule applies: `if len(space["interior_lighting"]) > 0 and any(interior_lighting["purpose_type"] == "RETAIL_DISPLAY" for interior_lighting in space["interior_lighting"]):`
            - return True: `return True`
        - else return False: `return False`

## Rule Logic:  
- 9.5.2.2(b) gives a formula (750 W + (Retail Area 1 × 0.40 W/ft2) + (Retail Area 2 × 0.40 W/ft2) + (Retail Area 3 × 0.70 W/ft2) + (Retail Area 4 × 1.00 W/ft2)) for retail display lighting that is based on four area categories.  We don't have access to these four area categories in the schema, so we will calculate the maximum and minimum values possible based on this function.  
- The maximum is calculated based on 100% of the space floor area being type 4: `maximum_retail_display_w = 750 + space_p["floor_area"]`
- The minimum is calculated based on none of the floor area being a retail area: `minimum_retail_display_w = 750`
- now calculate the total proposed interior display lighting power for this space - initialize at 0: `proposed_interior_display_w = 0`
- for each interior lighting in the proposed space: `for interior_lighting in space_p["interior_lighting"]:`
    - if the interior lighting purpose_type is RETAIL_DISPLAY, add the lighting wattage to proposed_interior_display_w: `if interior_lighting["purpose_type"] == "RETAIL_DISPLAY": proposed_interior_display_w += interior_lighting["power_per_area"] * space_p["floor_area"]`

- get the equivalent space in the baseline model: `space_b = get_component_by_id(space.id, B_RMD);`
- calculate the total baseline interior display lighting power for this space - initialize at 0: `baseline_interior_display_w = 0`
- for each interior lighting in the baseline space: `for interior_lighting in space_b["interior_lighting"]:`
    - if the interior lighting purpose_type is RETAIL_DISPLAY, add the lighting wattage to baseline_interior_display_w: `if interior_lighting["purpose_type"] == "RETAIL_DISPLAY": baseline_interior_display_w += interior_lighting["power_per_area"] * space_p["floor_area"]`

**Rule Assertion:**
- Case 1: If the proposed_interior_display_w is less than or equal to the minimum AND the baseline_interior_display_w is equal to the proposed, then PASS: `if((proposed_interior_display_w <= minimum_retail_display_w) and (baseline_interior_display_w == proposed_interior_display_w)): PASS`
- Case 2: Otherwise, if the baseline_interior_display_w is greater than the minimum of proposed_interior_display_w and maximum_retail_display_w, then FAIL: `elif baseline_interior_display_w > min(proposed_interior_display_w, maximum_retail_display_w): FAIL`
- Case 3: All other cases UNDETERMINED and provide note: `else: UNDETERMINED; note = "It could not be determined whether the baseline retail display lighting power is modeled correctly as the minimum of the proposed retail display lighting power and the allowance calculated according to the formulas in ASHRAE 90.1 Section 9.5.2.2(b)."`


**Notes:**  None 

**[Back](../_toc.md)**


