from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system

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
        find_one("$.cooling_system.type", hvac_b)
        == COOLING_SYSTEM_TYPE.DIRECT_EXPANSION
    )
