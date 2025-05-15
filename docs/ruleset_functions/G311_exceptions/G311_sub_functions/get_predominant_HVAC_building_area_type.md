# get_predominant_HVAC_building_area_type

**Description:** returns a String `predominant_HVAC_building_area_type` which is one of the HVAC building area types
- used to verify the correct type of HVAC baseline system (or systems)

**Inputs:**  
- **climate_zone** Climate Zone
- **RMI** 

**Returns:**  
- **predominant_HVAC_building_area_type**: A String of the predominant HVAC building area type, defined as the building area type with the largest floor area
 
**Function Call:** 
- **get_HVAC_building_area_types_and_zones**

## Logic:  

- call get_HVAC_building_area_types_and_zones `building_area_types_and_zones_dict = get_HVAC_building_area_types_and_zones(climate_zone, rmd)`
- sort the dict based on floor area size: `sorted_list = sorted(building_area_types_and_zones_dict.items(), key=lambda x: x[1]["AREA"], reverse = True)`
- the first item in the list will be the building area type with the largest area: `predominant_HVAC_building_area_type = sorted_list[0][0]`
	
     **Returns** `return predominant_HVAC_building_area_type`  

**[Back](../_toc.md)**
