from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.compare_schedules import (
    compare_schedules,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.is_space_a_computer_room import (
    is_space_a_computer_room,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import find_exactly_one_schedule

MISCELLANEOUS_EQUIPMENT = SchemaEnums.schema_enums["MiscellaneousEquipmentOptions"]

MONTH_FRACTIONS = {
    1: 0.25,
    2: 0.5,
    3: 0.75,
    4: 1,
    5: 0.25,
    6: 0.5,
    7: 0.75,
    8: 1,
    9: 0.25,
    10: 0.5,
    11: 0.75,
    12: 1,
}
DAYS_IN_MONTH = {
    1: 31,
    2: 28,  # If leap year, this will be replaced with 29
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


class Section12Rule4(RuleDefinitionListIndexedBase):
    """Rule 4 of ASHRAE 90.1-2019 Appendix G Section 12 (Receptacle)"""

    def __init__(self):
        super(Section12Rule4, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section12Rule4.RuleSetModelDescriptionRule(),
            index_rmd=BASELINE_0,
            id="12-4",
            description="Computer room equipment schedules shall be modeled as a constant fraction of the peak design load per the following monthly schedule: "
            "Months 1, 5, 9 — 25%; Months 2, 6, 10 — 50%; Months 3, 7, 11 — 75%; Months 4, 8, 12 — 100%",
            ruleset_section_title="Receptacle",
            standard_section="Section G3.1.3.16",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
            required_fields={"$": ["calendar"], "calendar": ["is_leap_year"]},
            data_items={"is_leap_year": (BASELINE_0, "calendar/is_leap_year")},
        )

    class RuleSetModelDescriptionRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section12Rule4.RuleSetModelDescriptionRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=Section12Rule4.RuleSetModelDescriptionRule.MiscEquipRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0

            for space_b in find_all(
                "$.buildings[*].building_segments[*].zones[*].spaces[*]", rmd_b
            ):
                if is_space_a_computer_room(rmd_b, space_b["id"]):
                    for misc_equip_b in space_b["miscellaneous_equipment"]:
                        if (
                            misc_equip_b.get("type")
                            != MISCELLANEOUS_EQUIPMENT.INFORMATION_TECHNOLOGY_EQUIPMENT
                        ):
                            return False
                        else:
                            return True

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0

            schedule_b = {
                mult_sch_b: find_exactly_one_schedule(rmd_b, mult_sch_b)[
                    "hourly_values"
                ]
                for mult_sch_b in find_all(
                    "$.buildings[*].building_segments[*].zones[*].spaces[*].miscellaneous_equipment[*].multiplier_schedule",
                    rmd_b,
                )
            }

            return {"schedule_b": schedule_b}

        class MiscEquipRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    Section12Rule4.RuleSetModelDescriptionRule.MiscEquipRule,
                    self,
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    required_fields={
                        "$": [
                            "multiplier_schedule",
                        ]
                    },
                )

            def get_calc_vals(self, context, data=None):
                misc_equip_b = context.BASELINE_0

                is_leap_year = data["is_leap_year"]
                schedule_b = data["schedule_b"]

                if is_leap_year:
                    DAYS_IN_MONTH[2] = 29

                hourly_multiplier_schedule_b = misc_equip_b["multiplier_schedule"]

                multiplier_schedule_b = schedule_b[hourly_multiplier_schedule_b]
                expected_hourly_values = []
                for month in range(1, 13):
                    expected_hourly_values.extend(
                        [MONTH_FRACTIONS[month]] * DAYS_IN_MONTH[month] * 24
                    )

                mask_schedule = [1] * 8784 if is_leap_year else [1] * 8760

                comparison_data = compare_schedules(
                    multiplier_schedule_b,
                    expected_hourly_values,
                    mask_schedule,
                    is_leap_year,
                )["total_hours_matched"]

                return {"comparison_data": comparison_data}

            def rule_check(self, context, calc_vals=None, data=None):
                comparison_data = calc_vals["comparison_data"]
                is_leap_year = data["is_leap_year"]

                return comparison_data == (8784 if is_leap_year else 8760)
