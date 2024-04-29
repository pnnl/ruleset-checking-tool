
# Boiler - Rule 21-8  

**Rule ID:** 21-8  
**Rule Description:** When the baseline building requires boilers, (for baseline system type = 1,5,7,11 and 12),  HWST for the baseline building shall be reset using an outdoor air dry-bulb reset schedule. 180F at 20F OAT, 150Fat 50F OAT, ramped linerarly between 150F and 180F.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 21 Boiler  
**Schema Version:** 0.0.34  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMD is modeled with a boiler

**Manual Check:** Yes  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** 

1. get_hw_loop_zone_list_w_area

**Applicability Checks:**
- use the function get_hw_loop_zone_list_w_area to see if there are zone terminal units connected to hot water loops: `hw_loop_zone_list_w_area_dictionary = get_hw_loop_zone_list_w_area(B-RMD)`
- Get all the heating loops connected to boilers in the baseline by creating heat_fluid_loops_set: `boiler_fluid_loops_set = set()`
- iterate through all the boilers the building looking for heating fluid loops: `for boiler in B_RMI.boilers:`
  - check if the boiler loop is in the hw_loop_zone_list_w_area_dictionary: `if boiler.loop.id in hw_loop_zone_list_w_area_dictionary:`
    - add the boiler loop to the boiler_fluid_loops_set: `boiler_fluid_loops_set.add(boiler.loop)`
- Check if there are heating loops connected to boilers by checking the length of the boiler_fluid_loops_set: `if len(boiler_fluid_loops_set) > 0: CHECK RULE LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- iterate through each fluid loop: `for boiler_fluid_loop in boiler_fluid_loops_set:`

**Rule Assertion:**
-  
    - check the tempearture reset is outdoor air reset 180F at 20F and 150F at 50F: `if boiler_fluid_loop.heating_design_and_control.temperature_reset_type == OUTDOOR_AIR_RESET`
    - `AND boiler_fluid_loop.heating_design_and_control.loop_supply_temperature_at_outdoor_high == 150`
    - `AND boiler_fluid_loop.heating_design_and_control.loop_supply_temperature_at_outdoor_low == 180`
    - `AND boiler_fluid_loop.heating_design_and_control.outdoor_high_for_loop_supply_reset_temperature equals == 50`
    - `AND boiler_fluid_loop.heating_design_and_control.outdoor_low_for_loop_supply_reset_temperature equals == 20:`
      - the rule passes: `PASS`
    - otherwise: `ELSE:`
      - the rule fails: `FAIL`


**Questions:**  
1.  Does this rule apply to any boiler loop, or only those serving heating systems?
2.  if it applies only to boiler loops serving heating systemers, is there any 

**[Back](../_toc.md)**
