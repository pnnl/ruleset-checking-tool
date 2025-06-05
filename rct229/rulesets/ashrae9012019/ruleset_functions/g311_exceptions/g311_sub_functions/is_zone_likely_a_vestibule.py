from pydash import filter_, flat_map
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zones_on_same_floor_list import (
    get_zones_on_same_floor_list,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import find_exactly_one_zone

LIGHTING_SPACE_OPTIONS = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
]
SURFACE_ADJACENT_TO_OPTIONS = SchemaEnums.schema_enums["SurfaceAdjacencyOptions"]

SUBSURFACE_CLASSIFICATION_OPTIONS = SchemaEnums.schema_enums[
    "SubsurfaceClassificationOptions"
]


ALLOWABLE_SPACE_LIGHTING_TYPES = [
    LIGHTING_SPACE_OPTIONS.CORRIDOR_FACILITY_FOR_THE_VISUALLY_IMPAIRED,
    LIGHTING_SPACE_OPTIONS.CORRIDOR_HOSPITAL,
    LIGHTING_SPACE_OPTIONS.CORRIDOR_ALL_OTHERS,
    LIGHTING_SPACE_OPTIONS.LOBBY_FACILITY_FOR_THE_VISUALLY_IMPAIRED,
    LIGHTING_SPACE_OPTIONS.LOBBY_HOTEL,
    LIGHTING_SPACE_OPTIONS.LOBBY_MOTION_PICTURE_THEATER,
    LIGHTING_SPACE_OPTIONS.LOBBY_PERFORMING_ARTS_THEATER,
    LIGHTING_SPACE_OPTIONS.LOBBY_ALL_OTHERS,
    LIGHTING_SPACE_OPTIONS.STAIRWELL,
]

VESTIBULE_AREA_THRESHOLD = 50 * ureg("ft^2")
VESTIBULE_AREA_MULTIPLIER_THRESHOLD = 0.2


def is_zone_likely_a_vestibule(rmd: dict, zone_id: str) -> bool:
    """
    following the guidelines in ASHRAE that a vestibule is defined as a sapce with at least one exterior door and with a surface area of no more than the greater of 50ft2 or 2% of the total area of the floor.  There is no 100% check for a vestibule, so a space that meets these requirements and also has only 6 surfaces (floor, ceiling and 4 walls) will return False

    Parameters
    ----------
    rmd: dict
    A dictionary representing a RuleModelInstance object as defined by the ASHRAE229 schema
    zone_id: string
    zone id

    Returns
    -------
    boolean, False means NO, True means MAYBE

    """
    zone = find_exactly_one_zone(rmd, zone_id)

    # The RDS interpretation is:
    # The flag is True when all spaces has either no lighting_space_type data or space.get("lighting_space_type") is in
    # ALLOWABLE_SPACE_LIGHTING_TYPES
    is_likely_a_vestibule = all(
        [
            # this covers both Null and in allowable list
            space.get("lighting_space_type") is None
            or space.get("lighting_space_type") in ALLOWABLE_SPACE_LIGHTING_TYPES
            for space in find_all("$.spaces[*]", zone)
        ]
    )

    if is_likely_a_vestibule:
        exterior_surfaces = filter_(
            find_all("$.surfaces[*]", zone),
            {"adjacent_to": SURFACE_ADJACENT_TO_OPTIONS.EXTERIOR},
        )
        exterior_subsurfaces = flat_map(
            exterior_surfaces, lambda surface: find_all("$.subsurfaces[*]", surface)
        )
        exterior_doors = filter_(
            exterior_subsurfaces,
            {"classification": SUBSURFACE_CLASSIFICATION_OPTIONS.DOOR},
        )
        exterior_door_surface_area = sum(
            [
                door.get("glazed_area", ZERO.AREA) + door.get("opaque_area", ZERO.AREA)
                for door in exterior_doors
            ],
            ZERO.AREA,
        )

        zone_ids_on_same_floor = get_zones_on_same_floor_list(rmd, zone_id)
        spaces_on_same_floor = flat_map(
            zone_ids_on_same_floor,
            lambda zone_id: find_all(
                "$.spaces[*]", find_exactly_one_zone(rmd, zone_id)
            ),
        )

        floor_area = sum(
            [space.get("floor_area", ZERO.AREA) for space in spaces_on_same_floor],
            ZERO.AREA,
        )

        zone_area = sum(find_all("$.spaces[*].floor_area", zone), ZERO.AREA)

        is_likely_a_vestibule = (
            exterior_door_surface_area > ZERO.AREA
            and zone_area
            <= max(
                VESTIBULE_AREA_THRESHOLD,
                VESTIBULE_AREA_MULTIPLIER_THRESHOLD * floor_area,
            )
        )

    return is_likely_a_vestibule
