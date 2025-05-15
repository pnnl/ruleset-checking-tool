from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_by_rmd_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system

Air_Economizer = SchemaEnums.schema_enums["AirEconomizerOptions"]


def is_economizer_modeled_in_proposed(rmd_b: dict, rmd_p: dict, hvac_id_b: str) -> bool:
    """
    The function returns true if at least one zone served by the baseline HVAC system sent to the function is served by an hvac system with an economizer in the proposed design. The function returns false otherwise.

    Parameters
    ----------
    rmd_b: dict baseline RMD at RuleSetModelDescription level
    rmd_p: dict proposed RMD at RuleSetModelDescription level
    hvac_id_b: string baseline HVAC id

    Returns: bool True if at least one zone served by the baseline HVAC system sent to the function is served by an hvac system with an economizer in the proposed design, False otherwise.
    -------

    """

    hvac_zone_list_w_area_dict = get_hvac_zone_list_w_area_by_rmd_dict(rmd_b)
    is_economizer_modeled = False
    for zone_id_b in hvac_zone_list_w_area_dict[hvac_id_b]["zone_list"]:
        hvac_list_p = get_list_hvac_systems_associated_with_zone(rmd_p, zone_id_b)
        for hvac_id_p in hvac_list_p:
            hvac_p = find_exactly_one_hvac_system(rmd_p, hvac_id_p)
            air_economizer_type_p = find_one("$.fan_system.air_economizer.type", hvac_p)
            if (
                air_economizer_type_p is not None
                and air_economizer_type_p != Air_Economizer.FIXED_FRACTION
            ):
                is_economizer_modeled = True

    return is_economizer_modeled
