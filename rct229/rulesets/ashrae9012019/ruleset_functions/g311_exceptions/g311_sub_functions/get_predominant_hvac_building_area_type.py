from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_hvac_building_area_types_and_zones_dict import (
    get_hvac_building_area_types_and_zones_dict,
)


def get_predominant_hvac_building_area_type(climate_zone: str, rmd: dict) -> str:
    """

    Sort the building area type and zones and return the building type that has the largest floor area
    Used to verify the correct type of HVAC baseline system (or systems)

    Parameters
    ----------
    climate_zone str
        One of the ClimateZoneOptions2019ASHRAE901 enumerated values
    rmd dict
        A dictionary representing a ruleset model instance as defined by the ASHRAE229 schema

    Returns
    -------
    string, HVAC building area type.
    """
    # building_area_types_and_zones_dict is guaranteed non-empty dict.
    building_area_types_and_zones_dict = get_hvac_building_area_types_and_zones_dict(
        climate_zone, rmd
    )
    # the sorted_hvac_building_area_type is a list of tuples that consist of two elements,
    # 0 index is the key in the original dict
    # 1 index is the value in the original dict
    sorted_hvac_building_area_type = sorted(
        building_area_types_and_zones_dict.items(),
        key=lambda x: x[1]["floor_area"],
        reverse=True,
    )
    # Taking out the first element (one with the largest floor_area) in the list and its first element (key)
    return sorted_hvac_building_area_type[0][0]
