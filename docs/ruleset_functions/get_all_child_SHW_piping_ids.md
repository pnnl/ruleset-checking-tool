## get_all_child_SHW_piping_ids  
  
Description: This function gets all the piping and child piping connected to SHW piping.  The ids of all of the piping is stored in a list
Inputs:
- **RMD**  
- **piping_id**  

Returns:  
- **piping_ids**: A list of all of the ids of the SHW piping connected to the given piping_id.  The list includes the original piping_id.  Example:  
["piping1","piping2"]

Function Call:

- get_obj_by_id
- get_all_child_SHW_piping_ids

Data Lookup: None

Logic:  
- get the piping object using get_object_by_id: `piping = get_obj_by_id(RMD, piping_id)`
- create the list: `piping_ids = [piping_id]`
- for each child ServiceWaterPiping, call this function, and extend the piping_ids list with the results: `for child_piping in piping.child:`
    - call this function with the child id: `child_ids = get_all_child_SHW_piping_ids(RMD, child_piping.id)`
    - extend the piping_ids list with the child_ids: `piping_ids.extend(child_ids)`

**Returns** piping_ids

**[Back](../_toc.md)**

**Notes:**
