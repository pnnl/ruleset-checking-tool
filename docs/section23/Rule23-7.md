
# Airside System - Rule 23-7  

**Schema Version:** 0.0.23  
**Mandatory Rule:** True  
**Rule ID:** 23-7  
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
2. baseline_system_type_compare()

**Applicability Checks:**  
- create a list of the target system types: `target_system_types = [HVAC_SYS.SYS_6,HVAC_SYS.SYS_8]`
- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-6, 8, 8a, 6b, 8b, continue to rule logic: `if any(baseline_system_type_compare(system_type, target_sys_type, false) for system_type in baseline_hvac_system_dict.keys() for target_system_type in target_system_types): CHECK RULE LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  
- create a list of eligible hvac system ids: `eligible_hvac_system_ids = []`

- for each baseline system type: `for baseline_system_type in baseline_hvac_system_dict:`

  - check if it is one of the eligible system types: `if any(baseline_system_type_compare(baseline_system_type, target_system_type, false) for target_system_type in target_system_types):`

    - add the hvac_ids for this sytem type to the list of eligible systems: `eligible_hvac_system_ids = eligible_hvac_system_ids + baseline_hvac_system_dict[baseline_system_type]`

- For each building segment in baseline ruleset model instance: `for building_segment_b in ASHRAE229.ruleset_model_instance[baseline]...building_segments:`

  - For each HVAC system in building segment: `for hvac_b in building_segment_b.heating_ventilating_air_conditioning_systems:`
  
    - Check if HVAC system is one of the eligible systems: `if hvac_b.id in eligible_hvac_system_ids:`

      **Rule Assertion:**

      - Case 1: For each HVAC system that is Type-6, 8, 8a, 6b, 8b, if supply temperature setpoint is constant: `if ( hvac_b.fan_system.temperature_control == "CONSTANT" ): PASS`

      - Case 2: Else: `else: FAIL`

**Notes:**
1. Updated the Rule ID from 23-9 to 23-7 on 11/28/2022


**[Back](../_toc.md)**
