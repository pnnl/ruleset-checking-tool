from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.utils.jsonpath_utils import find_all


class PRM9012019Rule02c29(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012019Rule02c29, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule02c29.BuildingRule(),
            index_rmd=BASELINE_0,
            id="6-6",
            description="Baseline building is not modeled with daylighting control",
            ruleset_section_title="Lighting",
            standard_section="Section G3.1-6 Modeling Requirements for the baseline building",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0/buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule02c29.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def get_calc_vals(self, context, data=None):
            building_p = context.BASELINE_0
            interior_lighting_instances_with_daylighting_control = find_all(
                f'$.building_segments[*].zones[*].spaces[*].interior_lighting[*][?(@.daylighting_control_type != "NONE")]',
                building_p,
            )
            ids_for_interior_lighting_instances_with_daylighting_control = [
                instance["id"]
                for instance in interior_lighting_instances_with_daylighting_control
            ]

            return {
                "ids_for_interior_lighting_instances_with_daylighting_control": ids_for_interior_lighting_instances_with_daylighting_control
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return (
                len(
                    calc_vals[
                        "ids_for_interior_lighting_instances_with_daylighting_control"
                    ]
                )
                == 0
            )
