
# Airside System - Rule 23-8  

**Schema Version:** 0.0.10  
**Mandatory Rule:** True  
**Rule ID:** 23-8  
**Rule Description:** For baseline systems 6 and 8, the minimum volume setpoint shall equal to 30% of peak primary design airflow or the rate required for minimum outside air whichever is larger.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)  
**Data Lookup:** None  
**Evaluation Context:** Building  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-6, 8, 8a, 6b, 8b.  

**Function Calls:**  

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

        - Case 1: For each terminal that is served by HVAC system that is Type-6, 8, 8a, 6b, 8b, if minimum volume setpoint is equal to 30% of peak primary design airflow or the rate required for minimum outside air, whichever is larger: `if terminal_b.minimum_airflow == MAX(terminal_b.primary_airflow * 0.3, terminal_b.minimum_outdoor_airflow): PASS`

        - Case 2: Else if minimum volume setpoint is less than 30% of peak primary design airflow or the rate required for minimum outside air, whichever is larger: `else if terminal_b.minimum_airflow < MAX(terminal_b.primary_airflow * 0.3, terminal_b.minimum_outdoor_airflow): FAIL`

        - Case 3: Else: `else: UNDETERMINED and raise_message "TERMINAL MINIMUM VOLUME SETPOINT IS HIGHER THAN 30% OF PEAK PRIMARY DESIGN AIRFLOW OR THE RATE REQUIRED FOR MINIMUM OUTSIDE AIR, WHICHEVER IS LARGER. VERIFY MINIMUM VOLUME SETPOINT IS MODELED CORRECTLY AS PER MINIMUM ACCREDITATION STANDARDS"`

**[Back](../_toc.md)**
