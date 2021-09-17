from rct229.utils.jsonpath_utils import find_all


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
    surface_type = None
    surface_tilt = surface["tilt"]

    # Check for roof
    if 0 <= surface_tilt < 60:
        surface_type = "ROOF"

    # Check for a floor type
    elif 120 <= surface_tilt <= 180:
        if (
            surface["construction"]["has_radiant_heating"]
            and surface["adjacent_to"] == "GROUND"
        ):
            surface_type = "HEATED SLAB-ON-GRADE"
        elif surface["adjacent_to"] == "GROUND":
            surface_type = "UNHEATED SLAB-ON-GRADE"
        else:
            surface_type = "FLOOR"

    # Is a wall
    elif surface["adjacent_to"] == "GROUND":
        surface_type = "BELOW-GRADE WALL"
    else:
        surface_type = "ABOVE-GRADE WALL"

    return surface_type
