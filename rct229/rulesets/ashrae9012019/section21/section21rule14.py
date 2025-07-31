from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)


class PRM9012019Rule29g28(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 21 (HVAC - Water Side)"""

    def __init__(self):
        super(PRM9012019Rule29g28, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule29g28.RulesetModelInstanceRule(),
            index_rmd=BASELINE_0,
            id="21-14",
            description="When the baseline building is modeled with a hot water plant, served by purchased HW "
            "system, hot water supply temperature reset is not modeled.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.1.3 Baseline HVAC System Requirements for Systems Utilizing Purchased "
            "Chilled Water and/or Purchased Heat",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
            manual_check_required_msg="Manual Check Required - Baseline is modeled with purchased hot water or steam.  "
            "Make sure that a hot water supply reset temperature is not modeled.",
            not_applicable_msg="Rule 21-14 Not Applicable - the baseline is not modeled with Purchased Hot Water or "
            "Steam",
        )

    class RulesetModelInstanceRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule29g28.RulesetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def applicability_check(self, context, calc_vals, data):
            rmd_b = context.BASELINE_0
            purchased_chw_hhw_status_dict_p = check_purchased_chw_hhw_status_dict(rmd_b)
            return purchased_chw_hhw_status_dict_p["purchased_heating"]
