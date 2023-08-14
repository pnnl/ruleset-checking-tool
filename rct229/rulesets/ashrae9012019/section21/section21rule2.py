from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)


class Section21Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 21 (HVAC - Water Side)"""

    def __init__(self):
        super(Section21Rule2, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            each_rule=Section21Rule2.RulesetModelInstanceRule(),
            index_rmr="proposed",
            id="21-2",
            description="For purchased HW/steam in the proposed model, the baseline shall have the same number of "
            "pumps as proposed.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.1.3 Baseline HVAC System Requirements for Systems Utilizing Purchased "
            "Chilled Water and/or Purchased Heat",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
            manual_check_required_msg="Manual Check Required - Proposed is modeled with purchased hot water or steam.  "
            "Make sure the baseline model uses the same number of pumps for the heating loop.",
            not_applicable_msg="Rule 21-1 Not Applicable - the proposed is not modeled with Purchased Hot Water or "
            "Steam",
        )

    class RulesetModelInstanceRule(PartialRuleDefinition):
        def __init__(self):
            super(
                Section21Rule2.RulesetModelInstanceRule,
                self,
            ).__init__(
                rmrs_used=UserBaselineProposedVals(False, False, True),
            )

        def applicability_check(self, context, calc_vals, data):
            rmi_p = context.proposed
            purchased_chw_hhw_status_dict_p = check_purchased_chw_hhw_status_dict(rmi_p)
            return purchased_chw_hhw_status_dict_p["purchased_heating"]
