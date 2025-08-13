from typing import List, Dict

from rct229.rulesets.ashrae9012019.data_fns.table_3_2_fns import table_3_2_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import assert_, get_first_attr_, getattr_, RCTException
from rct229.utils.jsonpath_utils import find_all, find_exactly_required_fields, find_one
from rct229.utils.pint_utils import ZERO

CAPACITY_THRESHOLD = 3.4 * ureg("Btu/(hr * ft2)")
CRAWLSPACE_HEIGHT_THRESHOLD = 7 * ureg("ft")


# Intended for export and internal use
class ZoneConditioningCategory:
    """Enumeration class for zone conditioning categories"""

    CONDITIONED_MIXED: str = "CONDITIONED MIXED"
    CONDITIONED_NON_RESIDENTIAL: str = "CONDITIONED NON-RESIDENTIAL"
    CONDITIONED_RESIDENTIAL: str = "CONDITIONED RESIDENTIAL"
    SEMI_HEATED: str = "SEMI-HEATED"
    UNCONDITIONED: str = "UNCONDITIONED"
    UNENCLOSED: str = "UNENCLOSED"


# Intended for internal use
GET_ZONE_CONDITIONING_CATEGORY_DICT__REQUIRED_FIELDS = {
    "building": {
        "building_segments[*].heating_ventilating_air_conditioning_systems[*].cooling_system": [
            "design_sensible_cool_capacity"
        ],
        "building_segments[*].heating_ventilating_air_conditioning_systems[*].heating_system": [
            "design_capacity"
        ],
        "building_segments[*].heating_ventilating_air_conditioning_systems[*].preheat_system": [
            "design_capacity"
        ],
        "building_segments[*].zones[*].spaces[*]": [
            "floor_area",
        ],
        "building_segments[*].zones[*].surfaces[*].subsurfaces[*]": [
            "u_factor",
        ],
    }
}


def get_zone_conditioning_category_rmd_dict(
    climate_zone: str, rmd: dict
) -> dict[str, ZoneConditioningCategory]:
    """
    Determines the zone conditioning category for every zone in an RMD.

    Parameters
    ----------
    climate_zone: str
        One of the ClimateZoneOptions2019ASHRAE901 enumerated values
    rmd: dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema
    Returns
    -------
    dict
        A dictionary that maps zones to one of the conditioning categories:
        CONDITIONED_MIXED, CONDITIONED_NON_RESIDENTIAL, CONDITIONED_RESIDENTIAL,
        SEMI_HEATED, UNCONDITIONED, UNENCOLOSED
    """
    zone_conditioning_category_rmd_dict = {}
    constructions = rmd.get("constructions", [])
    for building in find_all("$.buildings[*]", rmd):
        zone_conditioning_category_dict = get_zone_conditioning_category_dict(
            climate_zone, building, constructions
        )
        zone_conditioning_category_rmd_dict.update(zone_conditioning_category_dict)
    return zone_conditioning_category_rmd_dict


