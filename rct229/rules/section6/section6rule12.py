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

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section6Rule12.BuildingRule, self).__init__(
                required_fields={
                    "$": ["building_segments"],
                    "$.building_segments[*]": ["zones"],
                    "$.building_segments[*].zones[*]": ["surfaces"],
                    "$.building_segments[*].zones[*].surfaces[*]": ["adjacent_to", "subsurfaces"],
                    "$.building_segments[*].zones[*].spaces[*]": ["interior_lighting"],
                    "$.building_segments[*].zones[*].spaces[*].interior_lighting[*]": [
                        "daylighting_control_type"
                    ],
                },
                rmrs_used=UserBaselineProposedVals(False, False, True),
            )

        def get_calc_vals(self, context, data=None):
            building_p = context.proposed

            daylight_flag_u = False
            has_daylight_control_flag = False
            for subsurface in find_all("$..surfaces[*].subsurfaces[?classification != 'DOOR']", building_p):
                daylight_flag_u = True

            for lighting in find_all("$..spaces[*].interior_lighting[?daylighting_control_type != 'NONE']", building_p):
                has_daylight_control_flag = True

            interior_lighting_u = False

            # Question
            # 1. 'interior_lighting_u = space_u.interior_lighting'?? something's missing, should be True or False
            # 2, in the json file, there is no subsurfaces for case a

            return {
                "daylight_flag_u": daylight_flag_u,
                "has_daylight_control_flag":has_daylight_control_flag,
                "interior_lighting_u": interior_lighting_u,
            }

        def rule_check(self, context, calc_vals, data=None):
            daylight_flag_u = calc_vals["daylight_flag_u"]
            has_daylight_control_flag = calc_vals["has_daylight_control_flag"]

            return (not (daylight_flag_u and not has_daylight_control_flag) or
                    not (not daylight_flag_u and has_daylight_control_flag)
                    )

        def manual_check_required(self, context, calc_vals=None, data=None):
            daylight_flag_u = calc_vals["daylight_flag_u"]
            has_daylight_control_flag = calc_vals["has_daylight_control_flag"]

            return (daylight_flag_u and has_daylight_control_flag)


        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            daylight_flag_u = calc_vals["daylight_flag_u"]
            has_daylight_control_flag = calc_vals["has_daylight_control_flag"]
            inteior = True # calc_vals["interior_lighting_u"]

            if daylight_flag_u:
                if has_daylight_control_flag:
                    if not inteior:
                        manual_check_msg = MSG_WARN_DAYLIGHT_NO_SCHEDULE
                    else:
                        manual_check_msg = MSG_WARN_DAYLIGHT
                else:
                    manual_check_msg = MSG_WARN_NO_DAYLIGHT

            return manual_check_msg


