
# Airside System - Rule 23-1 

**Schema Version:** 0.0.34  
**Mandatory Rule:** TRUE   
**Rule ID:** 23-1  
**Rule Description:** System 2 and 4 - Electric air-source heat pumps shall be modeled with electric auxiliary heat and an outdoor air thermostat. The systems shall be controlled to energize auxiliary heat only when the outdoor air temperature is less than 40°F. The air-source heat pump shall be modeled to continue to operate while auxiliary heat is energized.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** G3.1.3.1 Heat Pumps (Systems 2 and 4)  
**Data Lookup:** None  
**Evaluation Context:** HVAC System  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-2, or 4  

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()
3. get_component_by_id()

**Applicability Checks:**  
- create a list of the target system types: `APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_2,HVAC_SYS.SYS_4]`
- Get B-RMR system types: `baseline_system_types_dict = get_baseline_system_types(B-RMR)`

- loop through the applicable system types: `for target_sys_type in APPLICABLE_SYS_TYPES:`
    - and loop through the baseline_system_types_dict to check the system types of the baseline systems: `for system_type in baseline_system_types_dict:`
        - do baseline_system_type_compare to determine whether the baseline_system_type is the applicable_system_type: `if((baseline_system_type_compare(system_type, target_sys_type, false)):`
            - the systems in the list: baseline_system_types_dict[system_type] are sys-2 or 4 - loop through the list of systems: `for hvac_system_id in baseline_system_types_dict[system_type]:`
            - `CONTINUE TO RULE LOGIC`
            - otherwise, rule not applicable: `else: RULE_NOT_APPLICABLE`
         
**Rule Logic:**  
- get the hvac system from the hvac_system_id: `hvac_system = get_component_by_id(hvac_system_id)`
- get the heating system: `heating_system = hvac_system.heating_system`
- get the heatpump_low_shutoff_temperature = `heatpump_low_shutoff = heating_system.heatpump_low_shutoff_temperature`
- get the auxiliary heat high temperature shutoff = 'aux_heat_high_temp_shutoff = heating_system.heatpump_auxilliary_heat_high_shutoff_temperature`
- get the auxiliary heat energy source: `aux_heat_energy_source = heatpump_auxilliary_heat_type`

**Rule Assertion:**
- Case 1: The auxiliary heat high temperature shutoff is greater than 40F, or the auxiliary heat energy source is anything other than electricity - FAIL: `if (aux_heat_high_temp_shutoff > 40) or (aux_heat_energy_source != "ELECTRIC_RESISTANCE"): FAIL`
- Case 2: The system type is 2 and the heatpump_low_shutoff is <= 17F, PASS: `if system_type == HVAC_SYS.2: if heatpump_low_shutoff <= 17: PASS`
- Case 3: The system type is 2 and the heatpump_low_shutoff is >25F, FAIL, provide a message: `elif system_type == HVAC_SYS.2 && heatpump_low_shutoff > 25:`
    - `FAIL; note = "Fail because low temperature heat pump shutoff is above 25F for system 2. The modeled low temperature heat pump shutoff value is " + heatpump_low_shutoff + "."`
- Case 4: the system type is 2 and the heatpump_low_shutoff is between 17F and 25: UNDETERMINED; provide a message: `else: UNDETERMINED; note = "Undetermined because the low temperature shutoff is between 17F and 25F for System Type 2.  Check with the rating authority to ensure correct shutoff temperature.  Low shutoff temperature is currently modeled at: " heatpump_low_shutoff = "."`
- Case 5: the system type is 4 (we already know it's 4, because we've checked the 3 SYS 2 cases above), and the low shutoff temperature is <=10F: PASS: `if heatpump_low_shutoff <= 10F: PASS`
- Case 6: anything else, FAIL: `ELSE: Fail`

**Notes:**

**[Back](../_toc.md)**
