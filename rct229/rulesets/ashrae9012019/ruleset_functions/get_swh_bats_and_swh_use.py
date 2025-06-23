from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_swh_bat import (
    get_building_segment_swh_bat,
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
        if swh_bat is None:
            # This means there is no service water uses and no types at building segments
            swh_bat = "UNDETERMINED"
        swh_and_swh_use_dict.setdefault(swh_bat, [])

        # TODO: Moving the `service_water_heating_uses` key to the `building_segments` level is being discussed. If the `service_water_heating_uses` key is moved, this function needs
        swh_and_swh_use_dict[swh_bat].extend(
            find_all(
                f'$.buildings[*].building_segments[*][?(@.id="{bldg_seg_id}")].zones[*].spaces[*].service_water_heating_uses[*]',
                rmd,
            )
        )

    return swh_and_swh_use_dict
