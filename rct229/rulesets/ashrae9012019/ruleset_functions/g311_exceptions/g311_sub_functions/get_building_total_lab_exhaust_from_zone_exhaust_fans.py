from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_zone,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_building_lab_zones_list import (
    get_building_lab_zones_list,
)
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.pint_utils import ZERO


def get_building_total_lab_exhaust_from_zone_exhaust_fans(rmi):
    """
    Determines the total exhaust air flow rate for zone exhaust fans in zones that have laboratory spaces
    The function returns either ZERO.FLOW or exhaust flow, which means it won't fail if data is missing or error.

    Parameters
    ----------
    rmi dict
        A dictionary representing a ruleset model instance as defined by the ASHRAE229 schema

    Returns
    -------
    A numerical value indicating the total building exhaust airflow for zone exhaust fans in zones that have laboratory spaces
    """
    total_exhaust = ZERO.FLOW
    laboratory_zone_list = get_building_lab_zones_list(rmi)
    for zone_id in laboratory_zone_list:
        design_airflow = find_one(
            "$.zonal_exhaust_fan.design_airflow", find_exactly_one_zone(rmi, zone_id)
        )
        if design_airflow:
            total_exhaust += design_airflow

    return total_exhaust
