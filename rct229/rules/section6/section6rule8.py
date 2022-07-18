from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.compare_schedules import compare_schedules
from rct229.ruleset_functions.normalize_interior_lighting_schedules import normalize_interior_lighting_schedules
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value
from rct229.utils.pint_utils import pint_sum, ZERO

MANUAL_CHECK_MSG = "Lighting schedule in P-RMD including adjusted lighting occupancy sensor reduction factor is " \
                   "higher than that in B-RMD. Verify Additional occupancy sensor control is modeled correctly in " \
                   "P-RMD. "
FAIL_MSG = "Schedule adjustment may be correct if space includes daylight control modeled by schedule adjustment or " \
           "individual workstation with lighting controlled by occupancy sensors (TABLE G3.7 Footnote c). "


class Section6Rule8(RuleDefinitionListIndexedBase):
    """Rule 8 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(Section6Rule8, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section6Rule8.RulesetModelInstanceRule(),
            index_rmr="proposed",
            id="6-8",
            description="Additional occupancy sensor controls in the proposed building are modeled through schedule "
                        "adjustments based on factors defined in Table G3.7.",
            list_path="ruleset_model_instances[0]",
            required_fields={"$": ["calendar"], "calendar": ["is_leap_year"]},
        )

    def create_data(self, context, data=None):
        rmd_b = context.baseline
        return {"is_leap_year": rmd_b["calendar"]["is_leap_year"]}

    class RulesetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section6Rule8.RulesetModelInstanceRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                each_rule=Section6Rule8.RulesetModelInstanceRule.BuildingRule(),
                index_rmr="proposed",
                list_path="buildings[*]",
                required_fields={"$": ["schedules"]},
            )

        def create_data(self, context, data=None):
            rmi_b = context.baseline
            rmi_p = context.proposed
            return {
                **data,
                "schedules_b": rmi_b["schedules"],
                "schedules_p": rmi_p["schedules"],
            }

        class BuildingRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section6Rule8.RulesetModelInstanceRule.BuildingRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    each_rule=Section6Rule8.RulesetModelInstanceRule.BuildingRule.ZoneRule(),
                    index_rmr="proposed",
                    list_path="$..zones[*]",
                )

            def create_data(self, context, data=None):
                building_p = context.proposed
                schedules_p = data["schedules_p"]
                return {
                    **data,
                    "building_open_schedule_p":  getattr_(
                        find_exactly_one_with_field_value("$", "id", building_p["building_open_schedule"], schedules_p),
                        "schedule", "hourly_values")
                }

            class ZoneRule(RuleDefinitionListIndexedBase):
                def __init__(self):
                    super(Section6Rule8.RulesetModelInstanceRule.BuildingRule.ZoneRule, self).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, True),
                        each_rule=Section6Rule8.RulesetModelInstanceRule.BuildingRule.ZoneRule.SpaceRule(),
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
                        "avg_space_height": zone_p.get("volume", ZERO.VOLUME) / pint_sum(find_all("spaces[*].floor_area", zone_p), ZERO.AREA)
                    }

                class SpaceRule(RuleDefinitionBase):
                    def __init__(self):
                        super(Section6Rule8.RulesetModelInstanceRule.BuildingRule.ZoneRule.SpaceRule, self).__init__(
                            rmrs_used=UserBaselineProposedVals(False, True, True),
                            manual_check_required_msg=MANUAL_CHECK_MSG,
                            fail_msg=FAIL_MSG
                        )

                    def get_calc_vals(self, context, data=None):
                        space_p = context.proposed
                        space_b = context.baseline
                        avg_space_height = data["avg_space_height"]
                        schedules_b = data["schedules_b"]
                        schedules_p = data["schedules_p"]
                        building_open_schedule_p = data["building_open_schedule_p"]

                        normalized_interior_lighting_schedule_b = normalize_interior_lighting_schedules(space_b, avg_space_height, schedules_b, adjust_for_credit=False)
                        normalized_interior_lighting_schedule_p = normalize_interior_lighting_schedules(space_p, avg_space_height, schedules_p, adjust_for_credit=True)
                        schedule_comparison_result = compare_schedules(normalized_interior_lighting_schedule_p, normalized_interior_lighting_schedule_b, building_open_schedule_p)

                        return {
                            "total_hours_compared": schedule_comparison_result["total_hours_compared"],
                            "total_hours_matched": schedule_comparison_result["total_hours_matched"],
                        }

                    def manual_check_required(self, context, calc_vals=None, data=None):
                        total_hours_compared = calc_vals["total_hours_compared"]
                        total_hours_matched = calc_vals["total_hours_matched"]
                        return total_hours_matched > total_hours_compared

                    def rule_check(self, context, calc_vals=None, data=None):
                        total_hours_compared = calc_vals["total_hours_compared"]
                        total_hours_matched = calc_vals["total_hours_matched"]
                        return total_hours_matched == total_hours_compared




