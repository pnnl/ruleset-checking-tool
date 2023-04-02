from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all


def are_all_hvac_sys_fan_objs_autosized(rmi):
    """Returns true or false. The function returns true if all supply fan objects associated with an hvac system are autosized.

    Parameters
    ----------
    rmi: json
         The RMR in which the fan system object is defined.

    Returns
    -------
    bool
        True: all supply fan objects associated with a hvac system are autosized.
        False: not all supply fan objects associated with a hvac system are autosized.

    """
    are_all_hvac_sys_fan_objs_autosized = True

    zones_and_terminal_units_served_by_hvac_sys_dict = (
        get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmi)
    )

    for hvac in find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        rmi,
    ):
        if hvac.get("fan_system") is not None:
            for sup_fan in getattr_(hvac["fan_system"], "supply fans", "supply_fans"):
                if (
                    getattr_(sup_fan, "is airflow autosized", "is_airflow_autosized")
                    == False
                ):
                    are_all_hvac_sys_fan_objs_autosized = False
                    return are_all_hvac_sys_fan_objs_autosized
        else:
            for terminal_id in zones_and_terminal_units_served_by_hvac_sys_dict[
                hvac["id"]
            ]["terminal_unit_list"]:
                terminals = find_all(
                    f'$.buildings[*].building_segments[*].zones[*].terminals[*][?(@.id="{terminal_id}")]',
                    rmi,
                )

                for terminal in terminals:
                    if (
                        getattr_(
                            terminal,
                            "is_airflow_autosized",
                            "fan",
                            "is_airflow_autosized",
                        )
                        == False
                    ):
                        are_all_hvac_sys_fan_objs_autosized = False
                        return are_all_hvac_sys_fan_objs_autosized

    return are_all_hvac_sys_fan_objs_autosized
