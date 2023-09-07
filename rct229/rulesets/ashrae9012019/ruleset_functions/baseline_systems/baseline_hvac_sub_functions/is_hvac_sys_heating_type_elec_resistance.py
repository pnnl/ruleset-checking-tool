from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]


def is_hvac_sys_heating_type_elec_resistance(rmi_b, hvac_b_id):
    """Returns TRUE if the HVAC system heating system heating type is ELECTRIC_RESISTANCE. Returns FALSE if the HVAC system heating system has anything other than ELECTRIC_RESISTANCE.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: the HVAC system heating system has ELECTRIC_RESISTANCE as the heating type
        False: the HVAC system has a heating system type other than ELECTRIC_RESISTANCE
    """
    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)

    return (
        find_one("$.heating_system.type", hvac_b) == HEATING_SYSTEM.ELECTRIC_RESISTANCE
    )
