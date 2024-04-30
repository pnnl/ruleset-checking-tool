from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019.data_fns.extra_schema_fns import proposed_equals_user


class Section1Rule7(RuleDefinitionBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 1 (Performance Calculation)"""

    def __init__(self):
        super(Section1Rule7, self).__init__(
            rmds_used=produce_ruleset_model_instance(
                USER=True, BASELINE_0=False, PROPOSED=True
            ),
            id="1-7",
            description="",
            ruleset_section_title="Performance Calculation",
            standard_section="",
            is_primary_rule=True,
            rmd_context="",
        )

    def is_applicable(self, context, data=None):
        proposed = context.PROPOSED
        user = context.USER
        return proposed and user

    def get_calc_vals(self, context, data=None):
        proposed = context.PROPOSED
        user = context.USER
        error_msg_list = []

        comparison_result = proposed_equals_user(
            index_context=proposed,
            compare_context=user,
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
