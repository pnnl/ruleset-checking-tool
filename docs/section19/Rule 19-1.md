# Section 19 - Rule 19-1  
**Schema Version:** 0.0.21  
**Mandatory Rule:** True  
**Rule ID:** 19-1   
**Rule Description:** HVAC system coil capacities for the baseline building design shall be oversized by 15% for cooling and 25% for heating..  
**Rule Assertion:** Options are Pass/Fail/IN_APPLICABLE     
**Appendix G Section:** Section G3.1.2.2    
**90.1 Section Reference:** None  

**Data Lookup:** None  

**Evaluation Context:** Each HeatingVentilationAirConditioningSystem Data Group  

**Applicability Checks:** 

1. Applies to the following baseline system types: 1, 1b, 2, 3, 3a, 3b, 4, 5, 5b, 6, 6b, 9 (systems with furnaces, heat pumps, and DX cooling coils)  

**Function Calls:**  
1. get_baseline_system_types()  


## Rule Logic:  
- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`  
- Check if this rule is applicable to any HVAC systems in the B_RMR, if not then the outcome is IN_APPLICABLE for all HVAC systems: `If any(hvac.id in baseline_hvac_system_dict[sys_type] for sys_type in ["SYS-1", "SYS-1b","SYS-2", "SYS-3", "SYS-3a", "SYS-4", "SYS-5", "SYS-5b", "SYS-6", "SYS-6b", "SYS-9"]):`   
    - For each hvac system in B_RMR: `for hvac in B_RMR...HeatingVentilationAirConditioningSystem:`    
        - Reset heating_oversizing_factor: `heating_oversizing_factor = ""`  
        - Reset cooling_oversizing_factor: `cooling_oversizing_factor = ""`  
        - Get baseline system type: `sys_type = list(baseline_hvac_system_dict.keys())[list(baseline_hvac_system_dict.values()).index(hvac.id)]`  
        - Check if the baseline system type has a furnace, heat pump, or DX cooling coil, ELSE then rule outcome for this HVAC system is NOT_APPLICABLE: `if sys_type in ["SYS-1", "SYS-1b","SYS-2", "SYS-3", "SYS-3a", "SYS-4", "SYS-5", "SYS-5b", "SYS-6", "SYS-6b", "SYS-9"]:`  
            - Check if the baseline hvac system type has a furnace or heat pump coil at the HVAC system level: `if sys_type in ["SYS-2", "SYS-3", "SYS-3a", "SYS-4", "SYS-9"]:`  
                - Get the over sizing factor associated with the heating coil: `heating_oversizing_factor = hvac.heating_system.oversizing_factor`     
            - Else: `Else: heating_oversizing_factor = "n/a"` 
            - Check if the baseline hvac system type has a DX cooling coil at the HVAC system level: `if sys_type in ["SYS-1", "SYS-1b", "SYS-2", "SYS-3", "SYS-3b", "SYS-4", "SYS-5", "SYS-5b", "SYS-6", "SYS-6b"]:`  
                - Get the over sizing factor associated with the cooling coil: `cooling_oversizing_factor = hvac.cooling_system.oversizing_factor`        
            - Else: `Else: cooling_oversizing_factor = "n/a"`   

            - **Rule Assertion:** 
            - Case 1: If heating_oversizing_factor = 25% and cooling_oversizing_factor = 15% then pass: `if heating_oversizing_factor == 25% AND cooling_oversizing_factor == 15%: outcome = "PASS"`  
            - Case 2: Else if heating_oversizing_factor = 25% and cooling_oversizing_factor = n/a then pass: `elif heating_oversizing_factor == 25% AND cooling_oversizing_factor == "n/a": outcome = "PASS"`  
            - Case 3: Else if cooling_oversizing_factor = 15% and heating_oversizing_factor = n/a then pass: `elif cooling_oversizing_factor == 15% AND heating_oversizing_factor == "n/a": outcome = "PASS"`  
            - Case 4: Else, fail: `Else: outcome = "Fail"`  



**Notes/Questions:**  
1. Sizing factor modeled identically across orientations will be checked by umbrella rule. 
2. Per dicussion with Mike R. and group rule applies to furnaces, heat pumps, and DX cooling coils.  


**[Back](_toc.md)**