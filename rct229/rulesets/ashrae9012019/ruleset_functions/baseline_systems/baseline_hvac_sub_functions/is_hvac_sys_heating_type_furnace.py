from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]


def is_hvac_sys_heating_type_furnace(rmd_b, hvac_b_id):
    """Returns TRUE if the HVAC system heating system heating type is furnace. Returns FALSE if the HVAC system
    heating system has anything other than furnace or if it has more than 1 heating system.

        Parameters
        ----------
        rmd_b : json
            RMD at RuleSetModelDescription level
        hvac_b_id : str
            The HVAC system ID.
        Returns
        -------
        bool
            True: the HVAC system heating system has furnace as the heating type
            False: the HVAC system has a heating system type other than furnace
    """
    hvac_b = find_exactly_one_hvac_system(rmd_b, hvac_b_id)

    return find_one("$.heating_system.type", hvac_b) == HEATING_SYSTEM.FURNACE
