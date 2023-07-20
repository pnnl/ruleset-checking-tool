from pydash import flow, flat_map

from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
    find_exactly_one_zone,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.is_zone_mechanically_cooled import (
    is_zone_mechanically_cooled,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.utils.jsonpath_utils import find_one, find_all

HeatingSystemOptions = schema_enums["HeatingSystemOptions"]
HeatingSourceOptions = schema_enums["HeatingSourceOptions"]


def is_hvac_system_non_heating(heating_type: str):
    return heating_type not in [None, HeatingSourceOptions.NONE]


def is_terminal_non_heating(terminal):
    return find_one("$.heating_source", terminal) not in [
        None,
        HeatingSourceOptions.NONE,
    ]


def is_zone_mechanically_heated_and_not_cooled(rmi, zone_id):
    """
    Determines whether a zone is mechanically heated, but not cooled. Checks for transfer air

    Parameters
    ----------
    rmi dict
        A dictionary representing a ruleset model instance as defined by the ASHRAE229 schema
    zone_id str
        zone id

    Returns
    -------
    Boolean True if it is determined to be heated, but not cooled, False otherwise.
    """
    list_hvac_system_ids = get_list_hvac_systems_associated_with_zone(rmi, zone_id)

    # function to check if hvac cooling system type is not None
    hvac_heating_sys_func = flow(
        lambda hvac_id: find_exactly_one_hvac_system(rmi, hvac_id),
        lambda hvac: find_one("$.heating_system.type", hvac),
        is_hvac_system_non_heating,
    )

    # function to check all terminals to check at least one terminal has a cooling source
    hvac_heating_terminal_func = flow(
        lambda z_id: find_exactly_one_zone(rmi, z_id),
        lambda z: find_all("$.terminals[*]", z),
        lambda terminal_list: flat_map(terminal_list, is_terminal_non_heating),
        any,
    )

    is_heated = any(
        flat_map(
            list_hvac_system_ids,
            lambda hvac_system_id: hvac_heating_sys_func(hvac_system_id),
        )
    ) or hvac_heating_terminal_func(zone_id)

    # Check if a zone is mechanically cooled
    is_cooled = is_zone_mechanically_cooled(rmi, zone_id)

    return is_heated and not is_cooled
