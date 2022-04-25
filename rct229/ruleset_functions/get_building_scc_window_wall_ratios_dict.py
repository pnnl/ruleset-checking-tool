from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
    SurfaceConditioningCategory as SCC,
)
from rct229.utils.assertions import assert_required_fields, getattr_
from rct229.utils.jsonpath_utils import find_all

DOOR = schema_enums["SubsurfaceClassificationType"].DOOR.name

# Intended for internal use
GET_BUILDING_SCC_WINDOW_WALL_RATIO_DICT__REQUIRED_FIELDS = {
    "building": {
        "$..surface[*]": ["adjacent_to"],
    }
}


def get_building_scc_window_wall_ratio_dict(climate_zone, building):
    """Determines the window to wall ratio for each surface conditioning category
    in a building

    Parameters
    ----------
    climate_zone : str
        One of the ClimateZone2019ASHRAE901 enumerated values
    building : dict
        A dictionary representing a building as defined by the ASHRAE229 schema

    Returns
    -------
    dict
        A dictionary that maps each surface conditioning category to its average
        window to wall ratio
    """
    assert_required_fields(
        GET_BUILDING_SCC_WINDOW_WALL_RATIO_DICT__REQUIRED_FIELDS["building"], building
    )

    # The dictionary to be returned
    get_building_scc_window_wall_ratio_dict = {}

    # Get the conditioning category for all the zones in the building
    scc_dict = get_surface_conditioning_category_dict(climate_zone, building)

    # Loop through all the surfaces in the building
    for surface in find_all("$..surfaces[*]", building):
        # surface conditioning category
        scc = scc_dict[surface["id"]]

        # Initialize total window areas
        total_res_window_area = ZERO.AREA
        total_nonres_window_area = ZERO.AREA
        total_mixed_window_area = ZERO.AREA
        total_semiheated_window_area = ZERO.AREA

        # Initialize total wall areas
        total_res_wall_area = ZERO.AREA
        total_nonres_wall_area = ZERO.AREA
        total_mixed_wall_area = ZERO.AREA
        total_semiheated_wall_area = ZERO.AREA

        if get_opaque_surface_type(surface) == OST.ABOVE_GRADE_WALL:
            if scc == SCC.EXTERIOR_RESIDENTIAL:
                total_res_wall_area += surface.get("area", ZERO.AREA)
                for subsurface in find_all("subsurfaces[*]", surface):
                    subsurface_classification = getattr_(subsurface, "subsurface", "classification")
                    if subsurface_classification ==

    return surface_conditioning_category_dict
