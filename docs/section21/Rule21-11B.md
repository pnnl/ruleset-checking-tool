
# Boiler - Rule 21-11B  

**Rule ID:** 21-11B  
**Rule Description:** The baseline building design uses boilers or purchased hot water, the hot water pumping system shall be modeled with continuous variable flow.  
**Rule Assertion:** B-RMR  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11.2, 12, 1a, 7a, 11.2a, 12a, 1b, 3b, 5b, 6b, 7b, 8b, 9b, 11b, 12b, 13b, 1c, 3c, 7c, 11c, 12c, 13c.

**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:**  

1. get_baseline_system_types()

**Applicability Checks:**  

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11.2, 12, 1a, 7a, 11.2a, 12a, 1b, 3b, 5b, 6b, 7b, 8b, 9b, 11b, 12b, 13b, 1c, 3c, 7c, 11c, 12c, 13c, continue to rule logic: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-1", "SYS-5", "SYS-7", "SYS-11.2", "SYS-12", "SYS-1A", "SYS-7A", "SYS-11.2A", "SYS-12A", "SYS-1B", "SYS-3B", "SYS-5B", "SYS-6B", "SYS-7B", "SYS-8B", "SYS-9B", "SYS-11B", "SYS-12B", "SYS-13B", "SYS-1C", "SYS-3C", "SYS-7C", "SYS-11C", "SYS-12C", "SYS-13C"]): CHECK_RULE_LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.RulesetModelInstance.fluid_loops:`

  - Check if fluid loop type is heating: `if fluid_loop_b.type == "HEATING"`

    **Rule Assertion - Component:**

    - Case 1: For each heating hot water loop, if loop is modeled with continuous variable flow: `if ( fluid_loop_b.heating_design_and_control.flow_control == "VARIABLE_FLOW" ) AND ( fluid_loop_b.operation == "CONTINUOUS" ): PASS`

    - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
