from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg

BUILDING_AREA_CUTTOFF = ureg("5000 ft2")


class Section6Rule5(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule5, self).__init__(
            id="6-5",
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section6Rule5.BuidlingRule(),
            index_rmr="baseline",
            description="Baseline building is modeled with automatic shutoff controls in buildings >5000 sq.ft.",
            required_fields={"$": ["schedules"]},
            list_path="ruleset_model_instances[0].buildings[*]",
        )

        def create_data(self, context, data={}):
            rmi_b = context.baseline
            rmi_p = context.proposed

            return {
                **data,
                "schedules_b": rmi_b["schedules"],
                "schedules_p": rmi_p["schedules"],
            }

        class BuildingRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section6Rule5.BuildingSegmentRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    each_rule=Section6Rule5.BuidlingRule.ZoneRule(),
                    required_fields={"$": ["building_open_schedule"]},
                )

            def is_applicable(self, context, data):
                building_total_area_b = pint_sum(
                    "$..spaces[*].floor_area", building_b, ZERO.AREA
                )

                return building_total_area_b > BUILDING_AREA_CUTTOFF

            def create_data(self, context, data={}):
                building_b = context.baseline

                return {
                    **data,
                    "building_open_schedule_b": building_b["building_open_schedule"],
                }

            class ZoneRule(RuleDefinitionListIndexedBase):
                def __init__(self):
                    super(Section6Rule5.BuildingRule.ZoneRule, self).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, True),
                        # required_fields={"$": []},
                    )

                def create_data(self, context, data=None):
                    return {
                        **data,
                        "avg_zone_height_b": get_avg_zone_height(zone_b),
                        "avg_zone_height_p": get_avg_zone_height(zone_p),
                    }

            class SpaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(Section6Rule5.SpaceRule, self).__init__(
                        rmrs_used=UserBaselineProposedVals(True, False, True),
                        required_fields={"$": ["interior_lighting"]},
                    )

                def get_calc_vals(self, context, data=None):
                    schedules_b = data["schedules_b"]
                    schedules_p = data["schedules_p"]
                    space_b = context.baseline
                    space_p = context.proposed
                    space_height_b = data["avg_zone_height_b"]
                    space_height_p = data["avg_zone_height_p"]
                    normalized_interior_lighting_schedule_b = (
                        normalize_interior_lighting_schedules(
                            space_b, space_height_b, schedules_b
                        )
                    )
                    normalized_interior_lighting_schedule_p = (
                        normalize_interior_lighting_schedules(
                            space_p, space_height_p, schedules_p
                        )
                    )

                    schedule_comparison_result = compare_schedules(
                        normalized_interior_lighting_schedule_b,
                        normalized_interior_lighting_schedule_p,
                        mask_schedule=building_open_schedule_b,
                        comparison_factor=-111,
                        is_leap_year=is_leap_year,
                    )

                    return {"schedule_comparison_result": schedule_comparison_result}

                def rule_check(self, context, calc_vals=None, data=None):
                    lighting_power_allowance_p = calc_vals["lighting_power_allowance_p"]
                    space_lighting_power_per_area_p = calc_vals[
                        "space_lighting_power_per_area_p"
                    ]
                    space_lighting_power_per_area_u = calc_vals[
                        "space_lighting_power_per_area_u"
                    ]

                    return space_lighting_power_per_area_p == max(
                        lighting_power_allowance_p, space_lighting_power_per_area_u
                    )
