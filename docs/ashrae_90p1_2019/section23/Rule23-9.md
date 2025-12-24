
# Airside System - Rule 23-9 

**Schema Version:** 0.0.34  
**Mandatory Rule:** True  
**Rule ID:** 23-9  
**Rule Description:** System 11 Minimum volume setpoint shall be the largest of 50% of the maximum design airflow rate and the minimum ventilation airflow rate or the airflow required to comply with codes or accredidation standards.      
**Rule Assertion:** B_RMD = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Exception to G3.1.3.13  
**Data Lookup:** None  
**Evaluation Context:** HVAC System  

**Applicability Checks:**  

1. B_RMD is modeled with at least one air-side system that is Type-11.  

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()
3. get_dict_of_zones_and_terminal_units_served_by_hvac_sys()

**Applicability Checks:**
- Get the system types dict for the baseline model: `baseline_system_types_dict = get_baseline_system_types(B_RMD)`
- Invert the dictionary to map each system ID to its system type: `hvac_id_to_sys_type = {hvac_system_id: system_type for system_type, hvac_ids in baseline_system_types_dict.items() for hvac_system_id in hvac_ids}`
- For each baseline HVAC system: `for baseline_hvac_system in B_RMD...heating_ventilating_air_conditioning_systems:`
    - Get the HVAC system ID: `hvac_system_id = baseline_hvac_system["id"]`
    - Get the HVAC system type: `hvac_system_type = hvac_id_to_sys_type[hvac_system_id]`
    - Determine whether the baseline system type is System 11: `if((baseline_system_type_compare(hvac_system_type, HVAC_SYS.SYS_11, False)):`
        - If it is System 11, the rule applies to the system: `CONTINUE TO RULE LOGIC`
    - Otherwise, the rule not applicable to the system : `else: NOT_APPLICABLE`
 
**Rule Logic:**  

- Get the HVAC system: `hvac_system = get_object_by_id(hvac_system_id)`  
- Get the fan system: `fan_system = hvac_system["fan_system"]`  
- Get the fan system minimum volume flow rate: `min_volume_flowrate = fan_system["minimum_airflow"]`  
- Get the fan system minimum ventilation air flow rate: `min_ventilation_flowrate = fan_system["minimum_outdoor_airflow"]`  
- Create a variable for the maximum volume flow rate: `maximum_supply_flowrate = 0.0`  
- For each supply fan in the system: `for supply_fan in fan_system["supply_fans"]:`  
    - Add the supply fan design_airflow to the maximum_supply_flowrate: `maximum_supply_flowrate += supply_fan["design_airflow"]`  

- Determine the minimum volume flow rate provided by the proposed model to the single zone served by this system. System-11 is a single-zone system by definition. This step checks that the minimum airflow provided meets or exceeds the rate required by local standards. It is assumed that the proposed model meets local standard requirements.

- Get a list of zones and terminal units served by this HVAC system: `zones_and_terminals_dict = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(B_RMD)[hvac_system_id]`
- Get the ID of the zone served by this HVAC system: `zone_id = zones_and_terminals_dict["ZONE_LIST"][0]`
- Get the zone in the proposed model: `zone_p = get_component_by_id(P_RMD, Zone, zone_id)`
- Initialize a list of 8760 hourly values to accumulate the total minimum volume flow rate of all terminals in the proposed zone: `minimum_volume_list_p = [0.0] * 8760`

- For each terminal in the proposed zone: `for terminal_p in zone_p["terminals"]:`  
    - Get the HVAC system associated with the terminal: `hvac_p = terminal_p["served_by_heating_ventilating_air_conditioning_system"]`  
    - Get the fan system: `fan_system_p = hvac_p["fan_system"]`  
    - Get the referenced operating schedule's hourly values: `operation_schedule_hourly_values_p = get_component_by_id(P_RMD, Schedule, fan_system_p["operating_schedule"])["hourly_values"]`  
    - Get the terminal minimum volume flowrate: `min_volume_p = terminal_p["minimum_airflow"]`  
    - For each hour of the year: `for hour in range(8760):`  
        - Accumulate the terminal's contribution to the zone's total minimum flowrate: `minimum_volume_list_p[hour] += min_volume_p * operation_schedule_hourly_values_p[hour]`  

- Calculate the effective proposed minimum volume flowrate by taking the maximum hourly total: `effective_min_volume_p = max(minimum_volume_list_p)`
- Define a reference minimum based on ventilation and supply sizing: `reference_minimum = max(min_ventilation_flowrate, 0.5 * maximum_supply_flowrate)`

**Rule Assertion:**

- Case 1: If the fan system minimum airflow equals the reference, and the proposed effective airflow is less than or equal to the reference → PASS: `if min_volume_flowrate == reference_minimum and effective_min_volume_p <= reference_minimum: PASS`

- Case 2: Else if the fan system minimum airflow is less than the maximum of (min_ventilation_flowrate, 0.5 * maximum_supply_flowrate, effective_min_volume_p) → FAIL: `elif min_volume_flowrate < max(min_ventilation_flowrate, 0.5 * maximum_supply_flowrate, effective_min_volume_p): FAIL`

- Case 3: Else if the proposed effective airflow is greater than the reference → UNDETERMINED with note: `elif effective_min_volume_p > reference_minimum: UNDETERMINED; note = "The airflow provided in the proposed model is greater than the maximum of the minimum ventilation flowrate and 50% of the maximum supply flowrate. We cannot determine whether your minimum volume flowrate meets the minimum airflow required to comply with codes or accreditation standards."`

- Case 4: Else all other cases → FAIL: `else: FAIL`


**Notes:**

**[Back](../_toc.md)**
