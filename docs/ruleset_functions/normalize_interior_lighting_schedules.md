
## normalize_interior_lighting_schedules

Description: This function would determine a normalized interior lighting schedule for interior_lighting data element in space. 

Inputs:
  - **Space**: The space in which its interior lightings need to determine a normalized schedule.
  - **adjust_for_credit**: Flag to indicate whether the schedule normalization needs to add control credit adjustment.

Returns:
- **space_normalized_schedule_array**: An array containing 8760 hourly values of a normalized schedule of the space data element.

Function Call:

- convert_schedule_to_hourly()

Data Lookup:

- Table G3.7

Applicability:

- space.interior_lighting
- space.miscellaneous_equipment (To be developed)

Logic:

- For each interior lighting in space: `for interior_lighting in space.interior_lighting:`

  - Get lighting power per area: `power_per_area = interior_lighting.power_per_area`

    - Add lighting power per area to space total: `space_total_power_per_area += power_per_area`
  
  - Set bonus_adjustment to 1.0: `bonus_adjustment = 1.0`
  
  - Check if `interior_lighting.occupancy_control_type` data is provided. Set to `OTHER` if this data is missing: `if not interior_lighting.has('occupancy_control_type): interior_lighting.occupancy_control_type = OTHER`

  - else if `interior_lighting.occupancy_control_type` is MANUAL_ON or PARTIAL_AUTO_ON, set bonus_adjustment to 1.25: `if interior_lighting.occupancy_control_type = [MANUAL_ON, PARTIAL_AUTO_ON]: bonus_adjustment = 1.25`

  - Check if adjust_for_credit is true and lighting uses schedule to model occupancy control, get occupancy control credit: `if adjust_for_credit and interior_lighting.are_schedules_used_for_modeling_occupancy_control: control_credit = data_lookup(table_G3_7, space.lighting_space_type, interior_lighting.occupancy_control_type, bonus_adjustment)`

  - Else, set occupancy control credit to 0: `else: control_credit = 0`

  - Get lighting schedule: `schedule = interior_lighting.lighting_multiplier_schedule`

    - If schedule is hourly type, adjust hourly values to exclude occupancy control credit, then multiply adjusted hourly values with power per area and save to an hourly use per area array: `if schedule.schedule_sequence_type == "HOURLY": hourly_use_per_area_array.append(hourly_value / (1 - control_credit) * power_per_area for hourly_value in schedule.hourly_values)`

    - Else, schedule is event type, convert schedule values to hourly: `else: converted_schedule_array = convert_schedule_to_hourly(schedule)`

      - Multiply hourly values with power per area and save to an hourly use per area array: `hourly_use_per_area_array.append(hourly_value / (1 - control_credit) * power_per_area for hourly_value in converted_schedule_array)`

  - Add hourly use per area array to space total hourly use per area array: `space_total_hourly_use_per_area_array = ( hourly_value_1 + hourly_value_2 for hourly_value_1, hourly_value_2 in zip(space_total_hourly_use_per_area_array, hourly_use_per_area_array) )`

- Divide space total hourly use per area array by space total power per area to get normalized hourly schedule array: `space_normalized_schedule_array = (hourly_value / space_total_power_per_area for hourly_value in space_total_hourly_use_per_area_array)`

**Returns** `return space_normalized_schedule_array`  

**Notes**:

  1. The current code requires Table 3.7 include additional column to account for manual-on and partial-auto-on credit (multiplied by 1.25).
  2. The function only works with hourly schedules
**[Back](../_toc.md)**