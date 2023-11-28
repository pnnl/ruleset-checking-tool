from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system

COOLING_SYSTEM_TYPE = SchemaEnums.schema_enums["CoolingSystemOptions"]


def is_hvac_sys_cooling_type_none_or_non_mechanical(rmi_b, hvac_b_id):
    """Returns TRUE if the HVAC system cooling type is None or Null or non_mechanical. Returns FALSE if the HVAC system has anything
    other than None or Null for the cooling type.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: HVAC system cooling type is None or Null
        False: HVAC system has anything other than None or Null for the cooling type
    """
    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)
    # Check if hvac_b has preheat system
    cooling_system_type = find_one("$.cooling_system.type", hvac_b)

    return cooling_system_type in [
        COOLING_SYSTEM_TYPE.NONE,
        COOLING_SYSTEM_TYPE.NON_MECHANICAL,
        None,
    ]
