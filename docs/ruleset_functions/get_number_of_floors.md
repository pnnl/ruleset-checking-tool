# get_number_of_floors
**Schema Version:** 0.0.28  

**Description:** gets the number of floors in the building.  Parking Garages are not counted

**Inputs:**  
- **RMI**: The baseline ruleset model instance

**Returns:**  
- **result**: an integer indicating the number of floors
 
**Function Call:**
- **get_zone_conditioning_category**

## Logic:
- check to see if Building.number_of_floors_above_grade and Building.number_of_floors_below_grade exisits, if so, the sum of these two numbers will be returned. `if Building.number_of_floors_above_grade != null && Building.number_of_floors_below_grade != null:`
	- set result equal to the number of floors above grade plus the number of floors below grade: `result = Building.number_of_floors_above_grade + null && Building.number_of_floors_below_grade`
- otherwise, the number of floors is not explicitly stated, count the number of floors based on floor_name:
	- use the function get_zone_conditioning_category to get a dictionary of zone id's and their conditioning category - we will only include conditioned zones in the building_area_types_with_total_area_and_zones_dict: `zone_conditioning_category_dict = get_zone_conditioning_category(RMI)`
	- create a set of the floor names.  We use a set because only unique elements can be added to the set: `floor_names = set()`
	- loop through the building segments: `for segment in RMI.building.building_segments:`
		- loop through the zones: `for zone in segment.zones:`
			- using zone_conditioning_category_dict, check if the zone is conditioned or semi-heated. `if zone_conditioning_category_dict[zone.id] == "CONDITIONED RESIDENTIAL" || zone_conditioning_category_dict[zone.id] == "CONDITIONED NON-RESIDENTIAL" || zone_conditioning_category_dict[zone.id] == "CONDITIONED MIXED" || zone_conditioning_category_dict[zone.id] == "SEMI-HEATED"`:
				- loop through the spaces in the zone: `for space in zone:`
					- eligible zones are zones that are not parking garage zones if any of the spaces are not PARKING_AREA_INTERIOR, then this zone is not exclusively a parking garage space: `if space.lighting_space_type != PARKING_AREA_INTERIOR:`
						- add the floor name to the set of floor names.  It doesn't matter if the floor name is already in the set, because a set, by definition can only have one of each item: `floor_names.add(zone.floor_name)`
	- the number of items in the set equals the number of floors in the building.  Set result equal to the length of the set: `result = len(floor_names)`

**Returns** `result`

**Notes/Questions:**  
1. Relies on a variable that is not currently in the schema: zone.elevation

**[Back](../_toc.md)**

**Notes**
1.  NOTE TO DEV TEAM - if there are not entries for either (Building.number_of_floors_above_grade AND Building.number_of_floors_below_grade) or (floor_names for every zone and space.lighting_space_type for all spaces), then we cannot evaluate with certainty the number of floors and none of the rules that rely on this function can be evaluated.
2.  function get_hvac_systems_5_6_serving_multiple_floors_b() also relies on logic to determine the number of floors.  Suggest modifying to call get_number_of_floors
3.  function depends on adding `number_of_floors_above_grade` and `number_of_floors_below_grade` at the Building level.  Issue #185 was created to address this.
