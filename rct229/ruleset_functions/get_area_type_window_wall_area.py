from get_surface_conditioning_category_dict import get_surface_conditioning_category_dict, SurfaceConditioningCategory
from get_opaque_surface_type import get_opaque_surface_type, ABOVE_GRADE_WALL
from rct229.utils.jsonpath_utils import find_all


def get_area_type_window_wall_area(climate_zone, building):
    scc_dictionary = get_surface_conditioning_category_dict(climate_zone, building)
    window_wall_areas_dictionary = {}
    for building_segment in find_all("building_segments[*]", building):
        area_type = building_segment.get("area_type_vertical_fenestration")
        if not area_type:
            area_type = "NONE"

        if area_type not in window_wall_areas_dictionary:
            window_wall_areas_dictionary[area_type] = {"TOTAL_WALL_AREA": 0.0, "TOTAL_WINDOW_AREA": 0.0}

        for surface in find_all("zones[*].surfaces[*]", building_segment):
            if (get_opaque_surface_type(
                surface) == ABOVE_GRADE_WALL) and (scc_dictionary[surface.id] in
                                                      [SurfaceConditioningCategory.EXTERIOR_RESIDENTIAL,
                                                        SurfaceConditioningCategory.EXTERIOR_NON_RESIDENTIAL,
                                                       SurfaceConditioningCategory.EXTERIOR_MIXED,
                                                       SurfaceConditioningCategory.SEMI_EXTERIOR]):
                window_wall_areas_dictionary[area_type]["TOTAL_WALL_AREA"] += surface.area

                # add sub-surfaces
                for subsurface in find_all("subsurfaces[*]", surface):
                    if (subsurface.classification == "DOOR") and ( subsurface.glazed_area > subsurface.opaque_area ):
                        window_wall_areas_dictionary[area_type]["TOTAL_WINDOW_AREA"] += (subsurface.glazed_area + subsurface.opaque_area)
                    else:
                        window_wall_areas_dictionary[area_type]["TOTAL_WINDOW_AREA"] += (subsurface.glazed_area + subsurface.opaque_area)
    return window_wall_areas_dictionary
