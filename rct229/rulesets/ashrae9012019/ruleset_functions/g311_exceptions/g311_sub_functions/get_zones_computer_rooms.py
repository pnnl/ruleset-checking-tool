from pydash import reduce_, curry

from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, pint_sum

LightingSpaceOptions2019ASHRAE901TG37 = schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
]


def get_zone_computer_rooms(rmi):
    """
    Returns a dictionary with the zones that have at least one computer room space associated with them in the RMR as the keys.
    The values associated with each key are in a list form. The list associated with each key contains the computer room
    floor area as the first item in the list and the total zone floor area as the second item in the list.

    Parameters
    ----------
    rmi dict
        A dictionary representing a RuleModelInstance object as defined by the ASHRAE229 schema

    Returns
    -------
    zones_with_computer_room_dict
        A dictionary with the zones that have at least one computer room space associated with them in the RMR as the keys.
        The values associated with each key are in a list form. The list associated with each key contains the computer
        room floor area as the first item in the list and the total zone floor area as the second item in the list.
    """
    computer_space_check_func = curry(
        lambda space: space.get("lighting_space_type")
        == LightingSpaceOptions2019ASHRAE901TG37.COMPUTER_ROOM
    )
    zone_with_computer_room_dict = {}

    for zone in find_all("$.buildings[*].building_segments[*].zones[*]", rmi):
        zone_has_computer_room_check = reduce_(
            find_all("$.spaces[*]", zone),
            lambda check, space: check or computer_space_check_func(space),
        )
        zone_computer_room_floor_area = pint_sum(
            [
                space.get("floor_area", ZERO.AREA)
                for space in find_all("$.spaces[*]", zone)
                if computer_space_check_func(space)
            ],
            ZERO.AREA,
        )

        total_zone_floor_area = pint_sum(
            [
                space.get("floor_area", ZERO.AREA)
                for space in find_all("$.spaces[*]", zone)
            ],
            ZERO.AREA,
        )

        if zone_has_computer_room_check:
            zone_with_computer_room_dict[zone["id"]] = {
                "zone_computer_room_floor_area": zone_computer_room_floor_area,
                "total_zone_floor_area": total_zone_floor_area,
            }

    return zone_with_computer_room_dict
