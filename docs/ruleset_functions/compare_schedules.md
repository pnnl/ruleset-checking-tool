
## compare_schedules

Description: This function would compare two schedules and determine if they match with or without a comparison factor when applicable.  

Inputs:
- **schedule_1**: First schedule.
- **schedule_2**: Second schedule.
- **mask_schedule**: The schedule that defines comparison mode for all 8760 hours in a year, i.e. if hourly value is 0, schedule_1 shall be equal to schedule_2; if hourly value is 1, schedule_1 shall be equal to schedule_2 times the comparison factor; if hourly value is 2, skip comparison for that hour;  
- **comparison_factor**: The target multiplier number for schedule_1 compared to schedule_2, i.e. when applicable, the hourly value in schedule_1 shall be equal to that in schedule_2 times the comparison_factor.

Returns:
- **compare_schedules_result_array**: An array containing the total number of hours that the function compares and the number of hours schedule_1 matches schedule_2 with the comparison_factor, i.e. [total_hours_compared, total_hours_match]

Function Call:

- get_schedule_8760_values_array()

Data Lookup: None

Logic:

- Get 8760 hourly values array for schedule_1, schedule_2 and mask_schedule: `hourly_value_sch_1 = get_schedule_8760_values_array(schedule_1), hourly_value_sch_2 = get_schedule_8760_values_array(schedule_2), hourly_value_mask_sch = get_schedule_8760_values_array(mask_schedule)`

- For each hour in mask_schedule's hourly values array: `for hourly_value in hourly_value_mask_sch:`

  - If hourly value is 0: `if hourly_value == 0:`

    - Add to the pool of hours need comparison: `total_hours_compared += 1`

    - If schedule_1 hourly value is equal to schedule_2, save to the pool of hours that meets requirement: `if hourly_value_sch_1 == hourly_value_sch_2: total_hours_match += 1`

  - Else if hourly value is 1: `else if hourly_value == 1:`

    - Add to the pool of hours need comparison: `total_hours_compared += 1`

    - If schedule_1 hourly value is equal to schedule_2 times comparison_factor, save to the pool of hours that meets requirement: `if hourly_value_sch_1 == hourly_value_sch_2 * comparison_factor: total_hours_match += 1`

- Save the total number of hours compared and the number of hours that meets requirement to output array: `compare_schedules_result_array = [total_hours_compared, total_hours_match]`

**Returns** compare_schedules_result_array

**[Back](../_toc.md)**

**Notes:**
1. mask_schedule might need to be for each second for future RDS.
