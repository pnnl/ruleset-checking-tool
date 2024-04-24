from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]
COOLING_SYSTEM = SchemaEnums.schema_enums["CoolingSystemOptions"]


def find_exactly_one_hvac_system(rmd: dict, hvac_id: str) -> dict:
    """
    Search for the HVAC data group in a ruleset model instance by matching hvac_id
    Raise exception if no matching HVAC

    Parameters
    ----------
    rmd: dict
    hvac_id: str

    Returns dict
    -------

    """
    return find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        "id",
        hvac_id,
        rmd,
    )


def find_exactly_one_terminal_unit(rmd: dict, terminal_unit_id: str) -> dict:
    """
    Search for the terminal unit data group in a ruleset model instance by matching terminal_unit_id
    Raise exception if no matching terminal unit
    Parameters
    ----------
    rmd: json
    terminal_unit_id: str

    Returns json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].zones[*].terminals[*]",
        "id",
        terminal_unit_id,
        rmd,
    )


def find_exactly_one_zone(rmd: dict, zone_id: str) -> dict:
    """
    Search for the zone data group in a ruleset model instance by matching zone_id
    Raise exception if no matching zone

    Parameters
    ----------
    rmd: json
    zone_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].zones[*]", "id", zone_id, rmd
    )


def find_exactly_one_space(rmd: dict, space_id: str) -> dict:
    """
    Search for the zone data group in a ruleset model instance by matching zone_id
    Raise exception if no matching zone

    Parameters
    ----------
    rmd: json
    space_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].zones[*].spaces[*]",
        "id",
        space_id,
        rmd,
    )


def find_exactly_one_schedule(rmd: dict, schedule_id: str) -> dict:
    """
    Search for the schedule data group in a ruleset model instance by matching schedule_id
    Raise exception if no matching schedule

    Parameters
    ----------
    rmd: json
    schedule_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value("$.schedules[*]", "id", schedule_id, rmd)


def find_exactly_one_child_loop(rmd, child_loop_id):
    """
    Search for a child loop data group (secondary loop) in a ruleset model instance by matching child_loop_id
    Raise exception if no matching zone
    Parameters
    ----------
    rmd: json
    child_loop_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.fluid_loops[*].child_loops[*]",
        "id",
        child_loop_id,
        rmd,
    )


def find_exactly_one_fluid_loop(rmd: dict, loop_id: str) -> dict:
    """
    Search for the loop data group in a ruleset model instance by matching loop_id
    Raise exception if no matching zone
    Parameters
    ----------
    rmd: dict
    loop_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.fluid_loops[*]",
        "id",
        loop_id,
        rmd,
    )


def has_heating_system(rmd: dict, hvac_id: str) -> bool:
    """
    Check whether the specified hvac system has a heating system.

    Parameters
    ----------
    rmd json
        A ruleset model instance for a RMD.

    hvac_id str
        The id of the hvac system to evaluate.

    Returns
    -------
    If heating system exists, it returns true. Otherwise, it returns false.
    """
    heating_system = find_exactly_one_hvac_system(rmd, hvac_id).get("heating_system")

    return (
        heating_system is not None
        and heating_system.get("type") is not None
        and heating_system["type"] != HEATING_SYSTEM.NONE
    )


def has_cooling_system(rmd: dict, hvac_id: str) -> bool:
    """
    Check whether the specified hvac system has a cooling system.

    Parameters
    ----------
    rmd json
        A ruleset model instance for a RMD.

    hvac_id str
        The id of the hvac system to evaluate.

    Returns
    -------
    If cooling system exists, it returns true. Otherwise, it returns false.
    """
    cooling_system = find_exactly_one_hvac_system(rmd, hvac_id).get("cooling_system")

    return (
        cooling_system is not None
        and cooling_system.get("type") is not None
        and cooling_system["type"] != COOLING_SYSTEM.NONE
    )


def has_preheat_system(rmd: dict, hvac_id: str) -> bool:
    """
    Check whether the specified hvac system has a preheat system.

    Parameters
    ----------
    rmd json
        A ruleset model instance for a RMD.

    hvac_id str
        The id of the hvac system to evaluate.

    Returns
    -------
    If preheat system exists, it returns true. Otherwise, it returns false.
    """
    preheat_system = find_exactly_one_hvac_system(rmd, hvac_id).get("preheat_system")

    return (
        preheat_system is not None
        and preheat_system.get("type") is not None
        and preheat_system["type"] != HEATING_SYSTEM.NONE
    )


def has_fan_system(rmd: dict, hvac_id: str) -> bool:
    """
    Check whether the specified hvac system has a fan system.

    Parameters
    ----------
    rmd json
        A ruleset model instance for a RMD.

    hvac_id str
        The id of the hvac system to evaluate.

    Returns
    -------
    If fan system exists, it returns true. Otherwise, it returns false.
    """

    return find_exactly_one_hvac_system(rmd, hvac_id).get("fan_system") is not None
