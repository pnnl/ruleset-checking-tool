from rct229.utils.jsonpath_utils import find_all


def get_swh_uses_associated_with_each_building_segment(
    rmd: dict, building_segment_id: str
) -> list[str]:
    """
    This function gets all the SWH uses connected to a building segment. This function is primarily to encapsulate getting service water heating uses in one function so that if a change is made in the schema as to how service water heating use is specified,
    the RCT only needs to change in one place.

    Parameters
    ----------
    rmd: dict
        RMD at RuleSetModelDescription level
    building_segment_id: str
        building segment id

    Returns
    -------
    swh_uses: list
        A list containing the ids of all service water heating uses associated with a building segment
    """

    swh_uses_list = find_all(
        f'$.buildings[*].building_segments[*][?(@.id="{building_segment_id}")].zones[*].spaces[*].service_water_heating_uses[*].id',
        rmd,
    )
    return swh_uses_list
