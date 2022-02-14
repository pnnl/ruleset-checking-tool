from dataclasses import dataclass

from rct229.data_fns.table_3_2_fns import table_3_2_lookup
from rct229.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_dict,
)
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import pint_sum

CAPACITY_THRESHOLD = 3.4 * ureg("Btu/(hr * ft2)")
CRAWLSPACE_HEIGHT_THRESHOLD = 7 * ureg("ft")
ZERO_AREA = 0 * ureg("ft2")
ZERO_POWER = 0 * ureg("Btu/hr")
ZERO_UA = 0 * ureg("ft2 * Btu / (hr * ft2 * R)")


# TODO: Need to include any additional requirements from get_hvac_zone_list_w_area_dict(building)
# TODO: Check for other required fields
# Intended for export and internal use
GET_ZONE_CONDITIONING_CATEGORY_DICT__REQUIRED_FIELDS = {
    "building": {
        "building_segments[*].zones[*]": ["spaces"],
        "building_segments[*].zones[*].spaces[*]": [
            "floor_area",
            "lighting_space_type",
        ],
    }
}


def assert_required_fields(req_fields, obj):
    assert all(
        [
            all([field in element for field in fields])
            for element in find_all(jpath, obj)
            for (jpath, fields) in req_fields
        ]
    )


# TODO: Review for comparison tolerances


@dataclass(frozen=True)
class _ZoneConditioningCategory:
    """Enumeration class for zone conditioning categories"""

    CONDITIONED_MIXED: str = "CONDITIONED MIXED"
    CONDITIONED_NON_RESIDENTIAL: str = "CONDITIONED NON-RESIDENTIAL"
    CONDITIONED_RESIDENTIAL: str = "CONDITIONED RESIDENTIAL"
    SEMI_HEATED: str = "SEMI-HEATED"
    UNCONDITIONED: str = "UNCONDITIONED"
    UNENCLOSED: str = "UNENCLOSED"


# Intended for export and internal use
ZONE_CONDITIONING_CATEGORY = _ZoneConditioningCategory()


