from typing import TypedDict

import pandas as pd
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_dict,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_required_fields

# Constants
# TODO: These should directly from the enumerations
SurfaceAdjacency = SchemaEnums.schema_enums["SurfaceAdjacencyOptions"]


# Intended for export and internal use
class SurfaceConditioningCategory:
    """Enumeration class for zone conditioning categories"""

    # Surface conditioning categories (export these)
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

# Intended for internal use
GET_SURFACE_CONDITIONING_CATEGORY_DICT__REQUIRED_FIELDS = {
    "building": {
        "$..surface[*]": ["adjacent_to"],
    }
}


def get_surface_conditioning_category_dict(climate_zone, building, constructions):
    """Determines the surface conditioning category for every surface in a building

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
        A dictionary that maps surfaces to one of the conditioning categories:
        EXTERIOR_RESIDENTIAL, EXTERIOR_NON_RESIDENTIAL, EXTERIOR_MIXED,
        SEMI_EXTERIOR, UNREGULATED
    """
    find_exactly_required_fields(
        GET_SURFACE_CONDITIONING_CATEGORY_DICT__REQUIRED_FIELDS["building"], building
    )

    # The dictionary to be returned
    surface_conditioning_category_dict = {}

    # Get the conditioning category for all the zones in the building
    zcc_dict = get_zone_conditioning_category_dict(
        climate_zone, building, constructions
    )

    # Loop through all the zones in the building
    for zone in find_all("building_segments[*].zones[*]", building):
        # Zone conditioning category
        zcc = zcc_dict[zone["id"]]

        # Loop through all the surfaces in the zone
        for surface in find_all("surfaces[*]", zone):
            surface_adjacent_to = surface["adjacent_to"]
            adjacency = (
                zcc_dict[getattr_(surface, "surface", "adjacent_zone")]
                if surface_adjacent_to == SurfaceAdjacency.INTERIOR
                else surface_adjacent_to
            )

            if adjacency in [SurfaceAdjacency.IDENTICAL, SurfaceAdjacency.UNDEFINED]:
                surface_conditioning_category_dict[
                    surface["id"]
                ] = SurfaceConditioningCategory.UNREGULATED

            elif zcc in SCC_DATA_FRAME.index and adjacency in SCC_DATA_FRAME.columns:
                surface_conditioning_category_dict[surface["id"]] = SCC_DATA_FRAME.at[
                    zcc,  # row index
                    adjacency,  # column index
                ]

            else:
                raise ValueError(
                    f"Combination of zone conditioning category '{zcc}' and surface adjacency '{adjacency}' has no mapping to a surface conditioning category"
                )

    return surface_conditioning_category_dict
