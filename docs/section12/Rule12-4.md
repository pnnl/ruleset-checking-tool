# Receptacle - Rule 12-4
**Schema Version** 0.0.37  
**Primary Rule:** True  
**Rule ID:** 12-4  
**Rule Description:** Computer room equipment schedules shall be modeled as a constant fraction of the peak design load per the following monthly schedule: Months 1, 5, 9 — 25%; Months 2, 6, 10 — 50%; Months 3, 7, 11 — 75%; Months 4, 8, 12 — 100%   
**Appendix G Section:** G3.1.3.16   
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**
1. Computer rooms are present in the baseline model  

**Manual Check:** None  
**Evaluation Context:** Each Miscellaneous Equipment object in the baseline model    
**Data Lookup:** None  
**Function Call:**
1) find_all
2) is_space_a_computer_room
3) compare_schedules

## Applicability Checks:  
- Iterate through the spaces in the baseline RMD: `for space_b in find_all("$.buildings[*].building_segments[*].zones[*].spaces[*]", B_RMD):`
  - Check if the space is a computer room: `if is_space_a_computer_room(B_RMD, space_b.id):`
    - Iterate through the miscelleneous equipment loads: `for misc_equip_b in space_b.miscellaneous_equipment:`
      - Check if the equipment is specified as anything other than IT equipment: `if misc_equip_b.type and misc_equip_b.type != "INFORMATION_TECHNOLOGY_EQUIPMENT":` 
        - Rule is not applicable: `return False`
      - Else, the equipment is IT equipment or the type was not specified so we assume that all miscellaneous equipment in the computer room is computer room equipment: `else:`
        - Rule is applicable: `return True`

## Rule Logic:
- Determine if it is a leap year: `is_leap_year = RPD.calendar.is_leap_year`
- Create a dictionary to map the month numbers to their respective fractions: `month_fractions = {1: 0.25, 2: 0.5, 3: 0.75, 4: 1, 5: 0.25, 6: 0.5, 7: 0.75, 8: 1, 9: 0.25, 10: 0.5, 11: 0.75, 12: 1}`
- Create a dictionary to map the number of days in each month: `days_in_month = {1: 31, 2: 29 if is_leap_year else 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}`
- Create an empty list to store the expected hourly values of the schedule: `expected_hourly_values = []`
- Iterate through the months of the year: `for month in range(1, 13):`
  - Get the fraction for the month: `fraction = month_fractions[month]`
  - Get the number of days in the month: `days = days_in_month[month]`
  - Append the hourly fraction to the list: `expected_hourly_values.extend([fraction] * days * 24)`
- Create the mask schedule to be used for comparison: `mask_schedule = [1] * 8784 if is_leap_year else [1] * 8760`
- Get the multiplier schedule that was modeled for the equipment: `multiplier_schedule_b = misc_equip_b.multiplier_schedule.hourly_values`
- Compare the modeled schedule with the expected schedule: `comparison_data = compare_schedules(multiplier_schedule_b, expected_hourly_values, mask_schedule)`

**Rule Assertion:**  
  - Case 1: If the modeled schedule matches the expected schedule for all hours, PASS:`if comparison_data["total_hours_matched"] == 8784 if is_leap_year else 8760: PASS`
  - Case 2: Else, FAIL:`else: FAIL`


**Notes:**  
1. It was noted that the is_space_a_computer_room function needs to be updated to better align with the definition of a computer room in the standard. Applicability will depend on the correct implementation so that computer rooms are only recognized if design electronic data equipment power density
exceeds 20 W/ft2 of conditioned floor area

- **[Back](../_toc.md)**
