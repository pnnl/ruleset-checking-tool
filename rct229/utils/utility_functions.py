from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value, find_one

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]
COOLING_SYSTEM = schema_enums["CoolingSystemOptions"]


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


def find_exactly_one_space(rmi, space_id):
    """
    Search for the zone data group in a ruleset model instance by matching zone_id
    Raise exception if no matching zone

    Parameters
    ----------
    rmi: json
    space_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*].zones[*].spaces[*]", "id", space_id, rmi
    )


def find_exactly_one_schedule(rmi, schedule_id):
    """
    Search for the schedule data group in a ruleset model instance by mathcing schedule_id
    Raise exception if no matching schedule

    Parameters
    ----------
    rmi: json
    scheduel_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value("$.schedules[*]", "id", schedule_id, rmi)


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
        and heating_system.get("type") is not None
        and heating_system["type"] != HEATING_SYSTEM.NONE
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
        and cooling_system.get("type") is not None
        and cooling_system["type"] != COOLING_SYSTEM.NONE
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
        and preheat_system.get("type") is not None
        and preheat_system["type"] != HEATING_SYSTEM.NONE
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


def get_max_schedule_multiplier_hourly_value_or_default(rmi, schedule_id, default=None):
    hourly_values = find_one(
        f'$.schedules[*][?(@.id="{schedule_id}")].hourly_values', rmi
    )
    return hourly_values if hourly_values else default
