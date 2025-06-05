from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import (
    find_exactly_one_hvac_system,
    find_exactly_one_terminal_unit,
)


def are_all_hvac_sys_fan_objs_autosized(rmd: dict, hvac_id: str) -> bool:
    """
    The function returns true if all supply fan objects associated with an hvac system are autosized.

    Parameters
    ----------
    rmd: dict RMD at RuleSetModelDescription level
    hvac_id: str HVAC id string

    Returns: bool True if all supply fan objects associate with an HVAC system are autosized, False otherwise,
    MissingKey Exception if missing critical keys
    -------

    """
    hvac = find_exactly_one_hvac_system(rmd, hvac_id)
    dict_of_zones_and_terminal_units_served_by_hvac_sys = (
        get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd)
    )

    return (
        all(
            [
                getattr_(supply_fan, "supply_fan", "is_airflow_calculated")
                for supply_fan in find_all("$.fan_system.supply_fans[*]", hvac)
            ]
        )
        if find_all("$.fan_system.supply_fans[*]", hvac)
        else all(
            [
                getattr_(
                    find_exactly_one_terminal_unit(rmd, terminal_id),
                    "terminal",
                    "fan",
                    "is_airflow_calculated",
                )
                for terminal_id in dict_of_zones_and_terminal_units_served_by_hvac_sys[
                    hvac_id
                ]["terminal_unit_list"]
            ]
        )
    )
