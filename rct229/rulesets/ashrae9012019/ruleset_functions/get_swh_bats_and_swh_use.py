from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_swh_bat import (
    get_building_segment_swh_bat,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.utils.jsonpath_utils import find_all


def get_swh_bats_and_swh_use(rmd: dict) -> dict:
    """
    This function gets all the SWH Uses and the SWH space types and sorts them into a dictionary where the keys are the ServiceWaterHeatingBuildingAreaOptions2019ASHRAE901
    and values are a list of ServiceWaterHeatingUse.ids

    Parameters
    ----------
    rmd: dict
        The ruleset model descriptions

    Returns
    -------
    swh_bat_and_SWH_use_dict: dict
        A dictionary containing where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 in the RMD and values are lists of SWHUse ids.
        Example: {"DORMITORY":["swh1","swh2","swh3"], "AUTOMOTIVE_FACILITY":["swhg1","swhg2","swhg3"]}
    """

    swh_and_swh_use_dict = {}
    for building_segment in find_all("$.buildings[*].building_segments[*]", rmd):
        bldg_seg_id = building_segment["id"]
        swh_bat = get_building_segment_swh_bat(rmd, bldg_seg_id)
        swh_and_swh_use_dict.setdefault(swh_bat, [])

        service_water_heating_use_ids = (
            get_swh_uses_associated_with_each_building_segment(rmd, bldg_seg_id)
        )

        swh_and_swh_use_dict[swh_bat].extend(service_water_heating_use_ids)

    return swh_and_swh_use_dict
