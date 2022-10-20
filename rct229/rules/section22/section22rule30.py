from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = ["SYS-11.1", "SYS-11.2", "SYS-11B"]
REQUIRED_PUMP_POWER = 22 * ureg("W/gpm")


class Section22Rule30(RuleDefinitionBase):
    """Rule 30 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule30, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            id="22-30",
            description="For chilled-water systems served by chiller(s) and serves baseline System-11, condenser-water pump power shall be 22 W/gpm.",
            rmr_context="ruleset_model_instances/0",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-11.1": ["hvac_sys_11.1"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    def get_calc_vals(self, context, data=None):
        rmi_b = context.baseline

        condenser_loop_pump_power_list = [
            True
            if std_equal(
                find_exactly_one_with_field_value(
                    "$..fluid_loops[*]", "id", condenser_loop_id, rmi_b
                ).get("pump_power_per_flow_rate"),
                REQUIRED_PUMP_POWER,
            )
            else False
            for condenser_loop_id in find_all("chillers[*].condensing_loop", rmi_b)
        ]
        return {"condenser_loop_pump_power_list": condenser_loop_pump_power_list}

    def rule_check(self, context, calc_vals=None, data=None):
        condenser_loop_pump_power_list = calc_vals["condenser_loop_pump_power_list"]
        return all(condenser_loop_pump_power_list)
