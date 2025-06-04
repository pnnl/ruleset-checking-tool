
# Airside System - Rule 23-6  

**Schema Version:** 0.0.23  
**Mandatory Rule:** True
**Rule ID:** 23-6  
**Rule Description:** For baseline systems 6 and 8, Fans in parallel VAV fan-powered boxes shall be sized for 50% of the peak design primary air (from the VAV air-handling unit) flow rate and shall be modeled with 0.35 W/cfm fan power.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)  
**Data Lookup:** None  
**Evaluation Context:** Building  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-6, 8, 8a, 6b, 8b.  

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()
3. get_dict_of_zones_and_terminal_units_served_by_hvac_sys() 
4. baseline_system_type_compare() 


**Applicability Checks:**  

- create a list of the target system types: target_system_types = [HVAC_SYS.SYS_6,HVAC_SYS.SYS_8]
- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMI)`

  - Check if B-RMI is modeled with at least one air-side system that is Type-6, 8, 8a, 6b, 8b, continue to rule logic: `if any(baseline_system_type_compare(system_type, target_sys_type, false) for system_type in baseline_hvac_system_dict.keys() for target_system_type in target_system_types): CHECK RULE LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  
- Create a list of the ids of the hvac systems that are one of the targeted system types: `eligible_systems = []`
- For each baseline system type in the baseline_hvac_system_dict: `for baseline_system_type in baseline_hvac_system_dict:`
  - check if the baseline_system_type is one of 6, 8, 8a, 6b, 8b: `if any(baseline_system_type_compare(baseline_system_type, target_system_type, false) for target_system_type in target_system_types):`
    - add the hvac_ids for this system type to the list of eligible_systems: `eligible_systems += baseline_hvac_system_dict[baseline_system_type]`


- get a dictionary of hvac systems, their zones and terminal units using the function get_dict_of_zones_and_terminal_units_served_by_hvac_sys : `dict_of_zones_and_terminal_units_served_by_hvac_sys = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(B_RMI)`
- loop through the hvac systems in the dictionary: `for hvac_b_id in dict_of_zones_and_terminal_units_served_by_hvac_sys:`
  - we do the rule check for each terminal: `for terminal_b_id in dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_b_id]["Terminal_Unit_List"]:`
    - get the terminal unit associated with the id: `terminal_b = match_data_element(B_RMI,Terminal,terminal_b_id)`

**Rule Assertion:**

      - Case 1: For each terminal that is served by HVAC system that is Type-6, 8, 8a, 6b, 8b, if fan in parallel VAV-powered box is sized for 50% of the peak design primary air (from the VAV air-handling unit) flow rate (CFM) and is modeled with 0.35W/cfm fan power: `if ( terminal_b.fan.design_airflow == terminal_b.primary_airflow * 0.5 ) AND ( get_fan_object_electric_power(B_RMD, terminal_b.fan.design_electric_power) == 0.35 * terminal_b.fan.design_airflow ): PASS`

      - Case 2: Else: `else: FAIL`
        
**Notes:**
1. Updated the Rule ID from 23-5 to 23-6 on 11/28/2022


**[Back](../_toc.md)**
