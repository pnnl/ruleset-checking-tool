
# Airside System - Rule 23-5 

**Schema Version:** 0.0.34  
**Mandatory Rule:** True  
**Rule ID:** 23-5  
**Rule Description:** For baseline systems 6 and 8, Fans in parallel VAV fan-powered boxes shall run as the first stage of heating before the reheat coil is energized.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** G3.1.3.14 Fan Power and Control (Systems 6 and 8)  
**Data Lookup:** None  
**Evaluation Context:** Terminal  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-6 or 8.  

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()

**Applicability Checks:**  
- create a list of the target system types: `APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_6, HVAC_SYS.SYS_8]`
- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

- make a list of hvac system type ids for systems that are one of 6 or 8: `hvac_sys_6_or_8_list = []`
- loop through the applicable system types: `for target_sys_type in APPLICABLE_SYS_TYPES:`
    - and loop through the baseline_system_types_dict to check the system types of the baseline systems: `for system_type in baseline_system_types_dict:`
        - do baseline_system_type_compare to determine whether the baseline_system_type is the applicable_system_type: `if((baseline_system_type_compare(system_type, target_sys_type, false)):`
            - the systems in the list: baseline_system_types_dict[system_type] are either sys-6 or 8, add them to hvac_sys_6_or_8_list: `hvac_sys_6_or_8_list.extend(baseline_system_types_dict[system_type])`

- go through all the zones in the buildings: `for zone in B-RMR....zones:`
    - look at the zone terminal, and then the zone terminal hvac system to determine if the zone terminal is connected to a system type 6 or 8: `for terminal in zone.terminals:`
        - check if the terminal is connected to a hvac system 6 or 8: `if zone.served_by_heating_ventilating_air_conditioning_system in hvac_sys_6_or_8_list:`
            - `CONTINUE TO RULE LOGIC`
        - otherwise not applicable: `else: NOT_APPLICABLE`
**Rule Logic:**
- if the terminal runs the fan as a first stage of heating before the reheat coil is turned on, then this terminal is compliant with the rule, return PASS: `if terminal.is_first_stage_heat_fan_powered_box: PASS`
- otherwise, the terminal is not compliant, return fail: `else: FAIL`


**Notes:**

1.  This rule relies on the data element terminal.is_first_stage_heat_fan_powered_box, which does not yet exist in the schema.  Furthermore, this rule logic assumes that it will be implemented as a boolean

**[Back](../_toc.md)**
