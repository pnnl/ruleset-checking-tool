
# Boiler - Rule 21-5  

**Rule ID:** 21-5  
**Rule Description:** The baseline building design boiler plant shall be modeled as having a single boiler if the baseline building design plant serves a conditioned floor area of 15,000sq.ft. or less, and as having two equally sized boilers for plants serving more than 15,000sq.ft.  
**Rule Assertion:** B-RMR  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11.2, 12, 1a, 7a, 11.2a, 12a.

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  1. get_baseline_system_types()
  2. get_zone_conditioning_category()
  3. get_loop_zone_list_w_area()

**Applicability Check:**

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`
  
  - Check if B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11.2, 12, 1a, 7a, 11.2a, 12a, continue to rule logic: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-1", "SYS-5", "SYS-7", "SYS-11.2", "SYS-12", "SYS-1A", "SYS-7A", "SYS-11.2A", "SYS-12A"]): CHECK_RULE_LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- Get zone conditioning category dictionary for B_RMR: `zone_conditioning_category_dict = get_zone_conditioning_category(B_RMR)`

- Get dictionary that saves the list of zones and the total floor area served by each CHW or HHW loop: `loop_zone_list_w_area_dict = get_loop_zone_list_w_area(B_RMR)`

- Get a list of loops attached to boilers `boiler_loop_ids = [boiler.loop for boiler in B_RMR.RulesetModelInstance.boilers]`

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.RulesetModelInstance.fluid_loops:`

  - Check if fluid loop is heating type and the fluid is attached to a boiler: `if fluid_loop_b.type == "HEATING" and fluid_loop_b.id in boiler_loop_ids:`

    - Add to the list of zones with their total floor area served by heating loop: `heating_loop_zone_list.append(loop_zone_list_w_area_dict[fluid_loop_b.id]["ZONE_LIST"]), heating_loop_conditioned_zone_area += loop_zone_list_w_area_dict[fluid_loop_b.id]["TOTAL_AREA"]`

- For each zone in B_RMR: `for zone_b in B_RMR...zones:`

  - Check if zone is classified as conditioned (including directly and indirectly conditioned) and zone is not connected to any heating loop: `if ( zone_conditioning_category_dict[zone_b.id] in ["CONDITIONED RESIDENTIAL", "CONDITIONED NON-RESIDENTIAL", "CONDITIONED MIXED"] ) AND ( NOT zone_b in heating_loop_zone_list ):`

    - Classify zone as indirectly conditioned and add zone total area to total area served by heating loop: `heating_loop_conditioned_zone_area += SUM(space.floor_area for space in zone.spaces)` (Note XC, in this logic zone might be adjacent to directly conditioned zones that are cooling only, but its area will still be added to HHW loop)

**Rule Assertion - Component:**

- Case 1: If baseline building design plant serves a conditioned floor area of 15,000sq.ft. or less, and if only one boiler is modeled in B_RMR: `if ( heating_loop_conditioned_zone_area <= 15000 ) AND ( LEN(B_RMR.RulesetModelInstance.boilers) == 1 ): PASS`

- Case 2: Else if baseline building design plant serves a conditioned floor area more than 15,000sq.ft. and two boilers are modeled in B_RMR and the two boilers are sized equally: `else if ( heating_loop_conditioned_zone_area > 15000 ) AND ( LEN(B_RMR.RulesetModelInstance.boilers) == 2 ) AND ( B_RMR.RulesetModelInstance.boilers[0].rated_capacity == B_RMR.RulesetModelInstance.boilers[1].rated_capacity ): PASS`

- Case 3: Else: `else: FAIL`

**Notes:**

1. This treats all buildings in an RMR (if it has multiple buildings) as one building with one HHW plant.


**[Back](../_toc.md)**