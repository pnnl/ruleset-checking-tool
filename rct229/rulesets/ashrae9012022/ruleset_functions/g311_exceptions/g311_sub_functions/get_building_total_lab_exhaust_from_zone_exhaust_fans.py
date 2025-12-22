from pint import Quantity
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_building_lab_zones_list import (
    get_building_lab_zones_list,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import find_exactly_one_zone


def get_building_total_lab_exhaust_from_zone_exhaust_fans(rmd: dict) -> Quantity:
    """
    Determines the total exhaust air flow rate for zone exhaust fans in zones that have laboratory spaces
    The function returns either ZERO.FLOW or exhaust flow, which means it won't fail if data is missing or error.

    Parameters
    ----------
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema

    Returns
    -------
    A numerical value indicating the total building exhaust airflow for zone exhaust fans in zones that have laboratory spaces
    """
    total_exhaust = ZERO.FLOW
    laboratory_zone_list = get_building_lab_zones_list(rmd)
    for zone_id in laboratory_zone_list:
        design_airflow = sum(
            find_all(
                "$.zonal_exhaust_fans[*].design_airflow",
                find_exactly_one_zone(rmd, zone_id),
            )
        )
        if design_airflow:
            total_exhaust += design_airflow

    return total_exhaust
