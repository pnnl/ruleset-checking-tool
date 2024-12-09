from pydash import flat_map
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.is_zone_mechanically_cooled import (
    is_zone_mechanically_cooled,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.utility_functions import (
    find_exactly_one_hvac_system,
    find_exactly_one_zone,
)

HeatingSystemOptions = SchemaEnums.schema_enums["HeatingSystemOptions"]
HeatingSourceOptions = SchemaEnums.schema_enums["HeatingSourceOptions"]


def is_zone_mechanically_heated_and_not_cooled(rmd: dict, zone_id: str) -> bool:
    """
    Determines whether a zone is mechanically heated, but not cooled. Checks for transfer air

    Parameters
    ----------
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema
    zone_id str
        zone id

    Returns
    -------
    Boolean True if it is determined to be heated, but not cooled, False otherwise.
    """
    list_hvac_system_ids = get_list_hvac_systems_associated_with_zone(rmd, zone_id)

    def does_hvac_has_heating_sys(hvac_system_id: str) -> bool:
        hvac = find_exactly_one_hvac_system(rmd, hvac_system_id)
        heating_type = find_one("$.heating_system.type", hvac)
        return heating_type not in [None, HeatingSourceOptions.NONE]

    def does_zone_terminals_have_heating_type(thermal_zone_id: str) -> bool:
        thermal_zone = find_exactly_one_zone(rmd, thermal_zone_id)
        terminal_list = find_all("$.terminals[*]", thermal_zone)
        return any(
            [
                find_one("$.heating_source", terminal)
                not in [None, HeatingSourceOptions.NONE]
                for terminal in terminal_list
            ]
        )

    is_heated = any(
        flat_map(
            list_hvac_system_ids,
            lambda hvac_system_id: does_hvac_has_heating_sys(hvac_system_id),
        )
    ) or does_zone_terminals_have_heating_type(zone_id)

    # Check if a zone is mechanically cooled
    is_cooled = is_zone_mechanically_cooled(rmd, zone_id)

    return is_heated and not is_cooled
