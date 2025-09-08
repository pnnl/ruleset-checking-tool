from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.compare_schedules import (
    compare_schedules,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import find_exactly_one_schedule

LIGHTING_SPACE = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]

EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES = [
    LIGHTING_SPACE.OFFICE_ENCLOSED,
    LIGHTING_SPACE.CONFERENCE_MEETING_MULTIPURPOSE_ROOM,
    LIGHTING_SPACE.COPY_PRINT_ROOM,
    LIGHTING_SPACE.LOUNGE_BREAKROOM_HEALTH_CARE_FACILITY,
    LIGHTING_SPACE.LOUNGE_BREAKROOM_ALL_OTHERS,
    LIGHTING_SPACE.CLASSROOM_LECTURE_HALL_TRAINING_ROOM_PENITENTIARY,
    LIGHTING_SPACE.CLASSROOM_LECTURE_HALL_TRAINING_ROOM_SCHOOL,
    LIGHTING_SPACE.CLASSROOM_LECTURE_HALL_TRAINING_ROOM_ALL_OTHER,
    LIGHTING_SPACE.OFFICE_OPEN_PLAN,
]


class PRM9012019Rule79w60(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 12 (Receptacle)"""

    def __init__(self):
        super(PRM9012019Rule79w60, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule79w60.RuleSetModelDescriptionRule(),
            index_rmd=PROPOSED,
            id="12-3",
            description="When receptacle controls are specified in the proposed building design for spaces where not required by Standard 90.1 2019 Section 8.4.2, "
            "the hourly receptacle schedule shall be reduced as specified in Standard 90.1-2019 Table G3.1 Section 12 Proposed Building Performance column.",
            ruleset_section_title="Receptacle",
            standard_section="Table G3.1-12 Proposed Building Performance column",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RuleSetModelDescriptionRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule79w60.RuleSetModelDescriptionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule79w60.RuleSetModelDescriptionRule.SpaceRule(),
                index_rmd=PROPOSED,
                list_path="$.buildings[*].building_segments[*].zones[*].spaces[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_p = context.PROPOSED

            spaces_with_receptacle_controls_beyond_req = []
            for space_p in find_all(
                "$.buildings[*].building_segments[*].zones[*].spaces[*]",
                rmd_p,
            ):
                lighting_space_type_p = getattr_(
                    space_p, "spaces", "lighting_space_type"
                )
                if lighting_space_type_p not in EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES:
                    for misc_equip_p in find_all(
                        "$.miscellaneous_equipment[*]", space_p
                    ):
                        automatic_controlled_percentage_p = misc_equip_p.get(
                            "automatic_controlled_percentage"
                        )
                        auto_receptacle_control_p = (
                            automatic_controlled_percentage_p
                            and automatic_controlled_percentage_p > 0.0
                        )
                        if auto_receptacle_control_p:
                            spaces_with_receptacle_controls_beyond_req.append(
                                misc_equip_p["id"]
                            )

            return spaces_with_receptacle_controls_beyond_req

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            schedule_b = {
                mult_sch_b: find_exactly_one_schedule(rmd_b, mult_sch_b)[
                    "hourly_values"
                ]
                for mult_sch_b in find_all(
                    "$.buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*].multiplier_schedule",
                    rmd_b,
                )
            }
            schedule_p = {
                mult_sch_p: find_exactly_one_schedule(rmd_p, mult_sch_p)[
                    "hourly_values"
                ]
                for mult_sch_p in find_all(
                    "$.buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*].multiplier_schedule",
                    rmd_p,
                )
            }

            return {
                "schedule_b": schedule_b,
                "schedule_p": schedule_p,
            }

        def list_filter(self, context_item, data):
            space_p = context_item.PROPOSED
            lighting_space_type_p = getattr_(space_p, "spaces", "lighting_space_type")
            return lighting_space_type_p not in EXPECTED_RECEPTACLE_CONTROL_SPACE_TYPES

        class SpaceRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    PRM9012019Rule79w60.RuleSetModelDescriptionRule.SpaceRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    each_rule=PRM9012019Rule79w60.RuleSetModelDescriptionRule.SpaceRule.MiscEquipRule(),
                    index_rmd=PROPOSED,
                    list_path="$.miscellaneous_equipment[*]",
                )

            def create_data(self, context, data):
                space_p = context.PROPOSED

                return {"space_type_p": space_p["lighting_space_type"]}

            class MiscEquipRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        PRM9012019Rule79w60.RuleSetModelDescriptionRule.SpaceRule.MiscEquipRule,
                        self,
                    ).__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=True
                        ),
                        required_fields={
                            "$": [
                                "multiplier_schedule",
                            ]
                        },
                        manual_check_required_msg="Credit for automatic receptacle controls was expected, but baseline and proposed miscellaneous equipment schedules are identical.",
                    )

                def is_applicable(self, context, data=None):
                    misc_equip_p = context.PROPOSED
                    automatic_controlled_percentage_p = misc_equip_p.get(
                        "automatic_controlled_percentage"
                    )
                    auto_receptacle_control_p = (
                        automatic_controlled_percentage_p
                        and automatic_controlled_percentage_p > 0.0
                    )
                    return auto_receptacle_control_p

                def get_not_applicable_msg(self, context, data=None):
                    misc_equip_p = context.PROPOSED
                    space_type_p = data["space_type_p"]
                    return f"Misc equipment {misc_equip_p['id']} is in a {space_type_p} space but it does not has automatic control."

                def get_calc_vals(self, context, data=None):
                    misc_equip_b = context.BASELINE_0
                    misc_equip_p = context.PROPOSED

                    space_type_p = data["space_type_p"]
                    schedule_b = data["schedule_b"]
                    schedule_p = data["schedule_p"]

                    expected_receptacle_power_credit = 0.1 * getattr_(
                        misc_equip_p,
                        "miscellaneous_equipment",
                        "automatic_controlled_percentage",
                    )

                    hourly_multiplier_schedule_b = misc_equip_b["multiplier_schedule"]
                    hourly_multiplier_schedule_p = misc_equip_p["multiplier_schedule"]

                    expected_hourly_values = [
                        hour_value * (1 - expected_receptacle_power_credit)
                        for hour_value in schedule_b[hourly_multiplier_schedule_b]
                    ]

                    mask_schedule = [1] * len(schedule_b["Plug Load Schedule"])
                    credit_comparison_data = compare_schedules(
                        expected_hourly_values,
                        schedule_p[hourly_multiplier_schedule_p],
                        mask_schedule,
                    )["total_hours_matched"]

                    no_credit_comparison_data = compare_schedules(
                        schedule_b[hourly_multiplier_schedule_b],
                        schedule_p[hourly_multiplier_schedule_p],
                        mask_schedule,
                    )["total_hours_matched"]

                    return {
                        "expected_hourly_values_len": len(expected_hourly_values),
                        "credit_comparison_total_hours_matched": credit_comparison_data,
                        "no_credit_comparison_total_hours_matched": no_credit_comparison_data,
                        "hourly_multiplier_schedule_len_b": len(
                            schedule_b[hourly_multiplier_schedule_b]
                        ),
                        "hourly_multiplier_schedule_len_p": len(
                            schedule_p[hourly_multiplier_schedule_p]
                        ),
                    }

                def manual_check_required(self, context, calc_vals=None, data=None):
                    no_credit_comparison_total_hours_matched = calc_vals[
                        "no_credit_comparison_total_hours_matched"
                    ]
                    hourly_multiplier_schedule_len_b = calc_vals[
                        "hourly_multiplier_schedule_len_b"
                    ]
                    hourly_multiplier_schedule_len_p = calc_vals[
                        "hourly_multiplier_schedule_len_p"
                    ]

                    return (
                        no_credit_comparison_total_hours_matched
                        == hourly_multiplier_schedule_len_b
                        == hourly_multiplier_schedule_len_p
                    )

                def rule_check(self, context, calc_vals=None, data=None):
                    expected_hourly_values_len = calc_vals["expected_hourly_values_len"]
                    credit_comparison_total_hours_matched = calc_vals[
                        "credit_comparison_total_hours_matched"
                    ]
                    hourly_multiplier_schedule_len_p = calc_vals[
                        "hourly_multiplier_schedule_len_p"
                    ]

                    return (
                        credit_comparison_total_hours_matched
                        == hourly_multiplier_schedule_len_p
                        == expected_hourly_values_len
                    )
