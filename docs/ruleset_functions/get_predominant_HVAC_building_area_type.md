# get_predominant_HVAC_building_area_type

**Description:** references the `get_HVAC_building_area_types_and_zones` function, and then sorts the list by area
- returns a String `predominant_HVAC_building_area_type` which is one of the HVAC building area types
- used to verify the correct type of HVAC baseline system (or systems)

**Inputs:**  
- **building_area_types_and_zones_dict** - this is a dictionary of the building area types, zones and total area of the BAT in the format given by the function get_HVAC_building_area_types_and_zones

**Returns:**  
- **predominant_HVAC_building_area_type**: A String of the predominant HVAC building area type, defined as the building area type with the largest floor area
 
**Function Call:** 
- **get_HVAC_building_area_types_and_zones**

## Logic:  

- call get_HVAC_building_area_types_and_zones and sort the list: `sorted_list = sorted(building_area_types_and_zones_dict.items(), key=lambda x: x[1]["AREA"], reverse = True)`
- the first item in the list will be the building area type with the largest area: `predominant_HVAC_building_area_type = sorted_list[0][0]`
	
	 **Returns** `return predominant_HVAC_building_area_type`  

**[Back](../_toc.md)**
