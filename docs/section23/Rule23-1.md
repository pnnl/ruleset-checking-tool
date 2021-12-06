
# CHW&CW - Rule 23-1  

**Rule ID:** 23-1  
**Rule Description:** For baseline systems 5-8 and 11, the SAT is reset higher by 5F under minimum cooling load conditions.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**Appendix G Section Reference:** Section G3.1.3.12 Supply Air Temperature Reset (Systems 5 through 8 and 11)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-5, 6, 7, 8, 11  

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:**  

1. baseline_hvac_type()  

## Rule Logic:  

- For each building segment in B_RMR: `for building_segment_b in B_RMR...building_segments:`

  - Get HVAC system: `hvac_b = building_segment_b.heating_ventilation_air_conditioning_systems`

    - Check if HVAC system is type 5, 6, 7, 8 or 11: `if baseline_hvac_type(hvac_b) in ["SYS-5", "SYS-6", "SYS-7", "SYS-8", "SYS-11"]:`

      - Set applicability flag: `rule_applicability_check = TRUE`

      - Get fan system of HVAC system: `fan_system_b = hvac_b.fan_systems` (See Note#1)

        **Rule Assertion:**

        - Case 1: For each HVAC system that is Type-5, 6, 7, 8 or 11, if supply air temperature is reset higher by 5F under minimum cooling load condition: `if ( fan_system_b.temperature_control == "ZONE_RESET" ) AND ( fan_system_b.reset_differential_temperature == 5 ): PASS`

        - Case 2: Else: `else: FAIL`

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-5, 6, 7, 8, or 11: `if rule_applicability_check: is_applicable = TRUE`

**[Back](../_toc.md)**

**Notes:**

1. For baseline hvac.fan_systems, assuming only one fan system is modeled. Might need a separate check for this. Note from schema: "Normally one fan system is used but second fan systems may be used when a direct outdoor air system is used."
