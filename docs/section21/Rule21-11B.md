
# Boiler - Rule 21-11B  

**Rule ID:** 21-11B  
**Rule Description:** When the system uses boilers the hot water system shall be modeled with continuous variable flow.  
**Rule Assertion:** B-RMR  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11(for climate zones other than 0 through 3A), 12, 1a, 7a, 11a(for climate zones other than 0 through 3A), 12a.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:**  

1. get_baseline_system_types()

**Applicability Checks:**  

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with any air-side system that is Type-11 or 11a: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-11", "SYS-11A"]):`

    - Check if B-RMR is in climate zones other than 0 through 3A, continue to rule logic: `if NOT B_RMR.ASHRAE229.weather.climate_zone in ["0A", "0B", "1A", "1B", "2A", "2B", "3A"]: CHECK_RULE_LOGIC`

    - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

  - Else: `else:`
  
    - Check if B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 12, 1a, 7a, 12a, continue to rule logic: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-1", "SYS-5", "SYS-7", "SYS-12", "SYS-1A", "SYS-7A", "SYS-12A"]): CHECK_RULE_LOGIC`

    - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each boiler in B_RMR, save boiler to loop boiler dictionary: `for boiler_b in B_RMR.ASHRAE229.boilers: loop_boiler_dict[boiler_b.loop].append(boiler_b)`

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop is connected to boiler(s): `if fluid_loop_b in loop_boiler_dict.keys()`

    **Rule Assertion - Component:**

    - Case 1: For heating hot water loop that boiler serves, if loop is modeled with continuous variable flow: `if ( fluid_loop_b.heating_design_and_control.flow_control == "VARIABLE_FLOW" ) AND ( fluid_loop_b.operation == "CONTINUOUS" ): PASS`

    - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
