
# Lighting - Rule 6-14  

**Rule ID:** 6-14  
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
2. match_data_element()

## Rule Logic:  

- **Applicability Check 1:** `if sum(space.floor_area for P_RMR...spaces) < 5000:`

- For each space in the Proposed model: `space_p in P_RMR...spaces:`

  - Get matching space from Baseline RMR: `space_b = match_data_element(B_RMR, Spaces, space_p.name)`

    - Get normalized space lighting schedule for B_RMR: `normalized_schedule_b = normalize_space_schedules(space_b.interior_lighting)`
  
  - For each interior lighting in space: `for interior_lighting_p in space_p.interior_lighting:`

    - Get multiplier schedule for lighting: `schedule_p = interior_lighting_p.lighting_multiplier_schedule`

    - Check if lighting has occupancy control: `if interior_lighting_p.occupancy_control_type != "NONE":`

      - Compare lighting schedule in P_RMR with 90% of lighting schedule in B_RMR: `compare_schedules_result_dictionary = compare_schedules(schedule_p, normalized_schedule_b, always_2_schedule, 0.9)`

    - Else, lighting does not have occupancy control, compare lighting schedule in P_RMR with that in B_RMR: `else: compare_schedules_result_dictionary = compare_schedules(schedule_p, normalized_schedule_b, always_1_schedule, 1)`

      **Rule Assertion:**

      - Case 1: For each lighting, if lighting has daylighting control and uses schedule to model daylighting control, request manual review: `if ( interior_lighting_p.daylighting_control_type != "NONE" ) AND ( interior_lighting_p.are_schedules_used_for_modeling_daylighting_control ): CAUTION and raise_warning "LIGHTING HAS DAYLIGHTING CONTROL AND USES SCHEDULE TO MODEL DAYLIGHTING CONTROL. VERIFY IF SCHEDULE ADJUSTMENT IS MODELED CORRECTLY."`

      - Case 2: Else if lighting does not have daylighting control, and lighting has occupancy control and each hourly lighting schedule fraction in P-RMR is equal to 0.9 times that in B-RMR: `else if ( interior_lighting_p.daylighting_control_type == "NONE" ) AND ( interior_lighting_p.occupancy_control_type != "NONE" ) AND ( interior_lighting_p.are_schedules_used_for_modeling_occupancy_control ) AND ( compare_schedules_result_dictionary[TOTAL_HOURS_COMPARED] == compare_schedules_result_dictionary[TOTAL_HOURS_MATCH] )`

      - Case 3: Else if lighting does not have daylighting control, and lighting does not have occupancy control, and each hourly lighting schedule fraction in P-RMR is equal to that in B-RMR: `else if ( interior_lighting_p.daylighting_control_type == "NONE" ) AND ( interior_lighting_p.occupancy_control_type == "NONE" ) AND ( compare_schedules_result_dictionary[TOTAL_HOURS_COMPARED] == compare_schedules_result_dictionary[TOTAL_HOURS_MATCH] )`

      - Case 4: Else: `else: FAIL and raise_warning "LIGHTING SCHEDULE EFLH IN P-RMR IS ${compare_schedules_result_dictionary[EFLH_DIFFERENCE]} OF THAT IN B-RMR."`

**[Back](../_toc.md)**
