from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
    find_exactly_one_terminal_unit,
    find_exactly_one_zone,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_building_lab_zones_list import (
    get_building_lab_zones_list,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_building_total_lab_exhaust_from_zone_exhaust_fans import (
    get_building_total_lab_exhaust_from_zone_exhaust_fans,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO, pint_sum

BUILDING_TOTAL_LAB_EXHAUST_CFM = 15_000 * ureg("ft^3 / min")


def does_zone_meet_g3_1_1d(rmi: dict, zone_id: str, zones_and_systems: dict):
    """
    Determines whether a given zone meets the G3_1_1d exception "For laboratory spaces in a building having a total
    laboratory exhaust rate greater than 15,000 cfm, use a single system of type 5 or 7 serving only those spaces."


    Parameters
    ----------
    rmi dict
        A dictionary representing a ruleset model instance as defined by the ASHRAE229 schema
    zone_id str
        zone id
    zones_and_systems dict
        This is a dict of the existing expected system types from the function get_zone_target_baseline_system

    Returns
    -------
    boolean True or False

    """
    laboratory_zones_list = get_building_lab_zones_list(rmi)
    building_total_lab_exhaust = get_building_total_lab_exhaust_from_zone_exhaust_fans(
        rmi
    )
    dict_of_zones_and_terminal_units_served_by_hvac_sys = (
        get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmi)
    )

    if building_total_lab_exhaust <= BUILDING_TOTAL_LAB_EXHAUST_CFM:
        for lab_zone_id in laboratory_zones_list:
            lab_zone = find_exactly_one_zone(rmi, lab_zone_id)
            hvac_sys_list_serving_zone = get_list_hvac_systems_associated_with_zone(
                rmi, lab_zone_id
            )

            zone_total_exhaust = ZERO.FLOW
            for hvac_id in hvac_sys_list_serving_zone:
                # sum of the exhaust air in the associated HVAC.
                hvac_system_total_exhaust_airflow = pint_sum(
                    find_all(
                        "$.fan_system.exhaust_fans[*].design_airflow",
                        find_exactly_one_hvac_system(rmi, hvac_id),
                    ),
                    ZERO.FLOW,
                )

                total_terminal_air_flow = ZERO.FLOW
                zone_primary_air_flow = ZERO.FLOW

                # The hvac_id seems to be guaranteed in this dictionary.
                # One alternative is to use getattr_ to avoid any possible errors.
                terminal_list_hvac_sys = (
                    dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_id][
                        "terminal_unit_list"
                    ]
                )

                for terminal_id in terminal_list_hvac_sys:
                    terminal_primary_airflow = find_exactly_one_terminal_unit(
                        rmi, terminal_id
                    ).get("primary_airflow", ZERO.FLOW)
                    total_terminal_air_flow += terminal_primary_airflow
                    # if the terminal is in the lab zone.
                    if find_one(f'$.terminals[*][?(@.id="{terminal_id}")]', lab_zone):
                        zone_primary_air_flow += terminal_primary_airflow

                if (
                    zone_primary_air_flow > ZERO.FLOW
                    and hvac_system_total_exhaust_airflow > ZERO.FLOW
                ):
                    # note: total_terminal_air_flow > zone_primary_air_flow > ZERO.FLOW
                    zone_total_exhaust += (
                        hvac_system_total_exhaust_airflow
                        * zone_primary_air_flow
                        / total_terminal_air_flow
                    )
                else:
                    zone_total_exhaust += hvac_system_total_exhaust_airflow

            building_total_lab_exhaust += (
                building_total_lab_exhaust + zone_total_exhaust
            )

    return (
        zone_id in laboratory_zones_list
        and building_total_lab_exhaust > BUILDING_TOTAL_LAB_EXHAUST_CFM
    )
