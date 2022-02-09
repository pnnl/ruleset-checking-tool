from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.json_utils import get_value_from_key
# Constants
DEGREES = ureg("degrees")
MIN_FLOOR_TILT = 120 * DEGREES
MAX_FLOOR_TILT = 180 * DEGREES
MIN_ROOF_TILT = 0 * DEGREES
MAX_ROOF_TILT = 60 * DEGREES


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
    tilt_resp = get_value_from_key("tilt", surface, __name__)
    if tilt_resp["status"] == "success":
        surface_tilt = tilt_resp["data"]
    else:
        return tilt_resp

    # Check for roof
    if MIN_ROOF_TILT <= surface_tilt < MAX_ROOF_TILT:
        surface_type = "ROOF"

    # Check for a floor type
    elif MIN_FLOOR_TILT <= surface_tilt <= MAX_FLOOR_TILT:
        if (
            surface["construction"].get("has_radiant_heating")
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
