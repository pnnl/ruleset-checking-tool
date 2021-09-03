
# Envelope - Rule 5-45  

**Rule ID:** 5-45  
**Rule Description:** The  infiltration schedules are the same in the proposed RMR as in the baseline RMR.  
**Rule Assertion:** B-RMR hourly fractions of infiltration:infiltration_multiplier_schedule_name = P-RMR hourly fractions of infiltration:infiltration_multiplier_schedule_name.  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design and Baseline  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** 

  1. compare_schedules()
  2. match_data_element()

## Rule Logic:  

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`  

  - For each thermal block in building segment: `for thermal_block_b in building_segment_b.thermal_blocks:`  

    - For each zone in thermal block: `for zone_b in thermal_block_b.zones:`

      - Get zone infiltration: `infiltration_b = zone_b.infiltration`  

      - Get matching zone in P_RMR: `zone_p = match_data_element(P_RMR, Zones, zone_b.id)`

        - Get zone infiltration in P_RMR: `infiltration_p = zone_p.infiltration`

          **Rule Assertion:**  

          - Case 1: If zone infiltration schedule in P_RMR matches that in B_RMR: `if compare_schedules(infiltration_b.multiplier_schedule, infiltration_p.multiplier_schedule) == "EQUAL": PASS`  

          - Case 2: Else: `Else: FAIL`

**[Back](../_toc.md)**
