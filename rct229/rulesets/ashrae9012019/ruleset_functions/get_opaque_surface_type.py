from typing import List, Dict

from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_

DEGREES = ureg("degrees")
MIN_FLOOR_TILT = 120 * DEGREES
MAX_FLOOR_TILT = 180 * DEGREES
MIN_ROOF_TILT = 0 * DEGREES
MAX_ROOF_TILT = 60 * DEGREES


# Intended for export and internal use
class OpaqueSurfaceType:
    """Enumeration class for opaque surface types"""

    ABOVE_GRADE_WALL: str = "ABOVE-GRADE WALL"
    BELOW_GRADE_WALL: str = "BELOW-GRADE WALL"
    FLOOR: str = "FLOOR"
    GROUND: str = "GROUND"
    HEATED_SOG: str = "HEATED SLAB-ON-GRADE"
    ROOF: str = "ROOF"
    UNHEATED_SOG: str = "UNHEATED SLAB-ON-GRADE"


def get_opaque_surface_type(
    surface: dict, constructions: List[Dict] | None = None
) -> str:
    """Determines a surface's opaque surface type

    Parameters
    ----------
    surface : dict
        A dictionary representing a surface as defined by the ASHRAE229 schema.
        It is assumed to have at least the minimal structure:
        {
            adjacent_to,
            construction: {
                has_radiant_heating
            },
            tilt
        }

    Returns
    -------
    str
        One of the following surface types: "ABOVE-GRADE WALL", "BELOW-GRADE WALL",
        "FLOOR", "HEATED SLAB-ON-GRADE", "ROOF", "UNHEATED SLAB-ON-GRADE"
    """
    surface_tilt = getattr_(surface, "surface", "tilt")

    # Check for roof
    if MIN_ROOF_TILT <= surface_tilt < MAX_ROOF_TILT:
        surface_type = OpaqueSurfaceType.ROOF

    # Check for a floor type
    elif MIN_FLOOR_TILT <= surface_tilt <= MAX_FLOOR_TILT:
        construction_id = getattr_(surface, "surface", "construction")
        if (
            next(
                (
                    c.get("has_radiant_heating")
                    for c in constructions or []
                    if c.get("id") == construction_id
                ),
                False,
            )
            if surface.get("adjacent_to") == OpaqueSurfaceType.GROUND
            else False
        ):
            surface_type = OpaqueSurfaceType.HEATED_SOG
        elif surface.get("adjacent_to") == OpaqueSurfaceType.GROUND:
            surface_type = OpaqueSurfaceType.UNHEATED_SOG
        else:
            surface_type = OpaqueSurfaceType.FLOOR

    # Is a wall
    elif surface.get("adjacent_to") == OpaqueSurfaceType.GROUND:
        surface_type = OpaqueSurfaceType.BELOW_GRADE_WALL
    else:
        surface_type = OpaqueSurfaceType.ABOVE_GRADE_WALL

    return surface_type
