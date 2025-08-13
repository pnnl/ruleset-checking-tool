from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

MSG_WARN_DAYLIGHT_NO_SCHEDULE = "Some of the spaces in zone are modeled with window(s) and/or skylight(s) and have daylighting controls modeled explicitly in the simulation tool. Verify that the mandatory lighting control requirements are met."
MSG_WARN_DAYLIGHT = "Some of the spaces in zone are modeled with window(s) and/or skylight(s) and have daylighting controls modeled via schedule adjustment. Verify that the mandatory lighting control requirements are met, and that the supporting documentation is provided for the schedule adjustment."
MSG_WARN_NO_DAYLIGHT = "Some of the spaces in zone are modeled with fenestration but no daylighting controls. The design must include mandatory daylighting controls unless any of the exceptions to 90.1 section 9.4.1.1 apply."

DOOR = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"].DOOR
EXTERIOR = SchemaEnums.schema_enums["SurfaceAdjacencyOptions"].EXTERIOR
NONE = SchemaEnums.schema_enums["LightingDaylightingControlOptions"].NONE


class PRM9012019Rule66m62(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012019Rule66m62, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule66m62.ZoneRule(),
            index_rmd=PROPOSED,
            id="6-7",
            description="Proposed building is modeled with daylighting controls directly or through schedule adjustments.",
            ruleset_section_title="Lighting",
            standard_section="Section G3.1-6(h) Lighting: Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*].building_segments[*].zones[*]",
        )

    class ZoneRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule66m62.ZoneRule, self).__init__(
                required_fields={"$": ["spaces", "surfaces"]},
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
            )

        def get_calc_vals(self, context, data=None):
            zone_p = context.PROPOSED

            daylight_flag_p = (
                len(
                    find_all(
                        # Doors in a surface adjacent to exterior
                        f'$.surfaces[*][?(@.adjacent_to = "{EXTERIOR}")].subsurfaces[*][?(@.classification != "{DOOR}")]',
                        zone_p,
                    )
                )
                > 0
            )

            has_daylight_control_flag = (
                len(
                    find_all(
                        # interior_lighting instances with daylighting_control_type set to NONE
                        f'$.spaces[*].interior_lighting[*][?(@.daylighting_control_type!= "{NONE}")]',
                        zone_p,
                    )
                )
                > 0
            )

            daylight_schedule_adjustment_flag = any(
                find_all(
                    # interior_lighting instances with are_schedules_used_for_modeling_daylighting_control set to True
                    "$.spaces[*].interior_lighting[*][?(@.are_schedules_used_for_modeling_daylighting_control = true)]",
                    zone_p,
                )
            )

            return {
                "daylight_flag_p": daylight_flag_p,
                "has_daylight_control_flag": has_daylight_control_flag,
                "daylight_schedule_adjustment_flag": daylight_schedule_adjustment_flag,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            daylight_flag_p = calc_vals["daylight_flag_p"]
            has_daylight_control_flag = calc_vals["has_daylight_control_flag"]

            return daylight_flag_p and has_daylight_control_flag

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            daylight_schedule_adjustment_flag = calc_vals[
                "daylight_schedule_adjustment_flag"
            ]

            return (
                MSG_WARN_DAYLIGHT
                if daylight_schedule_adjustment_flag
                else MSG_WARN_DAYLIGHT_NO_SCHEDULE
            )

        def rule_check(self, context, calc_vals, data=None):
            daylight_flag_p = calc_vals["daylight_flag_p"]
            has_daylight_control_flag = calc_vals["has_daylight_control_flag"]

            return not daylight_flag_p and not has_daylight_control_flag

        def get_fail_msg(self, context, calc_vals=None, data=None):
            daylight_flag_p = calc_vals["daylight_flag_p"]
            has_daylight_control_flag = calc_vals["has_daylight_control_flag"]

            return (
                MSG_WARN_NO_DAYLIGHT
                if daylight_flag_p and not has_daylight_control_flag
                else ""
            )
