from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType as OST,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    ZoneConditioningDataDict,
    get_surface_conditioning_category_dict,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all, find_exactly_required_fields
from rct229.utils.pint_utils import ZERO

DOOR = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"].DOOR

# Intended for internal use
GET_BUILDING_SCC_WINDOW_WALL_RATIO_DICT__REQUIRED_FIELDS = {
    "building": {
        "$.building_segments[*].zones[*].surfaces[*]": ["area"],
        "$.building_segments[*].zones[*].surfaces[*].subsurfaces[*]": [
            "classification"
        ],
    }
}


def get_building_scc_window_wall_ratios_dict(
    climate_zone: str, constructions: list, building: dict
) -> ZoneConditioningDataDict:
    """Determines the window to wall ratio for each surface conditioning category
    in a building

    Parameters
    ----------
    climate_zone : str
        One of the ClimateZoneOptions2019ASHRAE901 enumerated values
    constructions : list
        A list of construction dictionaries as defined by the ASHRAE229 schema
    building : dict
        A dictionary representing a building as defined by the ASHRAE229 schema

    Returns
    -------
    dict
        A dictionary that maps each surface conditioning category to its average
        window to wall ratio
    """
    find_exactly_required_fields(
        GET_BUILDING_SCC_WINDOW_WALL_RATIO_DICT__REQUIRED_FIELDS["building"], building
    )

    # Get the conditioning category for all the surfaces in the building
    scc_dict = get_surface_conditioning_category_dict(
        climate_zone, building, constructions
    )

    # Initialize total window areas
    total_res_window_area = ZERO.AREA
    total_nonres_window_area = ZERO.AREA
    total_mixed_window_area = ZERO.AREA
    total_semi_exterior_window_area = ZERO.AREA

    # Initialize total wall areas
    total_res_wall_area = ZERO.AREA
    total_nonres_wall_area = ZERO.AREA
    total_mixed_wall_area = ZERO.AREA
    total_semi_exterior_wall_area = ZERO.AREA

    # Loop through all the surfaces in the building
    for surface in find_all("$.building_segments[*].zones[*].surfaces[*]", building):
        # surface conditioning category
        scc = scc_dict[surface["id"]]

        if get_opaque_surface_type(surface) == OST.ABOVE_GRADE_WALL:
            surface_area = surface["area"]
            surface_window_area = ZERO.AREA
            for subsurface in find_all("$.subsurfaces[*]", surface):
                glazed_area = subsurface.get("glazed_area", ZERO.AREA)
                opaque_area = subsurface.get("opaque_area", ZERO.AREA)
                surface_window_area += (
                    glazed_area + opaque_area
                    if subsurface["classification"] != DOOR
                    or (glazed_area > opaque_area)
                    else ZERO.AREA
                )

            if scc == SCC.EXTERIOR_RESIDENTIAL:
                total_res_wall_area += surface_area
                total_res_window_area += surface_window_area
            elif scc == SCC.EXTERIOR_NON_RESIDENTIAL:
                total_nonres_wall_area += surface_area
                total_nonres_window_area += surface_window_area
            elif scc == SCC.EXTERIOR_MIXED:
                total_mixed_wall_area += surface_area
                total_mixed_window_area += surface_window_area
            elif scc == SCC.SEMI_EXTERIOR:
                total_semi_exterior_wall_area += surface_area
                total_semi_exterior_window_area += surface_window_area
            else:
                # Sanity check: the only remaining SCC option is UNREGULATED
                assert scc == SCC.UNREGULATED

    return {
        getattr(SCC, "EXTERIOR_RESIDENTIAL"): total_res_window_area
        / total_res_wall_area
        if total_res_wall_area > 0
        else 0,
        getattr(SCC, "EXTERIOR_NON_RESIDENTIAL"): total_nonres_window_area
        / total_nonres_wall_area
        if total_nonres_wall_area > 0
        else 0,
        getattr(SCC, "EXTERIOR_MIXED"): total_mixed_window_area / total_mixed_wall_area
        if total_mixed_wall_area > 0
        else 0,
        getattr(SCC, "SEMI_EXTERIOR"): total_semi_exterior_window_area
        / total_semi_exterior_wall_area
        if total_semi_exterior_wall_area > 0
        else 0,
    }
