from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one

APPLICABILITY_MSG = (
    "This building is a 24hr-facility with service water heating loads. If the building meets the prescriptive criteria for use of condenser heat recovery systems described in 90.1 Section 6.5.6.2, a system meeting the requirements of that section shall be included in the baseline building design regardless of the exceptions to Section 6.5.6.2. "
    "(Exceptions: 1. Facilities that employ condenser heat recovery for space heating with a heat recovery design exceeding 30% of the peak water-cooled condenser load at design conditions."
    " 2. Facilities that provide 60% of their service water heating from site-solar energy or siterecovered energy or from other sources.) Recommend manual review to determine if project complies."
)


class PRM9012019Rule52y79(RuleDefinitionListIndexedBase):
    """Rule 12 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule52y79, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule52y79.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-12",
            description="For large, 24-hour-per-day facilities that meet the prescriptive criteria for use of condenser heat recovery systems described in Section 6.5.6.2, a system meeting the requirements of that section shall be included in the baseline building design regardless of the exceptions to Section 6.5.6.2.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, d + exception",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule52y79.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule52y79.RMDRule.BuildingRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*]",
            )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            swh_uses_associated_with_each_building_segment_p = (
                get_swh_uses_associated_with_each_building_segment(rmd_p)
            )
            # Infer number of hours in the year (from any valid schedule)
            hours_this_year = None
            for sched in find_all("$.schedules[*].hourly_values", rmd_b):
                if isinstance(sched, list) and len(sched) > 0:
                    hours_this_year = len(sched)
                    break
            if hours_this_year is None:
                hours_this_year = 8760  # fallback default

            return {
                "schedules_b": find_all("$.schedules[*]", rmd_b),
                "schedules_p": find_all("$.schedules[*]", rmd_p),
                "hours_this_year": hours_this_year,
                "swh_uses_associated_with_each_building_segment_p": swh_uses_associated_with_each_building_segment_p,
            }

        class BuildingRule(PartialRuleDefinition):
            def __init__(self):
                super(PRM9012019Rule52y79.RMDRule.BuildingRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    manual_check_required_msg=APPLICABILITY_MSG,
                )

            def is_applicable(self, context, data=None):
                building_b = context.BASELINE_0
                building_p = context.PROPOSED
                schedules_b = data["schedules_b"]
                hours_this_year = data["hours_this_year"]

                # TODO revise the json path if the service_water_heating_uses is relocated in the schema
                service_water_heating_uses_p = find_all(
                    "$.building_segments[*].zones[*].spaces[*].service_water_heating_uses[*]",
                    building_p,
                )

                building_open_schedule_id_p = find_one(
                    "$.building_open_schedule", building_p
                )

                bldg_open_sch_id_b = getattr_(
                    building_b, "buildings", "building_open_schedule"
                )

                bldg_open_sch_b = next(
                    (
                        schedule_b["hourly_values"]
                        for schedule_b in schedules_b
                        if schedule_b["id"] == bldg_open_sch_id_b
                    ),
                    [],
                )

                return (
                    service_water_heating_uses_p
                    and building_open_schedule_id_p is not None
                    and sum(bldg_open_sch_b) == hours_this_year
                )

            def get_calc_vals(self, context, data=None):
                swh_uses_associated_with_each_building_segment_p = data[
                    "swh_uses_associated_with_each_building_segment_p"
                ]

                uses_associated_with_each_building_segment_p = {
                    bldg_seg_id: sum(
                        swh_uses.get("use", 0.0)
                        for swh_uses in swh_uses_associated_with_each_building_segment_p[
                            bldg_seg_id
                        ]
                    )
                    for bldg_seg_id in swh_uses_associated_with_each_building_segment_p
                }

                return {
                    "uses_associated_with_each_building_segment_p": uses_associated_with_each_building_segment_p
                }

            def applicability_check(self, context, calc_vals, data):
                uses_associated_with_each_building_segment_p = calc_vals[
                    "uses_associated_with_each_building_segment_p"
                ]

                return (
                    sum(list(uses_associated_with_each_building_segment_p.values()))
                    > 0.0
                )
