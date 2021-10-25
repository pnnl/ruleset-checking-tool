
# Boiler - Rule 21-5  

**Rule ID:** 21-5  
**Rule Description:** The baseline building design boiler plant shall be modeled as having a single boiler if the baseline building design plant serves a conditioned floor area of 15,000sq.ft. or less, and as having two equally sized boilers for plants serving more than 15,000sq.ft.  
**Rule Assertion:** B-RMR  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11, or 12
2. B-RMR is not modeled with purchase heating

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  1. get_zone_conditioning_category()

**Applicability Check:**

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11, or 12: `if PLACEHOLDER_AIRSIDE_SYSTEM_RULE-X-XX:`
2. B-RMR is not modeled with purchased heating: `if NOT Rule-21-1:`

## Rule Logic:  

- Get zone conditioning category dictionary for B_RMR: `zcc_b = get_zone_conditioning_category(B_RMR)`

- For each zone in B_RMR: `for zone_b in B_RMR...zones:`

  - Check if zone has HVAC terminals, get zone terminals: `if zone_b.terminals: zone_terminals_b = zone_b.terminals`

    - For each zone terminal: `for zone_terminal_b in zone_terminals_b:`

      - Check if zone area has not been added to any heating hot water loop: `if NOT zone_flag:`

        - Get HVAC system serving the terminal: `hvac_b = zone_b.terminals.served_by_heating_ventilation_air_conditioning_systems`

          - Get heating system from HVAC system: `heating_system_b = hvac_b.heating_system`

            - Check if heating system has heating hot water loop, get heating hot water loop: `if heating_system_b.hot_water_loop: hhw_loop_b = heating_system_b.hot_water_loop`

              - Save zone area to heating hot water loop: `loop_area_dict[hhw_loop_b] += sum(space.floor_area for space in zone_b.spaces)`

              - Set zone flag as True to avoid double counting the zone area: `zone_flag == TRUE`

- For each boiler in B_RMR, save boiler to loop boiler dictionary: `for boiler_b in B_RMR.ASHRAE229.boilers: loop_boiler_dict[boiler_b.loop].append(boiler_b)`

- For each heating hot water loop: `for hhw_loop in loop_area_dict.keys():`

  - Get all boilers on the loop: `boilers_array = loop_boiler_dict[hhw_loop]`

    **Rule Assertion:**

    - Case 1: If total conditioned area under the loop is 15,000sq.ft. or less and if only one boiler in on the loop: `if ( loop_area_dict[hhw_loop] <= 15000 ) AND ( boilers_array.size == 1 ): PASS`

    - Case 2: Else if total conditioned area under the loop is more than 15,000sq.ft. and two boilers are on the loop and the two boilers are sized equally: `else if ( loop_area_dict[hhw_loop] > 15000 ) AND ( boilers_array.size == 2 ) AND ( boilers_array[0].rated_capacity == boilers_array[1].rated_capacity ): PASS`

    - Case 3: Else: `FAIL`

**[Back](../_toc.md)**

**Notes:**

1. Indirectly conditioned zones does not have HVAC system, and may be adjacent to multiple directly conditioned zones served by different hvac systems. how to assign indirectly conditioned zone area?
2. Dependency, B-RMR air-side system that is Type-1, 5, 7, 11, or 12 is modeled correctly with heating hot water plant (e.g. Line 42) and with only one heating hot water plant per building (e.g. Line 44)
3. Or we get all air-side system that is Type-1, 5, 7, 11, or 12 and calculate the total area under these systems.
