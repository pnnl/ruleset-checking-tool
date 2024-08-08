
# Envelope - Rule 5-45  

**Rule ID:** 5-45  
**Rule Description:** The  infiltration schedules are the same in the proposed RMR as in the baseline RMR.  
**Rule Assertion:** B-RMR hourly fractions of infiltration:multiplier_schedule = P-RMR hourly fractions of infiltration:multiplier_schedule.  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design and Baseline  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** 

  1. compare_schedules()
  2. match_data_element()

## Rule Logic:  

- For each zone in the Baseline model: `for zone_b in B_RMR...zones:`

  - Get zone infiltration: `infiltration_b = zone_b.infiltration`

  - Get matching zone in P_RMR: `zone_p = match_data_element(P_RMR, Zones, zone_b.id)`

    - Get zone infiltration in P_RMR: `infiltration_p = zone_p.infiltration`

      - Compare infiltration schedules in B_RMR and P_RMR: `compare_schedules_result_dictionary = compare_schedules(infiltration_b.multiplier_schedule, infiltration_p.multiplier_schedule, always_1_schedule, 1, is_leap_year)`

      **Rule Assertion:**  

      - Case 1: For each zone, if each hourly zone infiltration schedule in P_RMR matches that in B_RMR: `if compare_schedules_result_dictionary[TOTAL_HOURS_COMPARED] == compare_schedules_result_dictionary[TOTAL_HOURS_MATCH]: PASS`

      - Case 2: Else: `Else: FAIL and raise_warning "BASELINE AND PROPOSED INFILTRATION SCHEDULES ARE NOT THE SAME. THE DIFFERENCE BETWEEN BASELINE EFLH AND PROPOSED EFLH IS EQUAL TO {COMPARE_SCHEDULES_RESULT_DICTIONARY[EFLH_DIFFERENCE]}"`

**Notes:**

1. BASELINE=PROPOSED match, archived on 10/26/2023

**[Back](../_toc.md)**
