from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0, PROPOSED, USER
from rct229.rulesets.ashrae9012019.ruleset_functions.compare_schedules import (
    compare_schedules,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all


class Section16Rule4(RuleDefinitionListIndexedBase):
    """Rule 4 of ASHRAE 90.1-2019 Appendix G Section 16 (Elevators)"""

    def __init__(self):
        super(Section16Rule4, self).__init__(
            rmds_used=produce_ruleset_model_instance(
                USER=False,
                BASELINE_0=True,
                PROPOSED=True,
            ),
            each_rule=Section16Rule4.BuildingRule(),
            index_rmd="baseline",
            id="16-4",
            description="The elevator cab lights shall be modeled with the same schedule as the elevator motor.",
            ruleset_section_title="Elevators",
            standard_section="Section G3.1",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="ruleset_model_descriptions[0].buildings[*].elevators[*]",
            required_fields={"$": ["calendar"], "$.calendar": ["is_leap_year"]},
            data_items={"is_leap_year_b": (BASELINE_0, "calendar/is_leap_year")},
        )

    def is_applicable(self, context, data=None):
        rmd_p = context.PROPOSED

        return (
            len(
                find_all(
                    "$.ruleset_model_descriptions[0].buildings[*].elevators", rmd_p
                )
            )
            > 0
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section16Rule4.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_instance(
                    USER=False,
                    BASELINE_0=True,
                    PROPOSED=True,
                ),
            )

        def get_calc_vals(self, context, data=None):
            building_b = context.BASELINE_0
            building_p = context.PROPOSED

            is_leap_year_b = data["is_leap_year_b"]
            mask_schedule = [1] * 8784 if is_leap_year_b else [1] * 8760

            cab_lighting_multiplier_schedule_b = getattr_(
                building_b,
                "building",
                "elevators",
                "cab_lighting_multiplier_schedule",
            )
            cab_lighting_multiplier_schedule_p = getattr_(
                building_p,
                "building",
                "elevators",
                "cab_lighting_multiplier_schedule",
            )

            compare_schedules = compare_schedules(
                cab_lighting_multiplier_schedule_b,
                cab_lighting_multiplier_schedule_p,
                mask_schedule,
                is_leap_year_b,
            )

            return {
                "cab_lighting_multiplier_schedule_b": cab_lighting_multiplier_schedule_b,
                "cab_lighting_multiplier_schedule_p": cab_lighting_multiplier_schedule_p,
                "compare_schedules": compare_schedules,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            compare_schedules = calc_vals["compare_schedules"]
            cab_lighting_multiplier_schedule_b = calc_vals[
                "cab_lighting_multiplier_schedule_b"
            ]
            cab_lighting_multiplier_schedule_p = calc_vals[
                "cab_lighting_multiplier_schedule_p"
            ]

            return (
                compare_schedules["total_hours_matched"]
                == len(cab_lighting_multiplier_schedule_b)
                == len(cab_lighting_multiplier_schedule_p)
            )
