
# Airside System - Rule 23-9  

**Schema Version:** 0.0.12  
**Mandatory Rule:** True  
**Rule ID:** 23-9  
**Rule Description:** Systems 6&8: Supply air temperature setpoint shall be constant at the design condition.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)  
**Data Lookup:** None  
**Evaluation Context:** Building  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-6, 8, 8a, 6b, 8b.  

**Function Calls:**  

1. get_baseline_system_types()
2. is_baseline_system_type()

**Applicability Checks:**  

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-6, 8, 8a, 6b, 8b, continue to rule logic: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-6", "SYS-8", "SYS-8A", "SYS-6B", "SYS-8B"]): CHECK_RULE_LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each building segment in baseline ruleset model instance: `for building_segment_b in ASHRAE229.ruleset_model_instance[baseline]...building_segments:`

  - For each HVAC system in building segment: `for hvac_b in building_segment_b.heating_ventilation_air_conditioning_systems:`
  
    - Check if HVAC system is type 6, 8, 8a, 6b, 8b: `if any(is_baseline_system_type(hvac_b, sys_type)) == TRUE for sys_type in ["SYS-6", "SYS-8", "SYS-8A", "SYS-6B", "SYS-8B"]):`

      **Rule Assertion:**

      - Case 1: For each HVAC system that is Type-6, 8, 8a, 6b, 8b, if supply temperature setpoint is constant: `if ( hvac_b.fan_system.temperature_control == "CONSTANT" ): PASS`

      - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
