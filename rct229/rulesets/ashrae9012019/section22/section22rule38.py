from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)


class Section22Rule38(PartialRuleDefinition):
    """Rule 38 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule38, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            id="22-38",
            description="Baseline systems served by purchased chilled water loop shall have a "
                        "minimum flow setpoint of 25%",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.10 Chilled-Water Pumps (Systems 7, 8, 11, 12, and 13)",
            is_primary_rule=False,
            rmr_context="ruleset_model_instances/0",
            manual_check_required_msg="Manual Check Required - Baseline is modeled with purchased chilled water.  Make sure " 
               "baseline systems served by purchased chilled water are modeled with the purchased chilled water loop having "
               "a minimum flow setpoint of 25%.",
            not_applicable_msg="Rule 22-38 Not Applicable - the baseline is not modeled with Purchased Chilled Water"
        )

    def applicability_check(self, context, calc_vals, data):
        rmi_b = context.baseline
        purchased_chw_hhw_status_dict_p = check_purchased_chw_hhw_status_dict(rmi_b)
        return purchased_chw_hhw_status_dict_p["purchased_cooling"]
