
# Boiler - Rule 21-5  

**Rule ID:** 21-5  
**Rule Description:** The baseline building design boiler plant shall be modeled as having a single boiler if the baseline building design plant serves a conditioned floor area of 15,000sq.ft. or less, and as having two equally sized boilers for plants serving more than 15,000sq.ft.  
**Rule Assertion:** B-RMR  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. Baseline system type is 1, 5, 7, 11, or 12

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  1. get_zone_conditioning_category()

## Rule Logic:  

- Get zone conditioning category dictionary for B_RMR: `zcc_b = get_zone_conditioning_category(B_RMR)`

- For each zone in B_RMR: `for zone_b in B_RMR...zones:`

  - Check if zone is conditioned: `if zcc_b[zone_b.id] in ["CONDITIONED RESIDENTIAL", "CONDITIONED NON-RESIDENTIAL", "CONDITIONED MIXED"]:`

    - Get HVAC system serving the zone: `hvac_sys_b =  zone_b.served_by_heating_ventilation_air_conditioning_systems`

      - Check if HVAC System is connected to hot water loop: `if hvac_sys_b.hot_water_loop:`

        - Calculate zone total floor area: `zone_area_b = sum(space.floor_area for space in zone_b.spaces)`

        - Add zone total floor area to the total area served by the hot water loop in a dictionary: `loop_area_dict[hvac_sys_b.hot_water_loop] += zone_area_b`

- For each conditioning component in B_RMR: `for conditioning_component_b in B_RMR.ASHRAE229.conditioning_components:`

  - Check if conditioning component is boiler, save boiler to loop boiler dictionary: `if conditioning_component_b IS boiler: loop_boiler_dict[conditioning_component_b.loop].append(conditioning_component_b)`

- For each hot water loop: `for hhw_loop in loop_area_dict.keys():`

  - Set applicability flag: `rule_applicability_check = TRUE`

  - Get all boilers on the loop: `boilers_array = loop_boiler_dict[hhw_loop]`

    **Rule Assertion:**

    - Case 1: If total conditioned area under the loop is 15,000sq.ft. or less and if only one boiler in on the loop: `if ( loop_area_dict[hhw_loop] <= 15000 ) AND ( boilers_array.size == 1 ): PASS`

    - Case 2: Else if total conditioned area under the loop is more than 15,000sq.ft. and two boilers are on the loop and the two boilers are sized equally: `else if ( loop_area_dict[hhw_loop] > 15000 ) AND ( boilers_array.size == 2 ) AND ( boilers_array[0].rated_capacity == boilers_array[1].rated_capacity ): PASS`

    - Case 3: Else: `FAIL`

**Applicability Check:**

1. Rule is applicable if B-RMR system type is 1, 5, 7, 11, or 12: `if PLACEHOLDER_AIRSIDE_SYSTEM_RULE-X-XX:`

**[Back](../_toc.md)**

**Notes:**

1. Indirectly conditioned zones does not have HVAC system, and may be adjacent to multiple directly conditioned zones served by different hvac systems. how to assign indirectly conditioned zone area?
