from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import USER
from rct229.utils.jsonpath_utils import find_all


class Section12Rule3(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 12 (Receptacle)"""

    def __init__(self):
        super(Section12Rule3, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=True, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=Section12Rule3.BuildingRule(),
            index_rmr=USER,
            id="12-3",
            description="User RMR Space ID in Proposed RMR",
            ruleset_section_title="Receptacle",
            standard_section="Section Table G3.1-12 Receptacles: Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0/buildings",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section12Rule3.BuildingRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=True, BASELINE_0=False, PROPOSED=True
                ),
                each_rule=Section12Rule3.BuildingRule.SpaceRule(),
                index_rmr=USER,
                list_path="$..spaces[*]",  # All spaces in the buliding
            )

        def create_data(self, context, data):
            # Get the Proposed space id values
            return {"proposed_space_ids": find_all("$..spaces[*].id", context.PROPOSED)}

        class SpaceRule(RuleDefinitionBase):
            def __init__(self):
                super(Section12Rule3.BuildingRule.SpaceRule, self).__init__(
                    # No longer need the proposed RMR
                    rmrs_used=produce_ruleset_model_instance(
                        USER=True, BASELINE_0=False, PROPOSED=False
                    ),
                )

            def get_calc_vals(self, context, data=None):
                return {
                    "user_space_id": context.USER["id"],
                }

            def rule_check(self, context, calc_vals, data):
                return calc_vals["user_space_id"] in data["proposed_space_ids"]
