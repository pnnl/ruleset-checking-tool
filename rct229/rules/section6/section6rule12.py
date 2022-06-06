from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all

MSG_WARN_DAYLIGHT_NO_SCHEDULE = "Some of the spaces in zone are modeled with window or skylight and some of the spaces in zone are modeled with daylighting control directly through simulation. Verify if the mandatory lighting control requirements are modeled correctly in zone."
MSG_WARN_DAYLIGHT = "Some of the spaces in zone are modeled with window or skylight and some of the spaces in zone are modeled with daylighting control with schedule. Verify if schedule adjustment is modeled correctly."
MSG_WARN_NO_DAYLIGHT = "Some of the spaces in zone are modeled with fenestration but no daylighting controls. The design must include mandatory daylighting controls unless any of the exceptions to 90.1 section 9.4.1.1€ apply."


class Section6Rule12(RuleDefinitionListIndexedBase):
    """Rule 12 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule12, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            each_rule=Section6Rule12.BuildingRule(),
            index_rmr="proposed",
            id="6-12",
            description="User building is modeled with daylighting controls directly or through schedule adjustments.",
            rmr_context="ruleset_model_instances/0/buildings",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section6Rule12.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, False, True),
                each_rule=Section6Rule12.BuildingRule.ZoneRule(),
                index_rmr="proposed",
                list_path="$..zones[*]",
            )

        class ZoneRule(RuleDefinitionBase):
            def __init__(self):
                super(Section6Rule12.BuildingRule.ZoneRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, False, True),
                    required_fields={
                        "$": ["spaces", "surfaces"],
                        "$.spaces[*]": ["interior_lighting"],
                        "$.spaces[*].interior_lighting[*]": [
                            "daylighting_control_type",
                            "are_schedules_used_for_modeling_daylighting_control",
                        ],
                        "$.surfaces[*]": [
                            "adjacent_to",
                            "subsurfaces",
                        ],
                    },
                )

            def get_calc_vals(self, context, data=None):
                building_p = context.proposed

                daylight_flag_u = False
                has_daylight_control_flag = False
                for subsurface in find_all(
                    "$..surfaces[*].subsurfaces[?classification != 'DOOR']", building_p
                ):
                    daylight_flag_u = True

                interior_lighting_u = False
                for lighting in find_all("$..spaces[*].interior_lighting", building_p):
                    interior_lighting_u = lighting[0][
                        "are_schedules_used_for_modeling_daylighting_control"
                    ]
                    if lighting[0]["daylighting_control_type"] != "NONE":
                        has_daylight_control_flag = True

                return {
                    "daylight_flag_u": daylight_flag_u,
                    "has_daylight_control_flag": has_daylight_control_flag,
                    "interior_lighting_u": interior_lighting_u,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                daylight_flag_u = calc_vals["daylight_flag_u"]

                return daylight_flag_u

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                daylight_flag_u = calc_vals["daylight_flag_u"]
                has_daylight_control_flag = calc_vals["has_daylight_control_flag"]
                interior_lighting_u = calc_vals["interior_lighting_u"]

                if daylight_flag_u:
                    if has_daylight_control_flag:
                        if interior_lighting_u:
                            manual_check_msg = MSG_WARN_DAYLIGHT
                        else:
                            manual_check_msg = MSG_WARN_DAYLIGHT_NO_SCHEDULE
                    else:
                        manual_check_msg = MSG_WARN_NO_DAYLIGHT

                return manual_check_msg

            def rule_check(self, context, calc_vals, data=None):
                daylight_flag_u = calc_vals["daylight_flag_u"]
                has_daylight_control_flag = calc_vals["has_daylight_control_flag"]

                return not daylight_flag_u and not has_daylight_control_flag
