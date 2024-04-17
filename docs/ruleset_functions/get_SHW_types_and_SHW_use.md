
## get_SHW_types_and_SHW_use

Description: This function gets all the SHW Uses and the SHW space types and sorts them into a dictionary where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 and values are a list if ServiceWaterHeatingUse.ids  

Inputs:
- **RMD**

Returns:
- **shw_and_SHW_use_dict**: A dictionary containing where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 in the RMD and values are lists of space ids.  Example:  
{"DORMITORY":["swh1","swh2","shw3"], "AUTOMOTIVE_FACILITY":["shwg1","shwg2","shwg3"]}

Function Call:

- get_SHW_types_and_spaces
- get_obj_by_id

Data Lookup: None

Logic:
- get the dictionary of SHW types and space ids from the function get_SHW_types_and_spaces: `shw_types_and_spaces_dict = get_SHW_types_and_spaces(RMD)`
- create a blank dictionary: `shw_and_SHW_use_dict = {}`
- look at space type in shw_types_and_spaces_dict: `for shw_use_type in shw_types_and_spaces_dict:`
    - create the blank list for the shw_use_type: `shw_types_and_spaces_dict[shw_use_type] = []`
    - look at each space: `for sp_id in shw_types_and_spaces_dict[shw_use_type]:`
        - get the space using get_obj_by_id: `space = get_obj_by_id(RMD, sp_id)`
        - get the service_water_heating_uses from the space and append them to the list using extend: `shw_and_SHW_use_dict[shw_use_type].extend space.service_water_heating_uses`

**Returns** shw_and_SHW_use_dict

**[Back](../_toc.md)**

**Notes:**

