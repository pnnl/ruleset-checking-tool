from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)


class Section21Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 21 (HVAC - Water Side)"""

    def __init__(self):
        super(Section21Rule1, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=Section21Rule1.RulesetModelInstanceRule(),
            index_rmr=PROPOSED,
            id="21-1",
            description="For systems using purchased hot water or steam, the heating source shall be "
            "modeled as purchased hot water or steam in both the proposed design and "
            "baseline building design. If any system in the proposed design uses purchased "
            "hot water or steam, all baseline systems with hot water coils shall use the "
            "same type of purchased hot water or steam.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.1.3 Baseline HVAC System Requirements for Systems Utilizing Purchased "
            "Chilled Water and/or Purchased Heat",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
            manual_check_required_msg="Manual Check Required - Proposed is modeled with purchased hot water or steam.  "
            "Make sure the heating source in the baseline building is also purchased hot water or steam.",
            not_applicable_msg="Rule 21-1 Not Applicable - the proposed is not modeled with Purchased Hot Water or "
            "Steam",
        )

    class RulesetModelInstanceRule(PartialRuleDefinition):
        def __init__(self):
            super(Section21Rule1.RulesetModelInstanceRule, self,).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
            )

        def applicability_check(self, context, calc_vals, data):
            rmi_p = context.PROPOSED
            purchased_chw_hhw_status_dict_p = check_purchased_chw_hhw_status_dict(rmi_p)
            return purchased_chw_hhw_status_dict_p["purchased_heating"]
