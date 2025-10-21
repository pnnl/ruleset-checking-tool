from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012022 import BASELINE_0
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all

LIGHTING_SPACE = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
LIGHTING_OCCUPANCY_CONTROL = SchemaEnums.schema_enums["LightingOccupancyControlOptions"]
SPACE_FUNCTION = SchemaEnums.schema_enums["SpaceFunctionOptions"]
BUILDING_AREA_LIMIT = 5000 * ureg("ft2")


class PRM9012022Rule86d29(RuleDefinitionListIndexedBase):
    """Rule 13 of ASHRAE 90.1-2022 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012022Rule86d29, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012022Rule86d29.BuildingRule(),
            index_rmd=BASELINE_0,
            id="6-13",
            description="In buildings >5000 ft2 lighting shall be modeled having occupancy sensors in employee lunch and break rooms, conference/meeting rooms, and classrooms (not including shop classrooms, laboratory classrooms, and preschool through 12th grade classrooms). These controls shall be reflected in the baseline building design lighting schedules.",
            ruleset_section_title="Lighting",
            standard_section="Table G3.1 #6 Baseline column",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012022Rule86d29.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012022Rule86d29.BuildingRule.SpaceRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].zones[*].spaces[*]",
            )

        def is_applicable(self, context, data=None):
            building_b = context.BASELINE_0

            building_area_b = sum(
                find_all(
                    "$.building_segments[*].zones[*].spaces[*].floor_area",
                    building_b,
                )
            )

            return building_area_b > BUILDING_AREA_LIMIT

        def list_filter(self, context_item, data):
            space_b = context_item.BASELINE_0

            return space_b.get("interior_lighting")

        class SpaceRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012022Rule86d29.BuildingRule.SpaceRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    required_fields={"$": ["lighting_space_type"]},
                )

            def is_applicable(self, context, data=None):
                space_b = context.BASELINE_0
                lighting_space_type_b = space_b["lighting_space_type"]
                space_function_b = space_b.get("function")

                return lighting_space_type_b in (
                    LIGHTING_SPACE.LOUNGE_BREAKROOM_ALL_OTHERS,
                    LIGHTING_SPACE.CONFERENCE_MEETING_MULTIPURPOSE_ROOM,
                    LIGHTING_SPACE.CLASSROOM_LECTURE_HALL_TRAINING_ROOM_PENITENTIARY,
                    LIGHTING_SPACE.CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER,
                    LIGHTING_SPACE.LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM,
                ) or (
                    space_function_b == SPACE_FUNCTION.LABORATORY
                    and lighting_space_type_b
                    == LIGHTING_SPACE.CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL
                )

            def get_calc_vals(self, context, data=None):
                space_b = context.BASELINE_0

                occupancy_sensor_controls_b = [
                    getattr_(
                        interior_lighting_b,
                        "interior_lighting",
                        "occupancy_control_type",
                    )
                    for interior_lighting_b in space_b["interior_lighting"]
                ]
                occupancy_sensor_schedules_b = [
                    getattr_(
                        interior_lighting_b,
                        "interior_lighting",
                        "are_schedules_used_for_modeling_occupancy_control",
                    )
                    for interior_lighting_b in space_b["interior_lighting"]
                ]

                return {
                    "occupancy_sensor_controls_b": occupancy_sensor_controls_b,
                    "occupancy_sensor_schedules_b": occupancy_sensor_schedules_b,
                }

            def rule_check(self, context, calc_vals=None, data=None):
                occupancy_sensor_controls_b = calc_vals["occupancy_sensor_controls_b"]
                occupancy_sensor_schedules_b = calc_vals["occupancy_sensor_schedules_b"]

                return not any(
                    val
                    in [
                        LIGHTING_OCCUPANCY_CONTROL.NONE,
                        LIGHTING_OCCUPANCY_CONTROL.MANUAL_ON,
                        None,
                    ]
                    for val in occupancy_sensor_controls_b
                ) and all(occupancy_sensor_schedules_b)
