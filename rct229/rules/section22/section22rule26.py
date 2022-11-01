from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.ruleset_functions.get_primary_secondary_loops_dict import (
    get_primary_secondary_loops_dict,
)
from rct229.schema.config import ureg

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_11_1B,
]

REQUIRED_PUMP_POWER_PER_FLOW_RATE = 12 * ureg("W/gpm")


class Section22Rule26(RuleDefinitionListIndexedBase):
    """Rule 26 of ASHRAE 90.1-2019 Appendix G Section 22 (Hot water loop)"""

    def __init__(self):
        super(Section22Rule26, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule26.PrimaryPumpRule(),
            index_rmr="baseline",
            id="22-26",
            description="For chilled-water systems served by chiller(s) and serves baseline System-11, the baseline building constant-volume primary pump power shall be modeled as 12 W/gpm.",
            rmr_context="ruleset_model_instances/0",
            list_path="pumps[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list contains all HVAC systems that are modeled in the rmi_b
        available_type_lists = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmi_b)

        return (
            any(
                [
                    available_type in APPLICABLE_SYS_TYPES
                    for available_type in available_type_lists
                ]
            )
            and primary_secondary_loop_dict
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        primary_secondary_loops_dict = get_primary_secondary_loops_dict(rmi_b)
        return {"primary_secondary_loops_dict": primary_secondary_loops_dict}

    def list_filter(self, context_item, data):
        pump_b = context_item.baseline
        primary_secondary_loops_dict = data["primary_secondary_loops_dict"]
        return pump_b["loop_or_piping"] in primary_secondary_loops_dict.keys()

    class PrimaryPumpRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule26.PrimaryPumpRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["speed_control"],
                },
            )

        def get_calc_vals(self, context, data=None):
            primary_pump_b = context.baseline
            primary_pump_power_per_flow_rate = primary_pump_b[
                "pump_power_per_flow_rate"
            ]
            return {
                "primary_pump_power_per_flow_rate": primary_pump_power_per_flow_rate
            }

        def rule_check(self, context, calc_vals=None, data=None):
            primary_pump_power_per_flow_rate = calc_vals[
                "primary_pump_power_per_flow_rate"
            ]
            return primary_pump_power_per_flow_rate == REQUIRED_PUMP_POWER_PER_FLOW_RATE
