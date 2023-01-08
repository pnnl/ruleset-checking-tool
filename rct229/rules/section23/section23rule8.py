from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
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
    HVAC_SYS.SYS_5B,
    HVAC_SYS.SYS_6B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_7C,
    HVAC_SYS.SYS_8A,
    HVAC_SYS.SYS_11_1A,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_11_1C,
    HVAC_SYS.SYS_11_1C,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_11_2A,
]


class Section23Rule8(RuleDefinitionListIndexedBase):
    """Rule 8 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(Section23Rule8, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section23Rule8.FanSystemRule(),
            index_rmr="baseline",
            id="23-8",
            description="System 5-8 and 11 - part load VAV fan power shall be modeled using either method 1 or 2 in Table G3.1.3.15. This rule will only validate data points from Method-1 Part-load Fan Power Data. However, both methods are equivalent. When modeling inputs are based on Method 2, values should be converted to Method 1 when writing to RMD.",
            rmr_context="ruleset_model_instances/0",
            list_path="$..fan_system",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list contains all HVAC systems that are modeled in the rmi_b
        available_sys_types = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]

        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_sys_types
            ]
        )

    class FanSystemRule(RuleDefinitionBase):
        def __init__(self):
            super(Section23Rule8.FanSystemRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["supply_fan"],
                    "supply_fan": ["design_airflow", "design_electric_power"],
                },
            )

        def get_calc_vals(self, context, data=None):
            fan_system_b = context.baseline
            design_airflow_b = fan_system_b["design_airflow"]
            design_electric_power_b = fan_system_b["design_electric_power"]

            return {
                "design_airflow_b": CalcQ("volumetric_flow_rate", design_airflow_b),
                "design_electric_power_b": CalcQ(
                    "electric_power", design_electric_power_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            design_airflow_b = calc_vals["design_airflow_b"]
            design_electric_power_b = calc_vals["design_electric_power_b"]
            output_validation_points = data["output_validation_points"]

            target_validation_points = [
                [
                    0.1 * constant * design_airflow_b,
                    0.1 * constant * design_electric_power_b,
                ]
                for constant in range(0, 11)
            ]

            return target_validation_points == output_validation_points
