# does_zone_meet_G3_1_1g
**Schema Version:** 0.0.22  

**Description:** returns a boolean value indicating whether the zone meets G3_1_1g:
 
**part1:** "If the baseline HVAC system serves HVAC zones that includes computer rooms,  baseline system 11 shall be used where the baseline HVAC system type is 7 or 8 and the total computer room peak cooling load is greater than 600,000 BTU/h (175 kW) AND <= 3,000,000"

**part 2:** If the baseline HVAC system serves HVAC zones that includes computer rooms,  Baseline System 11 shall be used for such HVAC zones in buildings with a total computer room peak cooling load greater than 3,000,000 Btu/h.

**part 3:** If the baseline HVAC system serves HVAC zones that includes computer rooms,  baseline system 3 or 4 shall be used for all HVAC other zones - that is zones where the computer room peak cooling load is= <600,000 Btu/h, and when the peak cooling load is between 600,000 btu/hr and 3,000,000 btu/hr and the baseline system type is not system 7 or 8.

**Inputs:** 
- **B_RMI**
- **zone_id**
- **starting_system_type**

**Returns:**  
- **result**: an enum - either NO or G1, G2, G3 for the 3 parts

**Function Call:**
- **get_component_by_id**
- **get_computer_zones_peak_cooling_load**
- **get_zones_computer_rooms**

## Logic:
- set the result variable to NO - only a positive test can give it a different value: `result = NO`
- get the list of zones with computer rooms using the function get_zones_computer_rooms to get a list of zones including computer rooms: `computer_room_zones_dict = get_zones_computer_rooms(B_RMI)`
- if the zone_id is in the computer_room_zones_dict, then this is a computer room zone and it is eligible: `if zone_id in computer_room_zones_dict:`
  - add the zone_peak_internal_load to the total_computer_peak_cooling_load: `total_computer_peak_cooling_load = get_computer_zones_peak_cooling_load(rmd, zone_id)`
  - check if the peak load is higher than 600,000 btu/hr `if total_computer_peak_cooling_load > 600,000 btu/hr: result = True`
  
    ```
    all these logic will move to the zone target basline function.
          - now determine which threshold (G1,G2,G3) the building meets
      - check if the total building peak computer cooling load is greater than 3,000,000 btu/hr: `if total_computer_peak_cooling_load > 3000000:`
          - set the result to G2: `result = G2`
      - else if the `starting_system_type` is SYS-7 or SYS-8 and the load is greater than 600,000 btu/hr: `elsif starting_system_type in ["SYS-7","SYS-8"] and total_computer_peak_cooling_load > 600000:`
          - set the result to G1: `result = G1`
      - the last category, G3 is a catch-all: `else:`
          - set the result to G3: `result = G3`
    
    ```
  
**Returns** `result`


**[Back](../_toc.md)**
