from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.utils.jsonpath_utils import find_all


class Section11Rule13(RuleDefinitionListIndexedBase):
    """Rule 13 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule13, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section11Rule13.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-13",
            description=(
                "Service water-heating energy consumption shall be calculated explicitly based upon the volume of service water heating required and the entering makeup water and the leaving service water-heating temperatures. Entering water temperatures shall be estimated based upon the location. Leaving temperatures shall be based upon the end-use requirements."
            ),
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, (e)",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section11Rule13.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                index_rmd=BASELINE_0,
                each_rule=Section11Rule13.RMDRule.BuildingRule(),
            )

        def get_calc_vals(self, context, data=None):
            rmd_b = context.BASELINE_0
            energy_required_to_heat_swh_use_dict = {}
            service_water_heating_use_dict = {}

            for building_segment in find_all(
                "$.buildings[*].building_segments[*]", rmd_b
            ):
                #     get_swh_uses_associated_with_each_building_segment(
                # rmd_b, building_segment["id"]
                for swh_use_id in get_swh_uses_associated_with_each_building_segment(
                    rmd_b, building_segment["id"]
                ):
                    energy_required_to_heat_swh_use = (
                        get_energy_required_to_heat_swh_use(
                            swh_use_id, rmd_b, building_segment["id"]
                        )
                    )
                    energy_required_to_heat_swh_use_dict[swh_use_id][
                        building_segment["id"]
                    ] = energy_required_to_heat_swh_use
            return {
                "energy_required_to_heat_swh_use_dict": energy_required_to_heat_swh_use_dict
            }

        class BuildingRule(PartialRuleDefinition):
            def __init__(self):
                super(Section11Rule13.RMDRule.BuildingRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                )

            def get_calc_vals(self, context, data=None):
                building_b = context.BASELINE_0
                is_applicable = False
                for building_segment in find_all("$.building_segments[*]", building_b):
                    for swh_id in get_swh_uses_associated_with_each_building_segment(
                        rmd_b, building_segment["id"]
                    ):
                        return
