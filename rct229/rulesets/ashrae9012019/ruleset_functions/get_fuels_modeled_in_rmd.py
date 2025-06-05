from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

ENERGY_SOURCE = SchemaEnums.schema_enums["EnergySourceOptions"]
HEATING_SOURCE = SchemaEnums.schema_enums["HeatingSourceOptions"]


# Mapping energy sources to keys
source_mapping = {
    ENERGY_SOURCE.PROPANE: "PROPANE",
    ENERGY_SOURCE.NATURAL_GAS: "NATURAL_GAS",
    ENERGY_SOURCE.ELECTRICITY: "ELECTRICITY",
    ENERGY_SOURCE.FUEL_OIL: "OIL",
    ENERGY_SOURCE.OTHER: "OTHER",
    HEATING_SOURCE.ELECTRIC: "ELECTRICITY",
    HEATING_SOURCE.OTHER: "OTHER",
}

# List of JSON paths to search
json_paths = [
    "$.boilers[*].energy_source_type",
    "$.chillers[*].energy_source_type",
    "$.external_fluid_sources[*].energy_source_type",
    "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].heating_system.energy_source_type",
    "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].preheat_system.energy_source_type",
    "$.buildings[*].building_segments[*].zones[*].terminals[*].heating_source",
    "$.service_water_heating_equipment[*].heater_fuel_type",
    "$.miscellaneous_equipment[*].energy_type",
]


def get_fuels_modeled_in_rmd(rmd: dict) -> list[str]:
    """
    Get a list of the fuels used in the RMD. Includes fuels used by HVAC systems including terminal units, chillers, boilers, ExternalFluidSources, and SWHs.

    Parameters
    ----------
    rmd: dict
         A dictionary representing a ruleset model description as defined by the ASHRAE229 schema

    Returns
    -------
        fuels_list: list
            A list that saves all the fuels modeled in the RMD

    """

    # Initial dictionary setup
    fuel_energy_source_dict = {
        "PROPANE": False,
        "NATURAL_GAS": False,
        "ELECTRICITY": False,
        "OIL": False,
        "OTHER": False,
    }

    # Loop over the paths and update the dictionary
    for json_path in json_paths:
        for energy_source in find_all(json_path, rmd):
            key = source_mapping.get(energy_source)
            if key:
                fuel_energy_source_dict[key] = True

    # Extract the list of fuels
    fuels_list = [key for key, value in fuel_energy_source_dict.items() if value]

    return fuels_list
