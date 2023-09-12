# get_lab_zone_hvac_systems  

**Description:** returns a list of HVAC systems serving only lab zones

**Inputs:**  
- **B_RMI**  
- **P_RMI**  

**Returns:**  
- **hvac_systems_serving_lab_zones**: A dictionary consisting of two lists of hvac system ids.  One list ["LAB_ZONES_ONLY"] is a list of hvac system ids where each hvac system serves only lab zones.  The other ["LAB_AND_OTHER"] is a list of hvac system ids where systems serve both labs and other zones.
 
**Function Call:**  

1. get_dict_of_zones_and_terminal_units_served_by_hvac_sys()
2. get_zone_target_baseline_system()

## Logic:   
- use the function get_zone_target_baseline_system to get the target baseline system types for each zone.  This will be used when checking for laboratory systems: `target_baseline_systems = get_zone_target_baseline_system(P_RMI, B_RMI)`
- create a list of laboratory zones meeting G3_1_1d: `building_lab_zones = [x for x in target_baseline_systems if target_baseline_systems[x]["SYSTEM_ORIGIN"] == G3_1_1d`
- create the result variable `hvac_systems_serving_lab_zones`: `hvac_systems_serving_lab_zones = {"LAB_ZONES_ONLY": [], "LAB_AND_OTHER": []}`
- continue with the logic only if there are lab zones in the building: `if len(building_lab_zones) > 0:`
  - use the function `get_dict_of_zones_and_terminal_units_served_by_hvac_sys` to get a dictionary of HVAC systems and the zones served: `dict_of_zones_and_hvac_systems = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(B_RMI)`
  - loop through each HVAC system: `for hvac_id in dict_of_zones_and_hvac_systems:`
    - get the list of zones served by the HVAC system: `zones_served_by_hvac_system = dict_of_zones_and_havc_systems[hvac_id]["ZONE_LIST"]`
    - now we need to compare this list to the list of lab zones.  If only lab zones are in zones_served_by_hvac_system, then this is a lab-only HVAC system: `if all(zone_id in building_lab_zones for zone_id in zones_served_by_hvac_system):`
      - this hvac system serves only lab zones, add it to the list: `hvac_systems_serving_lab_zones["LAB_ZONES_ONLY"].append(hvac_id)`
    - now we need to compare this list to the list of lab zones.  If any lab zones are in zones_served_by_hvac_system, then this a system that serves lab zones and other zones: `elif any(zone_id in building_lab_zones for zone_id in zones_served_by_hvac_system):`
      - this hvac system serves lab and other zones, add it to the list: `hvac_systems_serving_lab_zones["LAB_AND_OTHER"].append(hvac_id)`

**Returns** `return hvac_systems_serving_lab_zones`

**[Back](../_toc.md)**
