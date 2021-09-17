from rct229.data_fns.table_3_2_fns import table_3_2_lookup
from rct229.utils.jsonpath_utils import find_all

# TODO: Use pint to deal with units
CAPACITY_THRESHOLD_IP = 3.4  # Btu/(h*ft2)
CAPACITY_THRESHOLD = 3.154907451 * CAPACITY_THRESHOLD_IP  # W/m2
CRAWLSPACE_HEIGHT_THRESHOLD_IP = 7  # ft?
CRAWLSPACE_HEIGHT_THRESHOLD = 0.3048 * CRAWLSPACE_HEIGHT_THRESHOLD_IP  # m


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
    system_min_heating_output = table_3_2_lookup(climate_zone)

    directly_conditioned_zone_ids = []
    semiheated_zone_ids = []
    indirectly_conditioned_zone_ids = []

    # Determine eligibility for directly conditioned (heated or cooled) and
    # semi-heated zones
    for hvac_system in find_all(
        "building_segments[*].heating_ventilation_air_conditioning_systems[*]", building
    ):
        if (
            hvac_system["simulation_result_sensible_cool_capacity"]
            >= CAPACITY_THRESHOLD
            or hvac_system["simulation_result_heat_capacity"]
            >= system_min_heating_ouput
        ):
            directly_conditioned_zone_ids.extend(hvac_system["zones_served"])
        elif hvac_system["simulation_result_heat_capacity"] >= CAPACITY_THRESHOLD:
            semiheated_zone_ids.extend(
                [zone["id"] for zone in hvac_system["zones_served"]]
            )

    # Determine eligibility for indirectly conditioned zones
    for zone in find_all("building_segments[*].thermal_blocks[*].zones[*]", building):
        if zone["id"] not in directly_conditioned_zone_ids:
            lighting_space_types = find_all("spaces[*].lighting_space_type")
            any_space_type_in_zone_is_atrium = any(
                [
                    lighting_space_type in ["ATRIUM_LOW_MEDIUM", "ATRIUM_HIGH"]
                    for lighting_space_type in lighting_space_types
                ]
            )
            if any_space_type_in_zone_is_atrium:
                indirectly_conditioned_zone_ids.append(zone["id"])
            else:
                directly_conditioned_ua = 0
                other_ua = 0
                for surface in zone["surfaces"]:
                    if surface["adjacent_to"] == "INTERIOR":
                        adjacent_zone_id = surface["adjacent_zone_id"]
                        surface_fenestration_ua = sum(
                            [
                                (
                                    fenestration["glazing_area"]
                                    + fenestration["opaque_area"]
                                )
                                * fenestration["u_factor"]
                                for fenestration in surface["fenestration_subsurfaces"]
                            ]
                        )
                        surface_fenestration_area = sum(
                            [
                                (
                                    fenestration["glazing_area"]
                                    + fenestration["opaque_area"]
                                )
                            ]
                        )
                        surface_construction_ua = (
                            surface["area"] - surface_fenestration_area
                        ) * surface["construction"]["u_factor"]
                        surface_ua = surface_fenestration_ua + surface_construction_ua

                        if adjacent_zone_id in directly_conditioned_zone_ids:
                            directly_conditioned_ua += surface_ua
                        else:
                            other_ua += surface_ua
                if directly_conditioned_ua > other_ua:
                    indirectly_conditioned_zone_ids.append(zone["id"])

    for building_segment in building["building_segments"]:
        # Set residential and non-residential flags
        building_segment_residential_flag = False
        building_segment_nonresidential_flag = False
        building_segment_lighting_building_area_type = building_segment.get(
            "lighting_building_area_type"
        )
        if building_segment_lighting_building_area_type in [
            "DORMITORY",
            "HOTEL_MOTEL",
            "MULTIFAMILY",
        ]:
            building_segment_residential_flag = True
        elif building_segment_lighting_building_area_type is not None:
            building_segment_nonresidential_flag = True

        for zone in find_all("thermal_blocks[*].zones[*]", building_segment):
            zone_id = zone["id"]
            if (
                zone_id in directly_conditioned_zone_ids
                or zone_id in indirectly_conditioned_zone_ids
            ):
                # Set has_residential_spaces and has_nonresidential_spaces flags
                has_residential_spaces = False
                has_nonresidential_spaces = False
                for space in zone["spaces"]:
                    # Set space residential and non-residential flags
                    space_lighting_space_type = space.get("lighting_space_type")
                    if space_lighting_space_type in [
                        "DORMITORY_LIVING_QUARTERS",
                        "FIRE_STATION_SLEEPING_QUARTERS",
                        "GUEST_ROOM",
                        "DWELLING_UNIT",
                        "HEALTHCARE_FACILITY_NURSERY",
                        "HEALTHCARE_FACILITY_PATIENT_ROOM",
                    ]:
                        has_residential_spaces = True
                    elif space_lighting_space_type is not None:
                        has_nonresidential_spaces = True
                    elif building_segment_residential_flag:
                        has_residential_spaces = True
                    elif building_segment_nonresidential_flag:
                        has_nonresidential_spaces = True
                    else:
                        has_nonresidential_spaces = True

                if has_residential_spaces and has_nonresidential_spaces:
                    zone_conditioning_category_dict[zone_id] = "CONDITIONED MIXED"
                elif has_residential_spaces:
                    zone_conditioning_category_dict[zone_id] = "CONDITIONED RESIDENTIAL"
                elif has_nonresidential_spaces:
                    zone_conditioning_category_dict[
                        zone_id
                    ] = "CONDITIONED NON-RESIDENTIAL"

            elif zone_id in semiheated_zone_ids:
                zone_conditioning_category_dict[zone_id] = "SEMI-HEATED"
            elif any(
                [
                    lighting_space_type == "PARKING_AREA_INTERIOR"
                    for lighting_space_type in find_all(
                        "spaces[*].lighting_space_type", zone
                    )
                ]
            ):
                zone_conditioning_category_dict[zone_id] = "UNENCLOSED"
            # Check for crawlspace
            # TODO: Do they intend all, or do they want any?
            elif zone["volume"] / sum(find_all("spaces[*].floor_area", zone)) and any(
                [
                    get_opaque_surface_type(surface) == "FLOOR"
                    and surface["adjacent_to"] == "GROUND"
                    for surface in zone["surfaces"]
                ]
            ):
                zone_conditioning_category_dict[zone_id] = "UNENCLOSED"
            # Check for attic
            # TODO: Do they intend all, or do they want any?
            elif any(
                [
                    get_opaque_surface_type(surface) == "CEILING"
                    and surface["adjacent_to"] == "EXTERIOR"
                    for surface in zone["surfaces"]
                ]
            ):
                zone_conditioning_category_dict[zone_id] = "UNENCLOSED"

            else:
                one_conditioning_category_dict[zone_id] = "UNCONDITIONED"
