# zone_meets_G3_1_1g_part1
**Schema Version:** 0.0.22  

**Description:** returns a boolean value indicating whether the zone meets G3_1_1g_part1 - "If the baseline HVAC system serves HVAC zones that includes computer rooms,  baseline system 11 shall be used where the baseline HVAC system type is 7 or 8 and the total computer room peak cooling load is greater than 600,000 BTU/h (175 kW)."

**Inputs:** 
- **B_RMI**
- **zone_id**

**Returns:**  
- **result**: an enum - either YES or NO

**Function Call:**
- **find_zone**
- **zones_with_computer_room_dict_x**

## Logic:
- set the result variable to NO - only a positive test can give it a different value: `result = NO`
- determine whether the zone is a computer room using the function zones_with_computer_room_dict_x to get a list of zones including computer rooms: `computer_room_zones_dict = zones_with_computer_room_dict_x(B_RMI)`
  - if the zone.id is in the computer_room_zones_dict, then this is a computer room zone and it is not eligible: `if zone.id in computer_room_zones_dict:`
   - get the one: `zone = get_zone(zone_id)`
   - now determine whether the peak cooling load is above the threshold of 600,000 btu/hr: `if zone.peak_cooling_load > 600000:`
    - set result to YES: `result = YES`

**Returns** `result`

**[Back](../_toc.md)**
