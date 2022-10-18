# is_zone_a_vestibule
**Schema Version:** 0.0.22  

**Description:** following the guidelines in ASHRAE that a vestibule is defined as a sapce with at least one exterior door and with a surface area of no more than the greater of 50ft2 or 2% of the total area of the floor.  There is no 100% check for a vestibule, so a space that meets these requirements and also has only 6 surfaces (floor, ceiling and 4 walls) will return "LIKELY" - one that meets the official requirements but has more surfaces will return "POSSIBLY"

**Inputs:**  
- **zone**: the zone to be tested
- **RMR**: the building

**Returns:**  
- **vestibule_check**: A String with either "NO" or "LIKELY" OR "MAYBE"
 
**Function Call:** None

## Logic:  

- make a list of the surface adjacencies that would qualify a space as exterior: `surface_adjacencies = [SurfaceAdjacentToOptions.EXTERIOR]
- set result to "NO": `vestibule_check = "NO"`
- set has_exterior_door boolean to FALSE: `has_exterior_door = FALSE`
- first check if there is an exterior door in the zone by looping through the zone surfaces and then subsurfaces: `for surface in zone.surfaces:`
	if surface is exterior, check if there is door on the surface: `if surface.adjacent_to in surface_adjacencies:`
		- loop through the zone subsurfaces: `for subsurface in subsurfaces:`
			- check if the subsurface is a door: `if subsurface.classification == SubsurfaceClassificationOptions.DOOR:`
				- set has_exterior_door to TRUE: `has_exterior_door = TRUE`
				- break out of the loop (all we need is one exterior door to qualify as a vestibule): `break`

- if there is an exterior door, check the floor area requirement: `if has_exterior_door == TRUE:`
	- create a variable for the total floor area: `floor_area = 0`	
	- loop through the building adding the floor area of all zones on the same floor as the zone: `for building_segment in RMR.building_segments:`
		- loop through the zones: `for z in building_segment:`
			- check of z is on the same floor as the zone: `if z.floor_name == zone.floor_name:`
				- loop through the z spaces adding the area to the floor_area: `for space in z.spaces:`
					- add space area to floor_area: `floor_area = floor_area + space.floor_area`
	- create a variable for the target zone's area: `zone_area = 0`
	- find the floor area of the target zone by adding the floor area of the target zone's spaces: `for space in zone.spaces:`
		- add the space's floor area to zone_area: `zone_area = zone_area + space.area`
	- create a variable that equals that maximum vestibule floor area, which is the larger of 50ft2 or 2% of the floor area: `max_vestibule_area = max(50,0.02*floor_area)`
	- if the zone_area is less than or equal to max_vestibule_area, then this could be a vestibule: `if zone_area <= max_vestibule_area:`
		- now check the number of surfaces in the zone.  No more than 6 surfaces means it is very likely a vestibule: `if(len(zone.surfaces.length) <=6):`
			- vestibule_check = "LIKELY"
		- otherwise, this could be a long corridor (for a 40,000 ft2 floor, at 2% suface area & 10 ft wide, it would be 80ft long): `else:`
			- vestibule_check = "POSSIBLY"


	 **Returns** `return vestibule_check`  

**Notes/Questions:**  
1. Do any of the adjacency options from AdditionalSurfaceAdjacentToOptions2019ASHRAE901 need to be included in the list?


**[Back](../_toc.md)**
