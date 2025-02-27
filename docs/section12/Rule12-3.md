# Receptacle - Rule 12-3
**Schema Version** 0.0.37  
**Primary Rule:** True  
**Rule ID:** 12-3  
**Rule Description:** When receptacle controls are specified in the proposed building design for spaces where not required by Standard 90.1 2019 Section 8.4.2, the hourly receptacle schedule shall be reduced as specified in Standard 90.1-2019 Table G3.1 Section 12 Proposed Building Performance column.   
**Appendix G Section:** Table G3.1-12 Proposed Building Performance column  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR and P_RMR  
**Applicability Checks:**
1. Receptacle controls are installed in spaces where not required by Standard 90.1 2019, Section 8.4.2  

**Manual Check:** None  
**Evaluation Context:** Each Miscellaneous Equipment object in the proposed model    
**Data Lookup:** None  
**Function Call:**
1) get_component_by_id
2) compare_schedules

## Applicability Checks:  
- Create a list of the lighting space types that correspond to space types that may have receptacle control requirements in Section 8.4.2: `EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES = ["OFFICE_ENCLOSED", "CONFERENCE_MEETING_MULTIPURPOSE_ROOM", "COPY_PRINT_ROOM", "LOUNGE_BREAKROOM_HEALTH_CARE_FACILITY", "LOUNGE_BREAKROOM_ALL_OTHERS", "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_PENITENTIARY", "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL", "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER", "OFFICE_OPEN_PLAN"]`  
- Create a list to store the spaces that have receptacle controls installed where not required by Standard 90.1 2019, Section 8.4.2: `spaces_with_receptacle_controls_beyond_req = []`  
- Iterate through the spaces in the proposed model: `for space_p in P_RMD...spaces`  
  - Get the lighting space type: `space_type_p = space_p.lighting_space_type`  
  - Iterate through the miscellaneous equipment loads in the space: `for misc_equip_p in space_p.miscellaneous_equipment:`  
    - Get the proposed automatic receptacle control: `auto_receptacle_control_p = misc_equip_p.automatic_controlled_percentage > 0.0 `  
    - If the space type is not in the list of space types where receptacle controls may be required, and the space has automatic receptacle controls installed: `if space_type_p not in EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES and auto_receptacle_control_p:`  
      - Add the space to the list of spaces with receptacle controls installed where not required: `spaces_with_receptacle_controls_beyond_req.append(space_p.id)` 
- Rule is applicable if the list of spaces with receptacle controls installed where not required is not empty: `applicable = len(spaces_with_receptacle_controls_beyond_req) > 0`


## Rule Logic:  
- Iterate through the spaces in the proposed model: `for space_p in P_RMD...spaces`  
  - Get the lighting space type: `space_type_p = space_p.lighting_space_type` 
  - Iterate through the miscellaneous equipment loads in the space: `for misc_equip_p in space_p.miscellaneous_equipment:`  
    - Get the proposed automatic receptacle control: `auto_receptacle_control_p = misc_equip_p.automatic_controlled_percentage > 0.0 `  
    - If the space type is not in the list of space types where receptacle controls may be required, and the space has automatic receptacle controls installed: `if space_type_p not in EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES and auto_receptacle_control_p:`  
      - Get the percentage of controlled receptacles: `controlled_percentage = misc_equip_p.automatic_controlled_percentage`
      - Calculate the expected receptacle power credit: `expected_receptacle_power_credit = 0.10 * controlled_percentage`
      - Get the associated miscellaneous equipment object in the baseline model: `misc_equip_b = get_component_by_id(misc_equip_p.id, B_RMD)`
      - Get the baseline miscellaneous equipment multiplier schedule: `hourly_multiplier_schedule_b = misc_equip_b.multiplier_schedule`
      - Get the proposed miscellaneous equipment multiplier schedule: `hourly_multiplier_schedule_p = misc_equip_p.multiplier_schedule`
      - Create a list of expected hourly values based on the expected receptacle power credit: `expected_hourly_values = [hour_value * (1 - expected_receptacle_power_credit) for hour_value in hourly_multiplier_schedule_b.hourly_values]`
      - If it is a leap year, set the schedule comparison mask to 8784 hours, else set it to 8760 hours: `mask_schedule = [1] * 8784 if is_leap_year else [1] * 8760`
      - Compare the expected miscellaneous equipment load schedule to the proposed miscellaneous equipment load schedule: `credit_comparison_data = compare_schedules(expected_hourly_values, hourly_multiplier_schedule_p, mask_schedule)`
      - Compare the baseline miscellaneous equipment load schedule to the proposed miscellaneous equipment load schedule: `no_credit_comparison_data = compare_schedules(hourly_multiplier_schedule_b, hourly_multiplier_schedule_p, mask_schedule)`

       **Rule Assertion:**  
      - Case 1: If the expected receptacle power credit was applied as expected for all hours: PASS `if credit_comparison_data['total_hours_matched'] == len(hourly_multiplier_schedule_p.hourly_values == len(expected_hourly_values): PASS` 
      - Case 2: If a receptacle power credit was expected, but baseline and proposed are identical: UNDETERMINED and raise_message `if no_credit_comparison_data['total_hours_matched'] == len(hourly_multiplier_schedule_b.hourly_values == len(hourly_multiplier_schedule_p.hourly_values): UNDETERMINED and raise_message('Credit for automatic receptacle controls was expected, but baseline and proposed miscellaneous equipment schedules are identical')`  
      - Case 3: Else, a credit or penalty was applied incorrectly: FAIL `else: outcome = FAIL`  


**Notes:**  
1. The rule depends on a new data element being added to the schema: `automatic_controlled_percentage` for the Miscellaneous Equipment object.

- **[Back](../_toc.md)**
