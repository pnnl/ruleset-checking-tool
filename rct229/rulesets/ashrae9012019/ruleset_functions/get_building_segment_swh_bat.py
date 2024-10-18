from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel
from rct229.rulesets.ashrae9012019.ruleset_functions.get_energy_required_to_heat_swh_use import (
    get_energy_required_to_heat_swh_use,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value
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

    building_segment = find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*]",
        "id",
        building_segment_id,
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
            swh_use = find_exactly_one_with_field_value(
                f"$.zones[*].spaces[*].service_water_heating_uses[*]",
                "id",
                swh_use_id,
                building_segment,
            )

            if swh_use.get("use_units") == SERVICE_WATERH_EATING_USE_UNIT.OTHER:
                return RCTOutcomeLabel.UNDETERMINED

            swh_use_energy_by_space = get_energy_required_to_heat_swh_use(
                swh_use["id"], rmd, building_segment["id"], False
            )

            if swh_use.get("area_type"):
                area_type = swh_use["area_type"]
                swh_use_dict.setdefault(area_type, ZERO.ENERGY)
                swh_use_dict[area_type] += sum(swh_use_energy_by_space.values())
            else:
                for space_id in swh_use_energy_by_space:
                    space = find_exactly_one_with_field_value(
                        "$.zones[*].spaces[*]",
                        "id",
                        space_id,
                        building_segment,
                    )
                    if space.get("service_water_heating_building_area_type"):
                        service_water_heating_bat = space[
                            "service_water_heating_building_area_type"
                        ]
                        swh_use_dict.setdefault(service_water_heating_bat, ZERO.ENERGY)
                        swh_use_dict[
                            service_water_heating_bat
                        ] += swh_use_energy_by_space[space_id]
                    else:
                        swh_use_dict.setdefault(
                            RCTOutcomeLabel.UNDETERMINED, ZERO.ENERGY
                        )
                        swh_use_dict[
                            RCTOutcomeLabel.UNDETERMINED
                        ] += swh_use_energy_by_space[space_id]

        swh_use_dict_len = len(swh_use_dict)
        if swh_use_dict_len == 1 and RCTOutcomeLabel.UNDETERMINED not in swh_use_dict:
            building_segment_swh_bat = next(iter(swh_use_dict))  # get the key
        elif swh_use_dict_len == 1 and RCTOutcomeLabel.UNDETERMINED in swh_use_dict:
            building_segment_swh_bat = RCTOutcomeLabel.UNDETERMINED
        elif swh_use_dict_len == 2:
            if RCTOutcomeLabel.UNDETERMINED in swh_use_dict:
                # find a key name other than `UNDETERMINED`
                other_key = [
                    key
                    for key in list(swh_use_dict)
                    if key != RCTOutcomeLabel.UNDETERMINED
                ][0]
                building_segment_swh_bat = (
                    other_key
                    if swh_use_dict[RCTOutcomeLabel.UNDETERMINED]
                    < swh_use_dict[other_key]
                    else RCTOutcomeLabel.UNDETERMINED
                )
            else:
                # Extract the keys and values
                keys = list(swh_use_dict.keys())
                values = list(swh_use_dict.values())

                building_segment_swh_bat = keys[0] if values[0] > values[1] else keys[1]

        # TODO: what if swh_use_dict_len >= 3?

    return building_segment_swh_bat
