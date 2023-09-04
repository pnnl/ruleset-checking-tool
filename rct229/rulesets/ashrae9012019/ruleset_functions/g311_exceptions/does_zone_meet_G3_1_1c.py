from pydash import drop, map_
import numpy as np

from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zone_eflh import (
    get_zone_eflh,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zones_computer_rooms import (
    get_zone_computer_rooms,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zones_on_same_floor_list import (
    get_zones_on_same_floor_list,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_peak_internal_load_floor_area_dict import (
    get_zone_peak_internal_load_floor_area_dict,
)
from rct229.schema.config import ureg
from rct229.utils.pint_utils import ZERO

ELIGIBLE_PRIMARY_SYSTEM_TYPES = [
    # HVAC_SYS.SYS_5,
    # HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    # HVAC_SYS.SYS_8,
]

NUMBER_OF_WEEKS_IN_YEAR = 52.1429
NUMBER_OF_WEEKS_IN_LEAP_YEAR = 52.2857
LOAD_THRESHOLD = 10 * ureg("Btu/hr/ft2")
EFLH_THRESHOLD = 40


def does_zone_meet_g3_1_1c(rmi, zone_id, is_leap_year, zones_and_systems):
    """
    Determines whether a given zone meets the G3_1_1c exception "If the baseline HVAC system type is 5, 6, 7,
    8 use separate single-zone systems conforming with the requirements of system 3 or system 4 (depending on
    building heating source) for any spaces that have occupancy or process loads or schedules that differ
    significantly from the rest of the building. Peak thermal loads that differ by 10 Btu/h·ft2 (2.930710 W/sf) or
    more from the average of other spaces served by the system, or schedules that differ by more than 40 equivalent
    full-load hours per week from other spaces served by the system, are considered to differ significantly. Examples
    where this exception may be applicable include but are not limited to natatoriums and continually occupied
    security areas. This exception does not apply to computer rooms.

    Parameters
    ----------
    rmi dict
        A dictionary representing a ruleset model instance as defined by the ASHRAE229 schema
    zone_id str
        zone id
    is_leap_year boolean
        flag indicates whether the model is simulated in a leap year
    zones_and_systems dict
        a dict map zone to an object that carries expected_system_type and system type string

    Returns
    -------
    boolean, true or false
    """

    def get_zone_weekly_eflh(z_id):
        # function to get weekly zone eflh
        zone_eflh = get_zone_eflh(rmi, z_id, is_leap_year)
        return (
            zone_eflh / NUMBER_OF_WEEKS_IN_LEAP_YEAR
            if is_leap_year
            else zone_eflh / NUMBER_OF_WEEKS_IN_YEAR
        )

    expected_system_type = zones_and_systems[zone_id]["expected_system_type"]
    system_matched = any(
        [
            baseline_system_type_compare(
                expected_system_type,
                target_system_type,
                exact_match=False,
            )
            for target_system_type in ELIGIBLE_PRIMARY_SYSTEM_TYPES
        ]
    )
    meet_g3_1_1c_flag = False
    if system_matched:
        zones_on_same_floor_ids = get_zones_on_same_floor_list(rmi, zone_id)
        # drop zone_id in the list
        zones_on_same_floor_ids.remove(zone_id)
        # keep only matched system type
        zones_same_floor_same_system_type = list(
            filter(
                lambda other_zone_id: zones_and_systems[other_zone_id][
                    "expected_system_type"
                ]
                == expected_system_type,
                zones_on_same_floor_ids,
            )
        )
        # In here, the function assumes the zones_and_systems keys are
        # a list of conditioned or semi-conditioned zones only
        zone_load_and_eflh_list = [
            (
                get_zone_peak_internal_load_floor_area_dict(rmi, other_match_zone_id),
                get_zone_weekly_eflh(other_match_zone_id),
            )
            for other_match_zone_id in zones_same_floor_same_system_type
            if other_match_zone_id in zones_and_systems.keys()
        ]

        system_total_area = sum(map_(zone_load_and_eflh_list, "0.area"), ZERO.AREA)
        system_total_load = sum(map_(zone_load_and_eflh_list, "0.peak"), ZERO.POWER)
        avg_eflh = (
            np.dot(
                map_(zone_load_and_eflh_list, lambda zl: zl[1]),
                map_(zone_load_and_eflh_list, lambda zl: zl[0]["area"].magnitude),
            )
            / system_total_area.magnitude
        ) if system_total_area != ZERO.AREA else 0.0

        avg_internal_load = system_total_load / system_total_area if system_total_area != ZERO.AREA else 0.0

        zone_internal_loads = get_zone_peak_internal_load_floor_area_dict(rmi, zone_id)
        zone_eflh = get_zone_weekly_eflh(zone_id)

        meet_g3_1_1c_flag = (
            abs(
                zone_internal_loads["peak"] / zone_internal_loads["area"]
                - avg_internal_load
            )
            > LOAD_THRESHOLD
            or zone_eflh - avg_eflh > EFLH_THRESHOLD
        )

        if meet_g3_1_1c_flag:
            meet_g3_1_1c_flag = zone_id not in get_zone_computer_rooms(rmi)

    return meet_g3_1_1c_flag
