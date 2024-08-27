from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel
from rct229.rulesets.ashrae9012019.ruleset_functions.get_energy_required_to_heat_swh_use import (
    get_energy_required_to_heat_swh_use,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO

SERVICE_WATERH_EATING_USE_UNIT = SchemaEnums.schema_enums[
    "ServiceWaterHeatingUseUnitOptions"
]


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
        building_segment_swh_bat = building_segment[
            "service_water_heating_building_area_type"
        ]
    else:
        swh_use_dict = {}
        service_water_heating_use_ids = (
            get_swh_uses_associated_with_each_building_segment(rmd, building_segment_id)
        )

        for swh_use_id in service_water_heating_use_ids:
            swh_use = find_one(
                f'$.zones[*].spaces[*].service_water_heating_uses[*][?(@.id="{swh_use_id}")]',
                building_segment,
            )

            if (
                swh_use
                and getattr_(swh_use, "service_water_heating_uses", "use_units")
                == SERVICE_WATERH_EATING_USE_UNIT.OTHER
            ):
                return RCTOutcomeLabel.UNDETERMINED

            swh_use_energy_by_space = get_energy_required_to_heat_swh_use(
                swh_use, rmd, building_segment
            )

            if swh_use.get("area_type"):
                swh_use_dict.set_default(swh_use["area_type"], ZERO.ENERGY)
                swh_use_dict[swh_use["area_type"]] += sum(
                    swh_use_energy_by_space.values()
                )
            else:
                for space_id in swh_use_energy_by_space:
                    space = find_one(
                        f'$.zones[*].spaces[*][?(@.id="{space_id}")]',
                        building_segment,
                    )
                    if space.get("service_water_heating_bat"):
                        swh_use_dict.set_default(space["service_water_heating_bat"], 0)
                        swh_use_dict[
                            space["service_water_heating_bat"]
                        ] += swh_use_energy_by_space[space_id]
                    else:
                        swh_use_dict.set_default(RCTOutcomeLabel.UNDETERMINED, 0)
                        swh_use_dict[
                            RCTOutcomeLabel.UNDETERMINED
                        ] += swh_use_energy_by_space[space_id]

        swh_use_dict_len = len(swh_use_dict)
        if swh_use_dict_len == 1:
            building_segment_swh_bat = next(iter(swh_use_dict))  # get the first key
        elif swh_use_dict_len == 2:
            if RCTOutcomeLabel.UNDETERMINED in swh_use_dict:
                all_keys = list(swh_use_dict)
                all_keys.remove(RCTOutcomeLabel.UNDETERMINED)
                other_key = all_keys[0]
                if swh_use_dict[RCTOutcomeLabel.UNDETERMINED] < swh_use_dict[other_key]:
                    building_segment_swh_bat = other_key

    return building_segment_swh_bat
