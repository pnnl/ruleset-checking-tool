# is_zone_a_vestibule
**Schema Version:** 0.0.23  

**Description:** following the guidelines in ASHRAE that a vestibule is defined as a sapce with at least one exterior door and with a surface area of no more than the greater of 50ft2 or 2% of the total area of the floor.  There is no 100% check for a vestibule, so a space that meets these requirements and also has only 6 surfaces (floor, ceiling and 4 walls) will return False

We will also check that the lighting space type is in agreement with the space use as a vestibule.  If there is no lighting space type or one of the following lighting space types AND the zone meets the other checks then we return MAYBE:
	- CORRIDOR_FACILITY_FOR_THE_VISUALLY_IMPAIRED
	- CORRIDOR_HOSPITAL
	- CORRIDOR_ALL_OTHERS
	- LOBBY_FACILITY_FOR_THE_VISUALLY_IMPAIRED
	- LOBBY_HOTEL
	- LOBBY_MOTION_PICTURE_THEATER
	- LOBBY_PERFORMING_ARTS_THEATER
	- LOBBY_ALL_OTHERS
	- STAIRWELL
	

**Inputs:**  
- **zone**: the zone to be tested
- **RMR**: the building

**Returns:**  
- **vestibule_check**: boolean, False means NO, True means MAYBE
 
**Function Call:** 
- **get_zones_on_same_floor**

 
## setup for all function calls:
- make a list of the allowable space types: `allowable_space_lighting_types = [CORRIDOR_FACILITY_FOR_THE_VISUALLY_IMPAIRED, CORRIDOR_HOSPITAL, CORRIDOR_ALL_OTHERS, LOBBY_FACILITY_FOR_THE_VISUALLY_IMPAIRED, LOBBY_HOTEL, LOBBY_MOTION_PICTURE_THEATER, LOBBY_PERFORMING_ARTS_THEATER, LOBBY_ALL_OTHERS, STAIRWELL]

## Logic: 
- check if the zone spaces have either no lighting space type, or a lighting space type on the allowable_space_lighting_types list.  Start by looping through the spaces in the zone: `for space in zone.spaces:`
	- check if the space lighting type is NOT either Null or one of the allowable types in the list: `if not(space.lighting_space_type == Null or space.lighting_space_type in allowable_space_lighting_types):`
		- this is not an eligible space type, the function can return NO right away: `return False`

- if the function makes it this far, the zone contained only vestibule-compatible spaces and we continue with the rest of the vestibule check below

- make a list of the surface adjacencies that would qualify a space as exterior: `surface_adjacencies = [SurfaceAdjacentToOptions.EXTERIOR]
- set result to NO: `vestibule_check = False`
- create a variable to store the surface area of exterior doors: `exterior_door_surface_area = 0`
- first check if there is an exterior door in the zone by looping through the zone surfaces and then subsurfaces: `for surface in zone.surfaces:`
	if surface is exterior, check if there is door on the surface: `if surface.adjacent_to in surface_adjacencies:`
		- loop through the zone subsurfaces: `for subsurface in subsurfaces:`
			- check if the subsurface is a door: `if subsurface.classification == SubsurfaceClassificationOptions.DOOR:`
				- add the glazed and opaque area of the exterior door to the exterior_door_surface_area variable: `exterior_door_surface_area += subsurface.glazed_area + subsurface.opaque_area`
				
- if there were exterior doors, the exterior_door_surface_area will be greater than 0: `if exterior_door_surface_area > 0:`
	- create a variable for the total floor area: `floor_area = 0`	
	- get a list of zones on the same floor: `zones_on_same_floor = get_zones_on_same_floor(B_RMI, zone)`
	- loop through the building adding the floor area of all zones on the same floor as the zone: `for building_segment in RMR.building_segments:`
		- loop through the zones: `for z in building_segment:`
			- check of z is on the same floor by checking whether it is in the list of zones on the same floor: `if z in zones_on_same_floor:`
				- loop through the z spaces adding the area to the floor_area: `for space in z.spaces:`
					- add space area to floor_area: `floor_area = floor_area + space.floor_area`
	- create a variable for the target zone's area: `zone_area = 0`
	- find the floor area of the target zone by adding the floor area of the target zone's spaces: `for space in zone.spaces:`
		- add the space's floor area to zone_area: `zone_area = zone_area + space.area`
	- create a variable that equals that maximum vestibule floor area, which is the larger of 50ft2 or 2% of the floor area: `max_vestibule_area = max(50,0.02*floor_area)`
	- if the zone_area is less than or equal to max_vestibule_area, then this could be a vestibule: `if zone_area <= max_vestibule_area:`
		- this zone is possibly a vestibule.  Set vestibule check to MAYBE: `vestibule_check = True`


	 **Returns** `return vestibule_check`  

**Notes/Questions:**  



**[Back](../_toc.md)**
