from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.is_space_a_computer_room import (
    is_space_a_computer_room,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_by_rmd_dict,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import find_exactly_one_schedule

LIGHTING_SPACE_OPTION = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
]

COMPUTER_ROOM_REQ = 0.5


def get_hvac_systems_primarily_serving_comp_room(rmd: dict) -> list[str]:
    """
    Returns a list of HVAC systems in which the computer room space loads are the dominant loads for an HVAC system
    serving multiple spaces including computer rooms and non computer rooms (i.e., computer room spaces account for greater than 50% of cooling load).

     Parameters
     ----------
     rmd dict
         A dictionary representing a ruleset model description as defined by the ASHRAE229 schema

     Returns
     -------
     hvac_systems_primarily_serving_comp_rooms_list list
         A list of hvac systems in which the computer room space loads are the dominant loads for an HVAC system serving multiple spaces
         including computer rooms and non computer rooms (i.e., computer room spaces account for greater than 50% of cooling load).
    """

    hvac_zone_list_w_area_dict = get_hvac_zone_list_w_area_by_rmd_dict(rmd)
    zone_with_computer_room_list = list(
        {
            zone["id"]
            for zone in find_all("$.buildings[*].building_segments[*].zones[*]", rmd)
            for space in find_all("$.spaces[*]", zone)
            if space.get("lighting_space_type") == LIGHTING_SPACE_OPTION.COMPUTER_ROOM
        }
    )

    hvac_systems_primarily_serving_comp_rooms_list = []
    for hvac_id in find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
        rmd,
    ):
        assert_(
            hvac_zone_list_w_area_dict.get(hvac_id),
            f"HVAC system {hvac_id} is missing in the zone.terminals data group.",
        )

        hvac_system_serves_computer_room_space = False
        total_wattage_across_hvac_sys = ZERO.POWER
        total_wattage_across_hvac_sys_for_computer_room = ZERO.POWER
        for zone_id in hvac_zone_list_w_area_dict[hvac_id]["zone_list"]:
            total_zone_wattage_of_computer_rooms_only = ZERO.POWER
            total_wattage_zone = ZERO.POWER

            if zone_id in zone_with_computer_room_list:
                hvac_system_serves_computer_room_space = True

                for space in find_all(
                    f'$.buildings[*].building_segments[*].zones[*][?(@.id="{zone_id}")].spaces[*]',
                    rmd,
                ):
                    total_wattage_space = ZERO.POWER

                    # occupancy max wattage calculation
                    peak_occ_heat_gain = (
                        max(
                            find_exactly_one_schedule(
                                rmd,
                                getattr_(
                                    space, "spaces", "occupant_multiplier_schedule"
                                ),
                            ).get("hourly_cooling_design_day", 0.0)
                        )
                        * space.get("number_of_occupants", 0)
                        * space.get("occupant_sensible_heat_gain", ZERO.POWER)
                    )

                    # lighting max wattage calculation
                    lgt_wattage = sum(
                        [
                            max(
                                find_exactly_one_schedule(
                                    rmd,
                                    getattr_(
                                        int_lgt,
                                        "interior_lighting",
                                        "lighting_multiplier_schedule",
                                    ),
                                ).get("hourly_cooling_design_day", 0.0)
                            )
                            * int_lgt.get("power_per_area", ZERO.POWER_PER_AREA)
                            * space.get("floor_area", ZERO.AREA)
                            for int_lgt in space.get("interior_lighting", [])
                        ]
                    )

                    # miscellaneous max wattage calculation
                    misc_wattage = sum(
                        [
                            max(
                                find_exactly_one_schedule(
                                    rmd,
                                    getattr_(
                                        misc_obj,
                                        "miscellaneous_equipment",
                                        "multiplier_schedule",
                                    ),
                                ).get("hourly_cooling_design_day", 0.0)
                            )
                            * misc_obj.get("power", ZERO.POWER)
                            * misc_obj.get("sensible_fraction", 0.0)
                            for misc_obj in space.get("miscellaneous_equipment", [])
                        ]
                    )
                    tempo_wattage = peak_occ_heat_gain + lgt_wattage + misc_wattage
                    total_wattage_space += tempo_wattage
                    total_wattage_zone += tempo_wattage

                    # check if space is computer room type
                    if is_space_a_computer_room(rmd, space["id"]):
                        total_zone_wattage_of_computer_rooms_only += total_wattage_space

            total_wattage_across_hvac_sys_for_computer_room += (
                total_zone_wattage_of_computer_rooms_only
            )
            total_wattage_across_hvac_sys += total_wattage_zone

        if (
            hvac_system_serves_computer_room_space
            and total_wattage_across_hvac_sys_for_computer_room
            / total_wattage_across_hvac_sys
            > COMPUTER_ROOM_REQ
        ):
            hvac_systems_primarily_serving_comp_rooms_list.append(hvac_id)

    return hvac_systems_primarily_serving_comp_rooms_list
