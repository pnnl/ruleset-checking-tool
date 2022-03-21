# get_hvac_system_with_longest_fan_schedule_p

**Description:** Returns the HeatingVentilationAirAconditioningSystem.id associated with a zone (function input) in the proposed that has the longest fan schedule.

**Inputs:**
- **zone_p.id**: A zone id associated with the P_RMR to determine the HeatingVentilationAirAconditioningSystem.id that has the longest fan schedule.
- **P-RMR**: to determine the HeatingVentilationAirAconditioningSystem.id that has the longest fan schedule for a specific zone in the P_RMR.

**Returns:**
- **hvac_system_with_longest_fan_schedule_p**: the HeatingVentilationAirAconditioningSystem.id of the hvac system with the longest fan schedule serving a specific zone.
 
**Function Call:**

1. get_list_hvac_systems_associated_with_zone()

**Logic:**
- Get list of the hvac systems serving the zone in the proposed design model: `heating_ventilation_air_conditioning_systems_list_p = get_list_hvac_systems_associated_with_zone(P_RMR, zone_p.id)`

# Determine which of the hvac systems has the longest fan schedule
- For each hvac_p in heating_ventilation_air_conditioning_systems_list_p: `for hvac_p in heating_ventilation_air_conditioning_systems_list_p:`
    - Set fan_schedule_p to zero: `fan_schedule_p =0`       
    - For each value in the fan_schedule associated with the fan system associated with the hvac system: `for x in len(hvac_p.FanSystem[0].operating_schedule.hourly_values):`
        - Sum value for each hour in the fan operating schedule: `fan_schedule_p = fan_schedule_p + hvac_p.fan_systems[0].operating_schedule.hourly_values(x)`
    - Add sum to dictionary with the hvac system id as key and fan_schedule_p as value: `hvac_fan_schedule_dict[hvac_p.ID] = fan_schedule_p`
- Find the key for the hvac system with the longest schedule associated with zone_p: `hvac_system_with_longest_fan_schedule_p = max(hvac_fan_schedule_dict, key = hvac_fan_schedule_dict.get())`

 **Returns** `return hvac_system_with_longest_fan_schedule_p`  

**[Back](../_toc.md)**
