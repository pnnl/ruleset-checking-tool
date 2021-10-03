
# Boiler - Rule 21-2  

**Rule ID:** 21-2  
**Rule Description:** Baseline should include all on-site distribution pumps included in the Proposed design.  
**Rule Assertion:** B-RMR LEN(ASHRAE229:conditioning_component.pump) = P-RMR LEN(ASHRAE229:conditioning_component.pump) for pumps serving purchased hot water or steam loops  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.1.3.4 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. P-RMR is modeled with purchased hot water or steam

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

## Rule Logic:  

- For each conditioning component in P_RMR: `for conditioning_component_p in P_RMR.ASHRAE229.conditioning_components:`

  - Check if conditioning component is pump:`if conditioning_component_p IS Pump:`

    - Save pump to loop pump dictionary: `loop_pump_dictionary_p[conditioning_component_p.loop].append(conditioning_component_p)`

- For each conditioning component in B_RMR: `for conditioning_component_b in B_RMR.ASHRAE229.conditioning_components:`

  - Check if conditioning component is pump:`if conditioning_component_b IS Pump:`

    - Save pump to loop pump dictionary: `loop_pump_dictionary_b[conditioning_component_b.loop].append(conditioning_component_b)`

- For each conditioning component in P_RMR: `for conditioning_component_p in P_RMR.ASHRAE229.conditioning_components:`

  - Check if conditioning component is purchased hot water or steam in P_RMR: `if ( conditioning_component_p IS ExternalFluidSource ) AND ( conditioning_component_p.type in ["HOT_WATER", "STEAM] ):`

    - Set applicability flag: `rule_applicability_check = TRUE`

    - Get loop associated with external fluid source in P_RMR: `fluid_loop_p = conditioning_component_p.loop`

      - Get number of pumps serving the loop from loop pump dictionary in P_RMR: `num_of_pumps_p = LEN(loop_pump_dictionary_p[fluid_loop_p])`

      - Get matching fluid loop in B_RMR: `fluid_loop_b = match_data_element(B_RMR, FluidLoops, fluid_loop_p.id)`

        - Get number of pumps serving the loop from loop pump dictionary in B_RMR: `num_of_pumps_b = LEN(loop_pump_dictionary_b[fluid_loop_b])`

          **Rule Assertion:**

          - Case 1: For each external fluid source that is purchased hot water or steam in P-RMR, if number of pumps serving the loop in B-RMR matches that in P-RMR: `if num_of_pumps_p == num_of_pumps_b: PASS`

          - Case 2: Else: `else: FAIL`

**Applicability Check:**

1. Rule is applicable if P-RMR is modeled with purchased hot water or steam: `if rule_applicability_check: is_applicable = TRUE`

**[Back](../_toc.md)**

**Notes:**

1. Pending on how to get to external_fluid_source from conditioning_components.
