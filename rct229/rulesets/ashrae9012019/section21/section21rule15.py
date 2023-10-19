from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)


class Section21Rule15(RuleDefinitionListIndexedBase):
    """Rule 15 of ASHRAE 90.1-2019 Appendix G Section 21 (HVAC - Water Side)"""

    def __init__(self):
        super(Section21Rule15, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section21Rule15.RulesetModelInstanceRule(),
            index_rmr=BASELINE_0,
            id="21-15",
            description="When the baseline building is modeled with a hot water plant, served by purchased HW "
            "system, the hot water pump power shall be 14 W/gpm.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.1.3 Baseline HVAC System Requirements for Systems Utilizing Purchased "
            "Chilled Water and/or Purchased Heat",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
            manual_check_required_msg="Manual Check Required - Baseline is modeled with purchased hot water or steam.  "
            "Make sure that that the hot water pump power is 14 W/gpm.",
            not_applicable_msg="Rule 21-15 Not Applicable - the baseline is not modeled with Purchased Hot Water "
            "or Steam",
        )

    class RulesetModelInstanceRule(PartialRuleDefinition):
        def __init__(self):
            super(Section21Rule15.RulesetModelInstanceRule, self,).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def applicability_check(self, context, calc_vals, data):
            rmi_b = context.BASELINE_0
            purchased_chw_hhw_status_dict_p = check_purchased_chw_hhw_status_dict(rmi_b)
            return purchased_chw_hhw_status_dict_p["purchased_heating"]
