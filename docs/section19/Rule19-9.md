# Section 19 - Rule 19-9     
**Schema Version:** 0.0.22  
**Mandatory Rule:** True    
**Rule ID:** 19-9     
**Rule Description:** Air economizers shall not be included in baseline HVAC Systems 1, 2, 9, and 10.    
**Rule Assertion:** Options are Pass/Fail/NOT_APPLICABLE     
**Appendix G Section:** G3.1.2.6      
**90.1 Section Reference:** None  

**Data Lookup:** None  

**Evaluation Context:** Each HeatingVentilatingAirConditioningSystem  

**Applicability Checks:** 
1. Applies to baseline HVAC system types 1, 2, 9, and 10.

**Function Calls:**  
1. get_baseline_system_types()  
2. baseline_system_type_compare()  

## Rule Logic:   
**Applicability Check 1**   
- Create a list of the target system types: `target_system_types = [HVAC_SYS.SYS_1, HVAC_SYS.SYS_2, HVAC_SYS.SYS_9,HVAC_SYS.SYS_10]`
- Create dictionary of baseline system types: `baseline_system_types_dict = get_baseline_system_types(B_RMI)`  
- Check if B-RMR is modeled with at least one air-side system of the applicable type, if yes then carry on, if no then NOT_APPLICABLE for the project: `if any(baseline_system_type_compare(system_type, target_sys_type, false) for system_type in baseline_hvac_system_dict.keys() for target_system_type in target_system_types):` 
    - For each hvac system in the B_RMR: `for hvac in B_RMI...HeatingVentilatingAirConditioningSystem:` 
        - Get the baseline system type: `hvac_sys_type_b = list(baseline_system_types_dict.keys())[list(baseline_system_types_dict.values()).index(hvac.id)])`
        - Check if system type is of an applicable system type, if yes then carry on, if no then NOT_APPLICABLE for the hvac system:  `if any(baseline_system_type_compare(hvac_sys_type_b, target_sys_type, false) for target_system_type in target_system_types):`                     
            - **Rule Assertion:** 
            - Case 1: If there is NOT an AirEconomizer object associated with the fan (equals Null) or if the aireconomizer type is fixed fraction then pass: `if hvac.fan_system.AirEconomizer == Null OR hvac.fan_system.AirEconomizer.type == "FIXED_FRACTION": outcome = "PASS"`  
            - Case 2: Else, fail: `Else: outcome = "Fail"`  

**Notes/Questions:**  None

**[Back](../_toc.md)**