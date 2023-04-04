from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
    find_exactly_one_terminal_unit,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all


def are_all_hvac_sys_fan_objs_autosized(rmi, hvac_id):
    """
    The function returns true if all supply fan objects associated with an hvac system are autosized.

    Parameters
    ----------
    rmi: dict RMI at RuleSetModelInstance level
    hvac_id: str HVAC id string

    Returns: bool True if all supply fan objects associate with an HVAC system are autosized, False otherwise,
    MissingKey Exception if missing critcal keys
    -------

    """
    hvac = find_exactly_one_hvac_system(rmi, hvac_id)
    dict_of_zones_and_terminal_units_served_by_hvac_sys = (
        get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmi)
    )

    return (
        all(
            [
                getattr_(supply_fan, "supply_fan", "is_airflow_autosized")
                for supply_fan in find_all("$.supply_fans[*]", hvac["fan_system"])
            ]
        )
        if hvac.get("fan_system")
        else all(
            [
                getattr_(
                    find_exactly_one_terminal_unit(rmi, terminal_id),
                    "terminal",
                    "fan",
                    "is_airflow_autosized",
                )
                for terminal_id in dict_of_zones_and_terminal_units_served_by_hvac_sys[
                    hvac_id
                ]["terminal_unit_list"]
            ]
        )
    )
