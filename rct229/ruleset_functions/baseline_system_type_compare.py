import inspect

from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.utils.assertions import RCTException


def baseline_system_type_compare(system_type, target_system_type, exact_match=True):
    """

    Parameters
    ----------
    system_type: String the enum indicating the hvac system type example: SYS_5 or SYS_8c.  This will usually be the value given by the function get_baseline_system_types
    target_system_type: String the enum indicating the target system type, will usually be SYS_# without a further number or letter modifier
    exact_match: Bool TRUE or FALSE.  if exact_match is TRUE, then the system type must match exactly the enum given by hvac_system_type.  If false, an approximate match will return true.  This would be used in the case where the user wants any hvac system ot type 8, without having to type in 8a, 8b, 8c.  In this case, SYS_8 would be passed to the function and the function would return TRUE for any system 8, regardless of it's 8a, 8b, or 8c

    Returns
    -------
    True or False, indicating whether the hvac system type matches the hvac_system_type.
    """

    # A list of the attribute values from the HVAC_SYS class
    hvac_sys_list = [
        i[1]
        for i in inspect.getmembers(HVAC_SYS)
        if type(i[0]) is str and i[0].startswith("SYS")
    ]
    if system_type not in hvac_sys_list:
        raise RCTException(
            f"{system_type} does not match to any baseline HVAC system type"
        )
    if target_system_type not in hvac_sys_list:
        raise RCTException(
            f"{target_system_type} does not match to any baseline HVAC system type"
        )

    return (
        system_type == target_system_type
        if exact_match
        else target_system_type in HVAC_SYS.HVAC_SYSTEM_TYPE_DICTIONARY[system_type]
    )
