from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all

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
REQUIRED_PUMP_POWER_PER_FLOW_RATE = 19.0 * ureg("W/gpm")


class Section21Rule9(RuleDefinitionListIndexedBase):
    """Rule 9 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(Section21Rule9, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section21Rule9.HeatingFluidLoopRule(),
            index_rmr="baseline",
            id="21-9",
            description="When baseline building includes boilers, Hot Water Pump Power = 19W/gpm.",
            rmr_context="ruleset_model_instances/0",
            list_path="fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-12": ["hvac_sys_12"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        boiler_loop_ids = find_all("boilers[*].loop", rmi_b)
        return {"loop_boiler_dict": boiler_loop_ids}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.baseline
        loop_boiler_dict = data["loop_boiler_dict"]
        return fluid_loop_b["id"] in loop_boiler_dict

    class HeatingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section21Rule9.HeatingFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["pump_power_per_flow_rate"],
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.baseline
            pump_power_per_flow_rate = fluid_loop_b["pump_power_per_flow_rate"]
            return {
                "pump_power_per_flow_rate": pump_power_per_flow_rate,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            pump_power_per_flow_rate = calc_vals["pump_power_per_flow_rate"]
            return pump_power_per_flow_rate == REQUIRED_PUMP_POWER_PER_FLOW_RATE
