from pydash import chunk, count_by, curry, filter_, flatten_deep, flow, map_
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1c import (
    does_zone_meet_g3_1_1c,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1d import (
    does_zone_meet_g3_1_1d,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1e import (
    does_zone_meet_g3_1_1e,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1f import (
    does_zone_meet_g_3_1_1f,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1g import (
    does_zone_meet_g3_1_1g,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.expected_system_type_from_table_g311a_dict import (
    expected_system_type_from_table_g3_1_1_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_computer_zones_peak_cooling_load import (
    get_computer_zones_peak_cooling_load,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_hvac_building_area_types_and_zones_dict import (
    get_hvac_building_area_types_and_zones_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_number_of_floors import (
    get_number_of_floors,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_predominant_hvac_building_area_type import (
    get_predominant_hvac_building_area_type,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zone_hvac_bat import (
    get_zone_hvac_bat_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.is_cz_0_to_3a_bool import (
    is_cz_0_to_3a_bool,
)
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all, find_one

BUILDING_AREA_20000_ft2 = 20000 * ureg("ft2")
BUILDING_AREA_40000_ft2 = 40000 * ureg("ft2")
BUILDING_AREA_150000_ft2 = 150000 * ureg("ft2")
COMPUTER_ROOM_PEAK_COOLING_LOAD_600000_BTUH = 600000 * ureg("Btu/hr")
COMPUTER_ROOM_PEAK_COOLING_LOAD_3000000_BTUH = 3000000 * ureg("Btu/hr")


def get_zone_target_baseline_system(rmi_b, rmi_p, climate_zone_b):
    # zone_conditioning_category_dict = get_zone_conditioning_category_dict(
    #     climate_zone_b, rmi_b["buildings"][0]
    # )
    zone_conditioning_category_dict = {
        "Thermal Zone 1": "CONDITIONED MIXED",
        "Thermal Zone 2": "CONDITIONED NON-RESIDENTIAL",
    }

    zones_and_systems = {}
    for zone_b in find_all("$.buildings[*].building_segments[*].zones[*]", rmi_b):
        zone_id_b = zone_b["id"]
        if zone_conditioning_category_dict[zone_id_b] in [
            ZCC.CONDITIONED_RESIDENTIAL,
            ZCC.CONDITIONED_NON_RESIDENTIAL,
            ZCC.CONDITIONED_MIXED,
        ]:
            zones_and_systems[zone_id_b] = {}

    list_building_area_types_and_zones = get_hvac_building_area_types_and_zones_dict(
        climate_zone_b, rmi_b
    )
    predominant_building_area_type = get_predominant_hvac_building_area_type(
        climate_zone_b, rmi_b
    )

    num_floors = get_number_of_floors(climate_zone_b, rmi_b)

    area = list_building_area_types_and_zones[predominant_building_area_type][
        "floor_area"
    ]

    for building_area_type in list_building_area_types_and_zones:
        area += list_building_area_types_and_zones[building_area_type]["floor_area"]

    expected_system_type_dict = expected_system_type_from_table_g3_1_1_dict(
        predominant_building_area_type, climate_zone_b, num_floors, area
    )

    for zone in zones_and_systems:
        zones_and_systems[zone] = expected_system_type_dict

    if area > BUILDING_AREA_40000_ft2:
        for building_area_type in list_building_area_types_and_zones:
            if (
                list_building_area_types_and_zones[building_area_type]["floor_area"]
                >= BUILDING_AREA_20000_ft2
            ):
                secondary_system_type = expected_system_type_from_table_g3_1_1_dict(
                    building_area_type, climate_zone_b, num_floors, area
                )

                for zone in zones_and_systems:
                    if (
                        zone
                        in list_building_area_types_and_zones[building_area_type][
                            "zone_ids"
                        ]
                    ):
                        zones_and_systems[zone][
                            "expected_system_type"
                        ] = secondary_system_type["expected_system_type"]
                        zones_and_systems[zone]["system_origin"] = "G3_1_1b"

    zones_that_meetG3_1_1c_list = []
    # for zone in zones_and_systems:
    #     if does_zone_meet_g3_1_1c(rmi_b, zone, False, zones_and_systems):  # TODO is leap year true or false?
    #         zones_that_meetG3_1_1c_list.append(zone)

    for zone in zones_that_meetG3_1_1c_list:
        zones_and_systems[zone]["system_origin"] = "G3_1_1c"

        if is_cz_0_to_3a_bool(climate_zone_b):
            zones_and_systems[zone]["expected_system_type"] = HVAC_SYS.SYS_4
        else:
            zones_and_systems[zone]["expected_system_type"] = HVAC_SYS.SYS_3

    # select assigned system type based on total building area and number of floors
    if num_floors < 6 and area < BUILDING_AREA_150000_ft2:
        G3_1_1d_expected_system_type = HVAC_SYS.SYS_5
    else:
        G3_1_1d_expected_system_type = HVAC_SYS.SYS_7

    for zone in zones_and_systems:
        if does_zone_meet_g3_1_1d(rmi_b, zone):
            zones_and_systems[zone]["system_origin"] = "G3_1_1d"
            zones_and_systems[zone][
                "expected_system_type"
            ] = G3_1_1d_expected_system_type

    # G3.1.1e
    for zone in zones_and_systems:
        if not does_zone_meet_g3_1_1e(rmi_b, rmi_p, zone):
            zones_and_systems[zone]["system_origin"] = "G3_1_1e"

        if is_cz_0_to_3a_bool(climate_zone_b):
            zones_and_systems[zone]["expected_system_type"] = HVAC_SYS.SYS_10
        else:
            zones_and_systems[zone]["expected_system_type"] = HVAC_SYS.SYS_9

    # G3.1.1f
    for zone in zones_and_systems:
        if zones_and_systems[zone]["expected_system_type"] in [
            HVAC_SYS.SYS_9,
            HVAC_SYS.SYS_10,
        ]:
            zone_id = zone["id"]
            if does_zone_meet_g_3_1_1f(rmi_b, zone_id):
                zones_and_systems[zone]["system_origin"] = "G3_1_1f"

                bat = get_zone_hvac_bat_dict(rmi_b, zone_id)
                zones_and_systems[zone][
                    "expected_system_type"
                ] = expected_system_type_from_table_g3_1_1_dict(bat, num_floors, area)

    # G3.1.1g
    for zone in zones_and_systems:
        does_zone_meet_G = does_zone_meet_g3_1_1g(
            rmi_b,
            zone.id,
        )

        if does_zone_meet_G:
            total_computer_zones_peak_cooling_load = (
                get_computer_zones_peak_cooling_load(rmi_b, zone)
            )

        if (
            total_computer_zones_peak_cooling_load
            > COMPUTER_ROOM_PEAK_COOLING_LOAD_3000000_BTUH
        ):
            zones_and_systems[zone]["expected_system_type"] = HVAC_SYS.SYS_11_1
            zones_and_systems[zone]["system_origin"] = "G3_1_1g_part2"
        elif zones_and_systems[zone]["expected_system_type"] in [
            HVAC_SYS.SYS_7,
            HVAC_SYS.SYS_8,
        ]:
            if (
                total_computer_zones_peak_cooling_load
                > COMPUTER_ROOM_PEAK_COOLING_LOAD_600000_BTUH
            ):
                zones_and_systems[zone]["expected_system_type"] = HVAC_SYS.SYS_11_1
                zones_and_systems[zone]["system_origin"] = "G3_1_1g_part1"
            else:
                zones_and_systems[zone]["system_origin"] = "G3_1_1g_part3"
                if is_cz_0_to_3a_bool(climate_zone_b):
                    zones_and_systems[zone]["expected_system_type"] = HVAC_SYS.SYS_4
                else:
                    zones_and_systems[zone]["expected_system_type"] = HVAC_SYS.SYS_3

    return zones_and_systems
