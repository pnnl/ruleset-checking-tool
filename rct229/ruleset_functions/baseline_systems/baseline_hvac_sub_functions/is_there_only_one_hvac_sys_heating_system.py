from rct229.utils.jsonpath_utils import (
    find_all,
    find_all_with_field_value,
    find_exactly_one_with_field_value,
)


def is_there_only_one_hvac_sys_heating_system(rmi_b, hvac_b_id):
    """Returns TRUE if the HVAC system has only one heating system associated with it. Returns FALSE if the HVAC
    system has anything other than 1 heating system associated with it.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: the HVAC system has only one heating system associated with it.
        False: the HVAC system has anything other than 1 heating system associated with it.
    """
    is_there_only_one_hvac_sys_heating_system_flag = False

    hvac_b = find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems",
        "id",
        hvac_b_id,
        rmi_b,
    )
    heating_systems = find_all("heating_system[*]", hvac_b)
    if heating_systems and len(heating_systems) == 1:
        is_there_only_one_hvac_sys_heating_system_flag = True

    return is_there_only_one_hvac_sys_heating_system_flag