def get_zone_conditioning_category_dict(
    climate_zone: str, building: dict, constructions: list
) -> dict[str, ZoneConditioningCategory]:
    """Determines the zone conditioning category for every zone in a building

    Parameters
    ----------
    climate_zone : str
        One of the ClimateZoneOptions2019ASHRAE901 enumerated values
    building : dict
        A dictionary representing a building as defined by the ASHRAE229 schema
    constructions : list
        A list of construction dictionaries as defined by the ASHRAE229 schema
    Returns
    -------
    dict
        A dictionary that maps zones to one of the conditioning categories:
        CONDITIONED_MIXED, CONDITIONED_NON_RESIDENTIAL, CONDITIONED_RESIDENTIAL,
        SEMI_HEATED, UNCONDITIONED, UNENCOLOSED
    """
    if constructions is None:
        constructions = []

    find_exactly_required_fields(
        GET_ZONE_CONDITIONING_CATEGORY_DICT__REQUIRED_FIELDS["building"], building
    )

    # This will be the return value
    zone_conditioning_category_dict = {}

    # Create a mapping from an hvac system's id to the hvac system itself
    hvac_systems_dict = {
        hvac_system["id"]: hvac_system
        for hvac_system in find_all(
            "building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            building,
        )
    }

    # Get a dict that maps from hvac system id to {zones_list, total_area} dict
    hvac_zone_list_w_area_dict = get_hvac_zone_list_w_area_dict(building)

    # Produce a dict that maps each hvac system id to its cooling capacity
    hvac_cool_capacity_dict = {
        hvac_sys_id: (
            (
                hvac_systems_dict[hvac_sys_id]["cooling_system"][
                    "design_sensible_cool_capacity"
                ]
                if assert_(
                    hvac_systems_dict.get(hvac_sys_id),
                    f"HVAC system {hvac_sys_id} is missing in the HeatingVentilatingAiConditioningSystems data group.",
                )
                and find_one(
                    "$.cooling_system.design_sensible_cool_capacity",
                    hvac_systems_dict[hvac_sys_id],
                )
                # Handle nonexistent cooling_system
                else ZERO.POWER
            )
            / hvac_values["total_area"]
        )
        for (hvac_sys_id, hvac_values) in hvac_zone_list_w_area_dict.items()
    }

    # Produce a dict that maps each hvac system id to its heating capacity
    hvac_heat_capacity_dict = {
        hvac_sys_id: (
            (
                hvac_systems_dict[hvac_sys_id]["heating_system"]["design_capacity"]
                if assert_(
                    hvac_systems_dict.get(hvac_sys_id),
                    f"HVAC system {hvac_sys_id} is missing in the HeatingVentilatingAiConditioningSystems data group.",
                )
                and find_one(
                    "$.heating_system.design_capacity", hvac_systems_dict[hvac_sys_id]
                )
                # Handle missing heating_system
                else ZERO.POWER
            )
            + (
                hvac_systems_dict[hvac_sys_id]["preheat_system"]["design_capacity"]
                if assert_(
                    hvac_systems_dict.get(hvac_sys_id),
                    f"HVAC system {hvac_sys_id} is missing in the HeatingVentilatingAiConditioningSystems data group.",
                )
                and find_one(
                    "$.preheat_system.design_capacity", hvac_systems_dict[hvac_sys_id]
                )
                # Handle missing preheat_system
                else ZERO.POWER
            )
        )
        / hvac_values["total_area"]
        for (hvac_sys_id, hvac_values) in hvac_zone_list_w_area_dict.items()
    }

    # Get heated space criterion
    system_min_heating_output = table_3_2_lookup(climate_zone)[
        "system_min_heating_output"
    ]

    # Produce a dict that maps each zone id to a {"sensible_cooling", "heating"} dict
    # representing zone capacities
    zone_capacity_dict = {}
    for zone in find_all("$..zones[*]", building):
        zone_id = zone["id"]
        zone_area = sum(find_all("$..floor_area", zone), ZERO.AREA)
        assert_(zone_area > ZERO.AREA, f"zone:{zone_id} has no floor area")

        zone_capacity_dict[zone_id] = zone_capacity = {
            "sensible_cooling": ZERO.THERMAL_CAPACITY,
            "heating": ZERO.THERMAL_CAPACITY,
        }
        # Note: Allow for there being no terminals field
        for terminal in find_all("terminals[*]", zone):
            # Note: there is only one hvac system even though the field name is plural
            # This will change to singular in schema version 0.0.8
            hvac_sys_id = terminal.get(
                "served_by_heating_ventilating_air_conditioning_system"
            )

            # Add cooling and heating capacites for the terminal
            zone_capacity["sensible_cooling"] += hvac_cool_capacity_dict.get(
                hvac_sys_id, ZERO.THERMAL_CAPACITY
            )
            # Terminal heating_capacity will include baseboard capacity when hvac_sys_id is None
            zone_capacity["heating"] += hvac_heat_capacity_dict.get(
                hvac_sys_id, ZERO.THERMAL_CAPACITY
            ) + (terminal.get("heating_capacity", ZERO.POWER) / zone_area)

    # Determine eligibility for directly conditioned (heated or cooled) and
    # semi-heated zones
    directly_conditioned_zone_ids = []
    semiheated_zone_ids = []
    for zone in find_all("$..zones[*]", building):
        zone_id = zone["id"]

        if (zone_capacity_dict[zone_id]["sensible_cooling"] > CAPACITY_THRESHOLD) or (
            zone_capacity_dict[zone_id]["heating"] >= system_min_heating_output
        ):
            directly_conditioned_zone_ids.append(zone_id)
        elif zone_capacity_dict[zone_id]["heating"] >= CAPACITY_THRESHOLD:
            semiheated_zone_ids.append(zone_id)

    # Determine eligibility for indirectly conditioned zones
    indirectly_conditioned_zone_ids = []
    for zone in find_all("$..zones[*]", building):
        zone_id = zone["id"]

        if zone_id not in directly_conditioned_zone_ids:
            # Check for any ATRIUM type spaces
            # Note: any([]) is False
            if any(
                [
                    lighting_space_type in ["ATRIUM_LOW_MEDIUM", "ATRIUM_HIGH"]
                    for lighting_space_type in find_all(
                        "spaces[*].lighting_space_type", zone
                    )
                ]
            ):
                indirectly_conditioned_zone_ids.append(zone_id)  # zone_1_3
            # No ATRIUM spaces
            else:
                zone_directly_conditioned_ua = ZERO.UA
                zone_other_ua = ZERO.UA
                assert_(
                    find_all("surfaces[*]", zone), f"zone:{zone_id} has no surfaces"
                )
                for surface in zone["surfaces"]:
                    subsurfaces = find_all("$.subsurfaces[*]", surface)
                    # Calculate the total area of all subsurfaces
                    subsurfaces_area = sum(
                        [
                            subsurface.get("glazed_area", ZERO.AREA)
                            + subsurface.get("opaque_area", ZERO.AREA)
                            for subsurface in subsurfaces
                        ],
                        ZERO.AREA,  # value used if there are no subsurfaces
                    )
                    # Calculate the total UA for all subsurfaces
                    subsurfaces_ua = sum(
                        [
                            subsurface["u_factor"]
                            * (
                                # Can there be both glazed_area and opaque_area? Guessing not. Then should validate that at a high level.
                                subsurface.get("glazed_area", ZERO.AREA)
                                + subsurface.get("opaque_area", ZERO.AREA)
                            )
                            for subsurface in subsurfaces
                        ],
                        ZERO.UA,  # value used if there are no subsurfaces
                    )
                    # Calculate the area of the surface that is not part of a subsurface
                    non_subsurfaces_area = (
                        getattr_(surface, "surface", "area") - subsurfaces_area
                    )
                    surface_construction = find_construction_by_surface(
                        surface, constructions
                    )
                    # Calculate the UA for the surface
                    try:
                        surface_ua = (
                            get_first_attr_(
                                surface_construction,
                                "construction",
                                ["u_factor", "f_factor", "c_factor"],
                            )
                            * non_subsurfaces_area
                            + subsurfaces_ua
                        )
                    except Exception as e:
                        surface_ua = ZERO.UA

                    # Add the surface UA to one of the running totals for the zone
                    # according to whether the surface is adjacent to a directly conditioned
                    # zone or not
                    if getattr_(surface, "surface", "adjacent_to") == "INTERIOR":
                        if (
                            len(find_all("$.spaces[*]", zone)) <= 1
                            and getattr_(surface, "surface", "adjacent_zone")
                            in directly_conditioned_zone_ids
                        ):
                            # 1. check zone has only one space, if yes, use getattr_, if more than 1, can skip the ua calculation.
                            zone_directly_conditioned_ua += surface_ua  # zone_1_4
                        elif (
                            surface.get("adjacent_zone")
                            in directly_conditioned_zone_ids
                        ):
                            zone_directly_conditioned_ua += surface_ua  # zone_1_4
                        else:
                            zone_other_ua += surface_ua
                    else:
                        zone_other_ua += surface_ua  # zone_1_4

                # The zone is indirectly conditioned if it is thermally more strongly
                # connected to directly conditioned zones than to the exterior and other
                # types of zones
                if zone_directly_conditioned_ua > zone_other_ua:
                    indirectly_conditioned_zone_ids.append(zone_id)  # zone_1_4

    # Taking stock:
    # To this point, we have determined which zones are directly conditioned,
    # semi-heated, or indirectly conditioned.
    # Next we determine whether the zone is residential, non-residential, or mixed.
    for building_segment in find_all("building_segments[*]", building):
        # Set building_segment_is_residential and building_segment_is_nonresidential flags
        building_segment_is_residential = False
        building_segment_is_nonresidential = False

        building_segment_lighting_building_area_type = building_segment.get(
            "lighting_building_area_type"
        )
        if building_segment_lighting_building_area_type in [
            "DORMITORY",
            "HOTEL_MOTEL",
            "MULTIFAMILY",
        ]:
            building_segment_is_residential = True  # bldg_seg_1
        elif building_segment_lighting_building_area_type is not None:
            building_segment_is_nonresidential = True  # bldg_seg_2

        for zone in find_all("zones[*]", building_segment):
            zone_id = zone["id"]
            if (
                zone_id in directly_conditioned_zone_ids
                or zone_id in indirectly_conditioned_zone_ids
            ):
                # Determine zone_has_residential_spaces and zone_has_nonresidential_spaces flags
                zone_has_residential_spaces = False
                zone_has_nonresidential_spaces = False
                for space in find_all("spaces[*]", zone):
                    space_lighting_space_type = space.get("lighting_space_type")
                    if space_lighting_space_type in [
                        "DORMITORY_LIVING_QUARTERS",
                        "FIRE_STATION_SLEEPING_QUARTERS",
                        "GUEST_ROOM",
                        "DWELLING_UNIT",
                        "HEALTHCARE_FACILITY_NURSERY",
                        "HEALTHCARE_FACILITY_PATIENT_ROOM",
                    ]:
                        zone_has_residential_spaces = True  # space_1_1_1
                    elif space_lighting_space_type is not None:
                        zone_has_nonresidential_spaces = True  # space_1_1_2
                    elif building_segment_is_residential:
                        zone_has_residential_spaces = True  # space_1_1_3
                    elif building_segment_is_nonresidential:
                        zone_has_nonresidential_spaces = True  # space_2_1_1
                    else:
                        zone_has_nonresidential_spaces = True  # space_3_1_1

                if zone_has_residential_spaces and zone_has_nonresidential_spaces:
                    zone_conditioning_category_dict[
                        zone_id
                    ] = ZoneConditioningCategory.CONDITIONED_MIXED  # zone_1_1
                elif zone_has_residential_spaces:
                    zone_conditioning_category_dict[
                        zone_id
                    ] = ZoneConditioningCategory.CONDITIONED_RESIDENTIAL  # zone_1_4
                else:  # using else is fine b/c `zone_has_residential_spaces` and `zone_has_nonresidential_spaces` can't be False at the same time
                    zone_conditioning_category_dict[
                        zone_id
                    ] = (
                        ZoneConditioningCategory.CONDITIONED_NON_RESIDENTIAL
                    )  # zone_1_2, zone_1_3

            # To get here, the zone is neither directly nor indirectly conditioned
            # Check for semi-heated
            elif zone_id in semiheated_zone_ids:
                zone_conditioning_category_dict[
                    zone_id
                ] = ZoneConditioningCategory.SEMI_HEATED  # zone_1_5
            # Check for interior parking spaces
            elif any(
                [
                    lighting_space_type == "PARKING_AREA_INTERIOR"
                    for lighting_space_type in find_all(
                        "spaces[*].lighting_space_type", zone
                    )
                ]
            ):
                zone_conditioning_category_dict[
                    zone_id
                ] = ZoneConditioningCategory.UNENCLOSED  # zone_1_6
            # Check for crawlspace
            else:
                zone_volume = zone.get("volume", ZERO.VOLUME)
                assert_(
                    zone_volume > ZERO.VOLUME,
                    f"zone:{zone_id} has no volume",
                )
                zone_floor_area = sum(find_all("spaces[*].floor_area", zone), ZERO.AREA)
                assert_(
                    zone_floor_area > ZERO.AREA,
                    f"zone:{zone_id} has no floor area",
                )
                if zone_volume / zone_floor_area < CRAWLSPACE_HEIGHT_THRESHOLD and any(
                    [
                        get_opaque_surface_type(
                            surface,
                            find_construction_by_surface(surface, constructions).get(
                                "has_radiant_heat"
                            ),
                        )
                        in ["HEATED SLAB-ON-GRADE", "UNHEATED SLAB-ON-GRADE"]
                        and surface["adjacent_to"] == "GROUND"
                        for surface in zone["surfaces"]
                    ]
                ):
                    zone_conditioning_category_dict[
                        zone_id
                    ] = ZoneConditioningCategory.UNENCLOSED  # zone_1_7
                # Check for attic
                elif any(
                    [
                        get_opaque_surface_type(surface) == "ROOF"
                        and surface["adjacent_to"] == "EXTERIOR"
                        for surface in zone["surfaces"]
                    ]
                ):
                    zone_conditioning_category_dict[
                        zone_id
                    ] = ZoneConditioningCategory.UNENCLOSED  # zone_1_8
                # Anything else
                else:
                    zone_conditioning_category_dict[
                        zone_id
                    ] = ZoneConditioningCategory.UNCONDITIONED  # zone_1_9

    return zone_conditioning_category_dict


def find_construction_by_surface(surface: dict, constructions: List[Dict]) -> dict:
    surface_construction_id = getattr_(surface, "Surface", "construction")
    surface_construction = next(
        (
            construction
            for construction in constructions
            if construction["id"] == surface_construction_id
        ),
        {},  # empty dict if not found, to allow constructions to be optional
    )
    return surface_construction
