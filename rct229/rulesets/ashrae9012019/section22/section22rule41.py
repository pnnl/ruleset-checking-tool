from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)


class PRM9012019Rule68r93(PartialRuleDefinition):
    """Rule 41 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule68r93, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            id="22-41",
            description="Baseline chilled water systems that use purchased chilled water shall be modeled with a single chilled water loop.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section 22 CHW&CW Loop",
            is_primary_rule=False,
            rmd_context="ruleset_model_descriptions/0",
            manual_check_required_msg="B-RMD SHOULD BE MODELED WITH PURCHASED CHILLED WATER. VERIFY THAT THERE IS ONLY ONE PURCHASED CHILLED WATER LOOP IN THE BASELINE MODEL.",
        )

    def applicability_check(self, context, calc_vals, data):
        rmd_b = context.BASELINE_0
        purchased_chw_hhw_status_dict_b = check_purchased_chw_hhw_status_dict(rmd_b)

        return purchased_chw_hhw_status_dict_b["purchased_cooling"]
