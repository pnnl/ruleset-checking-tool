# get_hvac_system_with_longest_fan_schedule

**Description:** Returns the HeatingVentilationAirAconditioningSystem.id associated with a zone (function input) in the RMR (function input) that has the longest fan schedule.

**Inputs:**
- **zone_x.id**: A zone id associated with the RMR to determine the HeatingVentilationAirAconditioningSystem.id that has the longest fan schedule.
- **U,P, or B-RMR**: to determine the HeatingVentilationAirAconditioningSystem.id that has the longest fan schedule for a specific zone in the specified RMR.

**Returns:**
- **hvac_system_with_longest_fan_schedule_x**: the HeatingVentilationAirAconditioningSystem.id of the hvac system with the longest fan schedule serving a specific zone.
 
**Function Call:**

1. get_list_hvac_systems_associated_with_zone()

**Logic:**

- Get list of the hvac systems serving the zone in the RMR that was input to the function: `heating_ventilation_air_conditioning_systems_list_x = get_list_hvac_systems_associated_with_zone(x_RMR, zone_x.id)`

# Determine which of the hvac systems has the longest fan schedule
- For each hvac_x in heating_ventilation_air_conditioning_systems_list_x: `for hvac_x in heating_ventilation_air_conditioning_systems_list_x:`
    - Set fan_schedule_x to zero: `fan_schedule_x =0`       
    - For each value in the fan_schedule associated with the fan system associated with the hvac system: `for x in len(hvac_x.FanSystem[0].operating_schedule.hourly_values):`
        - Sum value for each hour in the fan operating schedule: `fan_schedule_x = fan_schedule_x + hvac_x.fan_systems[0].operating_schedule.hourly_values(x)`
    - Add sum to dictionary with the hvac system id as key and fan_schedule_x as value: `hvac_fan_schedule_dict[hvac_x.ID] = fan_schedule_x`
- Find the key for the hvac system with the longest schedule associated with zone_x: `hvac_system_with_longest_fan_schedule_x = max(hvac_fan_schedule_dict, key = hvac_fan_schedule_dict.get())`

 **Returns** `return hvac_system_with_longest_fan_schedule_x`  

**[Back](../_toc.md)**
