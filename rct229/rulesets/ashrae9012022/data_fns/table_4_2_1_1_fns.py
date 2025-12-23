from rct229.rulesets.ashrae9012019.data import data
from rct229.rulesets.ashrae9012019.data_fns.table_utils import find_osstd_table_entry

# This dictionary maps the ClimateZoneOptions2019ASHRAE901 enumerations to
# the corresponding climate zone values in the OSSTD file
# ashrae_90_1_table_4_2_1_1.json

table_4_2_1_1_climate_zone_enumeration_to_climate_zone_map = {
    "CZ0A": "0A and 1A",
    "CZ0B": "0B and 1B",
    "CZ1A": "0A and 1A",
    "CZ1B": "0B and 1B",
    "CZ2A": "2A",
    "CZ2B": "2B",
    "CZ3A": "3A",
    "CZ3B": "3B",
    "CZ3C": "3C",
    "CZ4A": "4A",
    "CZ4B": "4B",
    "CZ4C": "4C",
    "CZ5A": "5A",
    "CZ5B": "5B",
    "CZ5C": "5C",
    "CZ6A": "6A",
    "CZ6B": "6B",
    "CZ7": "7",
    "CZ8": "8",
}

# This dictionary maps the BuildingAreaTypeOptions2019ASHRAE901 enumerations to
# the corresponding climate zone values in the OSSTD file
# ashrae_90_1_table_4_2_1_1.json

table_4_2_1_1_building_area_type_enumeration_to_building_area_type_map = {
    "MULTIFAMILY": "Multifamily",
    "HEALTHCARE_HOSPITAL": "Healthcare/hospital",
    "HOTEL_MOTEL": "Hotel/motel",
    "OFFICE": "Office",
    "RESTAURANT": "Restaurant",
    "RETAIL": "Retail",
    "SCHOOL": "School",
    "WAREHOUSE": "Warehouse",
    "ALL_OTHER": "All others",
}


def table_4_2_1_1_lookup(
    building_area_type_enum_val: str, climate_zone_enum_val: str
) -> dict[str, float]:
    """Returns the building performance factor
    required by ASHRAE 90.1 Table 4.2.1.1
    Parameters
    ----------
    building_area_type_enum_val : str
        One of the building area type enumeration values
    climate_zone_enum_val : str
        One of the ClimateZoneOptions2019ASHRAE901 enumeration values
    Returns
    -------
    dict
        { building_performance_factor: float number – the building performance factor defined by Table 4.2.1.1}
    """
    building_area_type = (
        table_4_2_1_1_building_area_type_enumeration_to_building_area_type_map[
            building_area_type_enum_val
        ]
    )

    climate_zone = table_4_2_1_1_climate_zone_enumeration_to_climate_zone_map[
        climate_zone_enum_val
    ]

    osstd_entry = find_osstd_table_entry(
        [("building_area_type", building_area_type), ("climate_zone", climate_zone)],
        osstd_table=data["ashrae_90_1_table_4_2_1_1"],
    )
    building_performance_factor = osstd_entry["building_performance_factor"]

    return {"building_performance_factor": building_performance_factor}
