from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_swh_bat import (
    get_building_segment_swh_bat,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_bats_and_swh_use import (
    get_swh_bats_and_swh_use,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_components_associated_with_each_swh_bat import (
    get_swh_components_associated_with_each_swh_bat,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_type import (
    get_swh_equipment_type,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

SERVICE_WATER_HEATING_SPACE = SchemaEnums.schema_enums[
    "ServiceWaterHeatingAreaOptions2019ASHRAE901"
]

CASE3_MSG = (
    "The Service Water Heating Building Area type for this building segment is undetermined, and there are multiple building segments in the project. "
    "Therefore it cannot be determined whether this building segment shares a service water heating building area type with one of the other building segments."
)
CASE4_MSG = (
    "The Service Water Heating Building Area Type is 'OTHER' and is applied to multiple building segments. "
    "'OTHER' can describe multiple Service Water Heating Building Area Types. "
    "Confirm that Service Water Heating Building Area Type is provided with one and only one service water heating system."
)


class PRM9012019Rule40i48(RuleDefinitionListIndexedBase):
    """Rule 8 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule40i48, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule40i48.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-8",
            description="One system per building area type shall be modeled in the baseline.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, a + b",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule40i48.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False,
                    BASELINE_0=True,
                    PROPOSED=True,
                ),
                index_rmd=BASELINE_0,
                each_rule=PRM9012019Rule40i48.RMDRule.SWHBATRule(),
            )

        def create_data(self, context, data):
            rmd_p = context.PROPOSED
            rmd_b = context.BASELINE_0

            num_of_bldg_segment_b = len(
                find_all("$.buildings[*].building_segments[*]", rmd_b)
            )

            num_other_swh_bat_segment_b = len(
                [
                    True
                    for bldg_seg_b in find_all(
                        "$.buildings[*].building_segments[*]", rmd_b
                    )
                    if get_building_segment_swh_bat(rmd_b, bldg_seg_b["id"])
                    == SERVICE_WATER_HEATING_SPACE.ALL_OTHERS
                ]
            )

            service_water_heating_uses_p = {
                swh_use["id"]: swh_use.get("use", 0.0)
                for swh_use in find_all(
                    "$.service_water_heating_uses[*]",
                    rmd_p,
                )
            }

            swh_equip_type_b = {
                swh_equip_id: get_swh_equipment_type(rmd_b, swh_equip_id)
                for swh_equip_id in find_all(
                    "$.service_water_heating_equipment[*].id", rmd_b
                )
            }

            swh_bats_and_uses_b = get_swh_components_associated_with_each_swh_bat(rmd_b)

            num_swh_systems_b = {
                swh_bat: len(swh_use.swh_distribution)
                for swh_bat, swh_use in swh_bats_and_uses_b.items()
            }
            num_swh_equipment_this_use_b = {
                swh_bat: len(swh_use.swh_heating_eq)
                for swh_bat, swh_use in swh_bats_and_uses_b.items()
            }

            swh_bats_and_uses_p = get_swh_bats_and_swh_use(rmd_p)

            building_area_type_SWH_equip_dict_b = {}
            building_area_type_and_uses_p = {}
            for bat_type, SWH_Equipment_Associations in swh_bats_and_uses_b.items():
                building_area_type_SWH_equip_dict_b[bat_type] = {}
                building_area_type_SWH_equip_dict_b[bat_type]["id"] = bat_type
                building_area_type_SWH_equip_dict_b[bat_type][
                    "SWH_Equipment_Associations"
                ] = SWH_Equipment_Associations

                building_area_type_and_uses_p[bat_type] = {}
                building_area_type_and_uses_p[bat_type]["id"] = bat_type
                building_area_type_and_uses_p[bat_type][
                    "swh_bats_and_uses_p"
                ] = swh_bats_and_uses_p[bat_type]

            return {
                "num_of_bldg_segment_b": num_of_bldg_segment_b,
                "num_other_swh_bat_segment_b": num_other_swh_bat_segment_b,
                "num_swh_systems_b": num_swh_systems_b,
                "num_swh_equipment_this_use_b": num_swh_equipment_this_use_b,
                "swh_bats_and_uses_b": swh_bats_and_uses_b,
                "service_water_heating_uses_p": service_water_heating_uses_p,
                "swh_equip_type_b": swh_equip_type_b,
                "building_area_type_SWH_equip_dict_b": building_area_type_SWH_equip_dict_b,
                "building_area_type_and_uses_p": building_area_type_and_uses_p,
            }

        def create_context_list(self, context, data=None):
            building_area_type_SWH_equip_dict_b = data[
                "building_area_type_SWH_equip_dict_b"
            ]
            building_area_type_and_uses_p = data["building_area_type_and_uses_p"]

            return [
                produce_ruleset_model_description(
                    USER=False,
                    BASELINE_0=building_area_type_SWH_equip_dict_b[bat_type],
                    PROPOSED=building_area_type_and_uses_p[bat_type],
                )
                for bat_type, SWH_Equipment_Associations in building_area_type_SWH_equip_dict_b.items()
            ]

        class SWHBATRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule40i48.RMDRule.SWHBATRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                )

            def is_applicable(self, context, data=None):
                building_area_type_and_uses_p_b = context.PROPOSED
                service_water_heating_uses_p = data["service_water_heating_uses_p"]

                return all(
                    [
                        service_water_heating_uses_p[swh_uses_id_p] > 0.0
                        for swh_uses_id_p in building_area_type_and_uses_p_b[
                            "swh_bats_and_uses_p"
                        ]
                    ]
                )

            def get_calc_vals(self, context, data=None):
                swh_bats_and_equip_dict_this_use = context.BASELINE_0
                num_of_bldg_segment_b = data["num_of_bldg_segment_b"]
                swh_bats_and_uses_b = data["swh_bats_and_uses_b"]

                swh_bat_b = swh_bats_and_equip_dict_this_use["id"]

                num_swh_systems_b = data["num_swh_systems_b"][swh_bat_b]
                num_other_swh_bat_segment_b = data["num_other_swh_bat_segment_b"]

                is_referenced_in_other_bats_b = True
                if num_swh_systems_b == 1:
                    is_referenced_in_other_bats_b = False
                    swh_dist_id = swh_bats_and_uses_b[swh_bat_b].swh_distribution[0]
                    for other_swh_bat in swh_bats_and_uses_b:
                        if other_swh_bat != swh_bat_b:
                            if (
                                swh_dist_id
                                in swh_bats_and_uses_b[swh_bat_b].swh_distribution
                            ):
                                is_referenced_in_other_bats_b = True

                return {
                    "swh_bat_b": swh_bat_b,
                    "num_swh_systems_b": num_swh_systems_b,
                    "num_of_bldg_segment_b": num_of_bldg_segment_b,
                    "is_referenced_in_other_bats_b": is_referenced_in_other_bats_b,
                    "num_other_swh_bat_segment_b": num_other_swh_bat_segment_b,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                swh_bat_b = calc_vals["swh_bat_b"]
                num_of_bldg_segment_b = calc_vals["num_of_bldg_segment_b"]
                num_other_swh_bat_segment_b = calc_vals["num_other_swh_bat_segment_b"]

                return (swh_bat_b == "UNDETERMINED" and num_of_bldg_segment_b > 1) or (
                    swh_bat_b == SERVICE_WATER_HEATING_SPACE.ALL_OTHERS
                    and num_other_swh_bat_segment_b > 1
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                swh_bat_b = calc_vals["swh_bat_b"]
                multiple_segments_with_bat_other_b = (
                    calc_vals["num_other_swh_bat_segment_b"] > 1
                )

                UNDETERMINED_MSG = ""
                if swh_bat_b == "UNDETERMINED":
                    UNDETERMINED_MSG = CASE3_MSG
                elif multiple_segments_with_bat_other_b:
                    UNDETERMINED_MSG = CASE4_MSG

                return UNDETERMINED_MSG

            def rule_check(self, context, calc_vals=None, data=None):
                num_swh_systems_b = calc_vals["num_swh_systems_b"]
                swh_bat_b = calc_vals["swh_bat_b"]
                num_of_bldg_segment_b = calc_vals["num_of_bldg_segment_b"]
                is_referenced_in_other_bats_b = calc_vals[
                    "is_referenced_in_other_bats_b"
                ]

                return (
                    num_swh_systems_b == 1
                    or (swh_bat_b == "UNDETERMINED" and num_of_bldg_segment_b == 1)
                    or not is_referenced_in_other_bats_b
                )
