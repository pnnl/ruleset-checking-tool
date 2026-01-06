from typing import TypedDict

from rct229.rule_engine.memoize import memoize
from rct229.rulesets.ashrae9012022.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g3212_exceptions.does_zone_meet_G3_2_1_2_a import (
    does_zone_meet_g3_2_1_2_a,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g3212_exceptions.does_zone_meet_G3_2_1_2_b import (
    does_zone_meet_g3_2_1_2_b,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g3212_exceptions.does_zone_meet_G3_2_1_2_c import (
    does_zone_meet_g3_2_1_2_c,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g3212_exceptions.g3212_sub_functions.expected_system_type_from_table_g311a_dict import (
    expected_system_type_from_table_g3_1_1_dict,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g3212_exceptions.g3212_sub_functions.get_zones_computer_rooms import (
    get_zone_computer_rooms,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g3212_exceptions.g3212_sub_functions.get_zone_peak_internal_load_floor_area_dict import (
    get_zone_peak_internal_load_floor_area_dict,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g3212_exceptions.g3212_sub_functions.get_computer_zones_peak_cooling_load import (
    get_total_computer_zones_peak_cooling_load,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g3212_exceptions.g3212_sub_functions.get_hvac_building_area_types_and_zones_dict import (
    get_hvac_building_area_types_and_zones_dict,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g3212_exceptions.g3212_sub_functions.get_number_of_floors import (
    get_number_of_floors,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g3212_exceptions.g3212_sub_functions.get_predominant_hvac_building_area_type import (
    get_predominant_hvac_building_area_type,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g3212_exceptions.g3212_sub_functions.get_zone_hvac_bat import (
    get_zone_hvac_bat_dict,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.g3212_exceptions.g3212_sub_functions.is_zone_mechanically_cooled import (
    is_zone_mechanically_cooled,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
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
    G311 = "G3_1_1"
    G3212A = "G3_2_1_2a"  # exception for zones with different peak internal loads
    G3212B = "G3_2_1_2b"  # exception for laboratory exhaust
    G3212C = "G3_2_1_2c"  # exception for heating-only stairwells, vestibules, etc
    G3212D = (
        "G3_2_1_2d"  # exception for heating-only zones with cooling in proposed design
    )
    G3212E = "G3_2_1_2e"  # exception for computer rooms. mislabeled in the standard as a duplicated G3.1.1.2d. Corrected here to e.
    G3212F = "G3_2_1_2f"  # exception for residential-associated zones. Corrected here to f due to mislabeling above.


@memoize
def get_zone_target_baseline_system(
    rmd_b: dict, rmd_p: dict, climate_zone_b: str
) -> dict[str, ZoneandSystem]:

    zone_conditioning_category_dict = get_zone_conditioning_category_rmd_dict(
        climate_zone_b, rmd_b
    )

    bat_dict = get_hvac_building_area_types_and_zones_dict(climate_zone_b, rmd_b)
    predominant_bat = get_predominant_hvac_building_area_type(climate_zone_b, rmd_b)
    num_floors = get_number_of_floors(climate_zone_b, rmd_b)

    floor_area = sum(bat["floor_area"] for bat in bat_dict.values())

    baseline_sys = expected_system_type_from_table_g3_1_1_dict(
        predominant_bat,
        climate_zone_b,
        num_floors,
        floor_area,
    )

    is_cz_0_to_3a = is_cz_0_to_3a_bool(climate_zone_b)

    zones_and_systems: dict[str, ZoneandSystem] = {}

    for building in rmd_b.get("buildings", []):
        for segment in building.get("building_segments", []):
            for zone in segment.get("zones", []):
                zid = zone["id"]
                if zone_conditioning_category_dict.get(zid) in (
                    ZCC.CONDITIONED_RESIDENTIAL,
                    ZCC.CONDITIONED_NON_RESIDENTIAL,
                    ZCC.CONDITIONED_MIXED,
                ):
                    zones_and_systems[zid] = baseline_sys.copy()

    if floor_area > BUILDING_AREA_40000_ft2:
        for bat, bat_data in bat_dict.items():
            if (
                bat != predominant_bat
                and bat_data["floor_area"] >= BUILDING_AREA_20000_ft2
            ):
                secondary_sys = expected_system_type_from_table_g3_1_1_dict(
                    bat,
                    climate_zone_b,
                    num_floors,
                    floor_area,
                )["expected_system_type"]

                for zid in bat_data["zone_ids"]:
                    if zid in zones_and_systems:
                        zones_and_systems[zid] = {
                            "expected_system_type": secondary_sys,
                            "system_origin": SYSTEMORIGIN.G311,
                        }

    total_computer_peak = get_total_computer_zones_peak_cooling_load(rmd_b)
    computer_room_zones = get_zone_computer_rooms(rmd_b)

    for zid, zone_sys in list(zones_and_systems.items()):
        current_sys = zone_sys["expected_system_type"]

        if does_zone_meet_g3_2_1_2_a(rmd_b, zid, zones_and_systems):
            zones_and_systems[zid] = {
                "system_origin": SYSTEMORIGIN.G3212A,
                "expected_system_type": HVAC_SYS.SYS_4
                if is_cz_0_to_3a
                else HVAC_SYS.SYS_3,
            }
            current_sys = zones_and_systems[zid]["expected_system_type"]

        if does_zone_meet_g3_2_1_2_b(rmd_b, zid):
            zones_and_systems[zid] = {
                "system_origin": SYSTEMORIGIN.G3212B,
                "expected_system_type": HVAC_SYS.SYS_5
                if num_floors < REQ_FL_6 and floor_area < BUILDING_AREA_150000_ft2
                else HVAC_SYS.SYS_7,
            }
            current_sys = zones_and_systems[zid]["expected_system_type"]

        if does_zone_meet_g3_2_1_2_c(rmd_b, rmd_p, zid):
            zones_and_systems[zid] = {
                "system_origin": SYSTEMORIGIN.G3212C,
                "expected_system_type": HVAC_SYS.SYS_10
                if is_cz_0_to_3a
                else HVAC_SYS.SYS_9,
            }
            current_sys = zones_and_systems[zid]["expected_system_type"]

        if current_sys in (
            HVAC_SYS.SYS_9,
            HVAC_SYS.SYS_10,
        ) and is_zone_mechanically_cooled(rmd_b, zid):
            bat_map = get_zone_hvac_bat_dict(rmd_b, zid)
            dominant_bat = max(bat_map, key=bat_map.get)

            zones_and_systems[zid] = {
                "system_origin": SYSTEMORIGIN.G3212D,
                "expected_system_type": expected_system_type_from_table_g3_1_1_dict(
                    dominant_bat,
                    climate_zone_b,
                    num_floors,
                    floor_area,
                )["expected_system_type"],
            }
            current_sys = zones_and_systems[zid]["expected_system_type"]

        if zid in computer_room_zones:
            if total_computer_peak > COMPUTER_ROOM_PEAK_COOLING_LOAD_3000000_BTUH:
                zones_and_systems[zid] = {
                    "expected_system_type": HVAC_SYS.SYS_11_1,
                    "system_origin": SYSTEMORIGIN.G3212E,
                }
            else:
                peak = get_zone_peak_internal_load_floor_area_dict(rmd_b, zid)["peak"]
                if (
                    peak > COMPUTER_ROOM_PEAK_COOLING_LOAD_600000_BTUH
                    and current_sys in (HVAC_SYS.SYS_7, HVAC_SYS.SYS_8)
                ):
                    zones_and_systems[zid] = {
                        "expected_system_type": HVAC_SYS.SYS_11_1,
                        "system_origin": SYSTEMORIGIN.G3212E,
                    }
                else:
                    zones_and_systems[zid] = {
                        "expected_system_type": HVAC_SYS.SYS_4
                        if is_cz_0_to_3a
                        else HVAC_SYS.SYS_3,
                        "system_origin": SYSTEMORIGIN.G3212E,
                    }

        if (
            zone_conditioning_category_dict[zid]
            == ZCC.CONDITIONED_RESIDENTIAL_ASSOCIATED
        ):
            zones_and_systems[zid] = {
                "expected_system_type": HVAC_SYS.SYS_4
                if is_cz_0_to_3a
                else HVAC_SYS.SYS_3,
                "system_origin": SYSTEMORIGIN.G3212F,
            }

    return zones_and_systems
