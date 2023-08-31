from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_rmi_dict,
    ZoneConditioningCategory as ZCC,
)
from rct229.utils.jsonpath_utils import find_all


LightingSpaceOptions2019ASHRAE901TG37 = schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
]


def get_number_of_floors(climate_zone, rmi):
    """
    gets the number of floors in the building. Parking Garages are not counted

    Parameters
    ----------
    climate_zone: str
        One of the ClimateZoneOptions2019ASHRAE901 enumerated values
    rmi dict
        A dictionary representing a ruleset model instance as defined by the ASHRAE229 schema

    Returns
    -------
    number_of_floors Integer
        number of floors
    """

    number_of_floors = sum(
        [
            building.get("number_of_floors_above_grade", 0.0)
            + building.get("number_of_floors_below_grade", 0.0)
            for building in find_all("$.buildings[*]", rmi)
        ]
    )

    if number_of_floors <= 0.0:
        zone_conditioning_category_dict = get_zone_conditioning_category_rmi_dict(
            climate_zone, rmi
        )

        def is_zone_conditioned(zone):
            """
            Function returns a boolean. True if a zone is conditioned mixed, conditioned residential
            conditioned non residential or semi-heated
            """
            zcc = zone_conditioning_category_dict[zone["id"]]
            return (
                zcc == ZCC.CONDITIONED_MIXED
                or zcc == ZCC.CONDITIONED_RESIDENTIAL
                or zcc == ZCC.CONDITIONED_NON_RESIDENTIAL
                or zcc == ZCC.SEMI_HEATED
            )

        def any_space_in_zone_parking_garage(zone):
            "Function returns a boolean. True if any space in a zone are not parking area interior, False otherwise"
            return any(
                [
                    space.get("lighting_space_type", None)
                    != LightingSpaceOptions2019ASHRAE901TG37.PARKING_AREA_INTERIOR
                    for space in find_all("$.spaces[*]", zone)
                ]
            )

        zone_list = find_all("$.buildings[*].building_segments[*].zones[*]", rmi)
        conditioned_zone_list = filter(is_zone_conditioned, zone_list)
        no_parking_conditioned_zone_list = filter(
            any_space_in_zone_parking_garage, conditioned_zone_list
        )
        floor_names = [
            zone["floor_name"]
            # remove None
            for zone in no_parking_conditioned_zone_list
            if zone.get("floor_name")
        ]
        number_of_floors = len(floor_names)

    return number_of_floors
