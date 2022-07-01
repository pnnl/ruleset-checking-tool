
## normalize_interior_lighting_schedules

Description: This function would determine a normalized interior lighting schedule for interior_lighting data element in space. 

Inputs:
  - **Space.data_element**: The space data element that needs to determine a normalized schedule, e.g. space.interior_lighting.

Returns:
- **space_normalized_schedule_array**: An array containing 8760 hourly values of a normalized schedule of the space data element.

Data Lookup:

- Table G3.7

Applicability:

- space.interior_lighting
- space.miscellaneous_equipment (To be developed)

Logic:

- For each interior lighting in space: `for interior_lighting in space.interior_lighting:`

  - Get lighting power per area: `power_per_area = interior_lighting.power_per_area`

    - Add lighting power per area to space total: `space_total_power_per_area += power_per_area`

  - Get lighting schedule: `schedule = interior_lighting.lighting_multiplier_schedule`

    - If schedule is hourly type, multiply hourly values with power per area and save to an hourly use per area array: `if schedule.schedule_sequence_type == "HOURLY": hourly_use_per_area_array.append(hourly_value * power_per_area for hourly_value in schedule.hourly_values)`

    - Else, schedule is event type, convert schedule values to hourly: `else: converted_schedule_array = convert_schedule_to_hourly(schedule)`

      - Multiply hourly values with power per area and save to an hourly use per area array: `hourly_use_per_area_array.append(hourly_value * power_per_area for hourly_value in converted_schedule_array)`

  - Add hourly use per area array to space total hourly use per area array: `space_total_hourly_use_per_area_array = ( hourly_value_1 + hourly_value_2 for hourly_value_1, hourly_value_2 in zip(space_total_hourly_use_per_area_array, hourly_use_per_area_array) )`

- Divide space total hourly use per area array by space total power per area to get normalized hourly schedule array: `space_normalized_schedule_array = (hourly_value / space_total_power_per_area for hourly_value in space_total_hourly_use_per_area_array)`

**Returns** `return space_normalized_schedule_array`  

**Notes**:

1The function only works with hourly schedules
**[Back](../_toc.md)**