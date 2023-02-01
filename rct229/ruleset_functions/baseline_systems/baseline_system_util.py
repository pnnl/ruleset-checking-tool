from rct229.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]
COOLING_SYSTEM = schema_enums["CoolingSystemOptions"]


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
    SYS_8 = "Sys-8"
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
    SYS_13A = "Sys-13a"
    UNMATCHED = "Not_Sys"


HVAC_SYSTEM_TYPE_DICTIONARY = {
    HVAC_SYS.SYS_1: [HVAC_SYS.SYS_1, HVAC_SYS.SYS_1A, HVAC_SYS.SYS_1B, HVAC_SYS.SYS_1C],
    HVAC_SYS.SYS_2: [HVAC_SYS.SYS_2],
    HVAC_SYS.SYS_3: [HVAC_SYS.SYS_3, HVAC_SYS.SYS_3A, HVAC_SYS.SYS_3B, HVAC_SYS.SYS_3C],
    HVAC_SYS.SYS_4: [HVAC_SYS.SYS_4],
    HVAC_SYS.SYS_5: [HVAC_SYS.SYS_5, HVAC_SYS.SYS_5B],
    HVAC_SYS.SYS_6: [HVAC_SYS.SYS_6, HVAC_SYS.SYS_6B],
    HVAC_SYS.SYS_7: [HVAC_SYS.SYS_7, HVAC_SYS.SYS_7A, HVAC_SYS.SYS_7B, HVAC_SYS.SYS_7C],
    HVAC_SYS.SYS_8: [HVAC_SYS.SYS_8, HVAC_SYS.SYS_8A, HVAC_SYS.SYS_8B, HVAC_SYS.SYS_8C],
    HVAC_SYS.SYS_9: [HVAC_SYS.SYS_9, HVAC_SYS.SYS_9B],
    HVAC_SYS.SYS_10: [HVAC_SYS.SYS_10],
    HVAC_SYS.SYS_11_1: [
        HVAC_SYS.SYS_11_1,
        HVAC_SYS.SYS_11_1A,
        HVAC_SYS.SYS_11_1B,
        HVAC_SYS.SYS_11_1C,
    ],
    HVAC_SYS.SYS_11_2: [
        HVAC_SYS.SYS_11_2,
        HVAC_SYS.SYS_11_2A,
    ],
    HVAC_SYS.SYS_12: [
        HVAC_SYS.SYS_12,
        HVAC_SYS.SYS_12A,
        HVAC_SYS.SYS_12B,
        HVAC_SYS.SYS_12C,
    ],
    HVAC_SYS.SYS_13: [HVAC_SYS.SYS_13, HVAC_SYS.SYS_13A],
}


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
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
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


def find_exactly_one_child_loop(rmi, child_loop_id):
    """
    Search for a child loop data group (secondary loop) in a ruleset model instance by matching child_loop_id
    Raise exception if no matching zone
    Parameters
    ----------
    rmi: json
    child_loop_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.fluid_loops[*].child_loops[*]",
        "id",
        child_loop_id,
        rmi,
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


def has_heating_system(rmi, hvac_id):
    """
    Check whether the specified hvac system has a heating system.

    Parameters
    ----------
    rmi json
        A ruleset model instance for a RMD.

    hvac_id str
        The id of the hvac system to evaluate.

    Returns
    -------
    If heating system exists, it returns true. Otherwise, it returns false.
    """
    heating_system = find_exactly_one_hvac_system(rmi, hvac_id).get("heating_system")

    return (
        heating_system is not None
        and heating_system.get("heating_system_type") is not None
        and heating_system["heating_system_type"] != HEATING_SYSTEM.NONE
    )


def has_cooling_system(rmi, hvac_id):
    """
    Check whether the specified hvac system has a cooling system.

    Parameters
    ----------
    rmi json
        A ruleset model instance for a RMD.

    hvac_id str
        The id of the hvac system to evaluate.

    Returns
    -------
    If cooling system exists, it returns true. Otherwise, it returns false.
    """
    cooling_system = find_exactly_one_hvac_system(rmi, hvac_id).get("cooling_system")

    return (
        cooling_system is not None
        and cooling_system.get("cooling_system_type") is not None
        and cooling_system["cooling_system_type"] != COOLING_SYSTEM.NONE
    )


def has_preheat_system(rmi, hvac_id):
    """
    Check whether the specified hvac system has a preheat system.

    Parameters
    ----------
    rmi json
        A ruleset model instance for a RMD.

    hvac_id str
        The id of the hvac system to evaluate.

    Returns
    -------
    If preheat system exists, it returns true. Otherwise, it returns false.
    """
    preheat_system = find_exactly_one_hvac_system(rmi, hvac_id).get("preheat_system")

    return (
        preheat_system is not None
        and preheat_system.get("heating_system_type") is not None
        and preheat_system["heating_system_type"] != HEATING_SYSTEM.NONE
    )


def has_fan_system(rmi, hvac_id):
    """
    Check whether the specified hvac system has a fan system.

    Parameters
    ----------
    rmi json
        A ruleset model instance for a RMD.

    hvac_id str
        The id of the hvac system to evaluate.

    Returns
    -------
    If fan system exists, it returns true. Otherwise, it returns false.
    """

    return find_exactly_one_hvac_system(rmi, hvac_id).get("fan_system") is not None
