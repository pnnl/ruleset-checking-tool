
# Boiler - Rule 21-3  

**Rule ID:** 21-3  
**Rule Description:** Plant capacities shall be based on coincident loads.  
**Rule Assertion:** B-RMR FluidLoop.heating_design_and_control: is_sized_using_coincident_load = True  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.2.2 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B-RMR  
**Applicability Checks:**  

1. B-RMR is modeled with heating fluid loop(s)

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

## Rule Logic:  

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop type is heating: `if fluid_loop_b.type == "HEATING":`

    - Set applicability flag: `rule_applicability_check = TRUE`

    - Get heating design and control component for fluid loop: `heating_design_and_control_b = fluid_loop_b.heating_design_and_control`

      **Rule Assertion:**

      - Case 1: For each heating fluid loop, if heating design and control component is sized using coincident load: `if heating_design_and_control_b.is_sized_using_coincident_load: PASS`

      - Case 2: Else: `else: FAIL`

**Applicability Check:**

1. Rule is applicable if B-RMR is modeled with heating fluid loop(s): `if rule_applicability_check: is_applicable = TRUE`

**[Back](../_toc.md)**
