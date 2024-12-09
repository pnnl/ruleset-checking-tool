from rct229.schema.schema_enums import SchemaEnums

CLIMATE_ZONE_ASHRAE901_2019 = SchemaEnums.schema_enums[
    "ClimateZoneOptions2019ASHRAE901"
]

APPLICABLE_LIST = [
    CLIMATE_ZONE_ASHRAE901_2019.CZ0A,
    CLIMATE_ZONE_ASHRAE901_2019.CZ0B,
    CLIMATE_ZONE_ASHRAE901_2019.CZ1A,
    CLIMATE_ZONE_ASHRAE901_2019.CZ1B,
    CLIMATE_ZONE_ASHRAE901_2019.CZ2A,
    CLIMATE_ZONE_ASHRAE901_2019.CZ2B,
    CLIMATE_ZONE_ASHRAE901_2019.CZ3A,
]


def is_cz_0_to_3a_bool(climate_zone: str) -> bool:
    """
    Determines whether the building is in climate zone 0 to 3a - used for Appendix G Table G3.1.1-3

    Parameters
    ----------
    climate_zone: Str One of the option in the `ClimateZoneOptions2019ASHRAE901` from ASHRAE 901 2019 sub schema

    Returns
    -------
    Bool: true if it matches to the criteria, false otherwise.
    """
    return climate_zone in APPLICABLE_LIST
