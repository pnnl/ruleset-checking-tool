# Airside System - Rule 23-8  

 **Schema Version:** 0.0.23  
 **Mandatory Rule:** True  
 **Rule ID:** 23-10  
 **Rule Description:** System 5-8 and 11 - part load VAV fan power shall be modeled using either method 1 or 2 in Table G3.1.3.15. This rule will only validate data points from Method-1 Part-load Fan Power Data. However, both methods are equivalent. When modeling inputs are based on Method 2, values should be converted to Method 1 when writing to RMD.    
 **Rule Assertion:** B-RMR = expected value  
 **Appendix G Section:** Section 23 Air-side  
 **90.1 Section Reference:** Section G3.1.3.15 VAV Fan Part-Load Performance (Systems 5 through 8 and 11)  
 **Data Lookup:** Table G3.1.3.15  
 **Evaluation Context:** Building  

 **Applicability Checks:**  

 1. B-RMD is modeled with at least one air-side system that is Type-5, 6, 7, 8, 11.1, 11.2, 7a, 8a, 11.1a, 11.2a, 5b, 6b, 7b, 8b, 11.1b, 7c, 11.1c.  

 **Function Calls:**  

 1. get_baseline_system_types()  
 2. is_baseline_system_type()
 3. baseline_system_type_compare()

 **Applicability Checks:**  
 - create a list of the target system types: `target_system_types = [HVAC_SYS.SYS_5,HVAC_SYS.SYS_6,HVAC_SYS.SYS_7,HVAC_SYS.SYS-8,HVAC_SYS.SYS_11_1,HVAC_SYS.SYS_11_2]`
 - Get B-RMD system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMD)`

   - Check if B-RMD is modeled with at least one air-side system that is Type-5, 6, 7, 8, 11.1, 11.2, 7a, 8a, 11.1a, 11.2a, 5b, 6b, 7b, 8b, 11.1b, 7c, 11.1c, continue to rule logic: `if any(baseline_system_type_compare(system_type, target_sys_type, false) for system_type in baseline_system_types_dict.keys() for applicable_sys_type in APPLICABLE_SYS_TYPES): CHECK RULE LOGIC`

   - Else, rule is not applicable to B-RMD: `else: RULE_NOT_APPLICABLE`

 ## Rule Logic:  
 - create a list of eligible hvac systems: `eligible_hvac_system_ids = []`

- For each hvac system type in the baseline_hvac_system_dict: `for baseline_system_type in baseline_hvac_system_dict:`

  - check if it is one of the applicable systems (5-8, or 11): `if any(baseline_system_type_compare(baseline_system_type, target_system_type, false) for target_system_type in target_system_types):`
    - add the ids to the list of eligible systems: `eligible_hvac_system_ids = eligible_hvac_system_ids + baseline_hvac_system_dict[baseline_system_type]`    

 - For each hvac system type in the baseline_hvac_system_dict: `for supply_fan_b in B_RMI...heating_ventilating_air_conditioning_systems:`

   - Get fan system serving HVAC system: `fan_system_b = hvac_b.fan_system`

   - do the check for each fan in the fan system: `for supply_fan_b in fan_system_b.supply_fans:`

   - Get supply fan airflow,  supply fan power, and output_validation_points: `supply_airflow_b = supply_fan_b.design_airflow, design_power_b = supply_fan_b.design_electric_power, output_validation_points_b = supply_fan_b.output_validation_points`

   - Create target validation points for supply fan: `target_validation_points = [[0,0], [0.1*supply_airflow_b, 0.03*design_power_b], [0.2*supply_airflow_b, 0.07*design_power_b], [0.3*supply_airflow_b, 0.13*design_power_b], [0.4*supply_airflow_b, 0.21*design_power_b], [0.5*supply_airflow_b, 0.30*design_power_b], [0.6*supply_airflow_b, 0.41*design_power_b], [0.7*supply_airflow_b, 0.54*design_power_b], [0.8*supply_airflow_b, 0.68*design_power_b], [0.9*supply_airflow_b, 0.83*design_power_b], [supply_airflow_b, design_power_b]]`
   
   - Create output validation points for supply fan: `output_validation_points = [[output[airflow], output[result]] for output in output_validation_points_b]` 
    
     **Rule Assertion:**
     - Case 1: If all the supply fans in the fan_system meet the requirements of being modeled as part-load VAV per Table G3.1.3.15: `if fan_b.output_validation_points == target_validation_points: PASS`

     - Case 2: Else: `else: FAIL`