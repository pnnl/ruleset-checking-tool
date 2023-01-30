
# Lighting - Rule 6-9  

**Rule ID:** 6-9  
**Rule Description:** Proposed building is modeled with other programmable lighting controls through a 10% schedule reduction in buildings less than 5,000sq.ft.  
**Rule Assertion:** Proposed RMR = expected value  
**Appendix G Section:** Section G3.1-6(i) Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  

  1. Building total area is less than 5,000sq.ft.  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

**Function Call:**

1. compare_schedules()
2. normalize_space_schedules()
3. match_data_element()

## Rule Logic:  

- For each building in the Proposed model: `building_p in P_RMR.ASHRAE229.buildings:`

  - **Applicability Check 1:** `if sum(space.floor_area for building_p...spaces) < 5000:`
  
    - Get building open schedule in the proposed model: `building_open_schedule_p = building_p.building_open_schedule`  
  
      - For each space in the Proposed model building: `space_p in building_p...spaces:`

        - Get matching space from Baseline RMR: `space_b = match_data_element(B_RMR, Spaces, space_p.name)`

          - Get normalized space lighting schedule for B_RMR: `normalized_schedule_b = normalize_space_schedules(space_b.interior_lighting)`

        - Get normalized space lighting schedule for P_RMR: `normalized_schedule_p = normalize_space_schedules(space_p.interior_lighting)`

        - Compare normalized lighting schedule in P_RMR with normalized lighting schedule in B_RMR: `compare_schedules_result_dictionary = compare_schedules(normalized_schedule_p, normalized_schedule_b, building_open_schedule_p)`

        - For each interior lighting in space: `for lighting_p in space_p.interior_lighting:`

          - Check if any interior lighting in space has modeled daylight control using schedule, set daylight control flag to True: `if lighting_p.are_schedules_used_for_modeling_daylighting_control: daylight_control == TRUE`

        **Rule Assertion:**

        - Case 1: If space does not model any daylight control using schedule, and normalized space lighting schedule in P-RMR is equal to that in B-RMR: `if ( NOT daylight_control ) AND ( compare_schedules_result_dictionary[TOTAL_HOURS_COMPARED] == compare_schedules_result_dictionary[TOTAL_HOURS_MATCH] ): PASS`

        - Case 2: Else if space does not model any daylight control, and normalized space lighting schedule in P-RMR is not equal to that in B-RMR: `else if ( NOT daylight_control ) AND ( compare_schedules_result_dictionary[TOTAL_HOURS_COMPARED] != compare_schedules_result_dictionary[TOTAL_HOURS_MATCH] ): FAIL and raise_message "SPACE LIGHTING SCHEDULE EFLH IN P-RMR IS ${compare_schedules_result_dictionary[EFLH_DIFFERENCE]} OF THAT IN B-RMR."`

        - Case 3: Else, space models at least one daylight control using schedule: `else: UNDETERMINED and raise_message "SPACE MODELS AT LEAST ONE DAYLIGHT CONTROL USING SCHEDULE. VERIFY IF OTHER PROGRAMMABLE LIGHTING CONTROL IS MODELED CORRECTLY USING SCHEDULE. LIGHTING SCHEDULE EFLH IN P-RMR IS ${compare_schedules_result_dictionary[EFLH_DIFFERENCE]} OF THAT IN B-RMR."`

**Notes:**
  1. Updated the Rule ID from 6-14 to 6-10 on 6/3/2022
  2. Updated the Rule ID from 6-10 to 6-9 on 6/8/2022

**[Back](../_toc.md)**