def get_zone_conditioning_category_dict(climate_zone, building):
    """Determines the zone conditioning category for every zone in a building

    Parameters
    ----------
    climate_zone : str
        One of the ClimateZone2019ASHRAE901 enumerated values
    building : dict
        A dictionary representing a building as defined by the ASHRAE229 schema
    Returns
    -------
    dict
        A dictionary that maps zones to one of the conditioning categories:
        "CONDITIONED MIXED", "CONDITIONED NON-RESIDENTIAL", "CONDITIONED RESIDENTIAL",
        "SEMI-HEATED", "UNCONDITIONED", "UNENCLOSED"
    """
    assert_required_fields(
        GET_ZONE_CONDITIONING_CATEGORY_DICT__REQUIRED_FIELDS["building"], building
    )

    # Create a mapping from an hvac system's id to the hvac system itself
    hvac_systems_dict = {
        hvac_system["id"]: hvac_system
        for hvac_system in find_all(
            "building_segments[*].heating_ventilation_air_conditioning_systems[*]",
            building,
        )
    }

    # Get a dict that maps from hvac system id to {zones_list, total_area} dict
    hvac_zone_list_w_area_dict = get_hvac_zone_list_w_area_dict(building)

    # Produce a dict that maps each zone hvac system id to its cooling capacity
    hvac_cool_capacity_dict = {
        # Handle missing cooling_system
        hvac_sys_id: (
            (
                hvac_systems_dict[hvac_sys_id]["cooling_system"][
                    "sensible_cool_capacity"
                ]
                if "cooling_system" in hvac_systems_dict[hvac_sys_id]
                else ZERO_POWER
            )
            / hvac_values["total_area"]
        )
        for (hvac_sys_id, hvac_values) in hvac_zone_list_w_area_dict
    }
    # Produce a dict that maps each zone hvac system id to its heating capacity
    hvac_heat_capacity_dict = {
        hvac_sys_id: (
            # Handle missing heating_system and/or preheat_system
            (
                hvac_systems_dict[hvac_sys_id]["heating_system"]["heat_capacity"]
                if "heating_system" in hvac_systems_dict[hvac_sys_id]
                else ZERO_POWER
            )
            + (
                hvac_systems_dict[hvac_sys_id]["preheat_system"]["heat_capacity"]
                if "preheat_system" in hvac_systems_dict[hvac_sys_id]
                else ZERO_POWER
            )
        )
        / hvac_values["total_area"]
        for (hvac_sys_id, hvac_values) in hvac_zone_list_w_area_dict
    }

    # Get heated space criteria
    system_min_heating_output = table_3_2_lookup(climate_zone)[
        "system_min_heating_output"
    ]

    # Produce a dict that maps each zone id to a {"sensible_cooling", "heating"} dict
    # representing zone capacities
    zone_capacity_dict = {"sensible_cooling": ZERO_POWER, "heating": ZERO_POWER}
    for zone in find_all("$..zones[*]", building):
        zone_area = pint_sum([space["floor_area"] for space in zone["spaces"]])
        assert zone_area > ZERO_AREA

        for terminal in zone["terminals"]:
            # Note: there is only one hvac system even though the field name is plural
            # This will change to singular in schema version 0.0.8
            hvac_sys_id = hvac_systems_dict[
                terminal["served_by_heating_ventilation_air_conditioning_systems"]
            ]

            # Add cooling and heating capacites from the terminal
            zone_capacity_dict["sensible_cooling"] += hvac_cool_capacity_dict.get(
                hvac_sys_id, ZERO_POWER
            )
            zone_capacity_dict["heating"] += hvac_heat_capacity_dict.get(
                hvac_sys_id, ZERO_POWER
            ) + (terminal.get("heat_capacity", ZERO_POWER) / zone_area)

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
                zone_directly_conditioned_ua = ZERO_UA
                zone_other_ua = ZERO_UA
                for surface in zone["surfaces"]:
                    # Calculate the UA for the surface
                    surface_ua = pint_sum(
                        [
                            subsurface["u_factor"]
                            * (
                                # Can there be both glazed_area and opaque_area? Guessing not. Then should validate that at a high level.
                                subsurface.get("glazed_area", ZERO_AREA)
                                + subsurface.get("opaque_area", ZERO_AREA)
                            )
                            for subsurface in surface["subsurfaces"]
                        ]
                    )

                    # Add the surface UA to one of the running totals for the zone
                    # according to whether the surface is adjacent to a directly conditioned
                    # zone or not
                    adjacent_zone_id = surface["adjacent_zone"]
                    if (
                        surface["adjacent_to"] == "INTERIOR"
                        and adjacent_zone_id in directly_conditioned_zone_ids
                    ):
                        zone_directly_conditioned_ua += surface_ua  # zone_1_4
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
    for building_segment in building["building_segments"]:
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

        for zone in building_segment["zones"]:
            zone_id = zone["id"]
            if (
                zone_id in directly_conditioned_zone_ids
                or zone_id in indirectly_conditioned_zone_ids
            ):
                # Determine zone_has_residential_spaces and zone_has_nonresidential_spaces flags
                zone_has_residential_spaces = False
                zone_has_nonresidential_spaces = False
                for space in zone["spaces"]:
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
                    ] = ZONE_CONDITIONING_CATEGORY.CONDITIONED_MIXED  # zone_1_1
                elif zone_has_residential_spaces:
                    zone_conditioning_category_dict[
                        zone_id
                    ] = ZONE_CONDITIONING_CATEGORY.CONDITIONED_RESIDENTIAL  # zone_1_4
                elif zone_has_nonresidential_spaces:
                    zone_conditioning_category_dict[
                        zone_id
                    ] = (
                        ZONE_CONDITIONING_CATEGORY.CONDITIONED_NON_RESIDENTIAL
                    )  # zone_1_2, zone_1_3

            # To get here, the zone is neither directly or indirectly conditioned
            # Check for semi-heated
            elif zone_id in semiheated_zone_ids:
                zone_conditioning_category_dict[
                    zone_id
                ] = ZONE_CONDITIONING_CATEGORY.SEMI_HEATED  # zone_1_5
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
                ] = ZONE_CONDITIONING_CATEGORY.UNENCLOSED  # zone_1_6
            # Check for crawlspace
            # TODO: We should test that this zone has a volume and throw if not. This will
            # allow other zones to not have a volume field.
            elif zone["volume"] / pint_sum(
                find_all("spaces[*].floor_area", zone)
            ) < CRAWLSPACE_HEIGHT_THRESHOLD and any(
                [
                    get_opaque_surface_type(surface)
                    in ["HEATED SLAB-ON-GRADE", "UNHEATED SLAB-ON-GRADE"]
                    and surface["adjacent_to"] == "GROUND"
                    for surface in zone["surfaces"]
                ]
            ):
                zone_conditioning_category_dict[
                    zone_id
                ] = ZONE_CONDITIONING_CATEGORY.UNENCLOSED  # zone_1_7
            # Check for attic
            elif any(
                [
                    get_opaque_surface_type(surface) == "CEILING"
                    and surface["adjacent_to"] == "EXTERIOR"
                    for surface in zone["surfaces"]
                ]
            ):
                zone_conditioning_category_dict[
                    zone_id
                ] = ZONE_CONDITIONING_CATEGORY.UNENCLOSED  # zone_1_8
            # Anything else
            else:
                zone_conditioning_category_dict[
                    zone_id
                ] = ZONE_CONDITIONING_CATEGORY.UNCONDITIONED  # zone_1_9

    return zone_conditioning_category_dict
