from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]
COOLING_SYSTEM = SchemaEnums.schema_enums["CoolingSystemOptions"]


def find_exactly_one_hvac_system(rmd: dict, hvac_id: str) -> dict:
    """
    Search for the HVAC data group in a ruleset model description by matching hvac_id
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
    Search for the terminal unit data group in a ruleset model description by matching terminal_unit_id
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


def find_exactly_one_building_segment(rmd: dict, bldg_seg_id: str) -> dict:
    """
    Search for the building segment data group in a ruleset model description by matching bldg_seg_id
    Raise exception if no matching building segment

    Parameters
    ----------
    rmd: json
    bldg_seg_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*]", "id", bldg_seg_id, rmd
    )


def find_exactly_one_zone(rmd: dict, zone_id: str) -> dict:
    """
    Search for the zone data group in a ruleset model description by matching zone_id
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
    Search for the zone data group in a ruleset model description by matching zone_id
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
    Search for the schedule data group in a ruleset model description by matching schedule_id
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
    Search for a child loop data group (secondary loop) in a ruleset model description by matching child_loop_id
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
    Search for the loop data group in a ruleset model description by matching loop_id
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


def find_exactly_one_service_water_heating_distribution_system(
    rmd: dict, swh_distribution_system_id: str
) -> dict:
    """
    Search for the swh distribution system data group in a ruleset model description by matching swh_distribution_system_id:
    Raise exception if no matching distribution system
    Parameters
    ----------
    rmd: dict
    swh_distribution_system_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.service_water_heating_distribution_systems[*]",
        "id",
        swh_distribution_system_id,
        rmd,
    )


def find_exactly_one_construction(rmd: dict, construction_id: str) -> dict:
    """
    Search for the construction data group in a ruleset model description by matching construction_id:
    Raise exception if no matching construction

    Parameters
    ----------
    rmd
    construction_id

    Returns
    -------

    """
    return find_exactly_one_with_field_value(
        # TODO: Moving the `service_water_heating_uses` key to the `building_segments` level is being discussed. If the `service_water_heating_uses` key is moved, this function needs to be revisited.
        "$.constructions[*]",
        "id",
        construction_id,
        rmd,
    )


def find_exactly_one_service_water_heating_use(rmd: dict, swh_use_id: str) -> dict:
    """
    Search for the service water heating use data group in a ruleset model description by matching swh_id:
    Raise exception if no matching distribution system
    Parameters
    ----------
    rmd: dict
    swh_use_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        # TODO: Moving the `service_water_heating_uses` key to the `building_segments` level is being discussed. If the `service_water_heating_uses` key is moved, this function needs to be revisited.
        "$.service_water_heating_uses[*]",
        "id",
        swh_use_id,
        rmd,
    )


def find_exactly_one_service_water_heating_equipment(
    rmd: dict, swh_equipment_id: str
) -> dict:
    """
    Search for the service water heating equipment data group in a ruleset model description by matching swh_equipment_id:
    Raise exception if no matching swh equipment system

    Parameters
    ----------
    rmd: dict
    swh_equipment_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.service_water_heating_equipment[*]",
        "id",
        swh_equipment_id,
        rmd,
    )


def find_exactly_one_pump(rmd: dict, pump_id: str) -> dict:
    """
    Search for the pump data group in a ruleset model description by matching pump_id:
    Raise exception if no matching pump

    Parameters
    ----------
    rmd: dict
    pump_id: str

    Returns: json
    -------

    """
    return find_exactly_one_with_field_value(
        "$.pumps[*]",
        "id",
        pump_id,
        rmd,
    )


def has_heating_system(rmd: dict, hvac_id: str) -> bool:
    """
    Check whether the specified hvac system has a heating system.

    Parameters
    ----------
    rmd json
        A ruleset model description for a RMD.

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
        A ruleset model description for a RMD.

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
        A ruleset model description for a RMD.

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
        A ruleset model description for a RMD.

    hvac_id str
        The id of the hvac system to evaluate.

    Returns
    -------
    If fan system exists, it returns true. Otherwise, it returns false.
    """

    return find_exactly_one_hvac_system(rmd, hvac_id).get("fan_system") is not None
