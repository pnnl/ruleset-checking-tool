from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]


def is_hvac_sys_preheating_type_elec_resistance(rmd_b, hvac_b_id):
    """Returns TRUE if the HVAC system preheating system heating type is ELECTRIC_RESISTANCE. Returns FALSE if the
    HVAC system preheating system has anything other than ELECTRIC_RESISTANCE.

    Parameters
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: HVAC system preheating system has ELECTRIC_RESISTANCE as the heating type
        False: HVAC system has a preheating system type other than ELECTRIC_RESISTANCE
    """
    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmd_b, hvac_b_id)

    return (
        find_one("$.preheat_system.type", hvac_b) == HEATING_SYSTEM.ELECTRIC_RESISTANCE
    )
