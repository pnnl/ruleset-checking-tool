from typing import Optional, Type

from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
    HVAC_SYSTEM_TYPE_DICTIONARY,
)
from rct229.utils.assertions import assert_


def baseline_system_type_compare(
    system_type: HVAC_SYS,
    target_system_type: HVAC_SYS,
    exact_match: Optional[bool] = True,
) -> bool:
    """
    Parameters
    ----------
    system_type: String the enum indicating the hvac system type example: SYS_5 or SYS_8c.
    This will usually be the value given by the function get_baseline_system_types
    A None is acceptable and the function will raise RCTException which result in UNDETERMINED outcome.

    target_system_type: String the enum indicating the target system type, will usually be SYS_# (primary baseline
    system types) without a further number or letter modifier.

    exact_match: Bool TRUE or FALSE.  if exact_match is TRUE, then system_type must match exactly the enum given
    by target_system_type.  If false, an approximate match will return true.  This would be used in the case where
    the user wants any hvac system ot type 8, without having to type in 8a, 8b, 8c.  In this case, SYS_8 would be
    passed to the function and the function would return TRUE for any system 8, regardless of it's 8a, 8b, or 8c

    Returns
    -------
    True or False, indicating whether the hvac system type matches the hvac_system_type.
    """

    # A list of the available target system
    available_target_system_list = HVAC_SYSTEM_TYPE_DICTIONARY
    available_system_types = [
        system
        for key in HVAC_SYSTEM_TYPE_DICTIONARY
        for system in HVAC_SYSTEM_TYPE_DICTIONARY[key]
    ]
    available_system_types.extend(available_target_system_list)

    assert_(
        system_type in available_system_types,
        f"{system_type} does not match any baseline HVAC system type",
    )
    assert_(
        target_system_type in available_target_system_list,
        f"{target_system_type} does not match any primary "
        f"baseline HVAC system type",
    )

    return (
        system_type == target_system_type
        if exact_match
        else system_type in HVAC_SYSTEM_TYPE_DICTIONARY[target_system_type]
    )
