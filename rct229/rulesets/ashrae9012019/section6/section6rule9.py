from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.compare_schedules import (
    compare_schedules,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.normalize_interior_lighting_schedules import (
    normalize_interior_lighting_schedules,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value
from rct229.utils.pint_utils import ZERO

FLOOR_AREA_LIMIT = 5000 * ureg("ft2")  # square foot


class Section6Rule9(RuleDefinitionListIndexedBase):
    """Rule 9 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule9, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section6Rule9.RulesetModelInstanceRule(),
            index_rmr="proposed",
            id="6-9",
            description="Proposed building is modeled with other programmable lighting controls through a 10% "
            "schedule reduction in buildings less than 5,000sq.ft.",
            ruleset_section_title="Lighting",
            standard_section="Section G3.1-6(i) Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
            required_fields={"$": ["calendar"], "calendar": ["is_leap_year"]},
            data_items={"is_leap_year": ("proposed", "calendar/is_leap_year")},
        )

    class RulesetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section6Rule9.RulesetModelInstanceRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                each_rule=Section6Rule9.RulesetModelInstanceRule.BuildingRule(),
                index_rmr="proposed",
                list_path="buildings[*]",
                required_fields={"$": ["schedules"]},
                data_items={
                    "schedules_b": ("baseline", "schedules"),
                    "schedules_p": ("proposed", "schedules"),
                },
            )

        class BuildingRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    Section6Rule9.RulesetModelInstanceRule.BuildingRule, self
                ).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    each_rule=Section6Rule9.RulesetModelInstanceRule.BuildingRule.ZoneRule(),
                    index_rmr="proposed",
                    list_path="$..zones[*]",
                )

            def is_applicable(self, context, data=None):
                building_p = context.proposed
                return (
                    sum(find_all("spaces[*].floor_area", building_p), ZERO.AREA)
                    <= FLOOR_AREA_LIMIT
                )

            def create_data(self, context, data=None):
                building_p = context.proposed
                schedules_p = data["schedules_p"]
                return {
                    "building_open_schedule_p": getattr_(
                        find_exactly_one_with_field_value(
                            "$[*]",
                            "id",
                            building_p["building_open_schedule"],
                            schedules_p,
                        ),
                        "schedule",
                        "hourly_values",
                    ),
                }

            class ZoneRule(RuleDefinitionListIndexedBase):
                def __init__(self):
                    super(
                        Section6Rule9.RulesetModelInstanceRule.BuildingRule.ZoneRule,
                        self,
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, True),
                        each_rule=Section6Rule9.RulesetModelInstanceRule.BuildingRule.ZoneRule.SpaceRule(),
                        index_rmr="proposed",
                        list_path="spaces[*]",
                    )

                def create_data(self, context, data=None):
                    zone_p = context.proposed
                    return {
                        "avg_space_height": zone_p.get("volume", ZERO.VOLUME)
                        / sum(find_all("spaces[*].floor_area", zone_p), ZERO.AREA),
                    }

                class SpaceRule(RuleDefinitionBase):
                    def __init__(self):
                        super(
                            Section6Rule9.RulesetModelInstanceRule.BuildingRule.ZoneRule.SpaceRule,
                            self,
                        ).__init__(
                            rmrs_used=UserBaselineProposedVals(False, True, True)
                        )

                    def get_calc_vals(self, context, data=None):
                        space_p = context.proposed
                        space_b = context.baseline
                        avg_space_height = data["avg_space_height"]
                        schedules_b = data["schedules_b"]
                        schedules_p = data["schedules_p"]
                        building_open_schedule_p = data["building_open_schedule_p"]
                        is_leap_year = data["is_leap_year"]

                        normalized_schedule_b = normalize_interior_lighting_schedules(
                            space_b,
                            avg_space_height,
                            schedules_b,
                            adjust_for_credit=False,
                        )
                        normalized_schedule_p = normalize_interior_lighting_schedules(
                            space_p,
                            avg_space_height,
                            schedules_p,
                            adjust_for_credit=True,
                        )
                        schedule_comparison_result_dictionary = compare_schedules(
                            normalized_schedule_p,
                            normalized_schedule_b,
                            building_open_schedule_p,
                            is_leap_year=is_leap_year,
                        )
                        daylight_control = any(
                            find_all(
                                "interior_lighting[*].are_schedules_used_for_modeling_daylighting_control",
                                space_p,
                            )
                        )

                        return {
                            "daylight_control": daylight_control,
                            "total_hours_compared": schedule_comparison_result_dictionary[
                                "total_hours_compared"
                            ],
                            "total_hours_matched": schedule_comparison_result_dictionary[
                                "total_hours_matched"
                            ],
                            "eflh_difference": schedule_comparison_result_dictionary[
                                "eflh_difference"
                            ],
                        }

                    def manual_check_required(self, context, calc_vals=None, data=None):
                        daylight_control = calc_vals["daylight_control"]
                        return daylight_control

                    def get_manual_check_required_msg(
                        self, context, calc_vals=None, data=None
                    ):
                        elfh_differeces = calc_vals["eflh_difference"]
                        return (
                            f"Space models at least one daylight control using schedule. Verify if other "
                            f"programmable lighting control is modeled correctly using schedule. Lighting schedule "
                            f"EFLH in P-RMD is {elfh_differeces} of that in B-RMD. "
                        )

                    def rule_check(self, context, calc_vals=None, data=None):
                        total_hours_compared = calc_vals["total_hours_compared"]
                        total_hours_matched = calc_vals["total_hours_matched"]
                        return total_hours_matched == total_hours_compared

                    def get_fail_msg(self, context, calc_vals=None, data=None):
                        eflh_difference = calc_vals["eflh_difference"]
                        return f"Space lighting schedule EFLH in P-RMD is {eflh_difference} of that in B-RMD."
