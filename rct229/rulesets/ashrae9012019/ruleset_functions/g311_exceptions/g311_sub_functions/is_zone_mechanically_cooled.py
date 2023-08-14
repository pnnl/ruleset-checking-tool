import pydash
from pydash import flat_map, chain, flow, is_equal

from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_one, find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import find_exactly_one_hvac_system, find_exactly_one_zone

CoolingSystemOptions = schema_enums["CoolingSystemOptions"]
CoolingSourceOptions = schema_enums["CoolingSourceOptions"]


def is_hvac_system_non_cooling(cooling_type: str):
    return cooling_type not in [None, CoolingSystemOptions.NONE]


def is_terminal_non_cooling(terminal):
    return find_one("$.cooling_source", terminal) not in [
        None,
        CoolingSourceOptions.NONE,
    ]


def is_zone_mechanically_cooled(rmi, zone_id):
    """
    Function determines whether a zone is cooled. Checks for transfer air

    Parameters
    ----------
    rmi dict
        A dictionary representing a ruleset model instance as defined by the ASHRAE229 schema
    zone_id str
        zone id

    Returns
    -------
    Boolean True if it is determined to be cooled, False otherwise.
    """
    list_hvac_system_ids = get_list_hvac_systems_associated_with_zone(rmi, zone_id)

    # function to check if hvac cooling system type is not None
    hvac_cooling_sys_func = flow(
        lambda hvac_id: find_exactly_one_hvac_system(rmi, hvac_id),
        lambda hvac: find_one("$.cooling_system.type", hvac),
        is_hvac_system_non_cooling,
    )

    # function to check all terminals to check at least one terminal has a cooling source
    hvac_cooling_terminal_func = flow(
        lambda z_id: find_exactly_one_zone(rmi, z_id),
        lambda z: find_all("$.terminals[*]", z),
        lambda terminal_list: flat_map(terminal_list, is_terminal_non_cooling),
        any,
    )

    has_cooling_system = any(
        flat_map(
            list_hvac_system_ids,
            lambda hvac_system_id: hvac_cooling_sys_func(hvac_system_id),
        )
    ) or hvac_cooling_terminal_func(zone_id)

    if not has_cooling_system:
        zone = find_exactly_one_zone(rmi, zone_id)
        if zone.get("transfer_airflow_rate", ZERO.FLOW) > ZERO.FLOW:
            # in this case, we are checking the source zone
            transfer_source_zone_id = getattr_(
                zone, "Zone", "transfer_airflow_source_zone"
            )
            # get the HVAC system list from the source zone
            list_hvac_system_ids = get_list_hvac_systems_associated_with_zone(
                rmi, transfer_source_zone_id
            )
            has_cooling_system = any(
                flat_map(
                    list_hvac_system_ids,
                    lambda hvac_system_id: hvac_cooling_sys_func(hvac_system_id),
                )
            ) or hvac_cooling_terminal_func(transfer_source_zone_id)

    return has_cooling_system
