from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
)
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value, find_one

COOLING_SYSTEM_TYPE = schema_enums["CoolingSystemOptions"]


def is_hvac_sys_cooling_type_dx(rmi_b, hvac_b_id):
    """Returns TRUE if the HVAC system has DX cooling. Returns FALSE if the HVAC system has anything other than DX cooling.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: the HVAC system has DX cooling
        False: the HVAC system has a cooling system type other than DX
    """
    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)

    return (
        find_one("$.cooling_system.cooling_system_type", hvac_b)
        == COOLING_SYSTEM_TYPE.DIRECT_EXPANSION
    )
