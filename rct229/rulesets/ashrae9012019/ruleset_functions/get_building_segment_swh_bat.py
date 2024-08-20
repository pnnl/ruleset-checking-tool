from rct229.utils.jsonpath_utils import find_all
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_energy_required_to_heat_swh_use import (
    get_energy_required_to_heat_swh_use,
)
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value
from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel

def get_building_segment_swh_bat(rmd: dict, building_segment_id: str) -> str:
    """
    This function determines the SWH BAT for the given building segment.

    Parameters
    ----------
    rmd: dict
        RMD at RuleSetModelDescription level
    building_segment_id: str
        building segment id

    Returns
    -------
    building_segment_swh_bat: dict
        one of the ServiceWaterHeatingSpaceOptions2019ASHRAE901 options

    """

    building_segment = find_all(
        f'$.buildings[*].building_segments[*][?(@.id="{building_segment_id}")].zones[*].spaces[*].service_water_heating_uses[*]',
        rmd,
    )

    if building_segment.get("service_water_heating_building_area_type"):
        building_segment_swh_bat = building_segment["service_water_heating_building_area_type"]
    else:
        swh_use_dict = {}
        service_water_heating_use_ids = get_swh_uses_associated_with_each_building_segment(rmd, building_segment_id)

        for swh_use_id in service_water_heating_use_ids:
            swh_use = find_exactly_one_with_field_value(f'$.buildings[*].building_segment[*][?(@.id="{building_segment_id}")].zones[*]', "id", building_segment_id, rmd)

            swh_use_energy_by_space = get_energy_required_to_heat_swh_use(swh_use, rmd, building_segment)

            if swh_use.get("area_type"):
                swh_use_dict.set_default(swh_use["area_type"], 0)
                swh_use_dict[swh_use["area_type"]] += sum(swh_use_energy_by_space)
            else:
                swh_use_dict = 1

        if len(swh_use_dict) == 1:
            building_segment_swh_bat = list(swh_use_dict.keys())[0]
        elif len(swh_use_dict) == 2:
            if RCTOutcomeLabel.UNDETERMINED in swh_use_dict:
                all_keys = list(swh_use_dict.keys())
                all_keys.remove(RCTOutcomeLabel.UNDETERMINED)
                other_key = all_keys[0]
                if swh_use_dict[RCTOutcomeLabel.UNDETERMINED] < swh_use_dict[other_key]:
                    building_segment_swh_bat = other_key

    return building_segment_swh_bat
