from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.utils.jsonpath_utils import (
    find_all,
)


class Section11Rule6(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule6, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section11Rule6.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-6",
            description="Piping losses shall not be modeled.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, i",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section11Rule6.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=Section11Rule6.RMDRule.SWHDistRule(),
                index_rmd=BASELINE_0,
                list_path="$.service_water_heating_distribution_systems[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0

            swh_dist_sys_b = find_all(
                "$.service_water_heating_distribution_systems[*]", rmd_b
            )

            return swh_dist_sys_b

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0

            bldg_segment_ids = find_all("$.buildings[*].building_segments[*].id", rmd_b)

            for bldg_segment_id in bldg_segment_ids:
                swh_distribution_and_eq_list_b = (
                    get_swh_uses_associated_with_each_building_segment(
                        rmd_b, bldg_segment_id
                    )
                )

            return {"swh_distribution_and_eq_list_b": swh_distribution_and_eq_list_b}

        def list_filter(self, context, data=None):
            swh_dist_sys_b = context.BASELINE_0
            swh_distribution_and_eq_list_b = data["swh_distribution_and_eq_list_b"]

            return swh_dist_sys_b["id"] in swh_distribution_and_eq_list_b

        class SWHDistRule(RuleDefinitionBase):
            def __init__(self):
                super(Section11Rule6.RMDRule.SWHDistRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False,
                        BASELINE_0=True,
                        PROPOSED=False,
                    ),
                    required_fields={
                        "$": ["service_water_piping"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                swh_dist_sys_b = context.BASELINE_0

                piping_losses_modeled_b = [
                    service_water_piping.get("are_thermal_losses_modeled")
                    for service_water_piping in swh_dist_sys_b["service_water_piping"]
                ]

                return {"piping_losses_modeled_b": piping_losses_modeled_b}

            def rule_check(self, context, calc_vals=None, data=None):
                piping_losses_modeled_b = calc_vals["piping_losses_modeled_b"]

                return not any(piping_losses_modeled_b)