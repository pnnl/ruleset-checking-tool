from rct229.utils.jsonpath_utils import find_all
from rct229.utils.assertions import assert_


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

    spaces_served = []
    for bldg_segment in find_all("$.buildings[*].building_segments[*]", rmd):
        # Check if `swh_use_id` is in the building segment level
        if swh_use_id in bldg_segment.get("service_water_heating_uses", []):
            for space in find_all("$.zones[*].spaces[*]", bldg_segment):
                spaces_served.append(space["id"])

    # if `spaces_served` is an empty list, the SHW use is applied to only one space
    if not spaces_served:
        for space in find_all(
            "$.buildings[*].building_segments[*].zones[*].spaces[*]", rmd
        ):
            if swh_use_id in space.get("service_water_heating_uses", []):
                spaces_served.append(space["id"])

        # Make sure `swh_use_id` is not referenced by multiple spaces
        assert_(
            len(spaces_served) == 1,
            f"{swh_use_id} can't be referenced by multiple spaces.",
        )

    return spaces_served
