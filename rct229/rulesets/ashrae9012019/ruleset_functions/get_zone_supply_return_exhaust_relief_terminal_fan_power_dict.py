from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import \
    find_exactly_one_terminal_unit
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import \
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys
from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_object_electric_power import get_fan_object_electric_power
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import \
    get_list_hvac_systems_associated_with_zone
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO


def get_zone_supply_return_exhaust_relief_terminal_fan_power_dict(rmi):
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
    rmi: dict
    A dictionary representing a RuleModelInstance object as defined by the ASHRAE229 schema


    Returns ----------
    get_zone_supply_return_exhaust_relief_terminal_fan_power_dict: dict
    a dictionary that saves
    each zone's supply, return, exhaust, relief and terminal fan power as a list {zone.id: [supply fan power kW,
    return fan power kW, exhaust fan power kW, relief fan power kW, terminal fan power]}. Values will be equal to
    zero where not defined for a fan system. Zonal exhaust and non-mechanical cooling is not included.
    """

    dict_of_zones_and_terminal_units_served_by_hvac_sys = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmi)
    for zone in find_all("$.buildings[*].building_segments[*].zones[*]", rmi):
        zone_total_supply_fan_power = ZERO.POWER
        zone_total_return_fan_power = ZERO.POWER
        zone_total_exhaust_fan_power = ZERO.POWER
        zone_total_relief_fan_power = ZERO.POWER
        zone_total_terminal_fan_power = ZERO.POWER

        if zone.get("zonal_exhaust_fan"):
            zone_total_exhaust_fan_power = get_fan_object_electric_power(zone["zonal_exhaust_fan"])

        hvac_sys_list_serving_zone = get_list_hvac_systems_associated_with_zone(rmi, zone["id"])
        for hvac in hvac_sys_list_serving_zone:
            hvac_total_terminal_air_flow = ZERO.FLOW
            zone_primary_air_flow = ZERO.FLOW
            zone_ids_list_hvac_system = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac["id"]]["zone_list"]
            if hvac.get("fan_system") and zone_ids_list_hvac_system:
                terminal_id_list_hvac_system = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac["id"]]["terminal_unit_list"]
                for terminal_id in terminal_id_list_hvac_system:
                    terminal = find_exactly_one_terminal_unit(rmi, terminal_id)
                    terminal_primary_airflow = terminal.get("primary_airflow", ZERO.FLOW)
                    hvac_total_terminal_air_flow += terminal_primary_airflow
                    terminal_fan_power = get_fan_object_electric_power(terminal["fan"]) if terminal.get("fan") else terminal_fan_power = ZERO.POWER
                    zone_terminal_ids_list = find_all("$.terminals[*].id", zone)
                    if terminal_id in zone_terminal_ids_list:
                        zone_primary_air_flow += terminal_primary_airflow
                        zone_total_terminal_fan_power += terminal_fan_power


