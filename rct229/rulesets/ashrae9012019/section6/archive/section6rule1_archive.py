from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.utils.jsonpath_utils import find_all


class Section6Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule1, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=Section6Rule1.BuildingRule(),
            index_rmd=PROPOSED,
            id="6-1",
            description="For the proposed building, each space has the same lighting power as the corresponding space in the U-RMD",
            rmd_context="ruleset_model_descriptions/0/buildings",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section6Rule1.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=True, BASELINE_0=False, PROPOSED=True
                ),
                each_rule=Section6Rule1.BuildingRule.SpaceRule(),
                index_rmd=PROPOSED,
                list_path="$..spaces[*]",  # All spaces inside the building
            )

        class SpaceRule(RuleDefinitionBase):
            def __init__(self):
                super(Section6Rule1.BuildingRule.SpaceRule, self,).__init__(
                    required_fields={
                        "$": ["interior_lighting", "floor_area"],
                        "interior_lighting[*]": ["power_per_area"],
                    },
                    rmds_used=produce_ruleset_model_description(
                        USER=True, BASELINE_0=False, PROPOSED=True
                    ),
                )

            def get_calc_vals(self, context, data=None):
                space_lighting_power_per_area_user = sum(
                    find_all("$.interior_lighting[*].power_per_area", context.USER)
                )
                space_lighting_power_per_area_proposed = sum(
                    find_all("$.interior_lighting[*].power_per_area", context.PROPOSED)
                )
                space_lighting_power_user = (
                    space_lighting_power_per_area_user * context.USER["floor_area"]
                )

                return {
                    "space_lighting_power_user": space_lighting_power_per_area_user
                    * context.USER["floor_area"],
                    "space_lighting_power_proposed": space_lighting_power_per_area_proposed
                    * context.PROPOSED["floor_area"],
                }

            def rule_check(self, context, calc_vals, data=None):
                return (
                    calc_vals["space_lighting_power_user"]
                    == calc_vals["space_lighting_power_proposed"]
                )
