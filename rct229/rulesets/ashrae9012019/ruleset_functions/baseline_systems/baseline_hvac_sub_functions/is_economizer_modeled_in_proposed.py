from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_dict,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one

Air_Economizer = schema_enums["AirEconomizerOptions"]


def is_economizer_modeled_in_proposed(rmi_b, rmi_p):
    """
    The function returns true if at least one zone served by the baseline HVAC system sent to the function is served by an hvac system with an economizer in the proposed design. The function returns false otherwise.

    Parameters
    ----------
    rmi_b: dict baseline RMI at RuleSetModelInstance level
    rmi_p: dict proposed RMI at RuleSetModelInstance level

    Returns: bool True if at least one zone served by the baseline HVAC system sent to the function is served by an hvac system with an economizer in the proposed design, False otherwise.
    -------

    """

    hvac_zone_list_w_area_dict = get_hvac_zone_list_w_area_dict(rmi_b["buildings"][0])

    is_economizer_modeled_in_proposed = False
    for hvac_b in find_all(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        rmi_b,
    ):
        hvac_id_b = hvac_b["id"]
        hvac_p = find_exactly_one_hvac_system(rmi_p, hvac_id_b)
        air_economizer_type_p = find_one("$.fan_system.air_economizer.type", hvac_p)
        if (
            air_economizer_type_p is not None
            and air_economizer_type_p != Air_Economizer.FIXED_FRACTION
        ):
            is_economizer_modeled_in_proposed = True
            return is_economizer_modeled_in_proposed

    return is_economizer_modeled_in_proposed
