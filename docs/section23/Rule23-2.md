
# Airside System - Rule 23-2  

**Rule ID:** 23-2  
**Rule Description:** System 5 & 7 minimum volume setpoint shall be 30% of zone peak airflow, minimum outdoor airflow, or rate required to comply with minium accreditation standards whichever is larger.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**Appendix G Section Reference:** Section G3.1.3.13 VAV Minimum Flow Set Points (Systems 5 and 7)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-5 or 7  

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:**  

1. baseline_hvac_type()  

## Rule Logic:  

- For each zone in B_RMR: `for zone_b in B_RMR...zones:`

  - For each terminal in zone: `for terminal_b in zone_b.terminals:`

    - Get HVAC system serving terminal: `hvac_b = terminal_b.served_by_heating_ventilation_air_conditioning_systems`
  
      - Check if HVAC system is type 6 or 8: `if baseline_hvac_type(hvac_b) in ["SYS-5", "SYS-7"]:`

        - Set applicability flag: `rule_applicability_check = TRUE`

          **Rule Assertion:**

          - Case 1: For each terminal that is served by HVAC system that is Type-5 or 7, if minimum volume setpoint is equal to 30% of peak primary design airflow or the rate required for minimum outside air, whichever is larger: `if terminal_b.minimum_airflow == MAX(terminal_b.primary_airflow * 0.3, terminal_b.minimum_outdoor_airflow): PASS`

          - Case 2: Else if minimum volume setpoint is less than 30% of peak primary design airflow or the rate required for minimum outside air, whichever is larger: `else if terminal_b.minimum_airflow < MAX(terminal_b.primary_airflow * 0.3, terminal_b.minimum_outdoor_airflow): FAIL`

          - Case 3: Else: `else: UNDETERMINED and raise_message "TERMINAL MINIMUM VOLUME SETPOINT IS HIGHER THAN 30% OF PEAK PRIMARY DESIGN AIRFLOW OR THE RATE REQUIRED FOR MINIMUM OUTSIDE AIR, WHICHEVER IS LARGER. VERIFY MINIMUM VOLUME SETPOINT IS MODELED CORRECTLY AS PER MINIMUM ACCREDITATION STANDARDS"`

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-5 or 7: `if rule_applicability_check: is_applicable = TRUE`

**[Back](../_toc.md)**

**Notes:**

1. Right now this RDS assumes terminal.minimum_outdoor_airflow field does not consider outdoor air flow rate required to comply with minimum accreditation standards.
