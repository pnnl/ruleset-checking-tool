from rct229.rule_engine.rule_base import RuleDefinitionListIndexedBase, RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.compare_schedules import compare_schedules
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one_with_field_value
from rct229.utils.pint_utils import pint_sum, ZERO


class Section6Rule13(RuleDefinitionListIndexedBase):
    """Rule 13 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule13, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section6Rule13.RuleSetModelInstanceRule(),
            index_rmr="proposed",
            id="6-13",
            description="Additional occupancy sensor controls in the proposed building are modeled through schedule adjustments based on factors defined in Table G3.7.",
            list_path="ruleset_model_instances[0]",
            required_fields={"$": ["calendar"], "calendar": ["is_leap_year"]},
        )

    def create_data(self, context, data=None):
        rmd_b = context.baseline
        return {"is_leap_year": rmd_b["calendar"]["is_leap_year"]}

    class RuleSetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section6Rule13.RuleSetModelInstanceRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                each_rule=Section6Rule13.RuleSetModelInstanceRule.BuildingRule(),
                index_rmr="proposed",
                list_path="buildings[*]",
                required_fields={"$": ["schedules"]},
            )

        def create_data(self, context, data=None):
            rmd_b = context.baseline
            rmd_p = context.proposed
            return {
                **data,
                "schedules_b": rmd_b["schedules"],
                "schedules_p": rmd_p["schedules"],
            }

        class BuildingRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section6Rule13.RuleSetModelInstanceRule.BuildingRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    each_rule=Section6Rule13.RuleSetModelInstanceRule.BuildingRule.ZoneRule(),
                    index_rmr="proposed",
                    list_path="$..zones[*]",
                )

            def create_data(self, context, data=None):
                building_p = context.proposed
                schedules_p = data["schedules_p"]
                return {
                    **data,
                    "building_open_schedule_p":  getattr_(
                        find_one_with_field_value("$", "id", building_p["building_open_schedule"], schedules_p),
                        "schedule", "hourly_values")
                }

            class ZoneRule(RuleDefinitionListIndexedBase):
                def __init__(self):
                    super(Section6Rule13.RuleSetModelInstanceRule.BuildingRule.ZoneRule, self).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, True),
                        each_rule=Section6Rule13.RuleSetModelInstanceRule.BuildingRule.ZoneRule.SpaceRule(),
                        index_rmr="proposed",
                        list_path="spaces[*]",
                        required_fields={
                            "$": ["volume"]
                        }
                    )

                def create_data(self, context, data=None):
                    zone_p = context.proposed
                    return {
                        **data,
                        "avg_space_height": zone_p.get("volume", 0.0) / pint_sum(find_all("spaces[*].floor_area", zone_p), ZERO.AREA)
                    }

                class SpaceRule(RuleDefinitionBase):
                    def __init__(self):
                        super(Section6Rule13.RuleSetModelInstanceRule.BuildingRule.ZoneRule.SpaceRule, self).__init__(
                            rmrs_used=UserBaselineProposedVals(False, True, True)
                        )

                    def get_calc_vals(self, context, data=None):
                        space_p = context.proposed
                        space_b = context.baseline
                        avg_space_height = data["avg_space_height"]
                        schedules_b = data["schedules_b"]
                        schedules_p = data["schedules_p"]
                        building_open_schedule_p = data["building_open_schedule_p"]

                        normalized_schedule_b = normalize_space_schedules(space_b, avg_space_height, schedules_b)
                        normalized_schedule_p = normalized_space_schedules(space_p, avg_space_height, schedules_p)
                        schedule_comparison_result = compare_schedules(normalized_schedule_p, normalized_schedule_b, building_open_schedule_p, 1.0)




