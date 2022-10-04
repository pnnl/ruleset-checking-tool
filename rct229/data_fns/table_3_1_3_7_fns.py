from rct229.data import data
from rct229.data_fns.table_utils import find_osstd_table_entry
from rct229.schema.config import ureg


def table_3_1_3_7_lookup(climate_zone_enum_val):
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
    osstd_entry = find_osstd_table_entry(
        [("climate_zone", climate_zone_enum_val)],
        osstd_table=data["ashrae_90_1_table_G3_1_3_7"],
    )
    degree_fahrenheit = osstd_entry["degree_Fahrenheit"]
    leaving_water_temperature = degree_fahrenheit * ureg("degree_Fahrenheit")

    return {"leaving_water_temperature": leaving_water_temperature}
