from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import find_exactly_one_zone


def get_zones_on_same_floor_list(rmi, source_zone_id):
    """
    Provides a list of zone ids that are on the floor as the source zone (including the source zone id)

    Parameters
    ----------
    rmi dict
    A dictionary representing a RuleModelInstance object as defined by the ASHRAE229 schema

    source_zone_id string
    The zone id for which we want to find all other zones on the same floor

    Returns
    -------
    a list of zone ids that are on the same floor as the starting zone.  The list will include the starting zone.
    """

    source_zone_floor_name = getattr_(
        find_exactly_one_zone(rmi, source_zone_id), "Zone", "floor_name"
    )
    return find_all(
        f'$.buildings[*].building_segments[*].zones[*][?(@.floor_name="{source_zone_floor_name}")].id',
        rmi,
    )
