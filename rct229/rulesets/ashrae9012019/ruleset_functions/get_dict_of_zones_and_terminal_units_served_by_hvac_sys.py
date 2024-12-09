from typing import TypedDict

from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all


class ZonesTerminalUnitsServedByHVACSys(TypedDict):
    terminal_unit_list: list[str]
    zone_list: list[str]


def get_dict_of_zones_and_terminal_units_served_by_hvac_sys(
    rmd: dict,
) -> dict[str, ZonesTerminalUnitsServedByHVACSys]:
    """
    Returns a dictionary of zones and terminal unit IDs associated with each HVAC system in the RMD.

    Parameters
    ----------
    rmd: dict
    A dictionary representing a RuleModelDescription object as defined by the ASHRAE229 schema

    Returns ------- dict: a dictionary of zones and terminal unit IDs associated with each HVAC system in the RMD,
    {hvac_system_1.id: {"zone_list": [zone_1.id, zone_2.id, zone_3.id], "terminal_unit_list": [terminal_1.id,
    terminal_2.id, terminal_3.id]}, hvac_system_2.id: {"zone_list": [zone_4.id, zone_9.id, zone_30.id],
    "terminal_unit_list": [terminal_10.id, terminal_20.id, terminal_30.id]}}
    """
    dict_of_zones_and_terminal_units_served_by_hvac_sys = {}
    for zone in find_all("$.buildings[*].building_segments[*].zones[*]", rmd):
        zone_id = zone["id"]
        for terminal in find_all("$.terminals[*]", zone):
            terminal_id = terminal["id"]
            hvac_sys_id = terminal.get(
                "served_by_heating_ventilating_air_conditioning_system"
            )
            if hvac_sys_id:
                if (
                    hvac_sys_id
                    not in dict_of_zones_and_terminal_units_served_by_hvac_sys
                ):
                    dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_sys_id] = {
                        "terminal_unit_list": [],
                        "zone_list": [],
                    }

                zone_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[
                    hvac_sys_id
                ]["zone_list"]
                if zone_id not in zone_list:
                    zone_list.append(zone_id)

                terminal_unit_list = (
                    dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_sys_id][
                        "terminal_unit_list"
                    ]
                )
                if terminal_id not in terminal_unit_list:
                    terminal_unit_list.append(terminal_id)

    # verification - make sure all hvac ids in the zone.terminals are associated with the hvac systems in the data group
    hvac_id_list = find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
        rmd,
    )
    missing_hvac_id_list = []
    for key in dict_of_zones_and_terminal_units_served_by_hvac_sys:
        if key not in hvac_id_list:
            missing_hvac_id_list.append(key)
    assert_(
        len(missing_hvac_id_list) == 0,
        f"HVAC systems {missing_hvac_id_list} are missing in the HeatingVentilatingAirConditioningSystems data group.",
    )

    return dict_of_zones_and_terminal_units_served_by_hvac_sys
