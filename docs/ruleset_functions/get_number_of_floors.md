# get_number_of_floors
**Schema Version:** 0.0.22  

**Description:** gets the number of floors in the building

**Inputs:**
- **RMD**

**Returns:**  
- **result**: an integer indicating the number of floors
 
**Function Call:**

## Logic:
- create a set of the floor names.  We use a set because only unique elements can be added to the set: `floor_names = set()`
- loop through the building segments: `for segment in RMD.building.building_segments:`
	- loop through the zones: `for zone in segment.zones:`
		- add the floor name to the set of floor names.  If the floor name is already in the set, nothing happens at this step: `floor_names.add(zone.floor_name)`
- the number of items in the set equals the number of floors in the building.  Set result equal to the length of the set: `result = len(floor_names)`


**Returns** `result`


**Notes/Questions:**  

**[Back](../_toc.md)**
