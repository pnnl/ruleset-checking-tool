
# Airside System - Rule 23-9 

**Schema Version:** 0.0.34  
**Mandatory Rule:** True  
**Rule ID:** 23-9  
**Rule Description:** System 11 Minimum volume setpoint shall be the largest of 50% of the maximum design airflow rate, the minimum ventilation airflow rate or the airflow required to comply with codes or accredidation standards.    
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Exception to G3.1.3.13  
**Data Lookup:** None  
**Evaluation Context:** HVAC System  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-11.  

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()
3. get_dict_of_zones_and_terminal_units_served_by_hvac_sys()

**Applicability Checks:**  
- create a list of the target system types: `APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_11]`
- Get B-RMR system types: `baseline_system_types_dict = get_baseline_system_types(B-RMR)`

- loop through the applicable system types: `for target_sys_type in APPLICABLE_SYS_TYPES:`
    - and loop through the baseline_system_types_dict to check the system types of the baseline systems: `for system_type in baseline_system_types_dict:`
        - do baseline_system_type_compare to determine whether the baseline_system_type is the applicable_system_type: `if((baseline_system_type_compare(system_type, target_sys_type, false)):`
            - the systems in the list: baseline_system_types_dict[system_type] are sys-11 - loop through the list of systems: `for hvac_system_id in baseline_system_types_dict[system_type]:`
            - `CONTINUE TO RULE LOGIC`
            - otherwise, rule not applicable: `else: RULE_NOT_APPLICABLE`
 
**Rule Logic:**  

    - get the hvac system: `hvac_system = get_object_by_id(hvac_system_id)`  
    - get the fan system: `fan_system = hvac_system.fan_system`  
    - get the fan system minimum volume flow rate: `min_volume_flowrate = fan_system.minimum_airflow`  
    - get the fan system minimum ventilation air flow rate: `min_ventilation_flowrate = fan_system.minimum_outdoor_airflow`  
    - create a variable for the maximum volume flow rate: `maximum_supply_flowrate = 0`  
    - loop through each supply fan: `for supply_fan in fan_system.supply_fans:`  
        -- add the supply fan design_airflow to the maximum_supply_flowrate: `maximum_supply_flowrate += supply_fan.design_airflow`  

    - get the minimum volume flow rate of the proposed terminal for the same zone.  We only need to look at one zone because System-11 is a single-zone system by definition.  This is to do the 3rd check - that the minimum airflow is greater than the rate required to comply with local standards.  It is assumed that the proposed model meets the minimum requirements of local standards.  
    - use get_dict_of_zones_and_terminal_units_served_by_hvac_sys to get a list of zones and terminal units served by this HVAC system: `zones_and_terminals_dict = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(B_RMD)[hvac_system_id]`
    - get the id of the zone served by this HVAC system - there should only be one zone because System-11 is, by definition, a single zone system: `zone_id = zones_and_terminals_dict["ZONE_LIST"][0]`
    - get the zone in the proposed model: `zone_p = get_component_by_id(P_RMD, Zone, zone_id)`
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
  
    - Case 1: the minimum volume flow rate is equal to the maximum of the min_ventilation_flowrate, 50% of the maximum_supply_flowrate and the minimum supply air flowrate in the proposed model: PASS: `if min_volume_flowrate == max(min_ventilation_flowrate, 0.5 * maximum_supply_flowrate, min_volume_p): PASS`

    - Case 2: Else the minimum volume flow rate is equal to the maximum of the min_ventilation_flowrate and 50% of the maximum_supply_flowrate.  Due to the previous check, we know that the minimum volume flow rate is less than the proposed minimum volume flow: UNDETERMINED with note: `if min_volume_flowrate == max(min_ventilation_flowrate, 0.5 * maximum_supply_flowrate): UNDETERMINED; note = "The minimum volume flowrate is equal to the maximum of the minimum ventilation flowrate and 50% of the maximum supply flow rate, however it is less than the minimum volume flowrate in the proposed model.  Please double check that there are no additional codes or accreditation standards in regards to airflow." `  
    
    - Case 3: all other cases, the rule fails: `else: FAIL`


**Notes:**

**[Back](../_toc.md)**
