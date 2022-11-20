
# Airside System - Rule 23-5  

**Schema Version:** 0.0.23  
**Mandatory Rule:** True  
**Rule ID:** 23-5  
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


**Applicability Checks:**  

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMI)`

  - Check if B-RMI is modeled with at least one air-side system that is Type-6, 8, 8a, 6b, 8b, continue to rule logic: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-6", "SYS-8", "SYS-8A", "SYS-6B", "SYS-8B"]): CHECK_RULE_LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  
- Create a list of the ids of the hvac systems that are one of the targeted system types: `eligible_systems = []`
- For each baseline system type in the baseline_hvac_system_dict: `for baseline_system_type in baseline_hvac_system_dict:`
  - check if the baseline_system_type is one of 6, 8, 8a, 6b, 8b: `if baseline_system_type in ["SYS-6", "SYS-8", "SYS-8A", "SYS-6B", "SYS-8B"]:`
    - add the hvac_ids for this system type to the list of eligible_systems: `eligible_systems += baseline_hvac_system_dict[baseline_system_type]`


- For each zone in B_RMR: `for zone_b in B_RMI...zones:`

  - For each terminal in zone: `for terminal_b in zone_b.terminals:`

    - Get HVAC system serving terminal: `hvac_b = terminal_b.served_by_heating_ventilating_air_conditioning_system`
  
      - Check if HVAC system is type 6, 8, 8a, 6b, 8b: `if hvac_b in eligible_systems:`

        **Rule Assertion:**

        - Case 1: For each terminal that is served by HVAC system that is Type-6, 8, 8a, 6b, 8b, if fan in parallel VAV-powered box is sized for 50% of the peak design primary air (from the VAV air-handling unit) flow rate (CFM) and is modeled with 0.35W/cfm fan power: `if ( terminal_b.fan.design_airflow == terminal_b.primary_airflow * 0.5 ) AND ( terminal_b.fan.design_electric_power == 0.35 * terminal_b.fan.design_airflow ): PASS`

        - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
