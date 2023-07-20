from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg

# This dictionary maps the ClimateZoneOptions2019ASHRAE901 enumerations to
# the corresponding climate zone values in the OSSTD file
# ashrae_90_1_table_3_2.json
table_3_1_3_11_climate_zone_enumeration_to_climate_zone_map = {
    "CZ0A": "0A, 1A, 2A",
    "CZ0B": "0B, 1B, 2B, 3B, 3C, 4B, 4C, 5A, 6A, 7",
    "CZ1A": "0A, 1A, 2A",
    "CZ1B": "0B, 1B, 2B, 3B, 3C, 4B, 4C, 5A, 6A, 7",
    "CZ2A": "0A, 1A, 2A",
    "CZ2B": "0B, 1B, 2B, 3B, 3C, 4B, 4C, 5A, 6A, 7",
    "CZ3A": "3A,4A",
    "CZ3B": "0B, 1B, 2B, 3B, 3C, 4B, 4C, 5A, 6A, 7",
    "CZ3C": "0B, 1B, 2B, 3B, 3C, 4B, 4C, 5A, 6A, 7",
    "CZ4A": "3A,4A",
    "CZ4B": "0B, 1B, 2B, 3B, 3C, 4B, 4C, 5A, 6A, 7",
    "CZ4C": "0B, 1B, 2B, 3B, 3C, 4B, 4C, 5A, 6A, 7",
    "CZ5A": "0B, 1B, 2B, 3B, 3C, 4B, 4C, 5A, 6A, 7",
    "CZ5B": "5B, 5C, 6B, 8",
    "CZ5C": "5B, 5C, 6B, 8",
    "CZ6A": "0B, 1B, 2B, 3B, 3C, 4B, 4C, 5A, 6A, 7",
    "CZ6B": "5B, 5C, 6B, 8",
    "CZ7": "0B, 1B, 2B, 3B, 3C, 4B, 4C, 5A, 6A, 7",
    "CZ8": "5B, 5C, 6B, 8",
}


def table_3_1_3_11_lookup(climate_zone_enum_val):
    """Returns the heat rejection leaving water temperature
    required by ASHRAE 90.1 Table 3.1.3.7
    Parameters
    ----------
    climate_zone_enum_val : str
        One of the ClimateZoneOptions2019ASHRAE901 enumeration values
    Returns
    -------
    dict
        { leaving_water_temperature: Quantity – the leaving water temperature defined by Table 3.1.3.7 [degree-F]}
    """
    climate_zone = table_3_1_3_11_climate_zone_enumeration_to_climate_zone_map[
        climate_zone_enum_val
    ]

    osstd_entry = find_osstd_table_entry(
        [("climate_zone", climate_zone)],
        osstd_table=data["ashrae_90_1_table_G3_1_3_11"],
    )
    degree_fahrenheit = osstd_entry["leaving_water_temp_f"]
    leaving_water_temperature = ureg(f"{degree_fahrenheit} degree_Fahrenheit")

    return {"leaving_water_temperature": leaving_water_temperature}
