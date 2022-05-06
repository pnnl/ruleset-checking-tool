from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.compare_schedules import (
    LEAP_YEAR_HOURS,
    REGULAR_YEAR_HOURS,
    compare_schedules,
)


class Section5Rule45(RuleDefinitionListIndexedBase):
    """Rule 45 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule45, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section5Rule45.ZoneRule(),
            index_rmr="proposed",
            id="5-45",
            description="The infiltration schedules are the same in the proposed RMR as in the baseline RMR.",
            list_path="ruleset_model_instances[0].buildings[*].building_segments[*].zones[*]",
            required_fields={"$": ["calendar"], "calendar": ["is_leap_year"]},
        )

    def create_data(self, context, data=None):
        rmr_proposed = context.proposed
        return {"is_leap_year": rmr_proposed["calendar"]["is_leap_year"]}

    def list_filter(self, context_item, data=None):
        # baseline should match to proposed
        zone_p = context_item.proposed
        return "infiltration" in zone_p

    class ZoneRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule45.ZoneRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={"infiltration": ["multiplier_schedule"]},
            )

        def get_calc_vals(self, context, data=None):
            zone_b = context.baseline
            zone_p = context.proposed

            mask_schedule = [1.0] * (
                LEAP_YEAR_HOURS if data["is_leap_year"] else REGULAR_YEAR_HOURS
            )

            infiltration_p = zone_p["infiltration"]
            infiltration_b = zone_b["infiltration"]

            return compare_schedules(
                infiltration_b["multiplier_schedule"],
                infiltration_p["multiplier_schedule"],
                mask_schedule,
                1.0,
                data["is_leap_year"],
            )

        def rule_check(self, context, calc_vals=None, data=None):
            total_hours_compared = calc_vals["total_hours_compared"]
            total_hours_match = calc_vals["total_hours_matched"]
            # total_hours_compared needs to be greater than 0.0
            return (
                total_hours_compared > 0.0 and total_hours_compared == total_hours_match
            )

        def get_fail_msg(self, context, calc_vals=None, data=None):
            elfh_difference = calc_vals["elfh_difference"]
            return f"Baseline and proposed infiltration schedules are not the same. The difference of baseline EFLH to proposed EFLH is equal to {elfh_difference}."
