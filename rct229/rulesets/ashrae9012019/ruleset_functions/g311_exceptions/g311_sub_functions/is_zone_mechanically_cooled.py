from pydash import flat_map
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import (
    find_exactly_one_hvac_system,
    find_exactly_one_zone,
)

CoolingSystemOptions = SchemaEnums.schema_enums["CoolingSystemOptions"]
CoolingSourceOptions = SchemaEnums.schema_enums["CoolingSourceOptions"]


def is_zone_mechanically_cooled(rmd: dict, zone_id: str) -> bool:
    """
    Function determines whether a zone is cooled. Checks for transfer air

    Parameters
    ----------
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema
    zone_id str
        zone id

    Returns
    -------
    Boolean True if it is determined to be cooled, False otherwise.
    """
    list_hvac_system_ids = get_list_hvac_systems_associated_with_zone(rmd, zone_id)

    def does_hvac_has_cooling_sys(hvac_system_id: str) -> bool:
        hvac = find_exactly_one_hvac_system(rmd, hvac_system_id)
        cooling_type = find_one("$.cooling_system.type", hvac)
        return cooling_type not in [None, CoolingSourceOptions.NONE]

    def does_zone_terminals_have_cooling_type(thermal_zone_id: str) -> bool:
        thermal_zone = find_exactly_one_zone(rmd, thermal_zone_id)
        terminal_list = find_all("$.terminals[*]", thermal_zone)
        return any(
            [
                find_one("$.cooling_source", terminal)
                not in [None, CoolingSourceOptions.NONE]
                for terminal in terminal_list
            ]
        )

    has_cooling_system = any(
        flat_map(
            list_hvac_system_ids,
            lambda hvac_system_id: does_hvac_has_cooling_sys(hvac_system_id),
        )
    ) or does_zone_terminals_have_cooling_type(zone_id)

    if not has_cooling_system:
        zone = find_exactly_one_zone(rmd, zone_id)
        if zone.get("transfer_airflow_rate", ZERO.FLOW) > ZERO.FLOW:
            # in this case, we are checking the source zone
            transfer_source_zone_id = getattr_(
                zone, "Zone", "transfer_airflow_source_zone"
            )
            # get the HVAC system list from the source zone
            list_hvac_system_ids = get_list_hvac_systems_associated_with_zone(
                rmd, transfer_source_zone_id
            )
            has_cooling_system = any(
                flat_map(
                    list_hvac_system_ids,
                    lambda hvac_system_id: does_hvac_has_cooling_sys(hvac_system_id),
                )
            ) or does_zone_terminals_have_cooling_type(transfer_source_zone_id)

    return has_cooling_system
