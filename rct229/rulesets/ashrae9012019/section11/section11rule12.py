from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.utils.assertions import getattr_
from rct229.utils.utility_functions import find_exactly_one_schedule

APPLICABILITY_MSG = (
    "This building is a 24hr-facility with service water heating loads. If the building meets the prescriptive criteria for use of condenser heat recovery systems described in 90.1 Section 6.5.6.2, a system meeting the requirements of that section shall be included in the baseline building design regardless of the exceptions to Section 6.5.6.2. "
    "(Exceptions: 1. Facilities that employ condenser heat recovery for space heating with a heat recovery design exceeding 30% of the peak water-cooled condenser load at design conditions."
    " 2. Facilities that provide 60% of their service water heating from site-solar energy or siterecovered energy or from other sources.) Recommend manual review to determine if project complies."
)


class Section11Rule12(RuleDefinitionListIndexedBase):
    """Rule 12 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule12, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section11Rule12.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-12",
            description="For large, 24-hour-per-day facilities that meet the prescriptive criteria for use of condenser heat recovery systems described in Section 6.5.6.2, a system meeting the requirements of that section shall be included in the baseline building design regardless of the exceptions to Section 6.5.6.2.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, d + exception",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
            data_items={"is_leap_year_b": (BASELINE_0, "calendar/is_leap_year")},
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section11Rule12.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section11Rule12.RMDRule.BuildingRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*]",
            )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            return {"rmd_b": rmd_b, "rmd_p": rmd_p}

        class BuildingRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section11Rule12.RMDRule.BuildingRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    each_rule=Section11Rule12.RMDRule.BuildingRule.BuildingSegmentRule(),
                    index_rmd=BASELINE_0,
                    list_path="$.building_segments[*]",
                )

            def create_data(self, context, data):
                building_b = context.BASELINE_0
                rmd_b = data["rmd_b"]
                is_leap_year_b = data["is_leap_year_b"]

                bldg_open_sch_id_b = getattr_(
                    building_b, "buildings", "building_open_schedule"
                )

                bldg_open_sch_b = find_exactly_one_schedule(rmd_b, bldg_open_sch_id_b)[
                    "hourly_values"
                ]

                hours_this_year = (
                    LeapYear.LEAP_YEAR_HOURS
                    if is_leap_year_b
                    else LeapYear.REGULAR_YEAR_HOURS
                )

                return {
                    "bldg_open_sch_b": bldg_open_sch_b,
                    "hours_this_year": hours_this_year,
                }

            def list_filter(self, context_item, data):
                bldg_open_sch_b = data["bldg_open_sch_b"]
                hours_this_year = data["hours_this_year"]

                return sum(bldg_open_sch_b) == hours_this_year

            class BuildingSegmentRule(RuleDefinitionListIndexedBase):
                def __init__(self):
                    super(
                        Section11Rule12.RMDRule.BuildingRule.BuildingSegmentRule, self
                    ).__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=True
                        ),
                        each_rule=Section11Rule12.RMDRule.BuildingRule.BuildingSegmentRule.SWHRule(),
                        index_rmd=BASELINE_0,
                        list_path="$.zones[*].spaces[*].service_water_heating_uses[*]",
                    )

                def create_data(self, context, data):
                    building_segment_p = context.PROPOSED
                    rmd_p = data["rmd_p"]

                    service_water_heating_use_ids_list_p = (
                        get_swh_uses_associated_with_each_building_segment(
                            rmd_p, building_segment_p["id"]
                        )
                    )

                    return {
                        "service_water_heating_use_ids_list_p": service_water_heating_use_ids_list_p
                    }

                def list_filter(self, context_item, data):
                    swh_use_p = context_item.PROPOSED
                    served_by_distribution_system_p = getattr_(
                        swh_use_p,
                        "service_water_heating_uses",
                        "served_by_distribution_system",
                    )
                    service_water_heating_use_ids_list_p = data[
                        "service_water_heating_use_ids_list_p"
                    ]

                    return (
                        served_by_distribution_system_p
                        in service_water_heating_use_ids_list_p
                    )

                class SWHRule(PartialRuleDefinition):
                    def __init__(self):
                        super(
                            Section11Rule12.RMDRule.BuildingRule.BuildingSegmentRule.SWHRule,
                            self,
                        ).__init__(
                            rmds_used=produce_ruleset_model_description(
                                USER=False, BASELINE_0=False, PROPOSED=True
                            ),
                            manual_check_required_msg=APPLICABILITY_MSG,
                        )

                    def applicability_check(self, context, calc_vals, data):
                        swh_use_p = context.PROPOSED

                        return (
                            getattr_(swh_use_p, "service_water_heating_uses", "use") > 0
                        )
