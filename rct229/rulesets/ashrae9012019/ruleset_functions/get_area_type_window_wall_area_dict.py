from typing import Any, Dict

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
    get_surface_conditioning_category_dict,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO

DOOR = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"].DOOR
NONE_AREA_TYPE = "NONE"


class AreaTypeWindowWallAreaDict:
    total_wall_area: float | int
    total_window_area: float | int


def get_area_type_window_wall_area_dict(
    climate_zone: str, constructions: list, building: dict
) -> dict[str | Any, dict[str, Any]]:
    """Gets a dictionary mapping building area type to a dictionary of (total area of
    above grade vertical surfaces) and (total area of fenestration)

    Parameters
    ----------
    climate_zone : str
        One of the ClimateZoneOptions2019ASHRAE901 enumerated values
    constructions : list
        A list of construction objects as defined by the ASHRAE229 schema
    building : dict
        A dictionary representing a building as defined by the ASHRAE229 schema

    Returns
    -------
    dict
        A dictionary that saves each area type in a building as per Table G3.1.1-1 with its total fenestration
        and envelope above-grade wall areas,
        {"AREA_TYPE_1":
            {"total_wall_area": <total wall area under the area_type_1>,
            "total_window_area": <total window area under the area_type_1>},
        "AREA_TYPE_2":
            {"total_wall_area": <total wall area under the area_type_2>,
            "total_window_area": <total window area under the area_type_2>}
        }
    """
    # required fields for this function are coming from the nested functions.
    scc_dictionary = get_surface_conditioning_category_dict(
        climate_zone, building, constructions
    )
    window_wall_areas_dictionary = {}
    for building_segment in find_all("building_segments[*]", building):
        area_type = building_segment.get("area_type_vertical_fenestration")
        if not area_type:
            area_type = "NONE"

        if area_type not in window_wall_areas_dictionary:
            window_wall_areas_dictionary[area_type]: AreaTypeWindowWallAreaDict = {
                "total_wall_area": ZERO.AREA,
                "total_window_area": ZERO.AREA,
            }

        for surface in find_all("zones[*].surfaces[*]", building_segment):
            if (get_opaque_surface_type(surface) == OST.ABOVE_GRADE_WALL) and (
                scc_dictionary[surface["id"]]
                in [
                    SCC.EXTERIOR_RESIDENTIAL,
                    SCC.EXTERIOR_NON_RESIDENTIAL,
                    SCC.EXTERIOR_MIXED,
                    SCC.SEMI_EXTERIOR,
                ]
            ):
                window_wall_areas_dictionary[area_type]["total_wall_area"] += getattr_(
                    surface, "surface", "area"
                )

                # add sub-surfaces
                for subsurface in find_all("$.subsurfaces[*]", surface):
                    glazed_area = getattr_(subsurface, "subsurface", "glazed_area")
                    opaque_area = getattr_(subsurface, "subsurface", "opaque_area")
                    if (
                        getattr_(subsurface, "subsurface", "classification") == DOOR
                    ) and (glazed_area > opaque_area):
                        window_wall_areas_dictionary[area_type][
                            "total_window_area"
                        ] += (glazed_area + opaque_area)
                    else:
                        window_wall_areas_dictionary[area_type][
                            "total_window_area"
                        ] += (glazed_area + opaque_area)
    return window_wall_areas_dictionary
