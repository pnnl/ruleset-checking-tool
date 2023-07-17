# get_lab_zone_hvac_systems  

**Description:** returns a list of HVAC systems serving only lab zones

**Inputs:**  
- **B_RMI**

**Returns:**  
- **hvac_systems_serving_lab_zones**: A list of hvac system ids where each hvac system serves only lab zones
 
**Function Call:**  

1. get_dict_of_zones_and_terminal_units_served_by_hvac_sys()
2. get_building_lab_zones()

## Logic:   
- use the function `get_building_lab_zones` to get a list of the zones in the building that have lab space types: `building_lab_zones = get_building_lab_zones(B_RMI)`
- create the result variable `hvac_systems_serving_lab_zones`: `hvac_systems_serving_lab_zones = []`
- continue with the logic only if there are lab zones in the building: `if len(building_lab_zones) > 0:`
  - use the function `get_dict_of_zones_and_terminal_units_served_by_hvac_sys` to get a dictionary of HVAC systems and the zones served: `dict_of_zones_and_hvac_systems = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(B_RMI)`
  - loop through each HVAC system: `for hvac_id in dict_of_zones_and_hvac_systems:`
    - get the list of zones served by the HVAC system: `zones_served_by_hvac_system = dict_of_zones_and_havc_systems[hvac_id]["ZONE_LIST"]`
    - now we need to compare this list to the list of lab zones.  If only lab zones are in zones_served_by_hvac_system, then this is a lab-only HVAC system: `if all(hvac_zone in building_lab_zones for hvac_zone in zones_served_by_hvac_system):`
      - this hvac system serves only lab zones, add it to the list: `hvac_systems_serving_lab_zones.append(hvac_id)`

**Returns** `return hvac_systems_serving_lab_zones`

**[Back](../_toc.md)**
