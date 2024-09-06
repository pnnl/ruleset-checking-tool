from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_by_rmd_dict,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import find_exactly_one_zone

LightingSpaceOptionsG37 = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
]


def get_hvac_systems_primarily_serving_comp_room(rmd: dict) -> list[str]:
    """
    Returns a list of HVAC systems in which greater than 50% of the area served by the HVAC system is computer room
    space.

    Parameters
    ----------
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema

    Returns
    -------
    hvac_systems_primarily_serving_comp_rooms_list list
        A list of hvac systems in which greater than 50% of the area served by the HVAC system is computer room space.
    """
    hvac_zone_list_w_area_dict = get_hvac_zone_list_w_area_by_rmd_dict(rmd)
    hvac_systems_primarily_serving_comp_rooms_list = []

    for hvac in find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        rmd,
    ):
        assert_(
            hvac_zone_list_w_area_dict.get(hvac["id"]),
            f"HVAC system {hvac['id']} is missing in the  zone.terminals data group.",
        )
        hvac_sys_total_floor_area = hvac_zone_list_w_area_dict[hvac["id"]]["total_area"]
        hvac_sys_zone_id_list = hvac_zone_list_w_area_dict[hvac["id"]]["zone_list"]

        hvac_zones_list = [
            find_exactly_one_zone(rmd, zone_id) for zone_id in hvac_sys_zone_id_list
        ]
        hvac_spaces_list = [
            space for zone in hvac_zones_list for space in find_all("$.spaces[*]", zone)
        ]

        hvac_system_computer_room_floor_area = sum(
            [
                space.get("floor_area", ZERO.AREA)
                for space in hvac_spaces_list
                if space.get("lighting_space_type")
                == LightingSpaceOptionsG37.COMPUTER_ROOM
            ],
            ZERO.AREA,
        )

        assert_(
            hvac_sys_total_floor_area > ZERO.AREA,
            f"Total areas conditioned by HVAC: {hvac['id']} is less or "
            f"equal to 0. Check inputs!",
        )

        if hvac_system_computer_room_floor_area / hvac_sys_total_floor_area > 0.5:
            hvac_systems_primarily_serving_comp_rooms_list.append(hvac["id"])

    return hvac_systems_primarily_serving_comp_rooms_list
