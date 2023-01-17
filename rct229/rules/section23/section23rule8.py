from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
]
SUPPLY_AIRFLOW_COEFF = [0.1 * i for i in range(11)]
DESIGN_POWER_COEFF = [0.0, 0.03, 0.07, 0.13, 0.21, 0.30, 0.41, 0.54, 0.68, 0.83, 1.0]


class Section23Rule8(RuleDefinitionListIndexedBase):
    """Rule 8 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(Section23Rule8, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section23Rule8.SupplyFanRule(),
            index_rmr="baseline",
            id="23-8",
            description="System 5-8 and 11 - part load VAV fan power shall be modeled using either method 1 or 2 in Table G3.1.3.15. This rule will only validate data points from Method-1 Part-load Fan Power Data. However, both methods are equivalent. When modeling inputs are based on Method 2, values should be converted to Method 1 when writing to RMD.",
            ruleset_section_title="HVAC - Airside",
            standard_section="Section G3.1.3.15 VAV Fan Part-Load Performance (Systems 5 through 8 and 11)",
            is_primary_rule=False,
            rmr_context="ruleset_model_instances/0",
            list_path="$..supply_fans[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)

        return any(
            [
                baseline_system_type_compare(system_type, applicable_sys_type, False)
                for system_type in baseline_system_types_dict.keys()
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    class SupplyFanRule(RuleDefinitionBase):
        def __init__(self):
            super(Section23Rule8.SupplyFanRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": [
                        "design_airflow",
                        "design_electric_power",
                        "output_validation_points",
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            supply_fan_b = context.baseline

            design_airflow_b = supply_fan_b["design_airflow"]
            design_electric_power_b = supply_fan_b["design_electric_power"]
            output_validation_points_b = supply_fan_b["output_validation_points"]

            return {
                "design_airflow_b": CalcQ("air_flow_rate", design_airflow_b),
                "design_electric_power_b": CalcQ(
                    "electric_power", design_electric_power_b
                ),
                "output_validation_points_b": output_validation_points_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            design_airflow_b = calc_vals["design_airflow_b"]
            design_electric_power_b = calc_vals["design_electric_power_b"]
            output_validation_points_b = calc_vals["output_validation_points_b"]

            output_validation_points = [
                [output["airflow"], output["result"]]
                for output in output_validation_points_b
            ]

            target_validation_points = [
                [
                    SUPPLY_AIRFLOW_COEFF[idx] * design_airflow_b,
                    DESIGN_POWER_COEFF[idx] * design_electric_power_b,
                ]
                for idx in range(11)
            ]

            return all(
                list(
                    map(
                        lambda x, y: std_equal(x[0], y[0]),
                        output_validation_points,
                        target_validation_points,
                    )
                )
                and list(
                    map(
                        lambda x, y: std_equal(x[1], y[1]),
                        output_validation_points,
                        target_validation_points,
                    )
                )
            )
