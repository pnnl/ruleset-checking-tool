from rct229.utils.assertions import assert_required_fields
from rct229.utils.jsonpath_utils import find_all

# Intended for internal use
GET_AVG_ZONE_HT__REQUIRED_FIELDS = {
    "zone": {"$": ["volume"], "spaces[*]": ["floor_area"]}
}


def get_avg_zone_ht(zone):
    """Determines the average height of a zone

    The average height is the zone volumne divide by the total floor area
    of the zone's spaces.

    Parameters
    ----------
    zone : dict
        A Zone as described by ASHRAE229.schema.json

    Returns
    -------
    Pint Quantity
        The
    """
    assert_required_fields(GET_AVG_ZONE_HT__REQUIRED_FIELDS["zone"], zone)

    return zone["volume"] / sum(find_all("spaces[*].floor_area", zone))
