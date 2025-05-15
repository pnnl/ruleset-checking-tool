
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
 
  **Rule Assertion:**  
  
    - Case 1: the minimum volume flow rate is equal to the maximum of the min_ventilation_flowrate and 50% of the maximum_supply_flowrate - return PASS with a note: `if min_volume_flowrate == max(min_ventilation_flowrate, 0.5 * maximum_supply_flowrate): PASS; note = "The minimum volume flowrate is equal to the maximum of the minimum ventilation flowrate and 50% of the maximum supply flow rate.  If any airflow required to comply with codes or accredidation standards is MORE than this value, the minimum volume airflow should be set to this value.  We are not able to determine the airflow required to comply with codes or accreditation standards at this time, please double check that there are no additional codes or accreditation standards in regards to airflow." `  
    
    - Case 2: the minimum volume flow rate is greater than the maximum of the min_ventilation_flowrate and 50% of the maximum_supply_flowrate - return UNDETERMINED with a note: `elif min_volume_flowrate > max(min_ventilation_flowrate, 0.5 * maximum_supply_flowrate): UNDETERMINED; note = "The minimum volume flowrate is greater than the maximum of the minimum ventilation flowrate and 50% of the maximum supply flow rate.  This is correct IF the minimum volume flowrate is equal to any airflow required to comply with codes or accredidation standards, the system passes, otherwise it fails.  We are not able to determine the airflow required to comply with codes or accreditation standards at this time." `  
    
    - Case 3: all other cases, the rule fails: `else: FAIL`


**Notes:**

**[Back](../_toc.md)**
