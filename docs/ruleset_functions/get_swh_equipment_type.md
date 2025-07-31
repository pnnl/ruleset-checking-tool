## get_swh_equipment_type

Description: This function determines whether the swh equipment type is one of: (ELECTRIC_RESISTANCE_INSTANTANEOUS, ELECTRIC_RESISTANCE_STORAGE, GAS_STORAGE, PROPANE_INSTANTANEOUS, PROPANE_STORAGE, OTHER)

## Inputs:
- **RMD**
- **service_water_heating_equipment_id**

## Returns:
- **type**: A string, ex: type = "ELECTRIC_RESISTANCE_INSTANTANEOUS"

## Function Call: None  

## Data Lookup: None

## Logic:
- we need to find the following information about the SWH:
  - tank_type - (ELECTRIC_RESISTANCE_INSTANTANEOUS, ELECTRIC_RESISTANCE_STORAGE, GAS_STORAGE, OTHER)
- get the service water heating system: `swh_eq = get_object_by_id(service_water_heating_equipment_id,RMD)`
- get the type of service water heating tank: `swh_tank_type = swh_eq.tank.type`
- get the type of service water heating system: `swh_type = swh_eq.heater_type`
- the type will be one of the ServiceWaterHeaterTankOptions, which are more detailed than the four types we need.  Determine our type based on the detailed type.
- set the type to OTHER.  If the swh_tank_type is an identifiable type, type will be overwritten to that type: `type = "OTHER"`
- check if the swh_type is CONVENTIONAL, this is the only swh_type that leads us to a reconizable type for ASHRAE 90.1 Appendix G: `if swh_type == "CONVENTIONAL":`
  - if the swh_tank_type is CONSUMER_INSTANTANEOUS, COMMERCIAL_INSTANTANEOUS, or RESIDENTIAL_DUTY_COMMERCIAL_INSTANTANEOUS, set the type to INSTANTANEOUS: `if swh_tank_type in ["CONSUMER_INSTANTANEOUS", "COMMERCIAL_INSTANTANEOUS", "RESIDENTIAL_DUTY_COMMERCIAL_INSTANTANEOUS"]: type = "INSTANTANEOUS"`
  - if the swh_tank_type is CONSUMER_STORAGE or COMMERCIAL_STORAGE, set the type to STORAGE: `if swh_tank_type in ["CONSUMER_STORAGE", "COMMERCIAL_STORAGE"]: type = "STORAGE"`
  - get the fuel type of the equipment: `fuel_type = swh_eq.heater_fuel_type`
  - set the type based on swh_tank_type and fuel type: `if fuel_type == "ELECTRICITY":`
    - `if swh_tank_type == "INSTANTANEOUS": type = "ELECTRIC_RESISTANCE_INSTANTANEOUS"`
    - `elsif swh_tank_type == "STORAGE": type = "ELECTRIC_RESISTANCE_STORAGE"`
  - `elsif fule_type == "NATURAL_GAS":`
    - `if swh_tank_type == "INSTANTANEOUS": type = "GAS_INSTANTANEOUS"`
    - `elsif swh_tank_type == "STORAGE": type = "GAS_STORAGE"`
  - `elsif fule_type == "PROPANE":`
    - `if swh_tank_type == "INSTANTANEOUS": type = "PROPANE_INSTANTANEOUS"`
    - `elsif swh_tank_type == "STORAGE": type = "PROPANE_STORAGE"`
  - `elsif fule_type == "FUEL_OIL":`
    - `if swh_tank_type == "INSTANTANEOUS": type = "OIL_INSTANTANEOUS"`
    - `elsif swh_tank_type == "STORAGE": type = "OIL_STORAGE"`



**Returns** type

**[Back](../_toc.md)**

**Notes:**


