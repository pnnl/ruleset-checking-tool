
# Boiler - Rule 21-7  

**Rule ID:** 21-7  
**Rule Description:** When baseline building requires boilers, systems 1,5,7,11 and 12 - Model HWST = 180F and return design temp = 130F.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.3 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11.2, 12, 1a, 7a, 11.2a, 12a.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()

**Applicability Checks:**  

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11.2, 12, 1a, 7a, 11.2a, 12a, continue to rule logic: `if any(baseline_system_type_compare(sys_type, target_system_type, true) for sys_type in baseline_hvac_system_dict.keys() for target_system_type in [HVAC.SYS_1, HVAC.SYS_5, HVAC.SYS_7, HVAC.SYS_11_2, HVAC.SYS_12, HVAC.SYS_1A, HVAC.SYS_7A, HVAC.SYS_11_2A, HVAC.SYS_12A]): CHECK_RULE_LOGIC`


  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each boiler in B_RMI, save boiler to loop boiler list: `for boiler_b in B_RMI.RulesetModelInstance.boilers: loop_boiler_ids.append(boiler_b.id)`

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.RulesetModelInstance.fluid_loops:`

  - Check if fluid loop is connected to boiler(s): `if fluid_loop_b in loop_boiler_dict.keys()`

    **Rule Assertion - Component:**

    - Case 1: For each fluid loop that boiler serves, if design supply temperature is 180F and design return temperature is 130F: `if ( fluid_loop_b.heating_design_and_control.design_supply_temperature == 180 ) AND ( fluid_loop_b.heating_design_and_control.design_return_temperature == 130 ): PASS`

    - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
