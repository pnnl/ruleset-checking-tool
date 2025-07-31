
# Airside System - Rule 23-6  

**Schema Version:** 0.0.23  
**Mandatory Rule:** True
**Rule ID:** 23-6  
**Rule Description:** For baseline systems 6 and 8, Fans in parallel VAV fan-powered boxes shall be sized for 50% of the peak design primary air (from the VAV air-handling unit) flow rate and shall be modeled with 0.35 W/cfm fan power.  
**Rule Assertion:** B-RMD = Expected Value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)  
**Data Lookup:** None  
**Evaluation Context:** HVAC System  

**Applicability Checks:**  

1. HVAC System Type is either System 6 or System 8 (or their variants)

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()
3. get_dict_of_zones_and_terminal_units_served_by_hvac_sys() 
4. baseline_system_type_compare() 


**Applicability Checks:**  

- Create a list of the applicable system types: `APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_6, HVAC_SYS.SYS_8]`
- Get the baseline HVAC system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMD)`
- Loop through the applicable system types: `for system_type in APPLICABLE_SYS_TYPES:`
    - Loop through the baseline system types dict to check the system types of the baseline systems: `for modeled_system_type in baseline_system_types_dict:`
        - Determine whether the baseline system type is either System 6 or System 8: `if((baseline_system_type_compare(system_type, modeled_system_type, false)):`
            - If it is, the rule applies to this system: `CONTINUE TO RULE LOGIC`
        - Otherwise, the rule not applicable to this system: `else: NOT_APPLICABLE`

## Rule Logic:
- Get a dictionary of HVAC systems, their zones and terminal units: `dict_of_zones_and_terminal_units_served_by_hvac_sys = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(B_RMD)`
- For each HVAC system id in the dictionary: `for hvac_b_id in dict_of_zones_and_terminal_units_served_by_hvac_sys:`  
    - For each terminal served by the HVAC system: `for terminal_b_id in dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_b_id]["Terminal_Unit_List"]:`  
        - Get the terminal object: `terminal_b = get_component_by_id(B_RMD, Terminal, terminal_b_id)`
        - Get the fan object: `fan_b = terminal_b["fan"]`  
        - Calculate the expected fan design airflow (50% of primary airflow): `expected_design_airflow = terminal_b["primary_airflow"] * 0.5`  
        - Calculate the expected fan power: `expected_fan_power = 0.35 * expected_design_airflow`  
        - Get the actual fan power: `actual_fan_power = get_fan_object_electric_power(B_RMD, fan_b)`  
        - Check if the terminal meets both sizing and power conditions: `is_compliant = (fan_b["design_airflow"] == expected_design_airflow and actual_fan_power == expected_fan_power)`  
        - Record the result keyed by terminal ID: `terminal_results[terminal_b_id] = is_compliant`
  
**Rule Assertion:**

- Case 1: Every terminal that is served by HVAC system has a fan in parallel VAV-powered box sized for 50% of the peak design primary air (from the VAV air-handling unit) flow rate (CFM) and is modeled with 0.35W/cfm fan power: `if all(terminal_results.values()): PASS`

- Case 2: Else: `else: FAIL`
        
**Notes:**
1. Updated the Rule ID from 23-5 to 23-6 on 11/28/2022


**[Back](../_toc.md)**
