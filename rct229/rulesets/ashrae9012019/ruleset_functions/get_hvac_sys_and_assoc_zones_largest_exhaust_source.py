from typing import TypedDict

from pint import Quantity
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import (
    find_exactly_one_hvac_system,
    find_exactly_one_zone,
)


class HVACSysAssocZonesLargestExhaustSource(TypedDict):
    hvac_fan_sys_exhaust_sum: Quantity
    maximum_zone_exhaust: Quantity
    num_hvac_exhaust_fans: int
    maximum_hvac_exhaust: Quantity


def get_hvac_sys_and_assoc_zones_largest_exhaust_source(
    rmd: dict, hvac_sys_id: str
) -> HVACSysAssocZonesLargestExhaustSource:
    """
    Returns a list with the sum of the hvac fan system exhaust fan cfm values, the maximum zone level exhaust source
    across the zones associated with the HVAC system, the number of exhaust fans associated with the hvac fan system,
    and the maximum cfm of all of the exhaust fans associated with the hvac system fan system [
    hvac_sys_exhaust_cfm_sum, maximum_zone_exhaust, num_hvac_exhaust_fans, maximum_hvac_exhaust]. This is for
    evaluating G3.1.2.10 exception 6 which states "Where the largest exhaust source is less than 75% of the design
    outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed
    design.

    Parameters
    ----------
    rmd dict
    Dictionary of a rule model description object in which the largest exhaust source CFM is to be returned.

    hvac_sys_id str
    The hvac system object id for which the largest exhaust source is being determined.

    Returns
    -------
    get_hvac_sys_and_assoc_zones_largest_exhaust_source: dict
    A dictionary with the sum of the hvac fan system exhaust fan cfm values, the maximum zone level exhaust source
    across the zones associated with the HVAC system, the number of exhaust fans associated with the hvac fan system,
    and the maximum cfm of all of the exhaust fans associated with the hvac system fan system
    {
    hvac_fan_sys_exhaust_sum: 3000,
    maximum_zone_exhaust: 500,
    num_hvac_exhaust_fans: 2,
    maximum_hvac_exhaust: 3000
    }.
    This is for evaluating G3.1.2.10 exception 6 which states "Where the largest exhaust source is less than 75% of the
    design outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed
    design.
    """
    zones_and_terminal_units_served_by_hvac_sys_dict = (
        get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd)
    )
    assert_(
        hvac_sys_id in zones_and_terminal_units_served_by_hvac_sys_dict,
        f"HVAC {hvac_sys_id} does not "
        f"associated terminals and zones "
        f"connected with. Check inputs!",
    )

    # HVAC level exhaust fan
    hvac = find_exactly_one_hvac_system(rmd, hvac_sys_id)
    hvac_fan_sys_exhaust_list = find_all("$.fan_system.exhaust_fans[*]", hvac)
    hvac_fan_sys_exhaust_flow_list = [
        exhaust_fan.get("design_airflow", ZERO.FLOW)
        for exhaust_fan in hvac_fan_sys_exhaust_list
    ]

    # zone level exhaust fan
    zone_id_list = zones_and_terminal_units_served_by_hvac_sys_dict[hvac_sys_id][
        "zone_list"
    ]
    zone_fan_exhaust_flow_list = list(
        filter(
            None,
            [
                exhaust_fan.get("design_airflow")
                for zone_id in zone_id_list
                for exhaust_fan in find_exactly_one_zone(rmd, zone_id).get(
                    "zonal_exhaust_fans", []
                )
            ],
        )
    )

    return {
        "hvac_fan_sys_exhaust_sum": sum(hvac_fan_sys_exhaust_flow_list, ZERO.FLOW),
        "maximum_zone_exhaust": max(zone_fan_exhaust_flow_list, default=ZERO.FLOW),
        "num_hvac_exhaust_fans": len(hvac_fan_sys_exhaust_list),
        "maximum_hvac_exhaust": max(hvac_fan_sys_exhaust_flow_list, default=ZERO.FLOW),
    }
