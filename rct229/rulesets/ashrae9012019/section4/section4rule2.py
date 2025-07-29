from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019 import BASELINE_0, PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_rmd_dict,
)
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_exactly_one

CONDITIONED_ZONE_TYPE = [
    ZCC.CONDITIONED_MIXED,
    ZCC.CONDITIONED_NON_RESIDENTIAL,
    ZCC.CONDITIONED_RESIDENTIAL,
]
MANUAL_CHECK_MSG = "There is a humidity schedule mismatch between the baseline and proposed. Fail unless Table G3.1 #4 baseline column exception #s 1 and/or 2 are applicable"
FAIL_MSG_B = "Fail because a humidity schedule is defined in the baseline but not in the proposed."
FAIL_MSG_P = "Fail because a humidity schedule is defined in the proposed but not in the baseline."


class PRM9012019Rule85i93(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 4 (Schedules Setpoints)"""

    def __init__(self):
        super(PRM9012019Rule85i93, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule85i93.RuleSetModelInstanceRule(),
            index_rmd=BASELINE_0,
            id="4-2",
            description="Humidity Control Setpoints shall be the same for proposed design and baseline building design.",
            ruleset_section_title="Schedules Setpoints",
            standard_section="Section G3.1-4 Schedule Modeling Requirements for the Proposed design and Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RuleSetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule85i93.RuleSetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule85i93.RuleSetModelInstanceRule.ZoneRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*].building_segments[*].zones[*]",
                required_fields={
                    "$": ["weather"],
                    "weather": ["climate_zone"],
                },
            )

        def create_data(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            climate_zone = rmd_b["weather"]["climate_zone"]
            return {
                "climate_zone": climate_zone,
                "schedules_b": rmd_b.get("schedules"),
                "schedules_p": rmd_p.get("schedules"),
                "zcc_dict_b": get_zone_conditioning_category_rmd_dict(
                    climate_zone, rmd_b
                ),
            }

        def list_filter(self, context_item, data):
            zcc_dict_b = data["zcc_dict_b"]
            zone_b = context_item.BASELINE_0
            return zcc_dict_b[zone_b["id"]] in CONDITIONED_ZONE_TYPE

        class ZoneRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule85i93.RuleSetModelInstanceRule.ZoneRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    manual_check_required_msg=MANUAL_CHECK_MSG,
                )

            def get_calc_vals(self, context, data=None):

                zone_b = context.BASELINE_0
                zone_p = context.PROPOSED

                schedules_b = data["schedules_b"]
                schedules_p = data["schedules_p"]

                minimum_humidity_stpt_sch_id_b = zone_b.get(
                    "minimum_humidity_setpoint_schedule"
                )
                minimum_humidity_stpt_sch_id_p = zone_p.get(
                    "minimum_humidity_setpoint_schedule"
                )
                maximum_humidity_stpt_sch_id_b = zone_b.get(
                    "maximum_humidity_setpoint_schedule"
                )
                maximum_humidity_stpt_sch_id_p = zone_p.get(
                    "maximum_humidity_setpoint_schedule"
                )

                minimum_humidity_stpt_hourly_values_b = None
                if minimum_humidity_stpt_sch_id_b:
                    assert_(
                        schedules_b, f"schedules is missing in the RMD: {BASELINE_0}"
                    )
                    minimum_humidity_stpt_hourly_values_b = getattr_(
                        find_exactly_one(
                            f'$[*][?(@.id="{minimum_humidity_stpt_sch_id_b}")]',
                            schedules_b,
                        ),
                        "schedules",
                        "hourly_values",
                    )

                minimum_humidity_stpt_hourly_values_p = None
                if minimum_humidity_stpt_sch_id_p:
                    assert_(schedules_p, f"schedules is missing in the RMD: {PROPOSED}")
                    minimum_humidity_stpt_hourly_values_p = getattr_(
                        find_exactly_one(
                            f'$[*][?(@.id="{minimum_humidity_stpt_sch_id_p}")]',
                            schedules_p,
                        ),
                        "schedules",
                        "hourly_values",
                    )

                maximum_humidity_stpt_hourly_values_b = None
                if maximum_humidity_stpt_sch_id_b:
                    assert_(
                        schedules_b, f"schedules is missing in the RMD: {BASELINE_0}"
                    )
                    maximum_humidity_stpt_hourly_values_b = getattr_(
                        find_exactly_one(
                            f'$[*][?(@.id="{maximum_humidity_stpt_sch_id_b}")]',
                            schedules_b,
                        ),
                        "schedules",
                        "hourly_values",
                    )

                maximum_humidity_stpt_hourly_values_p = None
                if maximum_humidity_stpt_sch_id_p:
                    assert_(schedules_p, f"schedules is missing in the RMD: {PROPOSED}")
                    maximum_humidity_stpt_hourly_values_p = getattr_(
                        find_exactly_one(
                            f'$[*][?(@.id="{maximum_humidity_stpt_sch_id_p}")]',
                            schedules_p,
                        ),
                        "schedules",
                        "hourly_values",
                    )

                # None matches None or hourly values matched exactly.
                minimum_humidity_schedule_matched = (
                    minimum_humidity_stpt_hourly_values_b
                    == minimum_humidity_stpt_hourly_values_p
                )

                # ^ comparison for data type.
                minimum_humidity_schedule_type_matched = (
                    minimum_humidity_stpt_hourly_values_b is None
                ) == (minimum_humidity_stpt_hourly_values_p is None)

                maximum_humidity_schedule_matched = (
                    maximum_humidity_stpt_hourly_values_b
                    == maximum_humidity_stpt_hourly_values_p
                )
                maximum_humidity_schedule_type_matched = (
                    maximum_humidity_stpt_hourly_values_b is None
                ) == (maximum_humidity_stpt_hourly_values_p is None)

                return {
                    "minimum_humidity_stpt_sch_id_b": minimum_humidity_stpt_sch_id_b,
                    "minimum_humidity_stpt_sch_id_p": minimum_humidity_stpt_sch_id_p,
                    "minimum_humidity_schedule_matched": minimum_humidity_schedule_matched,
                    "minimum_humidity_schedule_type_matched": minimum_humidity_schedule_type_matched,
                    "maximum_humidity_stpt_sch_id_b": maximum_humidity_stpt_sch_id_b,
                    "maximum_humidity_stpt_sch_id_p": maximum_humidity_stpt_sch_id_p,
                    "maximum_humidity_schedule_matched": maximum_humidity_schedule_matched,
                    "maximum_humidity_schedule_type_matched": maximum_humidity_schedule_type_matched,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                minimum_humidity_schedule_matched = calc_vals[
                    "minimum_humidity_schedule_matched"
                ]
                minimum_humidity_schedule_type_matched = calc_vals[
                    "minimum_humidity_schedule_type_matched"
                ]
                maximum_humidity_schedule_matched = calc_vals[
                    "maximum_humidity_schedule_matched"
                ]
                maximum_humidity_schedule_type_matched = calc_vals[
                    "maximum_humidity_schedule_type_matched"
                ]

                return (
                    minimum_humidity_schedule_type_matched
                    and maximum_humidity_schedule_type_matched
                    and not (
                        minimum_humidity_schedule_matched
                        and maximum_humidity_schedule_matched
                    )
                )

            def rule_check(self, context, calc_vals=None, data=None):
                minimum_humidity_schedule_matched = calc_vals[
                    "minimum_humidity_schedule_matched"
                ]
                maximum_humidity_schedule_matched = calc_vals[
                    "maximum_humidity_schedule_matched"
                ]

                return (
                    minimum_humidity_schedule_matched
                    and maximum_humidity_schedule_matched
                )

            def get_fail_msg(self, context, calc_vals=None, data=None):
                minimum_humidity_stpt_sch_id_b = calc_vals[
                    "minimum_humidity_stpt_sch_id_b"
                ]
                maximum_humidity_stpt_sch_id_b = calc_vals[
                    "maximum_humidity_stpt_sch_id_b"
                ]

                # guaranteed that either b or p has Null
                return (
                    FAIL_MSG_B
                    if (
                        minimum_humidity_stpt_sch_id_b or maximum_humidity_stpt_sch_id_b
                    )
                    else FAIL_MSG_P
                )
