
# Airside System - Rule 23-3  

**Schema Version:** 0.0.39  
**Mandatory Rule:** True  
**Rule ID:** 23-3  
**Rule Description:** System 5, 6, 7 and 8 minimum volume setpoint shall be 30% of zone peak airflow, minimum outdoor airflow, or rate required to comply with minium accreditation standards whichever is larger.  
**Rule Assertion:** B-RMD = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Section G3.1.3.13 VAV Minimum Flow Set Points (Systems 5 and 7) and Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)  
**Data Lookup:** None  
**Evaluation Context:**  
**Applicability Checks:**  

1. B-RMD is modeled with at least one air-side system that is Type-5, 7, 7a, 5b, 7b, 7c, 6, 8, 8a, 6b, 8b.

**Function Calls:**  

1. get_baseline_system_types()
2. is_baseline_system_type()
3. baseline_system_type_compare()

**Applicability Checks:**  
- create a list of the target system types: `target_system_types = [HVAC_SYS.SYS_5,HVAC_SYS.SYS_6,HVAC_SYS.SYS_7,HVAC_SYS.SYS_8]`
- Get B-RMD system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMD)`

  - Check if B-RMD is modeled with at least one air-side system that is Type-5, 7, 7a, 5b, 7b, 7c, continue to rule logic: `if any(baseline_system_type_compare(system_type, target_sys_type, false) for system_type in baseline_hvac_system_dict.keys() for target_system_type in target_system_types): CHECK RULE LOGIC`

  - Else, rule is not applicable to B-RMD: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- create a list of eligible hvac systems: `eligible_hvac_system_ids = []`

- For each hvac system type in the baseline_hvac_system_dict: `for baseline_system_type in baseline_hvac_system_dict:`
  - check if it is one of the applicable systems (5, 6, 7, 8): `if any(baseline_system_type_compare(baseline_system_type, target_system_type, false) for target_system_type in target_system_types):`
    - add the ids to the list of eligible systems: `eligible_hvac_system_ids = eligible_hvac_system_ids + baseline_hvac_system_dict[baseline_system_type]`

- For each zone in B_RMD: `for zone_b in B_RMD...zones:`

  - For each terminal in zone: `for terminal_b in zone_b.terminals:`

    - Get HVAC system serving terminal: `hvac_b = terminal_b.served_by_heating_ventilating_air_conditioning_systems`
  
      - Check if HVAC system is one of the eligible systems: `if hvac_b.id in eligible_hvac_system_ids:`
        
        - get the minimum volume flow rate of the proposed terminal for the same zone.  This is to do the 3rd check - that the minimum airflow is greater than the rate required to comply with local standards.  It is assumed that the proposed model meets the minimum requirements of local standards.  First get the zone in the proposed model: `zone_p = get_component_by_id(P_RMD, Zone, zone_b.id)`
        - create a variable to hold the total minimum volume flow rate of all terminals in the proposed zone.  This will be an array of values, one for each hour of the year.  We will sum the minimum volume flowrate for each terminal by the availability of the terminal to take into account cases where the proposed zone has multiple terminals that do not operate at the same time: `minimum_volume_list_p = []`
        - look at each terminal in the proposed zone: `for terminal_p in zone_p.terminals:`
          - get the HVAC system associated with the terminal: `hvac_p = terminal_p.served_by_heating_ventilating_air_conditioning_system`
          - get the fan system: `fan_system_p = hvac_p.fan_system`
          - get the operation schedule hourly values: `operation_schedule_hourly_values_p = fan_system_p.operating_schedule.hourly_values`
          - get the terminal minimum volume flowrate: `min_volume_p = terminal_p.minimum_airflow`
          - multiply each value in the hourly schedule by the minimum airflow rate, and append this to the list of minimum volume flowrates: `minimum_volume_list_p.append([i * min_volume_p for i in operation_schedule_hourly_values_p]`
        - sum all of the values for each hour, so that the resulting list is a list of the sum of minimum flowrates across all terminals each hour of the year: `min_volume_flow_tot_p = [sum(values) for values in zip(*minimum_volume_list_p)]`
        - find the minimum non-zero value in the list: `min_volume_p = min(filter(lambda x: x != 0, min_volume_flow_tot_p))`

        **Rule Assertion:**    

        - Case 1: For each terminal that is served by HVAC system that is Type-5, 7, 7a, 5b, 7b, 7c, 6, 8, 8a, 6b, 8b, if minimum volume setpoint is equal to the maximum of: 30% of peak primary design airflow, the rate required for minimum outside air, or the proposed minimum volume airlfow, PASS: `if terminal_b.minimum_airflow == MAX(terminal_b.primary_airflow * 0.3, terminal_b.minimum_outdoor_airflow, minimum_volume_p): PASS`
       
        - Case 2: Else, if the minimum volume setpoint is equal to the maximum of 30% of peak primary design airflow, the rate required for minimum outside air, then UNDETERMINED with a note.  Due to the last check, this case indicates that the minimum volume flow is less than the proposed minimum airflow for the same zone.  Indicate to the AHJ to check if minimum airlfow in the baseline complies with local standards: `elif terminal_b.minimum_airflow == MAX(terminal_b.primary_airflow * 0.3, terminal_b.minimum_outdoor_airflow): UNDETERMINED; note = "The minimum volume flowrate is equal to the maximum of 30% of the terminal primary airflow rate and the terminal minimum outdoor airflow, but it is less than the minimum airflow in the proposed design.  Check that the baseline minimum airlfow is sufficient to comply with accredidation standards."`

        - Case 2: Else, all other cases: `else: FAIL`

**Notes:**
1. Updated the Rule ID from 23-2 to 23-3 on 11/28/2022


**[Back](../_toc.md)**
