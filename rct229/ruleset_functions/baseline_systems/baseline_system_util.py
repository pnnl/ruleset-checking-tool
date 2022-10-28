from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value


class HVAC_SYS:
    """Class holding HVAC system type value"""

    SYS_1 = "Sys-1"
    SYS_1A = "Sys-1a"
    SYS_1B = "Sys-1b"
    SYS_1C = "Sys-1c"
    SYS_2 = "Sys-2"
    SYS_3 = "Sys-3"
    SYS_3A = "Sys-3a"
    SYS_3B = "Sys-3b"
    SYS_3C = "Sys-3c"
    SYS_4 = "Sys-4"
    SYS_5 = "Sys-5"
    SYS_5B = "Sys-5b"
    SYS_6 = "Sys-6"
    SYS_6B = "Sys-6b"
    SYS_7 = "Sys-7"
    SYS_7A = "Sys-7a"
    SYS_7B = "Sys-7b"
    SYS_7C = "Sys-7c"
    SYS_8 = "Sys_8"
    SYS_8A = "Sys_8a"
    SYS_8B = "Sys-8b"
    SYS_8C = "Sys-8c"
    SYS_9 = "Sys-9"
    SYS_9B = "Sys-9b"
    SYS_10 = "Sys-10"
    SYS_11_1 = "Sys-11.1"
    SYS_11_1A = "Sys-11.1a"
    SYS_11_1B = "Sys-11.1b"
    SYS_11_1C = "Sys-11.1c"
    SYS_11_2 = "Sys-11.2"
    SYS_11_2A = "Sys-11.2a"
    SYS_12 = "Sys-12"
    SYS_12A = "Sys-12a"
    SYS_12B = "Sys-12b"
    SYS_12C = "Sys-12c"
    SYS_13 = "Sys-13"
    SYS_13A = "Sys-13A"
    SYS_13B = "Sys-13B"
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


def find_exactly_one_fluid_loop(rmi, loop_id):
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
