from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_bats_and_swh_use import (
    get_swh_bats_and_swh_use,
)
from rct229.utils.utility_functions import find_exactly_one_service_water_heating_use


class Section11Rule9(RuleDefinitionListIndexedBase):
    """Rule 9 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule9, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section11Rule9.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-9",
            description="The baseline system must be sized according to Standard 90.1 2019, Section 7.4.1.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, a",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(PartialRuleDefinition):
        def __init__(self):
            super(Section11Rule9.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=True,
                    BASELINE_0=True,
                    PROPOSED=False,
                ),
            )

        def applicability_check(self, context, calc_vals, data):
            rmd_u = context.USER
            rmd_b = context.BASELINE_0

            shw_bat_uses_dict_u = get_swh_bats_and_swh_use(rmd_u)

            return not all(
                find_exactly_one_service_water_heating_use(rmd_b, swh_use_id).get(
                    "use", 0.0
                )
                > 0.0
                for swh_bat_u in shw_bat_uses_dict_u
                for swh_use_id in shw_bat_uses_dict_u[swh_bat_u]
            )

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            rmd_u = context.USER
            rmd_b = context.BASELINE_0

            shw_bat_uses_dict_u = get_swh_bats_and_swh_use(rmd_u)

            swh_bat = ", ".join(
                swh_bat_u
                for swh_bat_u in shw_bat_uses_dict_u
                for swh_use_id in shw_bat_uses_dict_u[swh_bat_u]
                if find_exactly_one_service_water_heating_use(rmd_b, swh_use_id).get(
                    "use", 0.0
                )
                == 0.0
            )

            return f"Check that the baseline Service Water Heating System for Building Area Type {swh_bat} is sized according to ASHRAE Standard 90.1 2019, Section 7.4.1."
