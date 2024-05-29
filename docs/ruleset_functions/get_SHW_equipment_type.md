## get_SHW_equipment_type

## Description: This function determines whether the shw equipment type is one of: (ELECTRIC_RESISTANCE_INSTANTANEOUS, ELECTRIC_RESISTANCE_STORAGE, GAS_STORAGE, OTHER)

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
- get the type of service water heating system: `shw_type = swh_eq.type`
- the type will be one of the ServiceWaterHeaterTankOptions, which are more detailed than the four types we need.  Determine our type based on the detailed type.
- set the type to OTHER.  If the shw_type is an identifiable type, type will be overwritten to that type: `type = "OTHER"`
- if the shw_type is CONSUMER_INSTANTANEOUS, COMMERCIAL_INSTANTANEOUS, or RESIDENTIAL_DUTY_COMMERCIAL_INSTANTANEOUS, set the type to INSTANTANEOUS: `if shw_type in ["CONSUMER_INSTANTANEOUS", "COMMERCIAL_INSTANTANEOUS", "RESIDENTIAL_DUTY_COMMERCIAL_INSTANTANEOUS"]: type = "INSTANTANEOUS"`
- if the shw_type is CONSUMER_STORAGE or COMMERCIAL_STORAGE, set the type to STORAGE: `if shw_type in ["CONSUMER_STORAGE", "COMMERCIAL_STORAGE"]: type = "STORAGE"`
- get the fuel type of the equipment: `fuel_type = shw_eq.heater_fuel_type`
- set the type based on shw_type and fuel type: `if fuel_type == "ELECTRICITY":`
  - `if shw_type == "INSTANTANEOUS": type = "ELECTRIC_RESISTANCE_INSTANTANEOUS"`
  - `elsif shw_type == "STORAGE": type = "ELECTRIC_RESISTANCE_STORAGE"`
- `elsif fule_type == "NATURAL_GAS":`
  - `if shw_type == "INSTANTANEOUS": type = "GAS_INSTANTANEOUS"`
  - `elsif shw_type == "STORAGE": type = "GAS_STORAGE"`
- `elsif fule_type == "FUEL_OIL":`
  - `if shw_type == "INSTANTANEOUS": type = "OIL_INSTANTANEOUS"`
  - `elsif shw_type == "STORAGE": type = "OIL_STORAGE"`



**Returns** type

**[Back](../_toc.md)**

**Notes:**


