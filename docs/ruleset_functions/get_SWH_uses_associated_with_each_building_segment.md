## get_SWH_uses_associated_with_each_building_segment

Description: This function gets all the SWH uses connected to a building segment.  This function is primarily to encapsulate getting service water heating uses in one function so that if a change is made in the schema as to how service water heating use is specified, the RCT only needs to change in one place.   

Inputs:
- **RMD**
- **building_segment_id** - the id of the building segment

Returns:
- **swh_uses**: A list containing the served_by_distribution_systems of all service water heating uses associated with a building segment  

Function Call:
- get_obj_by_id  

Data Lookup: None

Logic:
- get the building segment: `building_segment = get_obj_by_id(RMD, building_segment_id)`
- create a blank list: `swh_uses = []`
- look at each swh use: `for served_by_distribution_system in building_segment.service_water_heating_uses.served_by_distribution_system:`
    - append the use to the list: `swh_uses.append(served_by_distribution_system)`


**Returns** swh_uses

**[Back](../_toc.md)**

**Notes:**
