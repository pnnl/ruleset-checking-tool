from rct229.utils.jsonpath_utils import find_all


def get_spaces_served_by_swh_use(rmd: dict, swh_use_id: str) -> list[str]:
    """
    This function determines the spaces served by a given SWH use. The convention is that if any spaces reference the swh_use, then the service water heating use applies to only those spaces.
    If no spaces reference the service water heating use, it applies to all spaces in the building segment.

    Parameters
    ----------
    rmd: dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema
    swh_use_id: str
        id of the `service_water_heating_uses` key

    Returns
    -------
    spaces_served: list of str
        list of space ids that has the sane service_water_heating_uses value
    """
    # TODO: Moving the `service_water_heating_uses` key to the `building_segments` level is being discussed. If the `service_water_heating_uses` key is moved, this function needs to be revisited.

    spaces_served = [
        space["id"]
        for space in find_all(
            "$.buildings[*].building_segments[*].zones[*].spaces[*]", rmd
        )
        for space_swh_use_id in find_all("$.service_water_heating_uses[*]", space)
        if swh_use_id == space_swh_use_id
    ]

    # if `spaces_served` is an empty list, apply to all spaces
    if not spaces_served:
        spaces_served = find_all(
            "$.buildings[*].building_segments[*].zones[*].spaces[*].id", rmd
        )

    return spaces_served
