import os

from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]
COOLING_SYSTEM = SchemaEnums.schema_enums["CoolingSystemOptions"]

_DISABLE_RMD_INDEX_CACHE = os.getenv("RCT_DISABLE_CACHE") == "1"
_RMD_INDEX_CACHE: dict[int, dict] = {}


def _build_rmd_indexes(rmd: dict) -> dict:
    indexes = {
        "hvac": {},
        "terminal": {},
        "building_segment": {},
        "zone": {},
        "space": {},
        "schedule": {},
        "fluid_loop": {},
        "child_loop": {},
        "pump": {},
        "construction": {},
        "swh_distribution": {},
        "swh_use": {},
        "swh_equipment": {},
    }

    for building in rmd.get("buildings", []):
        for segment in building.get("building_segments", []):
            indexes["building_segment"][segment["id"]] = segment

            for zone in segment.get("zones", []):
                indexes["zone"][zone["id"]] = zone

                for space in zone.get("spaces", []):
                    indexes["space"][space["id"]] = space

                for terminal in zone.get("terminals", []):
                    indexes["terminal"][terminal["id"]] = terminal

            for hvac in segment.get("heating_ventilating_air_conditioning_systems", []):
                indexes["hvac"][hvac["id"]] = hvac

            # service water heating uses may appear here
            for swh_use in segment.get("service_water_heating_uses", []):
                if isinstance(swh_use, dict):
                    indexes["swh_use"][swh_use["id"]] = swh_use

    for schedule in rmd.get("schedules", []):
        indexes["schedule"][schedule["id"]] = schedule

    for loop in rmd.get("fluid_loops", []):
        indexes["fluid_loop"][loop["id"]] = loop
        for child in loop.get("child_loops", []):
            indexes["child_loop"][child["id"]] = child

    for pump in rmd.get("pumps", []):
        indexes["pump"][pump["id"]] = pump

    for construction in rmd.get("constructions", []):
        indexes["construction"][construction["id"]] = construction

    for distribution in rmd.get("service_water_heating_distribution_systems", []):
        indexes["swh_distribution"][distribution["id"]] = distribution

    for swh_use in rmd.get("service_water_heating_uses", []):
        if isinstance(swh_use, dict):
            indexes["swh_use"][swh_use["id"]] = swh_use

    for swh_equipment in rmd.get("service_water_heating_equipment", []):
        indexes["swh_equipment"][swh_equipment["id"]] = swh_equipment

    return indexes


def _get_indexes(rmd: dict) -> dict:
    if _DISABLE_RMD_INDEX_CACHE:
        return _build_rmd_indexes(rmd)

    key = id(rmd)
    if key not in _RMD_INDEX_CACHE:
        _RMD_INDEX_CACHE[key] = _build_rmd_indexes(rmd)
    return _RMD_INDEX_CACHE[key]


def find_exactly_one_hvac_system(rmd: dict, hvac_id: str) -> dict:
    hvac = _get_indexes(rmd)["hvac"].get(hvac_id)
    assert_(hvac is not None, f"HVAC system '{hvac_id}' not found")
    return hvac


def find_exactly_one_terminal(rmd: dict, terminal_id: str) -> dict:
    terminal = _get_indexes(rmd)["terminal"].get(terminal_id)
    assert_(terminal is not None, f"Terminal '{terminal_id}' not found")
    return terminal


def find_exactly_one_building_segment(rmd: dict, bldg_seg_id: str) -> dict:
    segment = _get_indexes(rmd)["building_segment"].get(bldg_seg_id)
    assert_(segment is not None, f"Building segment '{bldg_seg_id}' not found")
    return segment


def find_exactly_one_zone(rmd: dict, zone_id: str) -> dict:
    zone = _get_indexes(rmd)["zone"].get(zone_id)
    assert_(zone is not None, f"Zone '{zone_id}' not found")
    return zone


def find_exactly_one_space(rmd: dict, space_id: str) -> dict:
    space = _get_indexes(rmd)["space"].get(space_id)
    assert_(space is not None, f"Space '{space_id}' not found")
    return space


def find_exactly_one_schedule(rmd: dict, schedule_id: str) -> dict:
    schedule = _get_indexes(rmd)["schedule"].get(schedule_id)
    assert_(schedule is not None, f"Schedule '{schedule_id}' not found")
    return schedule


def find_exactly_one_child_loop(rmd: dict, child_loop_id: str) -> dict:
    child = _get_indexes(rmd)["child_loop"].get(child_loop_id)
    assert_(child is not None, f"Child loop '{child_loop_id}' not found")
    return child


def find_exactly_one_fluid_loop(rmd: dict, loop_id: str) -> dict:
    loop = _get_indexes(rmd)["fluid_loop"].get(loop_id)
    assert_(loop is not None, f"Fluid loop '{loop_id}' not found")
    return loop


def find_exactly_one_service_water_heating_distribution_system(
    rmd: dict, swh_distribution_system_id: str
) -> dict:
    dist = _get_indexes(rmd)["swh_distribution"].get(swh_distribution_system_id)
    assert_(
        dist is not None,
        f"Service water heating distribution system "
        f"'{swh_distribution_system_id}' not found",
    )
    return dist


def find_exactly_one_construction(rmd: dict, construction_id: str) -> dict:
    construction = _get_indexes(rmd)["construction"].get(construction_id)
    assert_(
        construction is not None,
        f"Construction '{construction_id}' not found",
    )
    return construction


def find_exactly_one_service_water_heating_use(rmd: dict, swh_use_id: str) -> dict:
    swh_use = _get_indexes(rmd)["swh_use"].get(swh_use_id)
    assert_(
        swh_use is not None,
        f"Service water heating use '{swh_use_id}' not found",
    )
    return swh_use


def find_exactly_one_service_water_heating_equipment(
    rmd: dict, swh_equipment_id: str
) -> dict:
    equipment = _get_indexes(rmd)["swh_equipment"].get(swh_equipment_id)
    assert_(
        equipment is not None,
        f"Service water heating equipment '{swh_equipment_id}' not found",
    )
    return equipment


def find_exactly_one_pump(rmd: dict, pump_id: str) -> dict:
    pump = _get_indexes(rmd)["pump"].get(pump_id)
    assert_(pump is not None, f"Pump '{pump_id}' not found")
    return pump


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
    system = find_exactly_one_hvac_system(rmd, hvac_id).get("heating_system")
    return system is not None and system.get("type") not in (None, HEATING_SYSTEM.NONE)


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
    system = find_exactly_one_hvac_system(rmd, hvac_id).get("cooling_system")
    return system is not None and system.get("type") not in (None, COOLING_SYSTEM.NONE)


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
    system = find_exactly_one_hvac_system(rmd, hvac_id).get("preheat_system")
    return system is not None and system.get("type") not in (None, HEATING_SYSTEM.NONE)


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
    system = find_exactly_one_hvac_system(rmd, hvac_id).get("fan_system")
    return system is not None
