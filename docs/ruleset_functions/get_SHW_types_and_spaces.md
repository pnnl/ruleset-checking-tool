
## get_SHW_types_and_spaces

Description: This function gets all the spaces and the SHW space types and sorts them into a dictionary where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 and values are a list if space.ids  

Inputs:
- **RMD**

Returns:
- **shw_and_spaces_dict**: A dictionary containing where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 in the RMD and values are lists of space ids.  Example:  
{"DORMITORY":["sp1","sp2","sp3"], "AUTOMOTIVE_FACILITY":["g1","g2","g3"]}

Function Call:

- 

Data Lookup: None

Logic:

- create a blank dictionary: `shw_and_spaces_dict = {}`
- look at each space in the RMD: `for space in RMD...spaces:`
    - get the shw heating space type: `shw_heating_space_type = space.service_water_heating_space_type`
    - create the list in shw_and_spaces_dict for this space type if it doesn't exist: `shw_and_spaces_dict.set_default(shw_heating_space_type, [])`
    - append the space id to the list: `shw_and_spaces_dict[shw_heating_space_type].append(space.id)

**Returns** shw_and_spaces_dict

**[Back](../_toc.md)**

**Notes:**

