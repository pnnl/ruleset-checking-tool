
## compare_schedules

Description: This function would compare two schedules and determine if they match with or without a comparison factor when applicable.  

Inputs:
- **schedule_1**: First schedule.
- **schedule_2**: Second schedule.
- **mask_schedule**: The schedule that defines comparison mode for all 8760 hours in a year, i.e. if hourly value is 1, schedule_1 is evaluated to be equal to schedule_2; if hourly value is 0, comparison was skipped for that particular hour (example when evaluating shut off controls, only he building closed hrs are evaluated).  

Returns:
- **compare_schedules_result_dictionary**: A dictionary containing the total number of hours that the function compares, the number of hours schedule_1 matches schedule_2 with the comparison_factor, EFLH difference (EFLH_schedule_1 / EFLH_schedule_2) for schedule_1 and schedule_2, i.e. {"TOTAL_HOURS_COMPARED": total_hours_compared, "TOTAL_HOURS_MATCH": total_hours_match, "EFLH_DIFFERENCE: EFLH_difference}

Function Call:

- get_schedule_8760_values_array()

Data Lookup: None

Logic:

- Get 8760 hourly values array for schedule_1, schedule_2 and mask_schedule: `hourly_value_sch_1 = get_schedule_8760_values_array(schedule_1), hourly_value_sch_2 = get_schedule_8760_values_array(schedule_2), hourly_value_mask_sch = get_schedule_8760_values_array(mask_schedule)`

- For each hour in mask_schedule's hourly values array: `for hourly_value in hourly_value_mask_sch:`

  - If hourly value in mask_schedule is 1: `if hourly_value == 1:`

    - Add to the pool of hours need comparison: `total_hours_compared += 1`

    - Add to schedule_1 and schedule_2 EFLH numbers: `EFLH_schedule_1 += hourly_value_sch_1, EFLH_schedule_2 += hourly_value_sch_2`

    - If schedule_1 hourly value is equal to schedule_2, save to the pool of hours that meets requirement: `if hourly_value_sch_1 == hourly_value_sch_2: total_hours_match += 1`

- Calculate the EFLH difference for schedule_1 and schedule_2: `EFLH_difference = EFLH_schedule_1 / EFLH_schedule_2`

- Save the total number of hours compared, the number of hours that meets requirement, EFLH difference for schedule_1 and schedule_2 to output dictionary: `compare_schedules_result_array = {"TOTAL_HOURS_COMPARED": total_hours_compared, "TOTAL_HOURS_MATCH": total_hours_match, "EFLH_DIFFERENCE": EFLH_difference}`

**Returns** compare_schedules_result_array

**[Back](../_toc.md)**

**Notes:**
1. mask_schedule might need to be for each second for future RDS.
