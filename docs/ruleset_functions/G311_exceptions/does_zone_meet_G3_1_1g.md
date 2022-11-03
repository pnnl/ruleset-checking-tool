# does_zone_meet_G3_1_1g
**Schema Version:** 0.0.22  

**Description:** returns a boolean value indicating whether the zone meets G3_1_1g:
  **part1:** "If the baseline HVAC system serves HVAC zones that includes computer rooms,  baseline system 11 shall be used where the baseline HVAC system type is 7 or 8 and the total computer room peak cooling load is greater than 600,000 BTU/h (175 kW) AND <= 3,000,000"
  **part 2:** If the baseline HVAC system serves HVAC zones that includes computer rooms,  Baseline System 11 shall be used for such HVAC zones in buildings with a total computer room peak cooling load >greater than 3,000,000 Btu/h.
  **part 3:** If the baseline HVAC system serves HVAC zones that includes computer rooms,  baseline system 3 or 4 shall be used for all HVAC zones where the computer room peak cooling load is= <600,000 Btu/h

**Inputs:** 
- **B_RMI**
- **zone_id**
- **starting_system_type**

**Returns:**  
- **result**: an enum - either NO or G1, G2, G3 for the 3 parts

**Function Call:**
- **get_component_by_id**
- **get_zones_computer_rooms**

## Logic:
- set the result variable to NO - only a positive test can give it a different value: `result = NO`
- determine whether the zone is a computer room using the function get_zones_computer_rooms to get a list of zones including computer rooms: `computer_room_zones_dict = get_zones_computer_rooms(B_RMI)`
  - if the zone.id is in the computer_room_zones_dict, then this is a computer room zone and it is not eligible: `if zone.id in computer_room_zones_dict:`
   - set result to G3 only if the starting_system_type is SYS-7 or SYS-8: `result = G3 if starting_system_type in ["SYS-7","SYS-8"]`
   - get the zone: `zone = get_component_by_id(zone_id)`
   - now determine whether the peak cooling load is above the threshold of 3,000,000 btu/hr: `if zone.peak_cooling_load > 3000000:`
    - set result to G1: `result = G1`
   - else, if the load is greater than 600,000, it's G2: `elsif zone.peak_cooling_load > 600000:`
    - set the result to G2: `result = G2`
   - else it's G3: `else:`
    - set the result to G3: `result = G3` 

**Returns** `result`

**[Back](../_toc.md)**
