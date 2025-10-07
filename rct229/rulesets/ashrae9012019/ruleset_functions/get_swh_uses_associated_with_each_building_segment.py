from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import find_exactly_one_service_water_heating_use


def get_swh_uses_associated_with_each_building_segment(
    rmd: dict,
) -> dict[str : list[dict]]:
    """
    Description: This function gets all the SWH uses connected to a building segment. This function is primarily to encapsulate getting service water heating uses in one function so that if a change is made in the schema as to how service water heating use is specified, the RCT only needs to change in one place.

    Parameters
    ----------
    rmd: dict
        RMD at RuleSetModelDescription level

    Returns
    -------
    swh_uses_dict: dict
        A dictionary where the keys are all the building segment ids and the value is a list `service_water_heating_uses` object.
    """

    swh_uses_dict = {}
    for bldg_seg in find_all("$.buildings[*].building_segments[*]", rmd):
        swh_uses_id_list = find_all("$.service_water_heating_uses[*]", bldg_seg)

        for swh_use_list in find_all(
            "$.zones[*].spaces[*].service_water_heating_uses[*]", bldg_seg
        ):
            swh_uses_id_list.append(swh_use_list)

        # The reason why `list(set(swh_uses_id_list))` isn't used is when it's used, the order of swh uses id changed and this causes unexpected error in the unit test.
        swh_uses_id_list = list(dict.fromkeys(swh_uses_id_list))

        swh_uses_dict[bldg_seg["id"]] = [
            find_exactly_one_service_water_heating_use(rmd, swh_use_id)
            for swh_use_id in swh_uses_id_list
        ]

    return swh_uses_dict
