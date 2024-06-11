from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg

# This dictionary maps the ClimateZoneOptions2019ASHRAE901 enumerations to
# the corresponding climate zone values in the OSSTD file
# ashrae_90_1_table_3_2.json
table_3_2_climate_zone_enumeration_to_climate_zone_map = {
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
    "CZ8": "8",
}


def table_3_2_lookup(climate_zone_enum_val):
    """Returns the minimum heating output for a climate zone as
    required by ASHRAE 90.1 Table 3.2
    Parameters
    ----------
    climate_zone_enum_val : str
        One of the ClimateZoneOptions2019ASHRAE901 enumeration values
    Returns
    -------
    dict
        { system_min_heating_output: Quantity – the heating output for the given climate zone given by Table 3.2 [Btu/h-ft^2] }
    """
    climate_zone = table_3_2_climate_zone_enumeration_to_climate_zone_map[
        climate_zone_enum_val
    ]
    osstd_entry = find_osstd_table_entry(
        [("climate_zone", climate_zone)],
        osstd_table=data["ashrae_90_1_table_3_2"],
    )
    btuh_per_ft2 = osstd_entry["heating_output_btu/h-^2"]
    system_min_heating_output = btuh_per_ft2 * ureg(
        "british_thermal_unit / (hour * foot ** 2)"
    )

    return {"system_min_heating_output": system_min_heating_output}
