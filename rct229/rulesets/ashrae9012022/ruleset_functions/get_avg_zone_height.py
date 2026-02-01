from pint import Quantity
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all, find_exactly_required_fields
from rct229.utils.pint_utils import ZERO

# Intended for internal use
GET_AVG_ZONE_HEIGHT__REQUIRED_FIELDS = {"zone": {"$": ["spaces", "volume"]}}


def get_avg_zone_height(zone: dict) -> Quantity:
    """Determines average height of a zone as volume/floor area

    Parameters
    ----------
    zone : dict
        A dictionary representing a zone as defined by the ASHRAE229 schema.
        It is assumed to have at least the minimal structure:
        {
            spaces: [
                {
                    floor_area: <optional, but the total floor area must be positive>
                }
            ],
            volume:
        }

    Returns
    -------
    Quantity
        A Pint Quantity representing a length
    """
    find_exactly_required_fields(GET_AVG_ZONE_HEIGHT__REQUIRED_FIELDS["zone"], zone)

    zone_volume = zone["volume"]
    zone_floor_area = sum(find_all("$.spaces[*].floor_area", zone))

    assert_(
        zone_floor_area > ZERO.AREA, f"zone:{zone['id']} has zero total floor area."
    )

    return zone_volume / zone_floor_area
