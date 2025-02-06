from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019 import BASELINE_0
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
MANUAL_CHECK_MSG = (
    "There is a temperature schedule mismatch between the baseline and proposed. Fail unless "
    "Table G3.1 #4 baseline column exception #s 1 and/or 2 are applicable "
)


class PRM9012019Rule96q77(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 4 (Schedules Setpoints)"""

    def __init__(self):
        super(PRM9012019Rule96q77, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$": ["weather", "calendar"],
                "weather": ["climate_zone"],
                "calendar": ["is_leap_year"],
            },
            each_rule=PRM9012019Rule96q77.RuleSetModelInstanceRule(),
            index_rmd=BASELINE_0,
            id="4-1",
            description="Temperature Control Setpoints shall be the same for proposed design and baseline building design.",
            ruleset_section_title="Schedules Setpoints",
            standard_section="Section G3.1-4 Schedule Modeling Requirements for the Proposed design and Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
            data_items={
                "climate_zone_b": (BASELINE_0, "weather/climate_zone"),
                "is_leap_year_b": (BASELINE_0, "calendar/is_leap_year"),
            },
        )

    class RuleSetModelInstanceRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule96q77.RuleSetModelInstanceRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule96q77.RuleSetModelInstanceRule.ZoneRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*].building_segments[*].zones[*]",
                required_fields={"$": ["schedules"]},
            )

        def create_data(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            return {
                "schedules_b": rmd_b["schedules"],
                "schedules_p": rmd_p["schedules"],
                "zcc_dict_b": get_zone_conditioning_category_rmd_dict(
                    data["climate_zone_b"], rmd_b
                ),
            }

        def list_filter(self, context_item, data=None):
            zcc_dict_b = data["zcc_dict_b"]
            zone_b = context_item.BASELINE_0
            return zcc_dict_b[zone_b["id"]] in CONDITIONED_ZONE_TYPE

        class ZoneRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule96q77.RuleSetModelInstanceRule.ZoneRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    manual_check_required_msg=MANUAL_CHECK_MSG,
                )

            def get_calc_vals(self, context, data=None):
                is_leap_year = data["is_leap_year_b"]
                number_of_hours = (
                    LeapYear.LEAP_YEAR_HOURS
                    if is_leap_year
                    else LeapYear.REGULAR_YEAR_HOURS
                )

                zone_b = context.BASELINE_0
                zone_p = context.PROPOSED

                schedules_b = data["schedules_b"]
                schedules_p = data["schedules_p"]

                thermostat_cooling_stpt_sch_id_b = zone_b.get(
                    "thermostat_cooling_setpoint_schedule"
                )

                thermostat_cooling_stpt_sch_id_p = zone_p.get(
                    "thermostat_cooling_setpoint_schedule"
                )
                thermostat_heating_stpt_sch_id_b = zone_b.get(
                    "thermostat_heating_setpoint_schedule"
                )
                thermostat_heating_stpt_sch_id_p = zone_p.get(
                    "thermostat_heating_setpoint_schedule"
                )

                thermostat_cooling_stpt_hourly_values_b = (
                    getattr_(
                        find_exactly_one(
                            f'$[*][?(@.id="{thermostat_cooling_stpt_sch_id_b}")]',
                            schedules_b,
                        ),
                        "schedules",
                        "hourly_values",
                    )
                    if thermostat_cooling_stpt_sch_id_b
                    else [
                        getattr_(
                            zone_b, "zones", "design_thermostat_cooling_setpoint"
                        ).magnitude
                    ]
                    * number_of_hours
                )

                assert_(
                    len(thermostat_cooling_stpt_hourly_values_b) == number_of_hours,
                    f"Schedule id: {thermostat_cooling_stpt_sch_id_b} has number of hours of {len(thermostat_cooling_stpt_hourly_values_b)}, expecting {number_of_hours}",
                )

                thermostat_cooling_stpt_hourly_values_p = (
                    getattr_(
                        find_exactly_one(
                            f'$[*][?(@.id="{thermostat_cooling_stpt_sch_id_p}")]',
                            schedules_p,
                        ),
                        "schedules",
                        "hourly_values",
                    )
                    if thermostat_cooling_stpt_sch_id_p
                    else [
                        zone_p.getattr_(
                            zone_p, "design_thermostat_cooling_setpoint"
                        ).magnitude
                    ]
                    * number_of_hours
                )

                assert_(
                    len(thermostat_cooling_stpt_hourly_values_p) == number_of_hours,
                    f"Schedule id: {thermostat_cooling_stpt_sch_id_p} has number of hours of {len(thermostat_cooling_stpt_hourly_values_p)}, expecting {number_of_hours}",
                )

                thermostat_heating_stpt_hourly_values_b = (
                    getattr_(
                        find_exactly_one(
                            f'$[*][?(@.id="{thermostat_heating_stpt_sch_id_b}")]',
                            schedules_b,
                        ),
                        "schedules",
                        "hourly_values",
                    )
                    if thermostat_heating_stpt_sch_id_b
                    else [
                        zone_b.getattr_(
                            zone_b, "design_thermostat_heating_setpoint"
                        ).magnitude
                    ]
                    * number_of_hours
                )

                assert_(
                    len(thermostat_heating_stpt_hourly_values_b) == number_of_hours,
                    f"Schedule id: {thermostat_heating_stpt_sch_id_b} has number of hours of {len(thermostat_heating_stpt_hourly_values_b)}, expecting {number_of_hours}",
                )

                thermostat_heating_stpt_hourly_values_p = (
                    getattr_(
                        find_exactly_one(
                            f'$[*][?(@.id="{thermostat_heating_stpt_sch_id_p}")]',
                            schedules_p,
                        ),
                        "schedules",
                        "hourly_values",
                    )
                    if thermostat_heating_stpt_sch_id_p
                    else [
                        zone_p.getattr_(
                            zone_p, "design_thermostat_heating_setpoint"
                        ).magnitude
                    ]
                    * number_of_hours
                )

                assert_(
                    len(thermostat_heating_stpt_hourly_values_p) == number_of_hours,
                    f"Schedule id: {thermostat_heating_stpt_sch_id_p} has number of hours of {len(thermostat_heating_stpt_hourly_values_p)}, expecting {number_of_hours}",
                )

                cooling_schedule_matched = (
                    thermostat_cooling_stpt_hourly_values_b
                    == thermostat_cooling_stpt_hourly_values_p
                )
                heating_schedule_matched = (
                    thermostat_heating_stpt_hourly_values_b
                    == thermostat_heating_stpt_hourly_values_p
                )

                return {
                    "cooling_schedule_matched": cooling_schedule_matched,
                    "heating_schedule_matched": heating_schedule_matched,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                cooling_schedule_matched = calc_vals["cooling_schedule_matched"]
                heating_schedule_matched = calc_vals["heating_schedule_matched"]
                return not (cooling_schedule_matched and heating_schedule_matched)

            def rule_check(self, context, calc_vals=None, data=None):
                return True
