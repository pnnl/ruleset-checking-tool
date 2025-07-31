from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)


class PRM9012019Rule83m55(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 21 (HVAC - Water Side)"""

    def __init__(self):
        super(PRM9012019Rule83m55, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule83m55.RulesetModelInstanceRule(),
            index_rmd=PROPOSED,
            id="21-2",
            description="For purchased HW/steam in the proposed model, the baseline shall have the same number of "
            "pumps as proposed.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.1.3 Baseline HVAC System Requirements for Systems Utilizing Purchased "
            "Chilled Water and/or Purchased Heat",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
        )

    class RulesetModelInstanceRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule83m55.RulesetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                manual_check_required_msg="Manual Check Required - Proposed is modeled with purchased hot water or steam.  "
                "Make sure the baseline model uses the same number of pumps for the heating loop.",
                not_applicable_msg="Rule 21-2 Not Applicable - the proposed is not modeled with Purchased Hot Water or "
                "Steam",
            )

        def applicability_check(self, context, calc_vals, data):
            rmd_p = context.PROPOSED
            purchased_chw_hhw_status_dict_p = check_purchased_chw_hhw_status_dict(rmd_p)
            return purchased_chw_hhw_status_dict_p["purchased_heating"]
