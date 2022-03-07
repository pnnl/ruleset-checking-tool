from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all


class Section6Rule11(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule11, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section6Rule11.BuildingRule(),
            index_rmr="baseline",
            id="6-11",
            description="Baseline building is not modeled with daylighting control",
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section6Rule11.BuildingRule, self).__init__(
                required_fields={
                    "$": ["building_segments"],
                    "$.building_segments[*]": ["zones"],
                    "$.building_segments[*].zones[*]": ["spaces"],
                    "$.building_segments[*].zones[*].spaces[*]": ["interior_lighting"],
                    "$.building_segments[*].zones[*].spaces[*].interior_lighting[*]": [
                        "daylighting_control_type"
                    ],
                },
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def get_calc_vals(self, context, data=None):
            interior_lighting_instances_with_daylighting_control = find_all(
                "$..spaces[*].interior_lighting[?daylighting_control_type!='NONE']",
                context.baseline,
            )
            ids_for_interior_lighting_instances_with_daylighting_control = [
                instance["id"]
                for instance in interior_lighting_instances_with_daylighting_control
            ]

            return {
                "ids_for_interior_lighting_instances_with_daylighting_control": ids_for_interior_lighting_instances_with_daylighting_control
            }

        def rule_check(self, context, calc_vals, data=None):
            return (
                len(
                    calc_vals[
                        "ids_for_interior_lighting_instances_with_daylighting_control"
                    ]
                )
                == 0
            )
