from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_
from rct229.utils.compare_standard_val import std_le
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_1A,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_12A,
]

BOILER_RATED_CAPACITY_LOW_LIMIT = 300_000 * ureg("Btu/hr")
BOILER_RATED_CAPACITY_HIGH_LIMIT = 2_500_000 * ureg("Btu/hr")
BOILER_EFFICIENCY_80 = 0.8
BOILER_EFFICIENCY_75 = 0.75
BOILER_EFFICIENCY_METRIC_TYPE = SchemaEnums.schema_enums[
    "BoilerEfficiencyMetricOptions"
]


class PRM9012019Rule35d81(RuleDefinitionListIndexedBase):
    """Rule 17 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(PRM9012019Rule35d81, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule35d81.BoilerRule(),
            index_rmd=BASELINE_0,
            id="21-17",
            description="All boilers in the baseline building design shall be modeled at the minimum efficiency levels, both part load and full load, in accordance with Tables G3.5.6.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.2.1 General Baseline HVAC System Requirements - Equipment Efficiencies",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="boilers[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list containing all HVAC systems that are modeled in the rmd_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        )

    class BoilerRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule35d81.BoilerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": [
                        "rated_capacity",
                        "efficiency_metric_types",
                        "efficiency_metric_values",
                    ],
                },
                precision={
                    "boiler_efficiency_b": {
                        "precision": 0.01,
                    },
                    "boiler_rated_capacity_b": {
                        "precision": 0.0001,
                        "unit": "Btu/hr",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            boiler_b = context.BASELINE_0
            boiler_rated_capacity_b = boiler_b["rated_capacity"]
            boiler_efficiency_metric_types_b = boiler_b["efficiency_metric_types"]
            boiler_efficiency_metric_values_b = boiler_b["efficiency_metric_values"]

            assert_(
                len(boiler_efficiency_metric_types_b)
                == len(boiler_efficiency_metric_values_b)
                and 1 <= len(boiler_efficiency_metric_types_b) <= 3,
                "`efficiency_metric_types` and `efficiency_metric_values` must have the same length between 1 to 3",
            )

            efficiency_dict = dict(
                zip(boiler_efficiency_metric_types_b, boiler_efficiency_metric_values_b)
            )
            boiler_annual_fuel_utilization_efficiency_b = efficiency_dict.get(
                BOILER_EFFICIENCY_METRIC_TYPE.ANNUAL_FUEL_UTILIZATION, None
            )
            boiler_thermal_efficiency_b = efficiency_dict.get(
                BOILER_EFFICIENCY_METRIC_TYPE.THERMAL, None
            )
            boiler_combustion_efficiency_b = efficiency_dict.get(
                BOILER_EFFICIENCY_METRIC_TYPE.COMBUSTION, None
            )

            return {
                "boiler_rated_capacity_b": CalcQ("capacity", boiler_rated_capacity_b),
                "boiler_annual_fuel_utilization_efficiency_b": boiler_annual_fuel_utilization_efficiency_b,
                "boiler_thermal_efficiency_b": boiler_thermal_efficiency_b,
                "boiler_combustion_efficiency_b": boiler_combustion_efficiency_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            boiler_rated_capacity_b = calc_vals["boiler_rated_capacity_b"]
            boiler_annual_fuel_utilization_efficiency_b = calc_vals[
                "boiler_annual_fuel_utilization_efficiency_b"
            ]
            boiler_thermal_efficiency_b = calc_vals["boiler_thermal_efficiency_b"]
            boiler_combustion_efficiency_b = calc_vals["boiler_combustion_efficiency_b"]

            return (
                boiler_rated_capacity_b < BOILER_RATED_CAPACITY_LOW_LIMIT
                and boiler_annual_fuel_utilization_efficiency_b
                and self.precision_comparison["boiler_efficiency_b"](
                    boiler_annual_fuel_utilization_efficiency_b,
                    BOILER_EFFICIENCY_80,
                )
                or (
                    (
                        boiler_rated_capacity_b < BOILER_RATED_CAPACITY_HIGH_LIMIT
                        or self.precision_comparison["boiler_rated_capacity_b"](
                            boiler_rated_capacity_b, BOILER_RATED_CAPACITY_HIGH_LIMIT
                        )
                    )
                    and boiler_thermal_efficiency_b
                    and self.precision_comparison["boiler_efficiency_b"](
                        boiler_thermal_efficiency_b,
                        BOILER_EFFICIENCY_75,
                    )
                )
                or (
                    boiler_rated_capacity_b > BOILER_RATED_CAPACITY_HIGH_LIMIT
                    and boiler_combustion_efficiency_b
                    and self.precision_comparison["boiler_efficiency_b"](
                        boiler_combustion_efficiency_b,
                        BOILER_EFFICIENCY_80,
                    )
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            boiler_rated_capacity_b = calc_vals["boiler_rated_capacity_b"]
            boiler_annual_fuel_utilization_efficiency_b = calc_vals[
                "boiler_annual_fuel_utilization_efficiency_b"
            ]
            boiler_thermal_efficiency_b = calc_vals["boiler_thermal_efficiency_b"]
            boiler_combustion_efficiency_b = calc_vals["boiler_combustion_efficiency_b"]

            return (
                boiler_rated_capacity_b < BOILER_RATED_CAPACITY_LOW_LIMIT
                and boiler_annual_fuel_utilization_efficiency_b
                and std_equal(
                    BOILER_EFFICIENCY_80, boiler_annual_fuel_utilization_efficiency_b
                )
                or (
                    std_le(
                        val=boiler_rated_capacity_b,
                        std_val=BOILER_RATED_CAPACITY_HIGH_LIMIT,
                    )
                    and boiler_thermal_efficiency_b
                    and std_equal(BOILER_EFFICIENCY_75, boiler_thermal_efficiency_b)
                )
                or (
                    boiler_rated_capacity_b > BOILER_RATED_CAPACITY_HIGH_LIMIT
                    and boiler_combustion_efficiency_b
                    and std_equal(
                        val=boiler_combustion_efficiency_b, std_val=BOILER_EFFICIENCY_80
                    )
                )
            )
