from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.utils.jsonpath_utils import find_all


class PRM9012019Rule29i55(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule29i55, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule29i55.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-11",
            description=(
                "For buildings that will have no service water-heating loads, no service water-heating shall be "
                "modeled in baseline building model"
            ),
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, c",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule29i55.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule29i55.RMDRule.BuildingSegmentRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*].building_segments[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_p = context.PROPOSED
            swh_use_loads_p = sum(
                [
                    swh_use_p.get("use", 0.0)
                    for building_segment_p in find_all(
                        "$.buildings[*].building_segments[*]", rmd_p
                    )
                    for swh_use_p in get_swh_uses_associated_with_each_building_segment(
                        rmd_p
                    )[building_segment_p["id"]]
                ]
            )

            return swh_use_loads_p <= 0.0

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            building_segment_associated_swh_use_dict_b = {}
            for building_segment_b in find_all(
                "$.buildings[*].building_segments[*]", rmd_b
            ):
                swh_use_list_b = get_swh_uses_associated_with_each_building_segment(
                    rmd_b
                )[building_segment_b["id"]]
                building_segment_associated_swh_use_dict_b.setdefault(
                    building_segment_b["id"], []
                ).extend(swh_use_list_b)
            return {
                "building_segment_associated_swh_use_dict_b": building_segment_associated_swh_use_dict_b
            }

        class BuildingSegmentRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule29i55.RMDRule.BuildingSegmentRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                )

            def get_calc_vals(self, context, data=None):
                building_segment_b = context.BASELINE_0
                building_segment_associated_swh_use_dict_b = data[
                    "building_segment_associated_swh_use_dict_b"
                ]

                swh_use_loads_b = sum(
                    [
                        swh_use_b.get("use", 0.0)
                        for swh_use_b in building_segment_associated_swh_use_dict_b[
                            building_segment_b["id"]
                        ]
                    ]
                )
                return {"swh_use_loads_b": swh_use_loads_b}

            def rule_check(self, context, calc_vals=None, data=None):
                swh_use_loads_b = calc_vals["swh_use_loads_b"]
                return swh_use_loads_b <= 0.0
