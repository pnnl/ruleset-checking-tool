from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019.data_fns.extra_schema_fns import (
    baseline_equals_baseline,
)


class PRM9012019Rule51z38(RuleDefinitionBase):
    """Rule 9 of ASHRAE 90.1-2019 Appendix G Section 1 (Performance Calculation)"""

    def __init__(self):
        super(PRM9012019Rule51z38, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False,
                BASELINE_0=True,
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
                PROPOSED=False,
            ),
            rmds_used_optional=produce_ruleset_model_description(
                BASELINE_90=True,
                BASELINE_180=True,
                BASELINE_270=True,
            ),
            id="1-9",
            description="All baseline models shall be identical for all data elements identified in the schema hosted at data.standards.ashrae {{https://github.com/open229/ruleset-model-description-schema/blob/main/docs229/ASHRAE229_extra.schema.json}}",
            ruleset_section_title="Performance Calculation",
            standard_section="Table G3.1(1) Proposed Building Performance (a)",
            is_primary_rule=True,
            rmd_context="",
        )

    def is_applicable(self, context, data=None):
        baseline_0 = context.BASELINE_0
        baseline_90 = context.BASELINE_90
        baseline_180 = context.BASELINE_180
        baseline_270 = context.BASELINE_270
        return all([baseline_0, baseline_90, baseline_180, baseline_270])

    def get_calc_vals(self, context, data=None):
        baseline_0 = context.BASELINE_0
        baseline_90 = context.BASELINE_90
        baseline_180 = context.BASELINE_180
        baseline_270 = context.BASELINE_270

        error_msg_list = []
        comparison_result = all(
            baseline_equals_baseline(
                index_context=baseline_0,
                compare_context=baseline,
                error_msg_list=error_msg_list,
            )
            for baseline in [baseline_90, baseline_180, baseline_270]
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
