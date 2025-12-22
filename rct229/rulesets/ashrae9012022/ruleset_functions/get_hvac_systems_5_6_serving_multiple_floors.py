from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_by_rmd_dict,
)
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import find_exactly_one_zone

APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_5, HVAC_SYS.SYS_6]


def get_hvac_systems_5_6_serving_multiple_floors(rmd: dict) -> dict[str, int]:
    """
    Get the list of HVAC system IDs which are baseline system type 5 or 6 and are serving multiple floors.

    Parameters
    ----------
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema.

        To determine hvac system IDs which are baseline system types 5 or 6 and serve multiple floors.

    Returns
    -------
    hvac_systems_5_6_serving_multiple_floors_dict dict
        A dict that stores all hvac system IDs that are types 5 or 6 and serve multiple floors as dict keys,
        and the number of floors served as dict values.
    """
    baseline_hvac_system_types_dict = get_baseline_system_types(rmd)
    hvac_zone_list_w_area_dict = get_hvac_zone_list_w_area_by_rmd_dict(rmd)
    hvac_systems_5_6_serving_multiple_floors_dict = {}

    for hvac_b in find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        rmd,
    ):
        system_type_b = next(
            (
                key
                for key, values in baseline_hvac_system_types_dict.items()
                if hvac_b["id"] in values
            ),
            None,
        )

        if not any(
            baseline_system_type_compare(system_type_b, applicable_sys_type, False)
            for applicable_sys_type in APPLICABLE_SYS_TYPES
        ):
            continue

        assert_(
            hvac_zone_list_w_area_dict.get(hvac_b["id"]),
            f"HVAC system {hvac_b['id']} is missing in the zone.terminals data group.",
        )

        hvac_sys_zone_id_list = hvac_zone_list_w_area_dict[hvac_b["id"]]["zone_list"]

        hvac_zones_list = [
            find_exactly_one_zone(rmd, zone_id) for zone_id in hvac_sys_zone_id_list
        ]

        hvac_floors_served_set = {
            hvac_zone["floor_name"] for hvac_zone in hvac_zones_list
        }

        if len(hvac_floors_served_set) > 1:
            hvac_systems_5_6_serving_multiple_floors_dict[hvac_b["id"]] = len(
                hvac_floors_served_set
            )

    return hvac_systems_5_6_serving_multiple_floors_dict
