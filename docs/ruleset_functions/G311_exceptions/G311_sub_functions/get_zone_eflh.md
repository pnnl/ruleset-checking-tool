# get_zone_eflh

**Description:** provides the equivalent full load hours of the zone.  Equivalent full load hours are defined as: any hour where the occupancy fraction is greater than 5% AND the HVAC system is in occupied mode.  For this function, we are recognizing the HVAC system as being in occupied mode if ANY of the HVAC systems serving the zone are in occupied mode.
**Applicability Note:** hvac_system.fan_system.operation_schedule is being used as the HVAC operation schedule.  Therefore, this check will not work for radiant systems or other systems that do not include a fan

**Inputs:** 
- **RMI**
- **zone**

**Returns:**  
- **flh**: a number equal to the total equivalent full load hours for the year
 
**Function Call:**
- **get_list_hvac_systems_associated_with_zone**

## Logic:
- create a dictionary to hold information about the occupancy of each space: `people_info_for_spaces = {}`
- create a variable for the total number of zone occupants: `total_zone_occupants = 0`
- loop through the spaces in the zone collecting information about occupancy: `for space in zone.spaces:`
  - find the maximum schedule value accross the schedule hourly_values, design days and the number 1: `maximum_occupancy_schedule_value = max(max(space.occupant_multiplier_schedule.hourly_values), max(space.occupant_multiplier_schedule.hourly_heating_design_day), max(space.occupant_multiplier_schedule.hourly_cooling_design_day),1)`
  - add the maximum number of occupants of this space to the total number of zone occupants: `total_zone_occupants += space.number_of_occupants * maximum_occupancy_schedule_value`
  - append the information about the occupancy to the list - this takes the number of people assigned to the space, multipled by the maximum schedule value - which will be either 1, or a number greater than 1 if one of the schedules (hourly, heating design day, or cooling design day) has a value(s) greater than 1: `people_info_for_spaces[space]["NUM_OCCUPANTS] = space.number_of_occupants * maximum_occupancy_schedule_value`
  - `people_info_for_spaces[space]["SCHEDULE_HOURLY_VALUES"] = space.occupant_multiplier_schedule.hourly_values`
- get the list of the hvac systems associated with the zone: `hvac_systems_list = get_list_hvac_systems_associated_with_zone(RMI,zone.id)`
- create an index to which each full load hour will be added: `flh = 0`
- now create a variable num_hours_in_year which will take the number of hours in the schedule for the first (really any) space in people_info_for_spaces: `num_hours_in_year = len(people_info_for_spaces[list(people_info_for_spaces.keys())[0]]["SCHEDULE_HOURLY_VALUES"])`
- now calculate flh for each hour of the year: `for hour in range(num_hours_in_year):`
  - calculate the number of people in the zone this hour: `occupants_this_hour = 0`
  - loop through the people_info_for_spaces: `for space in people_info_for_spaces:`
    - multiply the max number of people in this space by the schedule value and add it to people_this_hour: `occupants_this_hour += space_people_info[space]["NUM_OCCUPANTS"] * space_people_info[space]["SCHEDULE_HOURLY_VALUES"][hour]`
  - check if the people this hour is greater than 5%: `if((occupants_this_hour / total_zone_occupants)>0.05:`
    - now check to see if there are any HVAC systems that are operational this hour.  Create a boolean: `hvac_systems_operational_this_hour = FALSE`
    - loop through the hvac_systems_list: `for hvac_system in hvac_systems_list:`
      - check if the hvac system has a fan system: `if hvac_system.fan_system != NULL:`
        - check if the HVAC system fan operating schedule is greater than 1 this hour: `if hvac_system.fan_system.operation_schedule[hour] == 1:`
          - the system is operational this hour, set the boolean to TRUE: `hvac_systems_operational_this_hour = TRUE`
    - check if the boolean is true: `if hvac_systems_operational_this_hour:`
      - add the hour to the flh: `flh += 1`

**Returns** `flh`

**Questions:**

**[Back](../_toc.md)**
