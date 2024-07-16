from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.utility_functions import find_exactly_one_zone


def get_zones_on_same_floor_list(rmd: dict, source_zone_id: str) -> list[str]:
    """
    Provides a list of zone ids that are on the floor as the source zone (including the source zone id)

    Parameters
    ----------
    rmd dict
    A dictionary representing a RuleModelInstance object as defined by the ASHRAE229 schema

    source_zone_id string
    The zone id for which we want to find all other zones on the same floor

    Returns
    -------
    a list of zone ids that are on the same floor as the starting zone.  The list will include the starting zone.
    """
    # not to raise exception if the zone is missing a floor_name
    # This will still result an empty list if no floor_name is found.
    source_zone_floor_name = find_one(
        "$.floor_name", find_exactly_one_zone(rmd, source_zone_id)
    )
    return find_all(
        f'$.buildings[*].building_segments[*].zones[*][?(@.floor_name="{source_zone_floor_name}")].id',
        rmd,
    )
