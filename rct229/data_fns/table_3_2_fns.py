import rct229
from rct229.data import data
from rct229.data_fns.table_utils import find_osstd_table_entry

# This dictionary maps the ClimateZone2019ASHRAE901 enumerations to
# the corresponding climate zone values in the OSSTD file
# ashrae_90_1_table_3_2.json
"""
The enumeration has been updated to match the following climate zones from the standard.
CZ0A, CZ0B -> "0"
CZ1A, CZ1B -> "1"
CZ2A, CZ2B -> "2"
CZ3A, CZ3B -> "3A,3B"
CZ3C -> "3C"
CZ4A, CZ4B -> "4A,4B"
CZ4C -> "4C"
CZ5A, CZ5B, CZ5C -> "5"
CZ6A, CZ6B -> "6"
CZ7 -> "7"
CZ8 -> "8"

"""
climate_zone_enumeration_to_climate_zone_type_map = {
    "CZ0A": "0",
    "CZ0B": "0",
    "CZ1A": "1",
    "CZ1B": "1",
    "CZ2A": "2",
    "CZ2B": "2",
    "CZ3A": "3A,3B",
    "CZ3B": "3A,3B",
    "CZ3C": "3C",
    "CZ4A": "4A,4B",
    "CZ4B": "4A,4B",
    "CZ4C": "4C",
    "CZ5A": "5",
    "CZ5B": "5",
    "CZ5C": "5",
    "CZ6A": "6",
    "CZ6B": "6",
    "CZ7": "7",
    "CZ8": "8"    
}

def table_3_2_lookup(climate_zone):
    """Returns the heating output for a climate zone as
    required by ASHRAE 90.1 Table 3.2
    Parameters
    ----------
    climate_zone : str
        One of the ClimateZone2019ASHRAE901 enumeration values
    Returns
    -------
    dict
        The Heating Output for a given Climate Zone given by Table 3.2 [Btu/h·ft^2]
    """
    climate_zone_type = climate_zone_enumeration_to_climate_zone_type_map[
        climate_zone
    ]
    osstd_entry = find_osstd_table_entry(
        [("climate_zone", climate_zone_type)],
        osstd_table=data["ashrae_90_1_table_3_2"],
    )
    system_min_heating_output = osstd_entry["Btu/h·ft^2"]
    return {"system_min_heating_output": system_min_heating_output}
