from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.is_space_a_computer_room import (
    is_space_a_computer_room,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO

LightingSpaceOptions2019ASHRAE901TG37 = schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
]


def get_zone_computer_rooms(rmi):
    """
    Returns a dictionary with the zones that have at least one computer room space associated with them in the RMR as the keys.
    The values associated with each key are in a dict form. The dict associated with each key contains the computer room
    floor area as the first item and the total zone floor area as the second item.

    Parameters
    ----------
    rmi dict
        A dictionary representing a RuleModelInstance object as defined by the ASHRAE229 schema

    Returns
    -------
    zones_with_computer_room_dict
        A dictionary with the zones that have at least one computer room space associated with them in the RMR as the keys.
        The values associated with each key are in a dict form. The dict associated with each key contains the computer room
        floor area as the first item and the total zone floor area as the second item.
    """
    zone_with_computer_room_dict = {}

    for zone in find_all("$.buildings[*].building_segments[*].zones[*]", rmi):
        zone_has_computer_room_check = any(
            [
                is_space_a_computer_room(rmi, space["id"])
                for space in find_all("$.spaces[*]", zone)
            ]
        )

        if zone_has_computer_room_check:
            zone_with_computer_room_dict[zone["id"]] = {
                "zone_computer_room_floor_area": sum(
                    [
                        space.get("floor_area", ZERO.AREA)
                        for space in find_all("$.spaces[*]", zone)
                        if is_space_a_computer_room(rmi, space["id"])
                    ],
                    ZERO.AREA,
                ),
                "total_zone_floor_area": sum(
                    [
                        space.get("floor_area", ZERO.AREA)
                        for space in find_all("$.spaces[*]", zone)
                    ],
                    ZERO.AREA,
                ),
            }

    return zone_with_computer_room_dict
