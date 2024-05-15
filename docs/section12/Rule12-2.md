# Receptacles - Rule 12-2
**Rule ID:** 12-2  
**Rule Description:** Based on the space type, receptacle controls may be required by Section 8.4.2. Receptacle schedules shall be identical to the proposed design except when receptacle controls, installed in spaces where not required by Section 8.4.2, are included in the proposed building design.  
**Rule Assertion:** Baseline RMD = Proposed RMD  
**Appendix G Section:** Section Table G3.1-12 Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  
**Data Lookup:** None  
**Evaluation Context:** Each miscellaneous equipment load

**Applicability Checks:** None

**Function Call**
match_data_element, compare_schedules


## Rule Logic:  
- Create a list of the lighting space types that correspond to space types that may have receptacle control requirements in Section 8.4.1: `EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES = ["OFFICE_ENCLOSED", "CONFERENCE_MEETING_MULTIPURPOSE_ROOM", "COPY_PRINT_ROOM", "LOUNGE_BREAKROOM_HEALTH_CARE_FACILITY", "LOUNGE_BREAKROOM_ALL_OTHERS", "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_PENITENTIARY", "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL", "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER", "OFFICE_OPEN_PLAN"]`  
- For each space in the baseline RMD: `for space_b in B_RMD.spaces:`  
  - Get the lighting space type: `space_type_b = space_b.lighting_space_type`
  - For each miscellaneous equipment load in the space: `for misc_equip_b in space_b.miscellaneous_equipment:`
    - Get the corresponding miscellaneous equipment load from the proposed RMD: `misc_equip_p = match_data_element(P_RMD, MiscellaneousEquipment, misc_equip_b.id)`
    - Get the baseline miscellaneous equipment load schedule: `misc_equip_schedule_b = misc_equip_b.multiplier_schedule`
    - Get the proposed miscellaneous equipment load schedule: `misc_equip_schedule_p = misc_equip_p.multiplier_schedule`
    - Get the baseline automatic receptacle control: `auto_receptacle_control_b = misc_equip_b.has_automatic_control`
    - Get the proposed automatic receptacle control: `auto_receptacle_control_p = misc_equip_p.has_automatic_control`
    - If it is a leap year, set the schedule comparison mask to 8784 hours, else set it to 8760 hours: `mask_schedule = [1] * 8784 if is_leap_year else [1] * 8760`
    - Compare the baseline miscellaneous equipment load schedule to the proposed miscellaneous equipment load schedule: `comparison_data = compare_schedules(misc_equip_schedule_b, misc_equip_schedule_p, mask_schedule)`
    
**Rule Assertion:**  
Case 1: If the baseline and proposed miscelleaneous equipment schedules match for all hours: PASS `if comparison_data['total_hours_matched'] == len(misc_equip_schedule_b == len(misc_equip_schedule_p): PASS`  
Case 2: Elif the proposed automatic receptacle control was not specified: UNDETERMINED `elif auto_receptacle_control_p == Null: UNDETERMINED`  
Case 3: Elif the baseline and proposed miscelleaneous equipment both have automatic controls, but schedules have unequal equivalent full load hours: FAIL and raise_message `elif auto_receptacle_control_p and auto_receptacle_control_b and comparison_data["eflh_difference"] != 0: FAIL and raise_message = "The baseline miscellaneous equipment schedule has automatic receptacle controls indicating that there is an applicable requirement for automatic controls for the space in Section 8.4.1. Miscellaneous equipment schedules may only differ when the proposed design has automatic receptacle controls and there are no applicable requirements in Section 8.4.1 for the space."`  
Case 4: Elif the proposed miscellaneous equipment schedule has fewer equivalent full load hours than the baseline miscellaneous equipment schedule, the proposed has automatic receptacle control, and the space type is not expected to have receptacle control requirements in Section 8.4.1 : PASS `elif comparison_data["eflh_difference"] > 0 and auto_receptacle_controls_p and space_type_b not in EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES: PASS`  
Case 5: Elif the proposed miscellaneous equipment schedule has fewer equivalent full load hours than the baseline miscellaneous equipment schedule, the proposed has automatic receptacle control, and the space type may have receptacle control requirements in Section 8.4.1, or the lighting space type was not defined : UNDETERMINED `elif (comparison_data["eflh_difference"] > 0 and auto_receptacle_controls_p and space_type_b in EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES) or space_type_b is None: UNDETERMINED and raise_message="A reduced schedule and automatic receptacle controls are present in the proposed design. The space type may have receptacle control requirements in Section 8.4.1. If that is the case, there should be no reduced schedule modeled."`  
Case 6: Elif the proposed miscellaneous equipment schedule has fewer equivalent full load hours than the baseline miscellaneous equipment schedule, the proposed does not have automatic receptacle control : FAIL `elif comparison_data["eflh_difference"] > 0 and not auto_receptacle_controls_p: FAIL`  
Case 7: Elif the proposed miscellaneous equipment schedule has more equivalent full load hours than the baseline miscellaneous equipment schedule: FAIL `elif comparison_data["eflh_difference"] < 0: FAIL and raise_msg = "Rule evaluation fails with a conservative outcome."`  
Case 8: Else: FAIL `else: FAIL`  


**[Back](../_toc.md)**
