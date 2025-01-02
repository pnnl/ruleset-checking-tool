from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system

COOLING_SYSTEM_TYPE = SchemaEnums.schema_enums["CoolingSystemOptions"]


def is_hvac_sys_cooling_type_dx(rmd_b, hvac_b_id):
    """Returns TRUE if the HVAC system has DX cooling. Returns FALSE if the HVAC system has anything other than DX cooling.

    Parameters
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: the HVAC system has DX cooling
        False: the HVAC system has a cooling system type other than DX
    """
    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmd_b, hvac_b_id)

    return (
        find_one("$.cooling_system.type", hvac_b)
        == COOLING_SYSTEM_TYPE.DIRECT_EXPANSION
    )
