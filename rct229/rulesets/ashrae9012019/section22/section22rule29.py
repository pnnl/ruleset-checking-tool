from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
    find_exactly_one_fluid_loop,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
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


class Section22Rule29(RuleDefinitionListIndexedBase):
    """Rule 29 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule29, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule29.CondensingFluidLoopRule(),
            index_rmr="baseline",
            id="22-29",
            description="For chilled-water systems served by chiller(s) and does not serve baseline System-11, condenser-water pump power shall be 19 W/gpm.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.11 Heat Rejection (Systems 7, 8, 11, 12, and 13)",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list containing all HVAC systems that are modeled in the rmi_b
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
        ) and not any(
            [
                available_type in NOT_APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        condenser_loop_pump_power_dict = {
            chiller["condensing_loop"]: find_exactly_one_fluid_loop(
                rmi_b, getattr_(chiller, "Chiller", "condensing_loop")
            ).get("pump_power_per_flow_rate")
            for chiller in find_all("chillers[*]", rmi_b)
        }
        return {"condenser_loop_pump_power_dict": condenser_loop_pump_power_dict}

    def list_filter(self, context_item, data):
        fluid_loops_b = context_item.baseline
        return fluid_loops_b.get("pump_power_per_flow_rate")

    class CondensingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule29.CondensingFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.baseline
            pump_power_per_flow_rate = fluid_loop_b["pump_power_per_flow_rate"]
            required_pump_power = REQUIRED_PUMP_POWER

            return {
                "pump_power_per_flow_rate": CalcQ(
                    "power_per_flow_rate", pump_power_per_flow_rate
                ),
                "required_pump_power": CalcQ(
                    "power_per_flow_rate", required_pump_power
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            pump_power_per_flow_rate = calc_vals["pump_power_per_flow_rate"]
            required_pump_power = calc_vals["required_pump_power"]

            return std_equal(pump_power_per_flow_rate, required_pump_power)
