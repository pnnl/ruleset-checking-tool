from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.get_opaque_surface_type import (
    ABOVE_GRADE_WALL,
    get_opaque_surface_type,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.assertions import (
    assert_,
    assert_nonempty_lists,
    assert_required_fields,
    getattr_,
)
from rct229.utils.jsonpath_utils import find_all

DOOR = schema_enums["SubsurfaceClassificationType"].DOOR.name


def get_area_type_window_wall_area(climate_zone, building):
    # required fields for this function are coming from the nested functions.
    scc_dictionary = get_surface_conditioning_category_dict(climate_zone, building)
    window_wall_areas_dictionary = {}
    for building_segment in find_all("building_segments[*]", building):
        area_type = building_segment.get("area_type_vertical_fenestration")
        if not area_type:
            area_type = "NONE"

        if area_type not in window_wall_areas_dictionary:
            window_wall_areas_dictionary[area_type] = {
                "TOTAL_WALL_AREA": 0.0,
                "TOTAL_WINDOW_AREA": 0.0,
            }

        for surface in find_all("zones[*].surfaces[*]", building_segment):
            if (get_opaque_surface_type(surface) == ABOVE_GRADE_WALL) and (
                scc_dictionary[surface["id"]]
                in [
                    SCC.EXTERIOR_RESIDENTIAL,
                    SCC.EXTERIOR_NON_RESIDENTIAL,
                    SCC.EXTERIOR_MIXED,
                    SCC.SEMI_EXTERIOR,
                ]
            ):
                assert_("area" in surface, f"surface:{surface['id']} has no area")
                window_wall_areas_dictionary[area_type]["TOTAL_WALL_AREA"] += surface[
                    "area"
                ]

                # add sub-surfaces
                for subsurface in find_all("subsurfaces[*]", surface):
                    assert_(
                        "classification" in subsurface,
                        f"subsurface:{subsurface['id']} has no classification",
                    )
                    assert_(
                        "glazed_area" in subsurface,
                        f"subsurface:{subsurface['id']} has no glazed_area",
                    )
                    assert_(
                        "opaque_area" in subsurface,
                        f"subsurface:{subsurface['id']} has no opaque_area",
                    )
                    if (subsurface["classification"] == DOOR) and (
                        subsurface["glazed_area"] > subsurface["opaque_area"]
                    ):
                        window_wall_areas_dictionary[area_type][
                            "TOTAL_WINDOW_AREA"
                        ] += (subsurface["glazed_area"] + subsurface["opaque_area"])
                    else:
                        window_wall_areas_dictionary[area_type][
                            "TOTAL_WINDOW_AREA"
                        ] += (subsurface["glazed_area"] + subsurface["opaque_area"])
    return window_wall_areas_dictionary
