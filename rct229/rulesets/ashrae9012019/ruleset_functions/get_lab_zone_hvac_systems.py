from typing import TypedDict

from pint import Quantity
from pydash import map_
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_target_baseline_system import (
    SYSTEMORIGIN,
    get_zone_target_baseline_system,
)


class HVACServeLabZoneDict(TypedDict):
    lab_zones_only: list[str]
    lab_and_other: list[str]


def get_lab_zone_hvac_systems(
    rmd_b: dict, rmd_p: dict, climate_zone: str
) -> HVACServeLabZoneDict:
    """
    returns a list of HVAC systems serving only lab zones

    Parameters
    ----------
    rmd_b: json
        RMD at RuleSetModelDescription level
    rmd_p: json
        RMD at RuleSetModelDescription level
    climate_zone: str
        baseline climate zone

    Returns
    -------
    hvac_systems_serving_lab_zones: A dictionary consisting of two lists of hvac system ids.
    One list ["lab_zones_only"] is a list of hvac system ids where each hvac system serves only lab zones.
    The other ["lab_and_other"] is a list of hvac system ids where systems serve both labs and other zones.
    """

    target_baseline_systems = get_zone_target_baseline_system(
        rmd_b, rmd_p, climate_zone
    )

    # find zone ids whose `system_origin` is `SYSTEMORIGIN.G311D`
    building_lab_zones = [
        zone_id_b
        for zone_id_b in target_baseline_systems
        if target_baseline_systems[zone_id_b]["system_origin"] == SYSTEMORIGIN.G311D
    ]

    hvac_systems_serving_lab_zones: HVACServeLabZoneDict = {
        "lab_zones_only": [],
        "lab_and_other": [],
    }
    if building_lab_zones:
        dict_of_zones_and_hvac_systems_b = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
        )

        for hvac_id_b in dict_of_zones_and_hvac_systems_b:
            zones_served_by_hvac_system_b = dict_of_zones_and_hvac_systems_b[hvac_id_b][
                "zone_list"
            ]

            is_zone_in_building_lab_zones_b = map_(
                zones_served_by_hvac_system_b,
                lambda zone_id_b: zone_id_b in building_lab_zones,
            )

            if all(is_zone_in_building_lab_zones_b):
                hvac_systems_serving_lab_zones["lab_zones_only"].append(hvac_id_b)

            elif any(is_zone_in_building_lab_zones_b):
                hvac_systems_serving_lab_zones["lab_and_other"].append(hvac_id_b)

    return hvac_systems_serving_lab_zones
