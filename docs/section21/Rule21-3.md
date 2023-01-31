
# Boiler - Rule 21-3  

**Rule ID:** 21-3  
**Rule Description:** Heating hot water plant capacity shall be based on coincident loads.  
**Rule Assertion:** B-RMR FluidLoop.heating_design_and_control: is_sized_using_coincident_load = True  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.2.2 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B-RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11.2, 12, 1a, 7a, 11.2a, 12a.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()

**Applicability Check:**

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`
  
  - Check if B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11.2, 12, 1a, 7a, 11.2a, 12a, continue to rule logic: `if any(baseline_system_type_compare(sys_type, target_system_type, true) for sys_type in baseline_hvac_system_dict.keys() for target_system_type in [HVAC.SYS_1, HVAC.SYS_5, HVAC.SYS_7, HVAC.SYS_11_2, HVAC.SYS_12, HVAC.SYS_1A,HVAC.SYS_7A, HVAC.SYS_11_2A, HVAC.SYS_12A]): CHECK_RULE_LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.RulesetModelInstance.fluid_loops:`

  - Check if fluid loop type is heating: `if fluid_loop_b.type == "HEATING":`

    - Get heating design and control component for fluid loop: `heating_design_and_control_b = fluid_loop_b.heating_design_and_control`

      **Rule Assertion - Component:**

      - Case 1: For each heating fluid loop, if heating design and control component is sized using coincident load: `if heating_design_and_control_b.is_sized_using_coincident_load: PASS`

      - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
