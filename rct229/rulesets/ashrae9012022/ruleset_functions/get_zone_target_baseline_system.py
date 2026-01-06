from typing import TypedDict

from rct229.rule_engine.memoize import memoize
from rct229.rulesets.ashrae9012022.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1c import (
    does_zone_meet_g3_1_1c,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1d import (
    does_zone_meet_g3_1_1d,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1e import (
    does_zone_meet_g3_1_1e,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1f import (
    does_zone_meet_g_3_1_1f,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g311_exceptions.does_zone_meet_G3_1_1g import (
    does_zone_meet_g3_1_1g,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g311_exceptions.g311_sub_functions.expected_system_type_from_table_g311a_dict import (
    expected_system_type_from_table_g3_1_1_dict,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g311_exceptions.g311_sub_functions.get_computer_zones_peak_cooling_load import (
    get_computer_zones_peak_cooling_load,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g311_exceptions.g311_sub_functions.get_hvac_building_area_types_and_zones_dict import (
    get_hvac_building_area_types_and_zones_dict,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g311_exceptions.g311_sub_functions.get_number_of_floors import (
    get_number_of_floors,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g311_exceptions.g311_sub_functions.get_predominant_hvac_building_area_type import (
    get_predominant_hvac_building_area_type,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g311_exceptions.g311_sub_functions.get_zone_hvac_bat import (
    get_zone_hvac_bat_dict,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_rmd_dict,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.is_cz_0_to_3a_bool import (
    is_cz_0_to_3a_bool,
)
from rct229.schema.config import ureg

BUILDING_AREA_20000_ft2 = 20000 * ureg("ft2")
BUILDING_AREA_40000_ft2 = 40000 * ureg("ft2")
BUILDING_AREA_150000_ft2 = 150000 * ureg("ft2")
REQ_FL_6 = 6
COMPUTER_ROOM_PEAK_COOLING_LOAD_600000_BTUH = 600000 * ureg("Btu/hr")
COMPUTER_ROOM_PEAK_COOLING_LOAD_3000000_BTUH = 3000000 * ureg("Btu/hr")


class ZoneandSystem(TypedDict):
    expected_system_type: str
    system_origin: str


class SYSTEMORIGIN:
    G311B = "G3_1_1b"
    G311C = "G3_1_1c"
    G311D = "G3_1_1d"
    G311E = "G3_1_1e"
    G311F = "G3_1_1f"


@memoize
def get_zone_target_baseline_system(
    rmd_b: dict, rmd_p: dict, climate_zone_b: str
) -> dict[str, ZoneandSystem]:

    zone_conditioning_category_dict = get_zone_conditioning_category_rmd_dict(
        climate_zone_b, rmd_b
    )

    list_building_area_types_and_zones_b = get_hvac_building_area_types_and_zones_dict(
        climate_zone_b, rmd_b
    )
    predominant_building_area_type_b = get_predominant_hvac_building_area_type(
        climate_zone_b, rmd_b
    )
    num_floors_b = get_number_of_floors(climate_zone_b, rmd_b)

    floor_area_b = sum(
        bat["floor_area"] for bat in list_building_area_types_and_zones_b.values()
    )

    baseline_system_dict = expected_system_type_from_table_g3_1_1_dict(
        predominant_building_area_type_b,
        climate_zone_b,
        num_floors_b,
        floor_area_b,
    )

    is_cz_0_to_3a = is_cz_0_to_3a_bool(climate_zone_b)

    # --------------------------------------------------------------
    # Initialize baseline zones
    # --------------------------------------------------------------
    zones_and_systems_b: dict[str, ZoneandSystem] = {}

    for building in rmd_b.get("buildings", []):
        for segment in building.get("building_segments", []):
            for zone in segment.get("zones", []):
                zone_id = zone["id"]
                if zone_conditioning_category_dict.get(zone_id) in (
                    ZCC.CONDITIONED_RESIDENTIAL,
                    ZCC.CONDITIONED_NON_RESIDENTIAL,
                    ZCC.CONDITIONED_MIXED,
                ):
                    zones_and_systems_b[zone_id] = baseline_system_dict.copy()

    # --------------------------------------------------------------
    # G3.1.1b
    # --------------------------------------------------------------
    if floor_area_b > BUILDING_AREA_40000_ft2:
        for bat, bat_data in list_building_area_types_and_zones_b.items():
            if (
                bat != predominant_building_area_type_b
                and bat_data["floor_area"] >= BUILDING_AREA_20000_ft2
            ):
                secondary_sys = expected_system_type_from_table_g3_1_1_dict(
                    bat,
                    climate_zone_b,
                    num_floors_b,
                    floor_area_b,
                )["expected_system_type"]

                for zone_id in bat_data["zone_ids"]:
                    if zone_id in zones_and_systems_b:
                        zones_and_systems_b[zone_id] = {
                            "expected_system_type": secondary_sys,
                            "system_origin": SYSTEMORIGIN.G311B,
                        }

    # --------------------------------------------------------------
    # Precompute expensive globals
    # --------------------------------------------------------------
    total_computer_peak = get_computer_zones_peak_cooling_load(rmd_b)

    # --------------------------------------------------------------
    # Per-zone exceptions (ordered)
    # --------------------------------------------------------------
    for zone_id, zone_sys in zones_and_systems_b.items():
        current_sys = zone_sys["expected_system_type"]

        # G3.1.1c
        if does_zone_meet_g3_1_1c(rmd_b, zone_id, zones_and_systems_b):
            zones_and_systems_b[zone_id] = {
                "system_origin": SYSTEMORIGIN.G311C,
                "expected_system_type": HVAC_SYS.SYS_4
                if is_cz_0_to_3a
                else HVAC_SYS.SYS_3,
            }
            current_sys = zones_and_systems_b[zone_id]["expected_system_type"]

        # G3.1.1d
        if does_zone_meet_g3_1_1d(rmd_b, zone_id):
            zones_and_systems_b[zone_id] = {
                "system_origin": SYSTEMORIGIN.G311D,
                "expected_system_type": HVAC_SYS.SYS_5
                if num_floors_b < REQ_FL_6 and floor_area_b < BUILDING_AREA_150000_ft2
                else HVAC_SYS.SYS_7,
            }
            current_sys = zones_and_systems_b[zone_id]["expected_system_type"]

        # G3.1.1e
        if does_zone_meet_g3_1_1e(rmd_b, rmd_p, zone_id):
            zones_and_systems_b[zone_id] = {
                "system_origin": SYSTEMORIGIN.G311E,
                "expected_system_type": HVAC_SYS.SYS_10
                if is_cz_0_to_3a
                else HVAC_SYS.SYS_9,
            }
            current_sys = zones_and_systems_b[zone_id]["expected_system_type"]

        # G3.1.1f
        if current_sys in (HVAC_SYS.SYS_9, HVAC_SYS.SYS_10) and does_zone_meet_g_3_1_1f(
            rmd_b, zone_id
        ):
            zone_hvac_bat_dict = get_zone_hvac_bat_dict(rmd_b, zone_id)
            dominant_bat = max(zone_hvac_bat_dict, key=zone_hvac_bat_dict.get)

            zones_and_systems_b[zone_id] = {
                "system_origin": SYSTEMORIGIN.G311F,
                "expected_system_type": expected_system_type_from_table_g3_1_1_dict(
                    dominant_bat,
                    climate_zone_b,
                    num_floors_b,
                    floor_area_b,
                )["expected_system_type"],
            }
            current_sys = zones_and_systems_b[zone_id]["expected_system_type"]

        # G3.1.1g
        if does_zone_meet_g3_1_1g(rmd_b, zone_id):
            if (
                total_computer_peak > COMPUTER_ROOM_PEAK_COOLING_LOAD_3000000_BTUH
                or current_sys in (HVAC_SYS.SYS_7, HVAC_SYS.SYS_8)
            ):
                zones_and_systems_b[zone_id] = {
                    "expected_system_type": HVAC_SYS.SYS_11_1,
                    "system_origin": "G3_1_1g_part2",
                }
            else:
                zones_and_systems_b[zone_id] = {
                    "expected_system_type": HVAC_SYS.SYS_4
                    if is_cz_0_to_3a
                    else HVAC_SYS.SYS_3,
                    "system_origin": "G3_1_1g_part3",
                }

    return zones_and_systems_b
