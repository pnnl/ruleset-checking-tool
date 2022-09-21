# Section 19 - Rule 19-1  
**Schema Version:** 0.0.21  
**Mandatory Rule:** True  
**Rule ID:** 19-1   
**Rule Description:** HVAC system coil capacities for the baseline building design shall be based on sizing runs for each orientation and shall be oversized by 15% for cooling and 25% for heating.  
**Rule Assertion:** Options are Pass/Fail/Undetermined     
**Appendix G Section:** Section G3.1.2.2    
**90.1 Section Reference:** None  

**Data Lookup:** None  

**Evaluation Context:** Each HeatingVentilationAirConditioningSystem Data Group  

**Applicability Checks:** None  

**Function Calls:**  
1. get_baseline_system_types()  


## Rule Logic:  
- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`  
- For each hvac system in B_RMR: `for hvac in B_RMR...HeatingVentilationAirConditioningSystem:`  
    - Reset the is_undetermined boolean variable: `is_undetermined = False`   
    - Reset heating_oversizing_factor: `heating_oversizing_factor = ""`  
    - Reset cooling_oversizing_factor: `cooling_oversizing_factor = ""`  
    - Get baseline system type: `sys_type = list(baseline_hvac_system_dict.keys())[list(baseline_hvac_system_dict.values()).index(hvac.id)]`  
    - Check if the baseline hvac system type is not Sys 1a, 1c, 9b, or 10 as these are not able to be assessed and the outcome is undetermined: `if sys_type Not in ["SYS-1a", "SYS-1c", "SYS-9b", "SYS-10"]:`  
        - Check if the baseline hvac system type has a heating coil at the HVAC system level: `if sys_type in ["SYS-1", "SYS-1b", "SYS-2", "SYS-3", "SYS-3a", "SYS-3b", "SYS-3c", "SYS-4", "SYS-9", "SYS-11.1", "SYS-11.2", "SYS-11.2a", "SYS-11.1a", "SYS-11b", "SYS-11c", "SYS-12", "SYS-12a", "SYS-12b", "SYS-12c", "SYS-13", "SYS-13a"]:`  
            - Get the over sizing factor associated with the heating coil: `heating_oversizing_factor = hvac.heating_system.oversizing_factor`  
        - Else if the baseline hvac system type has a preheat coil at the HVAC system level: `elif sys_type in ["SYS-5", "SYS-5b", "SYS-6", "SYS-6b", "SYS-7", "SYS-7a", "SYS-7b", "SYS7c", "SYS-8", "SYS-8a", "SYS-8b", "SYS-8c"]:`  
            - Get the over sizing factor associated with the preheat coil: `heating_oversizing_factor = hvac.preheat_system.oversizing_factor`  
        - Check if the baseline hvac system type has a cooling coil at the HVAC system level: `if sys_type in ["SYS-1", "SYS-1b", "SYS-2", "SYS-3", "SYS-3a", "SYS-3b", "SYS-3c", "SYS-4", "SYS-5", "SYS-5b", "SYS-6", "SYS-6b", "SYS-7", "SYS-7a", "SYS-7b", "SYS7c", "SYS-8", "SYS-8a", "SYS-8b", "SYS-8c", "SYS-11.1", "SYS-11.2", "SYS-11.2a", "SYS-11.1a", "SYS-11b", "SYS-11c", "SYS-12", "SYS-12a", "SYS-12b", "SYS-12c", "SYS-13", "SYS-13a"]:`  
            - Get the over sizing factor associated with the cooling coil: `cooling_oversizing_factor = hvac.cooling_system.oversizing_factor`        
        - Else: `Else: cooling_oversizing_factor = "n/a"`   
    - Else, set is_undetermined boolean variable to True: `is_undetermined boolean variable = True`   
    
    - **Rule Assertion:** 
    - Case 1: If heating_oversizing_factor = 1.25 and cooling_oversizing_factor = 1.15 then pass: `if heating_oversizing_factor == 1.25 AND cooling_oversizing_factor == 1.15: outcome = "PASS"`  
    - Case 2: Else if heating_oversizing_factor = 1.25 and cooling_oversizing_factor = n/a then pass: `elif heating_oversizing_factor == 1.25 AND cooling_oversizing_factor == "n/a": outcome = "PASS"`  
    - Case 3: Else if is_undetermined = True then outcome is UNDETERMINED: `elif is_undetermined == TRUE: outcome = "UNDETERMINED" and raise_message "Conduct a manual check of the over sizing factors for <hvac.id>"`  
    - Case 4: Else, fail: `Else: outcome = "Fail"`  



**Notes/Questions:**  
1. Shall we split this into 2 rules that assess heating and cooling separately? Perhaps not needed as above appears to work fine. 
2. Systems 1a, 1c, 9b, and 10 cannot be assessed because coils are defined at the terminal. This does not appear to impact anything though.
3. We already check that the project is modeled by orientation in Rule 5-1. The check that the sizing factors are consistent across orientations will be an umbrella check. 
4. Shall I update this to only check the oversizing factor for furnaces, heat pumps, and DX cooling based on exchanges with Mike R at PNNL?  
5. What would we expect for a 25% oversizing factor? 1.25 or 25%?

**[Back](_toc.md)**