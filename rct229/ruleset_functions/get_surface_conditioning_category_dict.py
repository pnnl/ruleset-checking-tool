import pandas as pd

from rct229.ruleset_functions.get_zone_conditioning_category_dict import (
    CONDITIONED_MIXED,
    CONDITIONED_NON_RESIDENTIAL,
    CONDITIONED_RESIDENTIAL,
    SEMI_HEATED,
    UNCONDITIONED,
    UNENCLOSED,
    mock_get_zone_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all

# Constants
# TODO: These should directly from the enumerations
EXTERIOR = "EXTERIOR"
GROUND = "GROUND"
INTERIOR = "INTERIOR"
# Surface conditioning categories (export these)
EXTERIOR_MIXED = "EXTERIOR MIXED"
EXTERIOR_NON_RESIDENTIAL = "EXTERIOR NON-RESIDENTIAL"
EXTERIOR_RESIDENTIAL = "EXTERIOR RESIDENTIAL"
SEMI_EXTERIOR = "SEMI-EXTERIOR"
UNREGULATED = "UNREGULATED"

SCC_DATA_FRAME = pd.DataFrame(
    data={
        CONDITIONED_RESIDENTIAL: [
            UNREGULATED,
            UNREGULATED,
            UNREGULATED,
            SEMI_EXTERIOR,
            EXTERIOR_RESIDENTIAL,
            SEMI_EXTERIOR,
        ],
        CONDITIONED_NON_RESIDENTIAL: [
            UNREGULATED,
            UNREGULATED,
            UNREGULATED,
            SEMI_EXTERIOR,
            EXTERIOR_NON_RESIDENTIAL,
            SEMI_EXTERIOR,
        ],
        CONDITIONED_MIXED: [
            UNREGULATED,
            UNREGULATED,
            UNREGULATED,
            SEMI_EXTERIOR,
            EXTERIOR_MIXED,
            SEMI_EXTERIOR,
        ],
        SEMI_HEATED: [
            SEMI_EXTERIOR,
            SEMI_EXTERIOR,
            SEMI_EXTERIOR,
            UNREGULATED,
            SEMI_EXTERIOR,
            SEMI_EXTERIOR,
        ],
        UNENCLOSED: [
            EXTERIOR_RESIDENTIAL,
            EXTERIOR_NON_RESIDENTIAL,
            EXTERIOR_MIXED,
            SEMI_EXTERIOR,
            UNREGULATED,
            UNREGULATED,
        ],
        UNCONDITIONED: [
            SEMI_EXTERIOR,
            SEMI_EXTERIOR,
            SEMI_EXTERIOR,
            SEMI_EXTERIOR,
            UNREGULATED,
            UNREGULATED,
        ],
        EXTERIOR: [
            EXTERIOR_RESIDENTIAL,
            EXTERIOR_NON_RESIDENTIAL,
            EXTERIOR_MIXED,
            SEMI_EXTERIOR,
            UNREGULATED,
            UNREGULATED,
        ],
        GROUND: [
            EXTERIOR_RESIDENTIAL,
            EXTERIOR_NON_RESIDENTIAL,
            EXTERIOR_MIXED,
            SEMI_EXTERIOR,
            UNREGULATED,
            UNREGULATED,
        ],
    },
    index=[
        CONDITIONED_RESIDENTIAL,
        CONDITIONED_NON_RESIDENTIAL,
        CONDITIONED_MIXED,
        SEMI_HEATED,
        UNENCLOSED,
        UNCONDITIONED,
    ],
)

# Intended for export and internal use
GET_SURFACE_CONDITIONING_CATEGORY_DICT = {
    "building": {
        "building_segments[*].zones[*]": [
            "surfaces"
        ],
        "building_segments[*].zones[*].surfaces[*]":[
            "adjacent_to", "adjacent_zone"
        ]
    }
}


def get_surface_conditioning_category_dict(climate_zone, building):
    """Determines the surface conditioning category for every surface in a building

    Parameters
    ----------
    climate_zone : str
        One of the ClimateZone2019ASHRAE901 enumerated values
    building : dict
        A dictionary representing a building as defined by the ASHRAE229 schema
    Returns
    -------
    dict
        A dictionary that maps surfaces to one of the conditioning categories:
        EXTERIOR_RESIDENTIAL, EXTERIOR_NON_RESIDENTIAL, EXTERIOR_MIXED,
        SEMI_EXTERIOR, UNREGULATED
    """
    # The dictionary to be returned
    surface_conditioning_category_dict = {}

    # Get the conditioning category for all the zones in the building
    zcc_dict = mock_get_zone_conditioning_category_dict(climate_zone, building)

    # Loop through all the zones in the building
    for zone in find_all("building_segments[*].zones[*]", building):
        # Zone conditioning category
        zcc = zcc_dict[zone["id"]]

        # Loop through all the surfaces in the zone
        for surface in zone["surfaces"]:
            surface_adjacent_to = surface["adjacent_to"]
            surface_conditioning_category_dict[surface["id"]] = SCC_DATA_FRAME.at[
                # row index
                zcc,
                # column index
                zcc_dict[surface["adjacent_zone"]]
                if surface_adjacent_to == INTERIOR
                else surface_adjacent_to,
            ]

    return surface_conditioning_category_dict
