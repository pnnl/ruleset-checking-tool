from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0, PROPOSED
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
from rct229.utils.std_comparisons import std_equal

FLOOR_AREA_LIMIT = 5000 * ureg("ft2")  # square foot


class PRM9012019Rule22c86(RuleDefinitionListIndexedBase):
    """Rule 9 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012019Rule22c86, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule22c86.RulesetModelInstanceRule(),
            index_rmd=PROPOSED,
            id="6-9",
            description="Proposed building is modeled with other programmable lighting controls through a 10% "
            "schedule reduction in buildings less than 5,000sq.ft.",
            ruleset_section_title="Lighting",
            standard_section="Section G3.1-6(i) Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RulesetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule22c86.RulesetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule22c86.RulesetModelInstanceRule.BuildingRule(),
                index_rmd=PROPOSED,
                list_path="buildings[*]",
                required_fields={
                    "$": ["schedules"],
                },
                data_items={
                    "schedules_b": (BASELINE_0, "schedules"),
                    "schedules_p": (PROPOSED, "schedules"),
                },
            )

        class BuildingRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(
                    PRM9012019Rule22c86.RulesetModelInstanceRule.BuildingRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    each_rule=PRM9012019Rule22c86.RulesetModelInstanceRule.BuildingRule.ZoneRule(),
                    index_rmd=PROPOSED,
                    list_path="$..zones[*]",
                )

            def is_applicable(self, context, data=None):
                building_p = context.PROPOSED
                total_floor_area_p = sum(
                    find_all("$.spaces[*].floor_area", building_p), ZERO.AREA
                )
                return (
                    self.precision_comparison(total_floor_area_p, FLOOR_AREA_LIMIT)
                    or total_floor_area_p < FLOOR_AREA_LIMIT
                )

            def create_data(self, context, data=None):
                building_p = context.PROPOSED
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
                        PRM9012019Rule22c86.RulesetModelInstanceRule.BuildingRule.ZoneRule,
                        self,
                    ).__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=True
                        ),
                        each_rule=PRM9012019Rule22c86.RulesetModelInstanceRule.BuildingRule.ZoneRule.SpaceRule(),
                        index_rmd=PROPOSED,
                        list_path="spaces[*]",
                    )

                def create_data(self, context, data=None):
                    zone_p = context.PROPOSED
                    return {
                        "avg_space_height": zone_p.get("volume", ZERO.VOLUME)
                        / sum(find_all("$.spaces[*].floor_area", zone_p), ZERO.AREA),
                    }

                class SpaceRule(RuleDefinitionBase):
                    def __init__(self):
                        super(
                            PRM9012019Rule22c86.RulesetModelInstanceRule.BuildingRule.ZoneRule.SpaceRule,
                            self,
                        ).__init__(
                            rmds_used=produce_ruleset_model_description(
                                USER=False, BASELINE_0=True, PROPOSED=True
                            ),
                            precision={
                                "total_hours_matched": {
                                    "precision": 1,
                                    "unit": "",
                                }
                            },
                        )

                    def get_calc_vals(self, context, data=None):
                        space_p = context.PROPOSED
                        space_b = context.BASELINE_0
                        avg_space_height = data["avg_space_height"]
                        schedules_b = data["schedules_b"]
                        schedules_p = data["schedules_p"]
                        building_open_schedule_p = data["building_open_schedule_p"]

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
                        return self.precision_comparison["total_hours_matched"](
                            total_hours_matched, total_hours_compared
                        )

                    def is_tolerance_fail(self, context, calc_vals=None, data=None):
                        total_hours_compared = calc_vals["total_hours_compared"]
                        total_hours_matched = calc_vals["total_hours_matched"]
                        return std_equal(total_hours_matched, total_hours_compared)

                    def get_fail_msg(self, context, calc_vals=None, data=None):
                        eflh_difference = calc_vals["eflh_difference"]
                        return f"Space lighting schedule EFLH in P-RMD is {eflh_difference} of that in B-RMD."
