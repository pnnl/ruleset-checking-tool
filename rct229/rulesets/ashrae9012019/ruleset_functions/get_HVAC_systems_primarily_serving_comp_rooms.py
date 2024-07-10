from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_by_rmi_dict,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO

LightingSpaceOptions2019ASHRAE901TG37 = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
]
COMPUTER_ROOM_RATIO_THRESHOLD = 0.5


def get_HVAC_systems_primarily_serving_comp_rooms(rmd: dict) -> list[str]:
    """
    Returns a list of HVAC systems in which greater than 50% of the area served by the HVAC system is computer room space.

    Parameters
    ----------
    rmd: json
        To develop a list of HVAC systems in which greater than 50% of the area served by the HVAC system is computer room space.

    Returns:
        hvac_systems_primarily_serving_comp_rooms_list: list
        A list of hvac systems in which greater than 50% of the area served by the HVAC system is computer room space.
    -------

    """

    # get each hvac system's serving area and zone list
    hvac_zone_list_w_area_dict = get_hvac_zone_list_w_area_by_rmi_dict(rmd)

    hvac_systems_primarily_serving_comp_rooms_list = []
    for hvac_id in find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
        rmd,
    ):
        hvac_system_serves_computer_room_space = False
        hvac_sys_computer_room_floor_area = ZERO.AREA
        if (
            hvac_id in hvac_zone_list_w_area_dict
        ):  # To prevent an error when an HVAC system doesn't serve any zone.
            hvac_total_floor_area = hvac_zone_list_w_area_dict[hvac_id]["total_area"]
            hvac_zone_list = hvac_zone_list_w_area_dict[hvac_id]["zone_list"]

            for zone_id in hvac_zone_list:
                for space in find_all(
                    f'$.buildings[*].building_segments[*].zones[*][?(@.id="{zone_id}")].spaces[*]',
                    rmd,
                ):
                    if (
                        space.get("lighting_space_type")
                        == LightingSpaceOptions2019ASHRAE901TG37.COMPUTER_ROOM
                    ):
                        hvac_system_serves_computer_room_space = True
                        hvac_sys_computer_room_floor_area += space.get(
                            "floor_area", ZERO.AREA
                        )

            if (
                hvac_system_serves_computer_room_space
                and hvac_sys_computer_room_floor_area / hvac_total_floor_area
                > COMPUTER_ROOM_RATIO_THRESHOLD
            ):
                hvac_systems_primarily_serving_comp_rooms_list.append(hvac_id)

    return hvac_systems_primarily_serving_comp_rooms_list
