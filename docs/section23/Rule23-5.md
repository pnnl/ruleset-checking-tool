
# Airside System - Rule 23-5  

**Rule ID:** 23-5  
**Rule Description:** For baseline systems 6 and 8, Fans in parallel VAV fan-powered boxes shall be sized for 50% of the peak design primary air (from the VAV air-handling unit) flow rate and shall be modeled with 0.35 W/cfm fan power.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**Appendix G Section Reference:** Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-6, 8, 8a, 6b, 8b.  

**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:**  

1. get_baseline_system_types()
2. is_baseline_system_type()

**Applicability Checks:**  

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-6, 8, 8a, 6b, 8b, continue to rule logic: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-6", "SYS-8", "SYS-8A", "SYS-6B", "SYS-8B"]): CHECK_RULE_LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each zone in B_RMR: `for zone_b in B_RMR...zones:`

  - For each terminal in zone: `for terminal_b in zone_b.terminals:`

    - Get HVAC system serving terminal: `hvac_b = terminal_b.served_by_heating_ventilation_air_conditioning_systems`
  
      - Check if HVAC system is type 6, 8, 8a, 6b, 8b: `if any(is_baseline_system_type(hvac_b, sys_type) == TRUE for sys_type in ["SYS-6", "SYS-8", "SYS-8A", "SYS-6B", "SYS-8B"]):`

        **Rule Assertion:**

        - Case 1: For each terminal that is served by HVAC system that is Type-6, 8, 8a, 6b, 8b, if fan in parallel VAV-powered box is sized for 50% of the peak design primary air (from the VAV air-handling unit) flow rate (CFM) and is modeled with 0.35W/cfm fan power: `if ( terminal_b.fan.design_airflow == terminal_b.primary_airflow * 0.5 ) AND ( terminal_b.fan.design_electric_power == 0.35 * terminal_b.fan.design_airflow ): PASS`

        - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**

**Notes:**

1. Right now the RDS checks both terminal.secondary_airflow and fan.design_airflow to make sure that both is 50% of primary airflow. Please confirm this approach.
