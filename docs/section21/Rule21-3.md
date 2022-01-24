
# Boiler - Rule 21-3  

**Rule ID:** 21-3  
**Rule Description:** Heating hot water plant capacity shall be based on coincident loads.  
**Rule Assertion:** B-RMR FluidLoop.heating_design_and_control: is_sized_using_coincident_load = True  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.2.2 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B-RMR  
**Applicability Checks:**  

1. P-RMR is modeled with purchased heating.
2. B-RMR is modeled with at least one air-side system that is Type-1a, 7, 11, 12 or that is Type-1, 5, 7, 11, 12.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:**  

1. check_purchased_chw_hhw()

**Applicability Check:**

1. Check if P-RMR is modeled with purchased cooling or purchased hot water/steam: `purchased_chw_hhw_status_dict = check_purchased_chw_hhw(P_RMR)`

  - If P-RMR is modeled with purchased hot water/steam, rule is not applicable: `if purchased_chw_hhw_status_dict["PURCHASED_HEATING"]: rule_applicability_flag = FALSE`

  - Else, P-RMR is not modeled with purchased hot water/steam, continue to next applicability check: `if NOT purchased_chw_hhw_status_dict["PURCHASED_HEATING"]:`

2. B-RMR is modeled with at least one air-side system that is Type-1a, 7, 11, 12 or that is Type-1, 5, 7, 11, 12:

  - If P-RMR is not modeled with purchased cooling: `if NOT purchased_chw_hhw_status_dict["PURCHASED_COOLING"]:`

    - Check if B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11 or 12, continue to rule logic: `PLACEHOLDER`

    - Else, rule is not applicable: `else: rule_applicability_flag = FALSE`

  - Else, P-RMR is modeled with purchased cooling: `else:`

    - Check if B-RMR is modeled with at least one air-side system that is Type-1a, 7, 11 or 12, continue to rule logic: `PLACEHOLDER`

    - Else, rule is not applicable: `else: rule_applicability_flag = FALSE`

## Rule Logic:  

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop type is heating: `if fluid_loop_b.type == "HEATING":`

    - Get heating design and control component for fluid loop: `heating_design_and_control_b = fluid_loop_b.heating_design_and_control`

      **Rule Assertion - Component:**

      - Case 1: For each heating fluid loop, if heating design and control component is sized using coincident load: `if heating_design_and_control_b.is_sized_using_coincident_load: PASS`

      - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
