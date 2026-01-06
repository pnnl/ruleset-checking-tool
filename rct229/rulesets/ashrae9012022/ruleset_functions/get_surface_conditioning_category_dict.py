import os
from typing import TypedDict

import pandas as pd
from rct229.rulesets.ashrae9012022.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
    get_zone_conditioning_category_dict,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_exactly_required_fields

# Constants
SurfaceAdjacency = SchemaEnums.schema_enums["SurfaceAdjacencyOptions"]

_DISABLE_SURFACE_COND_CACHE = os.getenv("RCT_DISABLE_CACHE") == "1"
# (rmd_type, climate_zone) → { building_id → surface_dict }
_SURFACE_COND_CACHE: dict[tuple[str, str], dict[str, dict]] = {}


class SurfaceConditioningCategory:
    EXTERIOR_MIXED: str = "EXTERIOR MIXED"
    EXTERIOR_NON_RESIDENTIAL: str = "EXTERIOR NON-RESIDENTIAL"
    EXTERIOR_RESIDENTIAL: str = "EXTERIOR RESIDENTIAL"
    SEMI_EXTERIOR: str = "SEMI-EXTERIOR"
    UNREGULATED: str = "UNREGULATED"


class ZoneConditioningDataDict(TypedDict):
    EXTERIOR_RESIDENTIAL: float
    EXTERIOR_NON_RESIDENTIAL: float
    EXTERIOR_MIXED: float
    SEMI_EXTERIOR: float


SCC_DATA_FRAME = pd.DataFrame(
    data={
        ZCC.CONDITIONED_RESIDENTIAL: [
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.EXTERIOR_RESIDENTIAL,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
        ],
        ZCC.CONDITIONED_NON_RESIDENTIAL: [
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.EXTERIOR_NON_RESIDENTIAL,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
        ],
        ZCC.CONDITIONED_MIXED: [
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.EXTERIOR_MIXED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
        ],
        ZCC.SEMI_HEATED: [
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
        ],
        ZCC.UNENCLOSED: [
            SurfaceConditioningCategory.EXTERIOR_RESIDENTIAL,
            SurfaceConditioningCategory.EXTERIOR_NON_RESIDENTIAL,
            SurfaceConditioningCategory.EXTERIOR_MIXED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
        ],
        ZCC.UNCONDITIONED: [
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
        ],
        SurfaceAdjacency.EXTERIOR: [
            SurfaceConditioningCategory.EXTERIOR_RESIDENTIAL,
            SurfaceConditioningCategory.EXTERIOR_NON_RESIDENTIAL,
            SurfaceConditioningCategory.EXTERIOR_MIXED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
        ],
        SurfaceAdjacency.GROUND: [
            SurfaceConditioningCategory.EXTERIOR_RESIDENTIAL,
            SurfaceConditioningCategory.EXTERIOR_NON_RESIDENTIAL,
            SurfaceConditioningCategory.EXTERIOR_MIXED,
            SurfaceConditioningCategory.SEMI_EXTERIOR,
            SurfaceConditioningCategory.UNREGULATED,
            SurfaceConditioningCategory.UNREGULATED,
        ],
    },
    index=[
        ZCC.CONDITIONED_RESIDENTIAL,
        ZCC.CONDITIONED_NON_RESIDENTIAL,
        ZCC.CONDITIONED_MIXED,
        ZCC.SEMI_HEATED,
        ZCC.UNENCLOSED,
        ZCC.UNCONDITIONED,
    ],
)

GET_SURFACE_CONDITIONING_CATEGORY_DICT__REQUIRED_FIELDS = {
    "building": {
        "$..surface[*]": ["adjacent_to"],
    }
}


def _get_surface_conditioning_category_dict_uncached(
    climate_zone, building, constructions, rmd_type
):
    find_exactly_required_fields(
        GET_SURFACE_CONDITIONING_CATEGORY_DICT__REQUIRED_FIELDS["building"], building
    )

    surface_conditioning_category_dict = {}

    zcc_dict = get_zone_conditioning_category_dict(
        climate_zone, building, constructions, rmd_type
    )

    for building_segment in building.get("building_segments", []):
        for zone in building_segment.get("zones", []):
            zcc = zcc_dict[zone["id"]]

            for surface in zone.get("surfaces", []):
                surface_adjacent_to = surface["adjacent_to"]
                adjacency = (
                    zcc_dict[getattr_(surface, "surface", "adjacent_zone")]
                    if surface_adjacent_to == SurfaceAdjacency.INTERIOR
                    else surface_adjacent_to
                )

                if adjacency in (
                    SurfaceAdjacency.IDENTICAL,
                    SurfaceAdjacency.UNDEFINED,
                ):
                    surface_conditioning_category_dict[
                        surface["id"]
                    ] = SurfaceConditioningCategory.UNREGULATED

                elif (
                    zcc in SCC_DATA_FRAME.index and adjacency in SCC_DATA_FRAME.columns
                ):
                    surface_conditioning_category_dict[
                        surface["id"]
                    ] = SCC_DATA_FRAME.at[zcc, adjacency]

                else:
                    raise ValueError(
                        f"Combination of zone conditioning category '{zcc}' "
                        f"and surface adjacency '{adjacency}' has no mapping "
                        f"to a surface conditioning category"
                    )

    return surface_conditioning_category_dict


def get_surface_conditioning_category_dict(
    climate_zone,
    building,
    constructions,
    rmd_type,
):
    if constructions is None:
        constructions = []

    if _DISABLE_SURFACE_COND_CACHE:
        return _get_surface_conditioning_category_dict_uncached(
            climate_zone, building, constructions, rmd_type
        )

    assert isinstance(rmd_type, str), type(rmd_type)

    cache_key = (rmd_type, climate_zone)
    building_id = building["id"]

    rmd_cache = _SURFACE_COND_CACHE.setdefault(cache_key, {})

    if building_id in rmd_cache:
        return rmd_cache[building_id]

    result = _get_surface_conditioning_category_dict_uncached(
        climate_zone, building, constructions, rmd_type
    )

    rmd_cache[building_id] = result
    return result
