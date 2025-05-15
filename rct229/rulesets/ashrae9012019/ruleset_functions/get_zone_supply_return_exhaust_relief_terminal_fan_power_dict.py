from typing import TypedDict

from pint import Quantity
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_object_electric_power import (
    get_fan_object_electric_power,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_system_object_supply_return_exhaust_relief_total_power_flow import (
    get_fan_system_object_supply_return_exhaust_relief_total_power_flow,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import (
    find_exactly_one_hvac_system,
    find_exactly_one_terminal_unit,
)


def FanPowerInfo(TypedDict):
    supply_fans_power: Quantity
    return_fans_power: Quantity
    exhaust_fans_power: Quantity
    relief_fans_power: Quantity
    terminal_fans_power: Quantity


def get_zone_supply_return_exhaust_relief_terminal_fan_power_dict(
    rmd: dict,
) -> dict[str, FanPowerInfo]:
    """
    Get the supply, return, exhaust, relief, and terminal total fan power for each zone. The function returns a
    dictionary that saves each zone's supply, return, exhaust, relief and terminal unit fan power as a list {zone.id:
    [supply fan power kW, return fan power kW, exhaust fan power kW, relief fan power kW, terminal fan power]}.
    Values will be equal to zero where not defined for a fan system. Zonal exhaust and non-mechanical cooling is not
    included. This function first identifies if a HVAC system is serving more than one zone, in which case the fan
    power is apportioned to the zone based on the fraction of airflow to that zone. For single zone systems,
    the fan power associated with the hvac system is added to the zone fan power. For systems defined at the
    terminal, such as FPFCU, it sums up the fan power specified at the terminal and assigns it to the zone.

    Parameters
    ----------
    rmd: dict
    A dictionary representing a RuleModelInstance object as defined by the ASHRAE229 schema


    Returns ----------
    get_zone_supply_return_exhaust_relief_terminal_fan_power_dict: dict
    a dictionary that saves
    each zone's supply, return, exhaust, relief and terminal fan power as a list {zone.id: [supply fan power kW,
    return fan power kW, exhaust fan power kW, relief fan power kW, terminal fan power]}. Values will be equal to
    zero where not defined for a fan system. Zonal exhaust and non-mechanical cooling is not included.
    """
    zone_supply_return_exhaust_relief_terminal_fan_power_dict = {}
    dict_of_zones_and_terminal_units_served_by_hvac_sys = (
        get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd)
    )
    for zone in find_all("$.buildings[*].building_segments[*].zones[*]", rmd):
        # Initialize parameters in a zone
        zone_total_supply_fan_power = ZERO.POWER
        zone_total_return_fan_power = ZERO.POWER
        zone_total_exhaust_fan_power = (
            get_fan_object_electric_power(zone["zonal_exhaust_fan"])
            if zone.get("zonal_exhaust_fan")
            else ZERO.POWER
        )
        zone_total_relief_fan_power = ZERO.POWER
        zone_total_terminal_fan_power = ZERO.POWER

        hvac_sys_list_serving_zone = get_list_hvac_systems_associated_with_zone(
            rmd, zone["id"]
        )
        for hvac_id in hvac_sys_list_serving_zone:
            hvac = find_exactly_one_hvac_system(rmd, hvac_id)
            hvac_system_zone_ids_list = (
                dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_id][
                    "zone_list"
                ]
            )
            hvac_system_terminal_id_list = (
                dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_id][
                    "terminal_unit_list"
                ]
            )

            # Make sure the HVAC system has more than one zone
            assert_(
                hvac_system_zone_ids_list,
                f"No zone associated with the HVAC {hvac_id}. Check inputs!",
            )
            # Make sure the HVAC system has more than one terminal
            assert_(
                hvac_system_terminal_id_list,
                f"No terminal associated with the HVAC {hvac_id}. Check inputs!",
            )

            # Find terminals in the zone that matches to the HVAC terminal list, and calculate the terminal fan power
            zone_hvac_terminal_intersection_list = list(
                set(hvac_system_terminal_id_list).intersection(
                    set(find_all("$.terminals[*].id", zone))
                )
            )
            # Convert terminal id list to terminal data list
            zone_hvac_intersection_terminals = [
                find_exactly_one_terminal_unit(rmd, zone_terminal_id)
                for zone_terminal_id in zone_hvac_terminal_intersection_list
            ]
            # calculate the total terminal fan power from an intersection list of zone
            zone_hvac_total_terminal_fan_power = sum(
                [
                    get_fan_object_electric_power(terminal["fan"])
                    for terminal in zone_hvac_intersection_terminals
                    if terminal.get("fan")
                ],
                ZERO.POWER,
            )
            zone_total_terminal_fan_power += zone_hvac_total_terminal_fan_power

            # if hvac has fan system, calculate the central fan power portion for the zone
            if hvac.get("fan_system"):
                hvac_system_terminal_list = [
                    find_exactly_one_terminal_unit(rmd, terminal_id)
                    for terminal_id in hvac_system_terminal_id_list
                ]
                hvac_total_terminal_air_flow = sum(
                    [
                        terminal.get("primary_airflow", ZERO.FLOW)
                        for terminal in hvac_system_terminal_list
                    ],
                    ZERO.FLOW,
                )
                # Make sure hvac_total_terminal_air_flow is greater than 0.0 to avoid 0 division error
                assert_(
                    hvac_total_terminal_air_flow > ZERO.FLOW,
                    f"Terminals connected with HVAC {hvac['id']} have 0.0 total air flow. Check inputs!",
                )

                zone_primary_air_flow = sum(
                    [
                        terminal.get("primary_airflow", ZERO.FLOW)
                        for terminal in zone_hvac_intersection_terminals
                    ],
                    ZERO.FLOW,
                )

                # Use ratio to adjust between 1 zone scenario and multi-zone scenario
                zone_to_hvac_air_flow_ratio = (
                    zone_primary_air_flow / hvac_total_terminal_air_flow
                    if len(hvac_system_zone_ids_list) > 1
                    else 1.0
                )

                fan_system_powers = (
                    get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                        hvac["fan_system"]
                    )
                )
                zone_total_supply_fan_power += (
                    fan_system_powers["supply_fans_power"] * zone_to_hvac_air_flow_ratio
                )
                zone_total_return_fan_power += (
                    fan_system_powers["return_fans_power"] * zone_to_hvac_air_flow_ratio
                )
                zone_total_exhaust_fan_power += (
                    fan_system_powers["exhaust_fans_power"]
                    * zone_to_hvac_air_flow_ratio
                )
                zone_total_relief_fan_power += (
                    fan_system_powers["relief_fans_power"] * zone_to_hvac_air_flow_ratio
                )
            else:
                zone_total_supply_fan_power += zone_hvac_total_terminal_fan_power

        zone_supply_return_exhaust_relief_terminal_fan_power_dict[zone["id"]] = {
            "supply_fans_power": zone_total_supply_fan_power,
            "return_fans_power": zone_total_return_fan_power,
            "exhaust_fans_power": zone_total_exhaust_fan_power,
            "relief_fans_power": zone_total_relief_fan_power,
            "terminal_fans_power": zone_total_terminal_fan_power,
        }
    return zone_supply_return_exhaust_relief_terminal_fan_power_dict
