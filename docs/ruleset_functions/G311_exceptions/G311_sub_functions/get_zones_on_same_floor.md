# get_zones_on_same_floor  

**Description:** Provides a list of zones that are on the floor as the starting zone

**Inputs:**  
- **U,P,or B-RMI**: The RMD in which the fan system object is defined. 
- **source_zone**: The zone for which we want to find all other zones on the same floor

**Returns:**  
- **zones_on_same_floor**: Returns a list of zones that are on the same floor as the starting zone.  The list will include the starting zone.   
 
**Function Call:** 

## Logic:  

- create list of zones on the same floor: `zones_on_same_floor`
- find the source zone floor name: `source_zone_floor_name = source_zone.floor_name`
- look through each building: `for building in RMI.buildings:`
  - look through each building segment: `for building_segment in building.building_segments:`
    - look through each zone: `for zone in building_segment:`
      - if the zone floor name is the same as the source zone floor name: `if zone.floor_name = source_zone_floor_name:`
        - add the zone id to the list: `zones_on_same_floor.append zone`

**Returns** `return zones_on_same_floor`  

**Comments/Questions**  Finalization of this function is awaiting guidance on the methodology used to group zones by floor (ie by floor_name, or by elevation, or by another metric)

**alternate logic based on zone elevation**

as the zone by checking whether the zone elevation is within 7.5' / 2 (3.25') of our zone - this is more or less the same logic used in the function get_number_of_floors: `if zone.elevation - 3.25 < z.elevation < zone.elevation + 3.25:`


**[Back](../_toc.md)**
