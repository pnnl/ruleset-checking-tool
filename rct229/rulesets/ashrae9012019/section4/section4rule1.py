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
            each_rule=PRM9012019Rule96q77.RuleSetModelInstanceRule(),
            index_rmd=BASELINE_0,
            id="4-1",
            description="Temperature control setpoints shall be the same for proposed design and baseline building design.",
            ruleset_section_title="Schedules Setpoints",
            standard_section="Section G3.1-4 Schedule Modeling Requirements for the Proposed design and Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
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
                required_fields={
                    "$": ["schedules", "weather"],
                    "weather": ["climate_zone"],
                },
            )

        def create_data(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            climate_zone_b = rmd_b["weather"]["climate_zone"]
            return {
                "schedules_b": rmd_b["schedules"],
                "schedules_p": rmd_p["schedules"],
                "climate_zone_b": climate_zone_b,
                "zcc_dict_b": get_zone_conditioning_category_rmd_dict(
                    climate_zone_b, rmd_b
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
                zone_b = context.BASELINE_0
                zone_p = context.PROPOSED

                schedules_b = data["schedules_b"]
                schedules_p = data["schedules_p"]

                cooling_id_b = zone_b.get("thermostat_cooling_setpoint_schedule")
                cooling_id_p = zone_p.get("thermostat_cooling_setpoint_schedule")
                heating_id_b = zone_b.get("thermostat_heating_setpoint_schedule")
                heating_id_p = zone_p.get("thermostat_heating_setpoint_schedule")

                # Cooling
                if cooling_id_b is not None:
                    cooling_match_b = find_exactly_one(
                        f'$[*][?(@.id="{cooling_id_b}")]', schedules_b
                    )
                    cooling_vals_b = getattr_(
                        cooling_match_b, "schedules", "hourly_values"
                    )
                else:
                    cooling_vals_b = None

                if cooling_id_p is not None:
                    cooling_match_p = find_exactly_one(
                        f'$[*][?(@.id="{cooling_id_p}")]', schedules_p
                    )
                    cooling_vals_p = getattr_(
                        cooling_match_p, "schedules", "hourly_values"
                    )
                else:
                    cooling_vals_p = None

                assert_(
                    (cooling_vals_b is None) == (cooling_vals_p is None),
                    "Cooling schedule must be found or not found for both Baseline and Proposed models.",
                )

                if cooling_vals_b is None:
                    cooling_val_b = getattr_(
                        zone_b, "zones", "design_thermostat_cooling_setpoint"
                    ).magnitude
                    cooling_val_p = getattr_(
                        zone_p, "design_thermostat_cooling_setpoint"
                    ).magnitude
                    cooling_schedule_matched = cooling_val_b == cooling_val_p
                else:
                    cooling_schedule_matched = cooling_vals_b == cooling_vals_p

                # Heating
                if heating_id_b is not None:
                    heating_match_b = find_exactly_one(
                        f'$[*][?(@.id="{heating_id_b}")]', schedules_b
                    )
                    heating_vals_b = getattr_(
                        heating_match_b, "schedules", "hourly_values"
                    )
                else:
                    heating_vals_b = None

                if heating_id_p is not None:
                    heating_match_p = find_exactly_one(
                        f'$[*][?(@.id="{heating_id_p}")]', schedules_p
                    )
                    heating_vals_p = getattr_(
                        heating_match_p, "schedules", "hourly_values"
                    )
                else:
                    heating_vals_p = None

                assert_(
                    (heating_vals_b is None) == (heating_vals_p is None),
                    "Heating schedule must be found or not found for both Baseline and Proposed models.",
                )

                if heating_vals_b is None:
                    heating_val_b = getattr_(
                        zone_b, "zones", "design_thermostat_heating_setpoint"
                    ).magnitude
                    heating_val_p = getattr_(
                        zone_p, "design_thermostat_heating_setpoint"
                    ).magnitude
                    heating_schedule_matched = heating_val_b == heating_val_p
                else:
                    heating_schedule_matched = heating_vals_b == heating_vals_p

                return {
                    "cooling_schedule_matched": cooling_schedule_matched,
                    "heating_schedule_matched": heating_schedule_matched,
                }

            def rule_check(self, context, calc_vals=None, data=None):
                cooling_schedule_matched = calc_vals["cooling_schedule_matched"]
                heating_schedule_matched = calc_vals["heating_schedule_matched"]

                return cooling_schedule_matched and heating_schedule_matched

            def get_fail_msg(self, context, calc_vals=None, data=None):

                return (
                    "There is a temperature schedule mismatch between the baseline and proposed RMDs. "
                    "Fail unless table G3.1 #4 baseline column exception #s 1 and/or 2 are applicable"
                )
