
# Lighting - Rule 6-12  

**Rule ID:** 6-12   
**Rule Description:** In buildings >5000 ft2 lighting shall be modeled having occupancy sensors in employee lunch and break rooms, conference/meeting rooms, and classrooms (not including shop classrooms, laboratory classrooms, and preschool through 12th grade classrooms). These controls shall be reflected in the baseline building design lighting schedules.  
**Rule Assertion:** Baseline RMD = expected value  
**Appendix G Section:** Table G3.1 #6 Baseline column

**Mandatory Rule:** True  
**Evaluation Context:** Each Space  
**Function Call:**  

- get_component_by_id()

## Applicability Check:  
1. Building area is greater than 5000 ft2
2. Space has lighting and lighting space type is one of the following: employee lunch and break rooms, conference/meeting rooms, and classrooms (not including shop classrooms, laboratory classrooms, and preschool through 12th grade classrooms)

## Rule Logic:
- For each building in the baseline model: `for building_b in B_RMD...buildings:`
  
  **Applicability Check 1:** 
  - Declare a variable for the building area: `building_area_b = 0`
  - Iterate the spaces in the building: `for space_b in building_b...spaces:`
     - Add the area of each space to the building area sum: `building_area_b += space_b...floor_area`
  - Check if the building area is greater than 5000 ft2: `if building_area_b > 5000: IS_APPLICABLE`
  
    - For each space in the building: `for space_b in building_b...spaces:`
      - Get the total interior lighting power in the space: `interior_lighting_power_b = sum([interior_lighting_b.get("power_per_area") for interior_lighting_b in space_b["interior_lighting"]])`
    
      **Applicability Check 2:**
      - Check if the space has lighting and the lighting space type is one of the specified types: `if interior_lighting_power_b > 0 and space_b["lighting_space_type"] in [LOUNGE_BREAKROOM_ALL_OTHERS, CONFERENCE_MEETING_MULTIPURPOSE_ROOM, CLASSROOM_LECTURE_HALL_TRAINING_ROOM_PENITENTIARY, CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER, LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM] or (space_b["function"] == LABORATORY and space_b["lighting_space_type"] == CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL): IS_APPLICABLE`
        - Create a list of the occupancy sensor controls in the space: `occupancy_sensor_controls_b = [interior_lighting_b.get("occupancy_control_type") for interior_lighting_b in space_b["interior_lighting"]`
        - Create a list of boolean values indicating if occupancy sensors were modeled via schedule adjustments: `occupancy_sensor_schedules_b = [interior_lighting_b.get("are_schedules_used_for_modeling_occupancy_control") for interior_lighting_b in space_b["interior_lighting"]`
        
        - **Rule Assertion:**
        - Case 1: The space function is plenum, crawlspace, or interstitial space and has lighting modeled: UNDETERMINED `if space_b["function"] in [PLENUM, CRAWLSPACE, INTERSTITIAL_SPACE]: UNDETERMINED and raise_warning("Unable to determine whether occupancy sensor lighting controls are required in plenum, crawlspace, or interstitial spaces.")`
        - Case 2: All interior lighting in the space is controlled by occupancy sensors and modeled via adjustments to the schedules: PASS `if not any(val in ["NONE", "MANUAL_ON", None] for val in occupancy_controls_b) and all(occupancy_sensor_schedules_b): PASS`
        - Case 3: Any interior lighting in the space is missing definitions for occupancy sensor type and schedule adjustments: UNDETERMINED `elif any(val is None for val in occupancy_controls_b) or any(val is None for val in occupancy_sensor_schedules_b): UNDETERMINED`
        - Case 4: Else, at least one interior lighting data group in the space is not controlled by occupancy sensors or modeled via adjustments to the schedules: FAIL `else: FAIL`

**Notes:**
None

**[Back](../_toc.md)**
