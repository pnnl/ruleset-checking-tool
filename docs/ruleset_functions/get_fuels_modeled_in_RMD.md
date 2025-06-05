# get_fuels_modeled_in_RMD

**Schema Version:** 0.0.23  
**Description:** Get a list of the fuels used in the RMD.  Includes fuels used by HVAC systems including terminal units, chillers, boilers, ExternalFluidSources, and SWHs.

**Inputs:**
- **U, P, or B-RMD**: To determine a list of the fuels used in the RMD.  Includes fuels used by HVAC systems including terminal units, chillers, boilers, ExternalFluidSources, and SWHs in the RMD.

**Returns:**
- **fuels_list**: A list that saves all the fuels modeled in the RMD.

**Function Call:**  None

## Logic:  
- Define json paths to explore: `json_paths = [$.boilers[*].energy_source_type, $.chillers[*].energy_source_type, $.external_fluid_sources[*].energy_source_type, $.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].heating_system.energy_source_type, $.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].preheat_system.energy_source_type, $.buildings[*].building_segments[*].zones[*].terminals[*].heating_source, $.service_water_heating_equipment[*].heater_fuel_type, $.miscellaneous_equipment[*].energy_type]`
- Define energy source maping keys: `source_mapping = {ENERGY_SOURCE.PROPANE: "PROPANE", ENERGY_SOURCE.NATURAL_GAS: "NATURAL_GAS", ENERGY_SOURCE.ELECTRICITY: "ELECTRICITY", ENERGY_SOURCE.FUEL_OIL: "OIL", ENERGY_SOURCE.OTHER: "OTHER", HEATING_SOURCE.ELECTRIC: "ELECTRICITY", HEATING_SOURCE.OTHER: "OTHER"}`
- Define an inital `fuel_energy_source_dict`: `fuel_energy_source_dict = {"PROPANE": False, "NATURAL_GAS": False, "ELECTRICITY": False, "OIL": False, "OTHER": False}`
- Loop over the json paths: `for json_path in json_paths:`
    - Find the energy_source value: ` for energy_source in find_all(json_path, rmd):`
        - Get the energy source type: `key = source_mapping.get(energy_source)`
        - If key exists: `if key:`
            - Assign True value: `fuel_energy_source_dict[key] = True`
- Extract the fuel sources: `fuels_list = [key for key, value in fuel_energy_source_dict.items() if value]`

**Returns** `return fuels_list`

**[Back](../_toc.md)**
