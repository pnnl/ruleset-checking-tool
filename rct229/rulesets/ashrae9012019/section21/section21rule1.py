from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.check_purchased_chw_hhw_status_dict import (
    check_purchased_chw_hhw_status_dict,
)


class PRM9012019Rule34f57(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 21 (HVAC - Water Side)"""

    def __init__(self):
        super(PRM9012019Rule34f57, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule34f57.RulesetModelInstanceRule(),
            index_rmd=PROPOSED,
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
        )

    class RulesetModelInstanceRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule34f57.RulesetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                manual_check_required_msg="Manual Check Required - Proposed is modeled with purchased hot water or steam.  "
                "Make sure the heating source in the baseline building is also purchased hot water or steam.",
                not_applicable_msg="Rule 21-1 Not Applicable - the proposed is not modeled with Purchased Hot Water or "
                "Steam",
            )

        def applicability_check(self, context, calc_vals, data):
            rmd_p = context.PROPOSED
            purchased_chw_hhw_status_dict_p = check_purchased_chw_hhw_status_dict(rmd_p)
            return purchased_chw_hhw_status_dict_p["purchased_heating"]
