# get_computer_zones_peak_cooling_load
**Schema Version:** 0.0.22  

**Description:** return peak load of computer zones in the building

**Inputs:** 
- **B_RMI**

**Returns:**  
- **result**: computer peak load

**Function Call:**
- **get_zones_computer_rooms**
- **get_zone_peak_internal_load**

## Logic:
- get the list of zones with computer rooms using the function get_zones_computer_rooms to get a list of zones including computer rooms: `computer_room_zones_dict = get_zones_computer_rooms(B_RMI)`
    - create a variable for the total peak computer room load: `total_computer_peak_cooling_load = 0`
    - loop through the computer room zones: `for computer_room_zone_id in computer_room_zones_dict:`
        - get the zone: `computer_room_zone = get_component_by_id(computer_room_zone_id)`
        - get the peak internal load for the computer_room_zone by calling the function get_zone_peak_internal_load (units are btu/sf/hr): `zone_peak_internal_load = get_zone_peak_internal_load_floor_area(B_RMI, computer_room_zone)["PEAK"]`
        - add the zone_peak_internal_load to the total_computer_peak_cooling_load: `total_computer_peak_cooling_load += zone_peak_internal_load`
    - return the computer peak load `return total_computer_peak_cooling_load`

**Returns** `total_computer_peak_cooling_load`


**[Back](../_toc.md)**
