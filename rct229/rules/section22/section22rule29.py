from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value

APPLICABLE_SYS_TYPES = [
    "SYS-7",
    "SYS-8",
    "SYS-12",
    "SYS-13",
    "SYS-7B",
    "SYS-8B",
    "SYS-12B",
    "SYS-13B",
]
NOT_APPLICABLE_SYS_TYPES = ["SYS-11.1", "SYS-11.2", "SYS-11B"]
REQUIRED_PUMP_POWER = 19 * ureg("W/gpm")


class Section22Rule29(RuleDefinitionBase):
    """Rule 29 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule29, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            # index_rmr="baseline",
            id="22-29",
            description="For chilled-water systems served by chiller(s) and does not serve baseline System-11, condenser-water pump power shall be 19 W/gpm.",
            rmr_context="ruleset_model_instances/0",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11": ["hvac_sys_11"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        ) and not any(
            [key in NOT_APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    def get_calc_vals(self, context, data=None):
        rmi_b = context.baseline
        condenser_loop_pump_power_list = [
            True
            if find_exactly_one_with_field_value(
                "$..fluid_loops[*]", "id", condenser_loop_id, rmi_b
            ).get("pump_power_per_flow_rate")
            == REQUIRED_PUMP_POWER
            else False
            for condenser_loop_id in find_all("chillers[*].condensing_loop", rmi_b)
        ]
        return {"condenser_loop_pump_power_list": condenser_loop_pump_power_list}

    def rule_check(self, context, calc_vals=None, data=None):
        condenser_loop_pump_power_list = calc_vals["condenser_loop_pump_power_list"]
        return all(condenser_loop_pump_power_list)
