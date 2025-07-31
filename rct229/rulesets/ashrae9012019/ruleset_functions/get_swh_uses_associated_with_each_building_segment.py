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
        A dictionary where the keys are all the building segment ids and the value is `service_water_heating_uses` object under the `service_water_heating_uses`.
    """
    swh_uses_dict = {
        bldg_seg["id"]: [
            find_exactly_one_service_water_heating_use(rmd, swh_use_id)
            for swh_use_id in find_all(
                "$.zones[*].spaces[*].service_water_heating_uses[*]", bldg_seg
            )
        ]
        for bldg_seg in find_all("$.buildings[*].building_segments[*]", rmd)
    }
    return swh_uses_dict
