from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.utils.std_comparisons import std_equal
from rct229.schema.config import ureg

APPLICABLE_SYS_TYPES = [
    "SYS-1",
    "SYS-5",
    "SYS-7",
    "SYS-11.2",
    "SYS-12",
    "SYS-1A",
    "SYS-7A",
    "SYS-11.2A",
    "SYS-12A",
]

BOILER_RATED_CAPACITY_LOW_LIMIT = 300000 * ureg("Btu/hr")
BOILER_RATED_CAPACITY_HIGH_LIMIT = 2500000 * ureg("Btu/hr")
BOILER_EFFICIENCY_80 = 0.8
BOILER_EFFICIENCY_75 = 0.75
BOILER_EFFICIENCY_METRIC = schema_enums["BoilerEfficiencyMetricOptions"]


class Section21Rule17(RuleDefinitionListIndexedBase):
    """Rule 17 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(Section21Rule17, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section21Rule17.BoilerRule(),
            index_rmr="baseline",
            id="21-17",
            description="All boilers in the baseline building design shall be modeled at the minimum efficiency levels, both part load and full load, in accordance with Tables G3.5.6.",
            rmr_context="ruleset_model_instances/0",
            list_path="boilers[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-12A": ["hvac_sys_12_a"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    class BoilerRule(RuleDefinitionBase):
        def __init__(self):
            super(Section21Rule17.BoilerRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["rated_capacity", "efficiency_metric", "efficiency"],
                },
            )

        def get_calc_vals(self, context, data=None):
            boiler_b = context.baseline
            boiler_rated_capacity_b = boiler_b["rated_capacity"]
            boiler_efficiency_metric_b = boiler_b["efficiency_metric"]
            boiler_efficiency_b = boiler_b["efficiency"]

            return {
                "boiler_rated_capacity_b": boiler_rated_capacity_b,
                "boiler_efficiency_metric_b": boiler_efficiency_metric_b,
                "boiler_efficiency_b": boiler_efficiency_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            boiler_rated_capacity_b = calc_vals["boiler_rated_capacity_b"]
            boiler_efficiency_metric_b = calc_vals["boiler_efficiency_metric_b"]
            boiler_efficiency_b = calc_vals["boiler_efficiency_b"]

            return (
                (
                    boiler_rated_capacity_b < BOILER_RATED_CAPACITY_LOW_LIMIT
                    and boiler_efficiency_metric_b
                    == BOILER_EFFICIENCY_METRIC.ANNUAL_FUEL_UTILIZATION
                    and std_equal(boiler_efficiency_b, BOILER_EFFICIENCY_80)
                )
                or (
                    boiler_rated_capacity_b <= BOILER_RATED_CAPACITY_HIGH_LIMIT
                    and boiler_efficiency_metric_b == BOILER_EFFICIENCY_METRIC.THERMAL
                    and std_equal(boiler_efficiency_b, BOILER_EFFICIENCY_75)
                )
                or (
                    boiler_rated_capacity_b > BOILER_RATED_CAPACITY_HIGH_LIMIT
                    and boiler_efficiency_metric_b
                    == BOILER_EFFICIENCY_METRIC.COMBUSTION
                    and std_equal(boiler_efficiency_b, BOILER_EFFICIENCY_80)
                )
            )
