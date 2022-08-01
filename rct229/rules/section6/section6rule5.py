from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.compare_schedules import compare_schedules
from rct229.ruleset_functions.get_avg_zone_height import get_avg_zone_height
from rct229.ruleset_functions.normalize_interior_lighting_schedules import (
    normalize_interior_lighting_schedules,
)
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.masks import invert_mask
from rct229.utils.pint_utils import ZERO, pint_sum

BUILDING_AREA_CUTTOFF = ureg("5000 ft2")


class Section6Rule5(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule5, self).__init__(
            id="6-5",
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section6Rule5.BuildingRule(),
            index_rmr="baseline",
            description="Baseline building is modeled with automatic shutoff controls in buildings >5000 sq.ft.",
            required_fields={
                "$": ["calendar", "schedules"],
                "calendar": ["is_leap_year"],
            },
            list_path="ruleset_model_instances[0].buildings[*]",
            data_items={
                "is_leap_year_b": ("baseline", "calendar/is_leap_year"),
                "schedules_b": ("baseline", "schedules"),
                "schedules_p": ("proposed", "schedules"),
            },
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section6Rule5.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                each_rule=Section6Rule5.BuildingRule.ZoneRule(),
                index_rmr="baseline",
                required_fields={"$": ["building_open_schedule"]},
                data_items={
                    "building_open_schedule_b": ("baseline", "building_open_schedule"),
                },
            )

        def is_applicable(self, context, data):
            building_b = context.baseline
            building_total_area_b = pint_sum(
                find_all("$..spaces[*].floor_area", building_b, ZERO.AREA)
            )

            return building_total_area_b > BUILDING_AREA_CUTTOFF

        class ZoneRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section6Rule5.BuildingRule.ZoneRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    each_rule=Section6Rule5.BuildingRule.ZoneRule.SpaceRule(),
                    index_rmr="baseline",
                )

            def create_data(self, context, data=None):
                zone_b = context.baseline
                zone_p = context.proposed
                return {
                    "avg_zone_height_b": get_avg_zone_height(zone_b),
                    "avg_zone_height_p": get_avg_zone_height(zone_p),
                }

            class SpaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(Section6Rule5.BuildingRule.ZoneRule.SpaceRule, self).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, True)
                    )

                def get_calc_vals(self, context, data=None):
                    is_leap_year_b = data["is_leap_year_b"]
                    schedules_b = data["schedules_b"]
                    schedules_p = data["schedules_p"]
                    space_b = context.baseline
                    space_p = context.proposed
                    space_height_b = data["avg_zone_height_b"]
                    space_height_p = data["avg_zone_height_p"]
                    normalized_interior_lighting_schedule_b = (
                        normalize_interior_lighting_schedules(
                            space_b,
                            space_height_b,
                            schedules_b,
                            adjust_for_credit=False,
                        )
                    )
                    normalized_interior_lighting_schedule_p = (
                        normalize_interior_lighting_schedules(
                            space_p,
                            space_height_p,
                            schedules_p,
                            adjust_for_credit=False,
                        )
                    )

                    schedule_comparison_result = compare_schedules(
                        normalized_interior_lighting_schedule_b,
                        normalized_interior_lighting_schedule_p,
                        mask_schedule=invert_mask(building_open_schedule_b),
                        is_leap_year=is_leap_year_b,
                    )

                    return {"schedule_comparison_result": schedule_comparison_result}

                def rule_check(self, context, calc_vals=None, data=None):
                    schedule_comparison_result = calc_vals["schedule_comparison_result"]

                    return (
                        schedule_comparison_result["total_hours_matched"]
                        == schedule_comparison_result["total_hours_matched"]
                    )
