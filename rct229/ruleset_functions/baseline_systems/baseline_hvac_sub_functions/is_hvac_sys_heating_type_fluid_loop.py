from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_there_only_one_hvac_sys_heating_system import \
    is_there_only_one_hvac_sys_heating_system
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]


def is_hvac_sys_heating_type_fluid_loop(rmi_b, hvac_b_id):
    """Returns TRUE if the HVAC system heating system heating type is fluid loop. Returns FALSE if the HVAC system
    heating system has anything other than fluid loop or if it has more than 1 heating system.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: HVAC system heating system has fluid loop as the heating type AND only one heating system is associated with the HVAC system
        False: HVAC system has a heating system type other than fluid loop or if it has more than one heating system.
    """
    is_hvac_sys_heating_type_fluid_loop_flag = False

    if is_there_only_one_hvac_sys_heating_system(rmi_b, hvac_b_id):
        hvac_b = find_exactly_one_with_field_value(
            "$.buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems",
            "id",
            hvac_b_id,
            rmi_b,
        )
        heating_system = hvac_b.get("heating_system")
        if heating_system:
            if heating_system.get("hot_water_loop") is not None and getattr_(heating_system, "heating_system",
                                                                             "heating_system_type") == HEATING_SYSTEM.FLUID_LOOP:
                is_hvac_sys_heating_type_fluid_loop_flag = True

    return is_hvac_sys_heating_type_fluid_loop_flag

