from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all

MSG_WARN_DAYLIGHT_NO_SCHEDULE = "Some of the spaces in zone are modeled with window(s) and/or skylight(s) and have daylighting controls modeled explicitly in the simulation tool. Verify that the mandatory lighting control requirements are met."
MSG_WARN_DAYLIGHT = "Some of the spaces in zone are modeled with window(s) and/or skylight(s) and have daylighting controls modeled via schedule adjustment. Verify that the mandatory lighting control requirements are met, and that the supporting documentation is provided for the schedule adjustment."
MSG_WARN_NO_DAYLIGHT = "Some of the spaces in zone are modeled with fenestration but no daylighting controls. The design must include mandatory daylighting controls unless any of the exceptions to 90.1 section 9.4.1.1€ apply."

DAYLIGHT_CONTROL_TYPE = schema_enums["LightingDaylightingControlType"].NONE


class Section6Rule7(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule7, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            each_rule=Section6Rule7.ZoneRule(),
            index_rmr="proposed",
            id="6-7",
            description="Proposed building is modeled with daylighting controls directly or through schedule adjustments.",
            list_path="ruleset_model_instances[0].buildings[*].building_segments[*].zones[*]",
        )

    class ZoneRule(RuleDefinitionBase):
        def __init__(self):
            super(Section6Rule7.ZoneRule, self,).__init__(
                required_fields={"$": ["spaces", "surfaces"]},
                rmrs_used=UserBaselineProposedVals(False, False, True),
            )

        def get_calc_vals(self, context, data=None):
            zone_p = context.proposed

            daylight_flag_p = (
                len(
                    find_all(
                        "$..surfaces[?adjacent_to = 'EXTERIOR'].subsurfaces[?classification != 'DOOR']",
                        zone_p,
                    )
                )
                > 0
            )

            has_daylight_control_flag = False
            for lighting in find_all("$..interior_lighting[*]", zone_p):
                interior_lighting_p = getattr_(
                    lighting,
                    "interior_lighting",
                    "are_schedules_used_for_modeling_daylighting_control",
                )

                if lighting["daylighting_control_type"] != DAYLIGHT_CONTROL_TYPE:
                    has_daylight_control_flag = True

            return {
                "daylight_flag_p": daylight_flag_p,
                "has_daylight_control_flag": has_daylight_control_flag,
                "interior_lighting_p": interior_lighting_p,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            daylight_flag_p = calc_vals["daylight_flag_p"]
            has_daylight_control_flag = calc_vals["has_daylight_control_flag"]

            return daylight_flag_p and has_daylight_control_flag

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            daylight_flag_p = calc_vals["daylight_flag_p"]
            has_daylight_control_flag = calc_vals["has_daylight_control_flag"]
            interior_lighting_p = calc_vals["interior_lighting_p"]

            if daylight_flag_p and has_daylight_control_flag:
                if interior_lighting_p:
                    manual_check_msg = MSG_WARN_DAYLIGHT
                else:
                    manual_check_msg = MSG_WARN_DAYLIGHT_NO_SCHEDULE

            return manual_check_msg

        def rule_check(self, context, calc_vals, data=None):
            daylight_flag_p = calc_vals["daylight_flag_p"]
            has_daylight_control_flag = calc_vals["has_daylight_control_flag"]

            return not daylight_flag_p and not has_daylight_control_flag

        def get_fail_msg(self, context, calc_vals=None, data=None):
            daylight_flag_p = calc_vals["daylight_flag_p"]
            has_daylight_control_flag = calc_vals["has_daylight_control_flag"]

            return MSG_WARN_NO_DAYLIGHT if daylight_flag_p and not has_daylight_control_flag else ""
