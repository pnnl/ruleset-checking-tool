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
            space["id"]
            for zone in find_all("$.buildings[*].building_segments[*].zones[*]", rmd)
            for space in find_all("$.spaces[*]", zone)
            if space.get("lighting_space_type") == LIGHTING_SPACE_OPTION.COMPUTER_ROOM
        }
    )

    hvac_systems_primarily_serving_comp_rooms_list = []
    for hvac in find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        rmd,
    ):
        assert_(
            hvac_zone_list_w_area_dict.get(hvac["id"]),
            f"HVAC system {hvac['id']} is missing in the zone.terminals data group.",
        )

        hvac_system_serves_computer_room_space = False
        total_Wattage_across_hvac_sys = ZERO.POWER
        total_Wattage_across_hvac_sys_for_computer_room = ZERO.POWER
        for zone in hvac_zone_list_w_area_dict[hvac["id"]]["zone_list"]:
            if zone["id"] in zone_with_computer_room_list:
                hvac_system_serves_computer_room_space = True
                total_Wattage_zone = ZERO.POWER
                total_zone_Wattage_of_computer_rooms_only = ZERO.POWER

                for space in zone:
                    total_Wattage_space = ZERO.POWER

                    space_is_a_computer_room = (
                        True if is_space_a_computer_room(rmd, space["id"]) else False
                    )

                    # occupancy max wattage calculation
                    max_design_cooling_multiplier_sch = max(
                        find_exactly_one_schedule(
                            rmd,
                            getattr_(space, "spaces", "occupant_multiplier_schedule"),
                        ).get("cooling_design_day_sequence", 0.0)
                    )

                    peak_occ_heat_gain = (
                        max_design_cooling_multiplier_sch
                        * space.get("number_of_occupants", 0)
                        * space.get("occupant_sensible_heat_gain", ZERO.POWER)
                    )

                    total_Wattage_space += peak_occ_heat_gain

                    # lighting max wattage calculation
                    temp_total_power = ZERO.POWER
                    for int_lgt in space.get("interior_lighting", []):
                        max_design_cooling_multiplier_sch = max(
                            find_exactly_one_schedule(
                                rmd,
                                getattr_(
                                    int_lgt,
                                    "interior_lighting",
                                    "lighting_multiplier_schedule",
                                ),
                            ).get("cooling_design_day_sequence", 0.0)
                        )
                        lgt_W = (
                            max_design_cooling_multiplier_sch
                            * int_lgt.get("power_per_area", ZERO.POWER_PER_AREA)
                            * space.get("floor_area", ZERO.AREA)
                        )

                        temp_total_power += lgt_W

                    total_Wattage_space += temp_total_power

                    # miscellaneous max wattage calculation
                    temp_total_power = ZERO.POWER
                    for misc_obj in space.get("miscellaneous_equipment", []):
                        max_design_cooling_multiplier_sch = max(
                            find_exactly_one_schedule(
                                rmd,
                                getattr_(
                                    misc_obj,
                                    "miscellaneous_equipment",
                                    "multiplier_schedule",
                                ),
                            ).get("cooling_design_day_sequence", 0.0)
                        )

                        misc_power = misc_obj.get("power", ZERO.POWER)

                        misc_W = (
                            max_design_cooling_multiplier_sch
                            * misc_power
                            * misc_obj.get("sensible_fraction", 0.0)
                        )

                        temp_total_power += misc_W

                    total_Wattage_space += temp_total_power

                total_Wattage_zone += total_Wattage_space

                if space_is_a_computer_room:
                    total_zone_Wattage_of_computer_rooms_only += total_Wattage_space

            total_Wattage_across_hvac_sys_for_computer_room += (
                total_zone_Wattage_of_computer_rooms_only
            )
            hvac_system_serves_computer_room_space = (
                total_Wattage_across_hvac_sys + total_Wattage_zone
            )

        if (
            hvac_system_serves_computer_room_space
            and hvac_system_serves_computer_room_space
            and total_Wattage_across_hvac_sys_for_computer_room
            / hvac_system_serves_computer_room_space
            > COMPUTER_ROOM_REQ
        ):
            hvac_systems_primarily_serving_comp_rooms_list.append(hvac["id"])

    return hvac_systems_primarily_serving_comp_rooms_list
