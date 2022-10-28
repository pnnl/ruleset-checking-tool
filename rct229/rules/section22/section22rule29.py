from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
    find_exactly_one_loop,
)
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_12B,
]
NOT_APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_11_1, HVAC_SYS.SYS_11_2, HVAC_SYS.SYS_11_1B]
REQUIRED_PUMP_POWER = 19 * ureg("W/gpm")


class Section22Rule29(RuleDefinitionBase):
    """Rule 29 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule29, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            id="22-29",
            description="For chilled-water systems served by chiller(s) and does not serve baseline System-11, condenser-water pump power shall be 19 W/gpm.",
            rmr_context="ruleset_model_instances/0",
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
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_lists
            ]
        ) and not any(
            [
                available_type in NOT_APPLICABLE_SYS_TYPES
                for available_type in available_type_lists
            ]
        )

    def get_calc_vals(self, context, data=None):
        rmi_b = context.baseline
        condenser_loop_pump_power_list = [
            find_exactly_one_loop(rmi_b, condenser_loop_id).get(
                "pump_power_per_flow_rate"
            )
            for condenser_loop_id in find_all("chillers[*].condensing_loop", rmi_b)
        ]
        return {"condenser_loop_pump_power_list": condenser_loop_pump_power_list}

    def rule_check(self, context, calc_vals=None, data=None):
        condenser_loop_pump_power_list = calc_vals["condenser_loop_pump_power_list"]
        return all([
            std_equal(pump_power, REQUIRED_PUMP_POWER)
            for pump_power in condenser_loop_pump_power_list
        ])
