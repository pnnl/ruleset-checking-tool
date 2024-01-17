from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0, PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_lab_zone_hvac_systems import (
    get_lab_zone_hvac_systems,
)

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_7,
]


class Section23Rule4(RuleDefinitionListIndexedBase):
    """Rule 4 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(Section23Rule4, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section23Rule4.RuleSetModelInstanceRule(),
            index_rmr=BASELINE_0,
            id="23-4",
            description="Baseline systems 5 & 7 serving lab spaces per G3.1.1c shall reduce lab exhaust and makeup air during unoccupied periods to 50% of zone peak airflow, the minimum outdoor airflow, or rate required to comply with minimum accreditation standards whichever is larger.",
            ruleset_section_title="HVAC - Airside",
            standard_section="Exception to G3.1.3.13 VAV Minimum Flow Set Points (Systems 5 and 7)",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
            required_fields={
                "$": ["calendar", "weather"],
                "weather": ["climate_zone"],
                "calendar": ["is_leap_year"],
            },
            data_items={
                "climate_zone_b": (BASELINE_0, "weather/climate_zone"),
                "is_leap_year_b": (BASELINE_0, "calendar/is_leap_year"),
            },
        )

    class RuleSetModelInstanceRule(PartialRuleDefinition):
        def __init__(self):
            super(Section23Rule4.RuleSetModelInstanceRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
            )

        def get_calc_vals(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            climate_zone_b = data["climate_zone_b"]
            is_leap_year_b = data["is_leap_year_b"]

            baseline_system_types_dict = get_baseline_system_types(rmd_b)

            hvac_sys_5_or_7_list = [
                system_type
                for system_type in baseline_system_types_dict
                for applicable_sys_type in APPLICABLE_SYS_TYPES
                if baseline_system_type_compare(system_type, applicable_sys_type, False)
            ]

            hvac_systems_serving_lab_zones = get_lab_zone_hvac_systems(
                rmd_b, rmd_p, climate_zone_b, is_leap_year_b
            )

            return {
                "hvac_sys_5_or_7_list": hvac_sys_5_or_7_list,
                "hvac_systems_serving_lab_zones": hvac_systems_serving_lab_zones,
            }

        def applicability_check(self, context, calc_vals, data):
            hvac_sys_5_or_7_list = calc_vals["hvac_sys_5_or_7_list"]
            hvac_systems_serving_lab_zones = calc_vals["hvac_systems_serving_lab_zones"]

            return any(
                [
                    hvac_sys_id
                    for hvac_sys_id in hvac_systems_serving_lab_zones["lab_zones_only"]
                    if hvac_sys_id in hvac_sys_5_or_7_list
                ]
            )
