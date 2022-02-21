from rct229.schema.config import ureg


DEGREES = ureg("degrees")
MIN_FLOOR_TILT = 120 * DEGREES
MAX_FLOOR_TILT = 180 * DEGREES
MIN_ROOF_TILT = 0 * DEGREES
MAX_ROOF_TILT = 60 * DEGREES

ABOVE_GRADE_WALL = "ABOVE-GRADE WALL"
BELOW_GRADE_WALL = "BELOW-GRADE WALL"
FLOOR = "FLOOR"
ROOF = "ROOF"
HEATED_SOG = "HEATED SLAB-ON-GRADE"
UNHEATED_SOG = "UNHEATED SLAB-ON-GRADE"


def get_opaque_surface_type(surface):
    """Determines a surface's opaque surface type

    Parameters
    ----------
    surface : dict
        A dictionary representing a surface as defined by the ASHRAE229 schema.
        It is assumed to have at least the minimal structure:
        {
            ajacent_to,
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
    surface_tilt = surface["tilt"]

    # Check for roof
    if MIN_ROOF_TILT <= surface_tilt < MAX_ROOF_TILT:
        surface_type = ROOF

    # Check for a floor type
    elif MIN_FLOOR_TILT <= surface_tilt <= MAX_FLOOR_TILT:
        if (
            surface["construction"].get("has_radiant_heating")
            and surface["adjacent_to"] == "GROUND"
        ):
            surface_type = HEATED_SOG
        elif surface["adjacent_to"] == "GROUND":
            surface_type = UNHEATED_SOG
        else:
            surface_type = FLOOR

    # Is a wall
    elif surface["adjacent_to"] == "GROUND":
        surface_type = BELOW_GRADE_WALL
    else:
        surface_type = ABOVE_GRADE_WALL

    return surface_type
