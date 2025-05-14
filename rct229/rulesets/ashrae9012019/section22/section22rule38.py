from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)


class PRM9012019Rule84g72(RuleDefinitionListIndexedBase):
    """Rule 38 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule84g72, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule84g72.RulesetModelInstanceRule(),
            index_rmd=BASELINE_0,
            id="22-38",
            description="Baseline chilled water loops that use purchased chilled water shall have a minimum flow setpoint of 25%.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.10 Chilled-Water Pumps (Systems 7, 8, 11, 12, and 13)",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
        )

    class RulesetModelInstanceRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule84g72.RulesetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                manual_check_required_msg="Manual Check Required - Baseline is modeled with purchased chilled water. Make sure "
                "baseline systems served by purchased chilled water are modeled with the purchased chilled water loop having "
                "a minimum flow setpoint of 25%.",
                not_applicable_msg="Rule 22-38 Not Applicable - the baseline is not modeled with Purchased Chilled Water",
            )

        def applicability_check(self, context, calc_vals, data):
            rmd_b = context.BASELINE_0
            purchased_chw_hhw_status_dict_p = check_purchased_chw_hhw_status_dict(rmd_b)
            return purchased_chw_hhw_status_dict_p["purchased_cooling"]
