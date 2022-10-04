from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value


class HVAC_SYS:
    """Class holding HVAC system type value"""

    SYS_7 = "Sys-7"
    SYS_7A = "Sys-7a"
    SYS_7B = "Sys-7b"
    SYS_7C = "Sys-7c"
    UNMATCHED = "Not_Sys"


def find_exactly_one_hvac_system(rmi, hvac_id):
    """
    Search for the HVAC data group in a ruleset model instance by matching hvac_id
    Raise exception if no matching HVAC

    Parameters
    ----------
    rmi: json
    hvac_id: str

    Returns json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems[*]",
        "id",
        hvac_id,
        rmi,
    )


def find_exactly_one_terminal_unit(rmi, terminal_unit_id):
    """
    Search for the terminal unit data group in a ruleset model instance by matching terminal_unit_id
    Raise exception if no matching terminal unit
    Parameters
    ----------
    rmi: json
    terminal_unit_id: str

    Returns json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].zones[*].terminals[*]",
        "id",
        terminal_unit_id,
        rmi,
    )


def find_exactly_one_zone(rmi, zone_id):
    """
    Search for the zone data group in a ruleset model instance by matching zone_id
    Raise exception if no matching zone

    Parameters
    ----------
    rmi: json
    zone_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].zones[*]", "id", zone_id, rmi
    )


def find_exactly_one_loop(rmi, loop_id):
    """
    Search for the loop data group in a ruleset model instance by matching loop_id
    Raise exception if no matching zone
    Parameters
    ----------
    rmi: json
    loop_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.fluid_loops[*]",
        "id",
        loop_id,
        rmi,
    )
