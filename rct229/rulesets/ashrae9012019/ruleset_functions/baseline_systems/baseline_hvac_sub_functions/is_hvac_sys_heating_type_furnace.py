from rct229.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
)
from rct229.utils.jsonpath_utils import find_one

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]


def is_hvac_sys_heating_type_furnace(rmi_b, hvac_b_id):
    """Returns TRUE if the HVAC system heating system heating type is furnace. Returns FALSE if the HVAC system
    heating system has anything other than furnace or if it has more than 1 heating system.

        Parameters
        ----------
        rmi_b : json
            RMD at RuleSetModelInstance level
        hvac_b_id : str
            The HVAC system ID.
        Returns
        -------
        bool
            True: the HVAC system heating system has furnace as the heating type
            False: the HVAC system has a heating system type other than furnace
    """
    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)

    return (
        find_one("$.heating_system.heating_system_type", hvac_b)
        == HEATING_SYSTEM.FURNACE
    )
