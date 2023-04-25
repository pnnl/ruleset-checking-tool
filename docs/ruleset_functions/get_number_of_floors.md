# get_number_of_floors
**Schema Version:** 0.0.23  

**Description:** gets the number of floors in the building - logic is based on looking at the elevation of zones - zones with an elevation of <0 are considered underground and are not counted.  Parking Garages are not counted

**Inputs:**
- **zone_input_list** - the list of the zones for which we want to get the number of floors (changed from RMI to this so that we can get the number of floors for a limited list of zones, for example for the function get_hvac_systems_5_6_serving_multiple_floors_b)

**Returns:**  
- **result**: an integer indicating the number of floors
 
**Function Call:**

## Logic:
- make a list of eligible zones in the building: `zone_list = []`
	- loop through each zone in the input list: `for zone in zone_input_list: `
		- eligible zones are zones with an elevation greater than zero: `if zone.elevation > 0`
			- loop throught the spaces in the zone: `for space in zone:`
				- eligible zones are zones that are not parking garage zones if any of the spaces are not PARKING_GARAGE, then this zone is not exclusively a parking garage space: `if space.lighting_space_type != PARKING_GARAGE:`
					- add the zone to the zone_list: `zone_list.append(zone)`
					- break out of the loop: `break`

- sort the list by zone elevation: `zone_list.sort(key = lambda x: x.elevation)`

- create an integer num_of_floors: `num_of_floors = 0`

- when we find floors, we'll remove the zones from the zone_list, until there are no more zones in the list, so we create a loop using `while` and the condition `len(zone_list) > 0`: `while len(zone_list) > 0:`
	- the first zone in the list will be the one with the lowest elevation, create variable elevation equal to this first zone's elevation: `elevation = zone_list[0].elevation`
	- until we find a zone with an elevation greater than 7.5' (2.286m) higher than this base elevation, count the zones as being on the same floor - this step insures that zones that have a slightly different elevation, such as a signle step up or down do not get counted as being on different floors: `while zone_list[0].elevation <= elevation + 2.286:`
		- remove the first zone on the list from the master zone_list: `zone_list.remove(zone_list[0])`
		- break out of the loop if there are no more zones in the list: `if len(zone_list) == 0: break`
	- increment the number of floors: `num_of_floors += 1`

**Returns** `result`

**Notes/Questions:**  
1. Relies on a variable that is not currently in the schema: zone.elevation

**[Back](../_toc.md)**


**below is the old logic based on floor names**
- create a set of the floor names.  We use a set because only unique elements can be added to the set: `floor_names = set()`
- loop through the building segments: `for segment in RMI.building.building_segments:`
	- loop through the zones: `for zone in segment.zones:`
		- add the floor name to the set of floor names.  If the floor name is already in the set, nothing happens at this step: `floor_names.add(zone.floor_name)`
- the number of items in the set equals the number of floors in the building.  Set result equal to the length of the set: `result = len(floor_names)`


**Returns** `result`


**Notes**
1.  function get_hvac_systems_5_6_serving_multiple_floors_b() also relies on logic to determine the number of floors.  Suggest modifying to call get_number_of_floors
