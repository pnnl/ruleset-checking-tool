from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)


class Section22Rule39(RuleDefinitionListIndexedBase):
    """Rule 39 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule39, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule39.RulesetModelInstanceRule(),
            index_rmr="baseline",
            id="22-39",
            description="Baseline systems served by purchased chilled water loop shall be modeled "
            "with a distribution pump whose pump power is 16W/gpm",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.10 Chilled-Water Pumps (Systems 7, 8, 11, 12, and 13)",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
            manual_check_required_msg="Manual Check Required - Baseline is modeled with purchased chilled water.  Make sure "
            "baseline systems served by purchased chilled water are modeled with a distribution pump whose pump ower is 16W/gpm.",
            not_applicable_msg="Rule 22-39 Not Applicable - the baseline is not modeled with Purchased Chilled Water",
        )

    class RulesetModelInstanceRule(PartialRuleDefinition):
        def __init__(self):
            super(Section22Rule39.RulesetModelInstanceRule, self,).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def applicability_check(self, context, calc_vals, data):
            rmi_b = context.baseline
            purchased_chw_hhw_status_dict_p = check_purchased_chw_hhw_status_dict(rmi_b)
            return purchased_chw_hhw_status_dict_p["purchased_cooling"]
