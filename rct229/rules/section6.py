from numpy import sum
from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all

# Rule Definitions for Section 6 of 90.1-2019 Appendix G


# ------------------------


class Section6Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule1, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, False, True),
            each_rule=Section6Rule1.BuildingRule(),
            index_rmr="proposed",
            id="6-1",
            description="For the proposed building, each space has the same lighting power as the corresponding space in the U-RMR",
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section6Rule1.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, True),
                each_rule=Section6Rule1.BuildingRule.SpaceRule(),
                index_rmr="proposed",
                list_path="$..spaces[*]",  # All spaces inside the building
            )

        class SpaceRule(RuleDefinitionBase):
            def __init__(self):
                super(Section6Rule1.BuildingRule.SpaceRule, self,).__init__(
                    required_fields={
                        "$": ["interior_lighting", "floor_area"],
                        "interior_lighting[*]": ["power_per_area"],
                    },
                    rmrs_used=UserBaselineProposedVals(True, False, True),
                )

            def get_calc_vals(self, context, data=None):
                space_lighting_power_per_area_user = sum(
                    find_all("interior_lighting[*].power_per_area", context.user)
                )
                space_lighting_power_per_area_proposed = sum(
                    find_all("interior_lighting[*].power_per_area", context.proposed)
                )

                return {
                    "space_lighting_power_user": space_lighting_power_per_area_user
                    * context.user["floor_area"],
                    "space_lighting_power_proposed": space_lighting_power_per_area_proposed
                    * context.proposed["floor_area"],
                }

            def rule_check(self, context, calc_vals, data=None):
                return (
                    calc_vals["space_lighting_power_user"]
                    == calc_vals["space_lighting_power_proposed"]
                )


# ------------------------


class Section6Rule2(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule1, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            each_rule=Section6Rule1.BuildingRule(),
            index_rmr="proposed",
            id="6-2",
            description="The total building interior lighting power shall not exceed the interior lighting power allowance determined using either Table G3.7 or G3.8.",
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section6Rule2.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, False, True),
                each_rule=Section6Rule1.BuildingRule.BuildingSegmentRule(),
                index_rmr="proposed",
                rmr_context="building_segments",
            )

        class BuildingSegmentRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section6Rule2.BuildingRule.BuildingSegmentRule, self,).__init__(
                    required_fields={
                        "$": ["lighting_building_area_type"],
                    },
                    rmrs_used=UserBaselineProposedVals(False, False, True),
                    list_path="$..spaces[*]",  # All spaces inside the building segment
                )

            def create_data(self, context, data=None):
                # Pass this on to SpaceRule
                return {
                    "lighting_uses_building_area_method": building_segment_lighting_uses_building_area_method(
                        context.proposed
                    )
                }

        class SpaceRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    Section6Rule1.BuildingRule.BuildingSegmentRule.SpaceRule,
                    self,
                ).__init__(
                    required_fields={
                        "$": ["interior_lighting", "floor_area"],
                        "interior_lighting[*]": ["power_per_area"],
                    },
                    rmrs_used=UserBaselineProposedVals(True, False, True),
                )

            def get_calc_vals(self, context, data=None):
                space_lighting_power_per_area_user = sum(
                    find_all("interior_lighting[*].power_per_area", context.user)
                )
                space_lighting_power_per_area_proposed = sum(
                    find_all("interior_lighting[*].power_per_area", context.proposed)
                )

                return {
                    "space_lighting_power_user": space_lighting_power_per_area_user
                    * context.user["floor_area"],
                    "space_lighting_power_proposed": space_lighting_power_per_area_proposed
                    * context.proposed["floor_area"],
                }

            def rule_check(self, context, calc_vals, data=None):
                return (
                    calc_vals["space_lighting_power_user"]
                    == calc_vals["space_lighting_power_proposed"]
                )


# ------------------------


class Section6Rule11(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule11, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section6Rule11.BuildingRule(),
            index_rmr="proposed",
            id="6-11",
            description="Baseline building is not modeled with daylighting control",
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section6Rule11.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section6Rule11.BuildingRule.SpaceRule(),
                index_rmr="baseline",
                list_path="$..interior_lighting",  # All interior_lighting objects for the building
            )

        class InteriorLightingRule(RuleDefinitionBase):
            def __init__(self):
                super(Section6Rule11.BuildingRule.InteriorLightingRule, self,).__init__(
                    required_fields={
                        "$": ["has_daylighting_control"],
                    },
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                )

            def get_calc_vals(self, context, data=None):
                return {
                    "has_daylighting_control": context.baseline["has_daylight_control"]
                }

            def rule_check(self, context, calc_vals, data=None):
                return calc_vals["has_daylighting_control"] == False


# ------------------------
# ------------------------
