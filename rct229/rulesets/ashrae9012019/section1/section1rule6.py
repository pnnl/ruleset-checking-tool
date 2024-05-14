from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019.data_fns.extra_schema_fns import (
    baseline_equals_proposed,
)


class Section1Rule6(RuleDefinitionBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 1 (Performance Calculation)"""

    def __init__(self):
        super(Section1Rule6, self).__init__(
            rmds_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            id="1-6",
            description="temp",
            ruleset_section_title="Performance Calculation",
            standard_section="a",
            is_primary_rule=True,
            rmd_context="",
        )

    def is_applicable(self, context, data=None):
        proposed = context.PROPOSED
        baseline = context.BASELINE_0
        return proposed and baseline

    def get_calc_vals(self, context, data=None):
        proposed = context.PROPOSED
        baseline = context.BASELINE_0
        error_msg_list = []

        comparison_result = baseline_equals_proposed(
            index_context=baseline,
            compare_context=proposed,
            error_msg_list=error_msg_list,
        )

        return {
            "comparison_result": comparison_result,
            "error_msg_list": error_msg_list,
        }

    def rule_check(self, context, calc_vals=None, data=None):
        result = calc_vals["comparison_result"]
        return result

    def get_fail_msg(self, context, calc_vals=None, data=None):
        return calc_vals["error_msg_list"]
