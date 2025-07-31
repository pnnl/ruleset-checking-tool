from pint import Quantity
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
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import (
    find_exactly_one_hvac_system,
    find_exactly_one_terminal_unit,
    find_exactly_one_zone,
)

BUILDING_TOTAL_LAB_EXHAUST_CFM_THRESHOLD = 15_000 * ureg("ft^3 / min")


def does_zone_meet_g3_1_1d(rmd: dict, zone_id: str) -> bool:
    """
    Determines whether a given zone meets the G3_1_1d exception "For laboratory spaces in a building having a total
    laboratory exhaust rate greater than 15,000 cfm, use a single system of type 5 or 7 serving only those spaces."


    Parameters
    ----------
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema
    zone_id str
        zone id

    Returns
    -------
    boolean True or False

    """

    def sum_total_primary_airflow_from_terminals_func(terminal_list: list) -> Quantity:
        """
        Return sum of the primary airflow from all terminals in the terminal list
        Return ZERO.FLOW if none is found.
        """
        return sum(
            [
                find_exactly_one_terminal_unit(rmd, terminal_id).get(
                    "primary_airflow", ZERO.FLOW
                )
                for terminal_id in terminal_list
            ],
            ZERO.FLOW,
        )

    def sum_zone_primary_airflow_from_terminals_func(
        terminal_list: list, zone: dict
    ) -> Quantity:
        """
        Return sum of the primary airflow from all terminals exist both in the terminal_list and zone
        Return ZERO.FLOW if none is found.
        """
        return sum(
            [
                find_exactly_one_terminal_unit(rmd, terminal_id).get(
                    "primary_airflow", ZERO.FLOW
                )
                for terminal_id in terminal_list
                if find_one(f'$.terminals[*][?(@.id="{terminal_id}")]', zone)
            ],
            ZERO.FLOW,
        )

    def sum_hvac_total_exhaust_air_func(hvac_id: str) -> Quantity:
        """Return sum of the design airflow from all exhaust fans in the HVAC."""
        return sum(
            find_all(
                "$.fan_system.exhaust_fans[*].design_airflow",
                find_exactly_one_hvac_system(rmd, hvac_id),
            ),
            ZERO.FLOW,
        )

    laboratory_zones_list = get_building_lab_zones_list(rmd)
    building_total_lab_exhaust = get_building_total_lab_exhaust_from_zone_exhaust_fans(
        rmd
    )

    dict_of_zones_and_terminal_units_served_by_hvac_sys = (
        get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd)
    )

    if building_total_lab_exhaust <= BUILDING_TOTAL_LAB_EXHAUST_CFM_THRESHOLD:
        for lab_zone_id in laboratory_zones_list:
            lab_zone = find_exactly_one_zone(rmd, lab_zone_id)
            hvac_sys_list_serving_zone = get_list_hvac_systems_associated_with_zone(
                rmd, lab_zone_id
            )

            zone_total_exhaust = ZERO.FLOW
            for hvac_id in hvac_sys_list_serving_zone:
                # The hvac_id seems to be guaranteed in this dictionary.
                # One alternative is to use getattr_ to avoid any possible errors.
                terminal_list_hvac_sys = (
                    dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_id][
                        "terminal_unit_list"
                    ]
                )

                # sum of the exhaust air in the HVAC.
                hvac_system_total_exhaust_airflow = sum_hvac_total_exhaust_air_func(
                    hvac_id
                )

                # sum of primary airflow from terminals that have association with the HVAC.
                total_terminal_air_flow = sum_total_primary_airflow_from_terminals_func(
                    terminal_list_hvac_sys
                )

                # sum of primary airflow from terminals that have association with the lab zone
                zone_primary_air_flow = sum_zone_primary_airflow_from_terminals_func(
                    terminal_list_hvac_sys, lab_zone
                )

                if zone_primary_air_flow > ZERO.FLOW:
                    # note: total_terminal_air_flow > zone_primary_air_flow > ZERO.FLOW
                    zone_total_exhaust += (
                        hvac_system_total_exhaust_airflow
                        * zone_primary_air_flow
                        / total_terminal_air_flow
                    )
                else:
                    zone_total_exhaust += hvac_system_total_exhaust_airflow

            building_total_lab_exhaust += zone_total_exhaust

    return (
        zone_id in laboratory_zones_list
        and building_total_lab_exhaust > BUILDING_TOTAL_LAB_EXHAUST_CFM_THRESHOLD
    )
