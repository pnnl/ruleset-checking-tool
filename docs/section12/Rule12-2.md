# Receptacles - Rule 12-2
**Rule ID:** 12-2  
**Rule Description:** Depending on the space type, receptacle controls may be required by 90.1 Section 8.4.2. Receptacle schedules shall be modeled identically to the proposed design except when receptacle controls are specified in the proposed design for spaces where not required by Section 8.4.2.  
**Rule Assertion:** Baseline RMD = Proposed RMD  
**Appendix G Section:** Table G3.1-12 Proposed Building Performance column  
**Appendix G Section Reference:** None  
**Data Lookup:** None  
**Evaluation Context:** Each miscellaneous equipment load

**Applicability Checks:** None

**Function Call**
find_exactly_one_schedule, find_all, compare_schedules


## Rule Logic:  
- Create a list of the lighting space types that correspond to space types that may have receptacle control requirements in Section 8.4.1: `EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES = ["OFFICE_ENCLOSED", "CONFERENCE_MEETING_MULTIPURPOSE_ROOM", "COPY_PRINT_ROOM", "LOUNGE_BREAKROOM_HEALTH_CARE_FACILITY", "LOUNGE_BREAKROOM_ALL_OTHERS", "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_PENITENTIARY", "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL", "CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER", "OFFICE_OPEN_PLAN"]`  
- For each space in the baseline RMD: `for space_b in B_RMD.spaces:`  
  - Get the lighting space type: `space_type_b = space_b.lighting_space_type`
  - For each miscellaneous equipment load in the space: `for misc_equip_b in space_b.miscellaneous_equipment:`
    - Get the corresponding miscellaneous equipment load from the proposed RMD: `misc_equip_p = match_data_element(P_RMD, MiscellaneousEquipment, misc_equip_b.id)`
    - Get the baseline miscellaneous equipment load schedule: `misc_equip_schedule_b = misc_equip_b.multiplier_schedule`
    - Get the proposed miscellaneous equipment load schedule: `misc_equip_schedule_p = misc_equip_p.multiplier_schedule`
    - Get the baseline automatic receptacle control: `auto_receptacle_control_b = misc_equip_b.automatic_controlled_percentage > 0.0`
    - Get the proposed automatic receptacle control: `auto_receptacle_control_p = misc_equip_p.automatic_controlled_percentage > 0.0`
    - If it is a leap year, set the schedule comparison mask to 8784 hours, else set it to 8760 hours: `mask_schedule = [1] * 8784 if is_leap_year else [1] * 8760`
    - Compare the baseline miscellaneous equipment load schedule to the proposed miscellaneous equipment load schedule: `comparison_data = compare_schedules(misc_equip_schedule_b, misc_equip_schedule_p, mask_schedule)`
    
    **Rule Assertion:**  
      Case 1: The baseline and proposed miscelleaneous equipment schedules match for all hours: PASS `if comparison_data['total_hours_matched'] == len(misc_equip_schedule_b == len(misc_equip_schedule_p): PASS`   
      Case 2: The baseline and proposed miscelleaneous equipment both have automatic controls, but schedules have unequal equivalent full load hours: FAIL and raise message `elif auto_receptacle_control_p and auto_receptacle_control_b and comparison_data["eflh_difference"] != 0: FAIL and raise_message = "The baseline miscellaneous equipment schedule has automatic receptacle controls indicating that there is an applicable requirement for automatic controls for the space in Section 8.4.2. Miscellaneous equipment schedules may only differ when the proposed design has automatic receptacle controls and there are no applicable requirements in Section 8.4.2 for the space."`  
      Case 3: The proposed miscellaneous equipment schedule has fewer equivalent full load hours than the baseline miscellaneous equipment schedule, the proposed has automatic receptacle control, and the space type is not expected to have receptacle control requirements in Section 8.4.2 : PASS `elif comparison_data["eflh_difference"] > 0 and auto_receptacle_control_p and space_type_b not in EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES: PASS`  
      Case 4: The proposed miscellaneous equipment schedule has fewer equivalent full load hours than the baseline miscellaneous equipment schedule, the baseline does not have automatic receptacle control, the proposed has automatic receptacle control, and the space type may have receptacle control requirements in Section 8.4.2, or the lighting space type was not defined : UNDETERMINED and raise message`elif (comparison_data["eflh_difference"] > 0 and not auto_receptacle_control_b and auto_receptacle_control_p and space_type_b in EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES) or space_type_b is None: UNDETERMINED and raise_message="A reduced schedule and automatic receptacle controls are present in the proposed design. The space type may have receptacle control requirements in Section 8.4.2. If that is the case, there should be no reduced schedule modeled."`  
      Case 5: The proposed miscellaneous equipment schedule has fewer equivalent full load hours than the baseline miscellaneous equipment schedule, the proposed does not have automatic receptacle control : FAIL `elif comparison_data["eflh_difference"] > 0 and not auto_receptacle_control_p: FAIL`  
      Case 6: The proposed miscellaneous equipment schedule has more equivalent full load hours than the baseline miscellaneous equipment schedule: FAIL `elif comparison_data["eflh_difference"] < 0: FAIL and raise_msg = "Rule evaluation fails with a conservative outcome. The proposed schedule equivalent full load hours is greater than the baseline."`  
      Case 7: The proposed automatic receptacle control was not specified: UNDETERMINED and raise message`elif auto_receptacle_control_p == Null: UNDETERMINED and raise_message = "The proposed miscellaneous equipment schedule has reduced equivalent full load hours compared the baseline but it could not be determined if automatic receptacle controls are present in the proposed design to justify the credit."`
      Case 8: Else: FAIL `else: FAIL`  


**[Back](../_toc.md)**
