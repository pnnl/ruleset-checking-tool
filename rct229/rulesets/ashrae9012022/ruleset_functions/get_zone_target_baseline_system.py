from typing import TypedDict

from pydash import juxtapose
from rct229.rule_engine.memoize import memoize
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
    get_zone_conditioning_category_rmd_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.is_cz_0_to_3a_bool import (
    is_cz_0_to_3a_bool,
)
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all

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
    """
    Following G3.1.1, determines the baseline system type for each zone in a building

    Parameters
    ----------
    rmd_b: json
        RMD at RuleSetModelDescription level
    rmd_p: json
        RMD at RuleSetModelDescription level
    climate_zone_b: str
        baseline climate zone


    Returns
    -------
    zones_and_systems: a dictionary with zone / list pairs where the first value in the list is the expected system type (ex SYS_3) and the second value is the rule used to choose the system, (eg "G3_1_1e"): zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] = SYS_3; zones_and_systems[zone]["SYSTEM_ORIGIN"] = "G3_1_1e"

    """

    zone_conditioning_category_dict = get_zone_conditioning_category_rmd_dict(
        climate_zone_b, rmd_b
    )

    (
        list_building_area_types_and_zones_b,
        predominant_building_area_type_b,
        num_floors_b,
    ) = juxtapose(
        lambda cz, rmd: get_hvac_building_area_types_and_zones_dict(cz, rmd),
        lambda cz, rmd: get_predominant_hvac_building_area_type(cz, rmd),
        lambda cz, rmd: get_number_of_floors(cz, rmd),
    )(
        climate_zone_b, rmd_b
    )

    floor_area_b = sum(
        [
            list_building_area_types_and_zones_b[bat]["floor_area"]
            for bat in list_building_area_types_and_zones_b
        ]
    )
    expected_system_type_dict_b = expected_system_type_from_table_g3_1_1_dict(
        predominant_building_area_type_b, climate_zone_b, num_floors_b, floor_area_b
    )

    is_cz_0_to_3a_result_bool = is_cz_0_to_3a_bool(climate_zone_b)

    zones_and_systems_b = {
        zone_b["id"]: expected_system_type_dict_b
        for zone_b in find_all("$.buildings[*].building_segments[*].zones[*]", rmd_b)
        if zone_conditioning_category_dict[zone_b["id"]]
        in (
            ZCC.CONDITIONED_RESIDENTIAL,
            ZCC.CONDITIONED_NON_RESIDENTIAL,
            ZCC.CONDITIONED_MIXED,
        )
    }

    # go through each exception to Table G3.1.1 in order
    # G3.1.1b
    if floor_area_b > BUILDING_AREA_40000_ft2:
        for building_area_type in list_building_area_types_and_zones_b:
            if building_area_type != predominant_building_area_type_b and (
                list_building_area_types_and_zones_b[building_area_type]["floor_area"]
                >= BUILDING_AREA_20000_ft2
            ):
                secondary_system_type_b = expected_system_type_from_table_g3_1_1_dict(
                    building_area_type,
                    climate_zone_b,
                    num_floors_b,
                    floor_area_b,
                )
                for zone_id_b in zones_and_systems_b:
                    if (
                        zone_id_b
                        in list_building_area_types_and_zones_b[building_area_type][
                            "zone_ids"
                        ]
                    ):
                        zones_and_systems_b[zone_id_b] = {
                            "expected_system_type": secondary_system_type_b[
                                "expected_system_type"
                            ],
                            "system_origin": SYSTEMORIGIN.G311B,
                        }

    for zone_id_b in zones_and_systems_b:
        # G3.1.1c
        if does_zone_meet_g3_1_1c(rmd_b, zone_id_b, zones_and_systems_b):
            zones_and_systems_b[zone_id_b] = {
                "system_origin": SYSTEMORIGIN.G311C,
                "expected_system_type": HVAC_SYS.SYS_4
                if is_cz_0_to_3a_result_bool
                else HVAC_SYS.SYS_3,
            }

        # G3.1.1d
        if does_zone_meet_g3_1_1d(rmd_b, zone_id_b):
            zones_and_systems_b[zone_id_b] = {
                "system_origin": SYSTEMORIGIN.G311D,
                "expected_system_type": HVAC_SYS.SYS_5
                if num_floors_b < REQ_FL_6 and floor_area_b < BUILDING_AREA_150000_ft2
                else HVAC_SYS.SYS_7,
            }

        # G3.1.1e
        if does_zone_meet_g3_1_1e(rmd_b, rmd_p, zone_id_b):
            zones_and_systems_b[zone_id_b] = {
                "system_origin": SYSTEMORIGIN.G311E,
                "expected_system_type": HVAC_SYS.SYS_10
                if is_cz_0_to_3a_result_bool
                else HVAC_SYS.SYS_9,
            }

        # G3.1.1f
        if does_zone_meet_g_3_1_1f(rmd_b, zone_id_b) and zones_and_systems_b[zone_id_b][
            "expected_system_type"
        ] in (
            HVAC_SYS.SYS_9,
            HVAC_SYS.SYS_10,
        ):
            zone_hvac_bat_dict_b = get_zone_hvac_bat_dict(rmd_b, zone_id_b)

            zones_and_systems_b[zone_id_b] = {
                "system_origin": SYSTEMORIGIN.G311F,
                "expected_system_type": expected_system_type_from_table_g3_1_1_dict(
                    max(zone_hvac_bat_dict_b, key=zone_hvac_bat_dict_b.get),
                    climate_zone_b,
                    num_floors_b,
                    floor_area_b,
                )["expected_system_type"],
            }

        # G3.1.1g
        if does_zone_meet_g3_1_1g(
            rmd_b,
            zone_id_b,
        ):
            total_computer_zones_peak_cooling_load_b = (
                get_computer_zones_peak_cooling_load(rmd_b)
            )
            if (
                total_computer_zones_peak_cooling_load_b
                > COMPUTER_ROOM_PEAK_COOLING_LOAD_3000000_BTUH
            ) or (
                zones_and_systems_b[zone_id_b]["expected_system_type"]
                in (
                    HVAC_SYS.SYS_7,
                    HVAC_SYS.SYS_8,
                )
            ):
                zones_and_systems_b[zone_id_b] = {
                    "expected_system_type": HVAC_SYS.SYS_11_1,
                    "system_origin": "G3_1_1g_part2",
                }
            else:
                zones_and_systems_b[zone_id_b] = {
                    "expected_system_type": HVAC_SYS.SYS_4
                    if is_cz_0_to_3a_result_bool
                    else HVAC_SYS.SYS_3,
                    "system_origin": "G3_1_1g_part3",
                }

    return zones_and_systems_b
