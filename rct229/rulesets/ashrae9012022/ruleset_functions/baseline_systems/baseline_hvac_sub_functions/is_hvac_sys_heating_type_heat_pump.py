from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]


def is_hvac_sys_heating_type_heat_pump(rmd_b, hvac_b_id):
    """Returns TRUE if the HVAC system has heat pump as the heating system type. Returns FALSE if the HVAC system has
    anything other than heat pump as the heating system type or if it has more than 1 heating system.

        Parameters
        ----------
        rmd_b : json
            RMD at RuleSetModelDescription level
        hvac_b_id : str
            The HVAC system ID.

        Returns
        -------
        bool
            True: the HVAC system has heat pump as the heating system type
            False: the HVAC system has a heating system type other than heat pump as the heating system type
    """
    hvac_b = find_exactly_one_hvac_system(rmd_b, hvac_b_id)

    return find_one("$.heating_system.type", hvac_b) == HEATING_SYSTEM.HEAT_PUMP
