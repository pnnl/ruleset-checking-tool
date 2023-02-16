
# Boiler - Rule 21-8  

**Rule ID:** 21-8  
**Rule Description:** When the baseline building requires boilers, (for baseline system type = 1,5,7,11 and 12),  HWST for the baseline building shall be reset using an outdoor air dry-bulb reset schedule. 180F at 20F OAT, 150Fat 50F OAT, ramped linerarly between 150F and 180F.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 21 Boiler  
**Schema Version:** 0.0.023  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMD is modeled with a boiler

**Manual Check:** Yes  
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

- Get all the heating loops connected to boilers in the baseline by creating heat_fluid_loops_set: `heat_fluid_loops_set = set()`
- iterate through all the boilers the building looking for heating fluid loops: `for boiler in B_RMI.boilers:`
  - add the boiler loop to the heat_fluid_loops_set: `heat_fluid_loops_set.add(boiler.loop)`
- iterate through each fluid loop: `for heating_fluid_loop in heat_fluid_loops_set:`

**Rule Assertion:**
-  
    - check the tempearture reset is outdoor air reset 180F at 20F and 150F at 50F: `if heating_fluid_loop.heating_design_and_control.temperature_reset_type == OUTDOOR_AIR_RESET`
    - `AND heating_fluid_loop.heating_design_and_control.loop_supply_temperature_at_outdoor_high == 150`
    - `AND heating_fluid_loop.heating_design_and_control.loop_supply_temperature_at_outdoor_low == 180`
    - `AND heating_fluid_loop.heating_design_and_control.outdoor_high_for_loop_supply_reset_temperature equals == 50`
    - `AND heating_fluid_loop.heating_design_and_control.outdoor_low_for_loop_supply_reset_temperature equals == 20:`
      - the rule passes: `PASS`
    - otherwise: `ELSE:`
      - the rule fails: `FAIL`


**[Back](../_toc.md)**
