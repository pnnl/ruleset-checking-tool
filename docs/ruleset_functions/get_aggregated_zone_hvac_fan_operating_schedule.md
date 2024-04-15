# get_aggregated_zone_hvac_fan_operating_schedule

**Description:** This function loops through all of the HVAC system fan operating schedules associated with a specific zone and creates an aggregated fan operating schedule for the zone. More specifically, if any of the fan operating schedules associated with any of the hvac systems serving the zone have a 1 for a particular hour of the year then the aggregated schedule will equal 1 for that particular hour of the year. The function will check this for each hour of the year and return an 8760 aggregated fan operating schedule. 

**Inputs:**
- **zone_x.id**: A zone id associated with the RMR for which to create the aggregated fan operating schedule as described above.
- **U,P, or B-RMR**: used to create the aggregated fan operating schedule for the specified zone.

**Returns:**
- **aggregated_zone_hvac_fan_operating_schedule_x**: 8760 aggregated fan operating schedule for the zone.
 
**Function Call:**

1. get_list_hvac_systems_associated_with_zone()

**Logic:**
- Create an object from the RMR that was input to the function: `X_RMR = RMR`
- Get list of the hvac systems serving the zone in the X_RMR: `heating_ventilating_air_conditioning_systems_list_x = get_list_hvac_systems_associated_with_zone(X_RMR, zone_x.id)`
- Get the number of hvac systems serving the zone: `num_hvac_systems_x = len(heating_ventilating_air_conditioning_systems_list_x)`
- Loop through each hvac system and create a list of fan system operating schedule 8760 hourly values (this is basically a list containing lists of 8760 values for each fan system) for each fan system: `for hvac_x in heating_ventilating_air_conditioning_systems_list_x:`
    - Get the fan system associated with the hvac system: `fan_systems_x = hvac_x.fan_system[0].id`
    - Get he fan schedule associated with the fan system: `fan_schedule_x = fan_system_x.operating_schedule`
    - Get the list of hourly values associated with the fan schedule (convert to an 8760 schedule using a function if needed): `fan_schedule_hourly_values_x = fan_schedule_x.hourly_values`
    - Add the list of hourly values to the list of fan system schedules: `hourly_schedule_values_list= hourly_schedule_values_list.append(fan_schedule_hourly_values_x)`
- Loop through each hour of the year to create the aggregated schedule: `For x in Range(8760):`
    - Reset hour equals one boolean variable: `hour_equals_one = FALSE`
    - Loop through each fan schedule for this hour to check if it equals one: `For y in Range(num_hvac_systems_x):`
        - Check if the value equals 1: `if hourly_schedule_values_list[y][x] = 1: hour_equals_one = TRUE`
    - If the hour equals one boolean variable equals true then set the value in the aggregated schedule equal to one for this hour, otherwise set it equal to 0: `if hour_equals_one == True:aggregated_zone_hvac_fan_operating_schedule_x[x] = 1`   
    - Else: `Else: aggregated_zone_hvac_fan_operating_schedule_x[x] = 0`

 **Returns** `return aggregated_zone_hvac_fan_operating_schedule_x`  

**[Back](../_toc.md)**
