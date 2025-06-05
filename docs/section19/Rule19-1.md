# Section 19 - Rule 19-1  
**Schema Version:** 0.0.21  
**Mandatory Rule:** True  
**Rule ID:** 19-1   
**Rule Description:** HVAC system coil capacities for the baseline building design shall be oversized by 15% for cooling and 25% for heating.  
**Rule Assertion:** Options are Pass/Fail/NOT_APPLICABLE     
**Appendix G Section:** Section G3.1.2.2    
**90.1 Section Reference:** None  

**Data Lookup:** None  

**Evaluation Context:** Each HeatingVentilationAirConditioningSystem Data Group  

**Applicability Checks:** 

1. Applies to the baseline with furnaces, heat pumps, and/or DX cooling coils.  

**Function Calls:**  
1. is_hvac_sys_heating_type_furnace()
2. is_hvac_sys_heating_type_heat_pump()
3. is_hvac_sys_cooling_type_DX()  


## Rule Logic:  
**Applicability Check 1:**  Checks each HVAC system for applicability  (does it have a furnace, heatpump, and/or DX cooling) otherwise NOT_APPLICABLE
- For each hvac system in B_RMR: `for hvac in B_RMR...HeatingVentilationAirConditioningSystem:`    
    - Reset heating_oversizing_factor (whatever is the best way to do this): `heating_oversizing_factor = ""`  
    - Reset cooling_oversizing_factor (whatever is the best way to do this): `cooling_oversizing_factor = ""`  
    - Reset heating_oversizing_applicable boolean: `heating_oversizing_applicable = TRUE`  
    - Reset cooling_oversizing_applicable boolean: `cooling_oversizing_applicable = TRUE`     
    - Check if the baseline system type has a furnace, heat pump, and/or DX cooling coil, ELSE then rule outcome for this HVAC system is NOT_APPLICABLE: `if is_hvac_sys_heating_type_furnace(B_RMR, hvac.id) == TRUE OR is_hvac_sys_heating_type_heat_pump(B_RMR, hvac.id) ==  TRUE OR is_hvac_sys_cooling_type_DX(B_RMR, hvac.id) == TRUE:`   
        - Check if the baseline hvac system type has a furnace or heat pump coil at the HVAC system level: `if is_hvac_sys_heating_type_furnace(B_RMR, hvac.id) == TRUE OR is_hvac_sys_heating_type_heat_pump(B_RMR, hvac.id) ==  TRUE:`  
            - Get the over sizing factor associated with the heating coil: `heating_oversizing_factor = hvac.heating_system.oversizing_factor`     
        - Else: `Else: heating_oversizing_applicable = FALSE` 
        - Check if the baseline hvac system type has a DX cooling coil at the HVAC system level: `if is_hvac_sys_cooling_type_DX(B_RMR, hvac.id) == TRUE:`  
            - Get the over sizing factor associated with the cooling coil: `cooling_oversizing_factor = hvac.cooling_system.oversizing_factor`        
        - Else: `Else: cooling_oversizing_applicable = FALSE`   

        - **Rule Assertion:** 
        - Case 1: If heating_oversizing_factor = 25% and cooling_oversizing_factor = 15% and hvac.heating_system.is_autosized ==  TRUE AND hvac.cooling_system.is_autosized ==  TRUE  then pass: `if heating_oversizing_factor == 25% AND cooling_oversizing_factor == 15% AND hvac.heating_system.is_autosized ==  TRUE AND hvac.cooling_system.is_autosized ==  TRUE: outcome = "PASS"`  
        - Case 2: Else if heating_oversizing_factor = 25% and hvac.heating_system.is_autosized ==  TRUE and cooling_oversizing_applicable == FALSE then pass: `elif heating_oversizing_factor == 25% AND hvac.heating_system.is_autosized ==  TRUE AND cooling_oversizing_applicable == FALSE: outcome = "PASS"`  
        - Case 3: Else if cooling_oversizing_factor = 15% and hvac.cooling_system.is_autosized ==  TRUE and heating_oversizing_applicable ==  FALSE then pass: `elif cooling_oversizing_factor == 15% AND hvac.cooling_system.is_autosized ==  TRUE AND heating_oversizing_applicable ==  FALSE: outcome = "PASS"`  
        - Case 4: Else, fail: `Else: outcome = "Fail"`  



**Notes/Questions:**  
1. Sizing factor modeled identically across orientations will be checked by umbrella rule. 
2. Per discussion with Mike R. and group rule applies to furnaces, heat pumps, and DX cooling coils.  


**[Back](../_toc.md)**