from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal
from rct229.utils.utility_functions import find_exactly_one_fluid_loop

APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_11_1, HVAC_SYS.SYS_11_2, HVAC_SYS.SYS_11_1B]
REQUIRED_PUMP_POWER = 22 * ureg("W/gpm")


class Section22Rule30(RuleDefinitionListIndexedBase):
    """Rule 30 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule30, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section22Rule30.CondensingFluidLoopRule(),
            index_rmr=BASELINE_0,
            id="22-30",
            description="For chilled-water systems served by chiller(s) and serves baseline System-11, condenser-water pump power shall be 22 W/gpm.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.11 Heat Rejection (Systems 7, 8, 11, 12, and 13)",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.BASELINE_0
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
        )

    def create_data(self, context, data):
        rmi_b = context.BASELINE_0
        condenser_loop_pump_power_dict = {
            chiller["condensing_loop"]: find_exactly_one_fluid_loop(
                rmi_b, chiller["condensing_loop"]
            ).get("pump_power_per_flow_rate")
            for chiller in find_all("chillers[*]", rmi_b)
        }
        return {"condenser_loop_pump_power_dict": condenser_loop_pump_power_dict}

    def list_filter(self, context_item, data):
        fluid_loops_b = context_item.BASELINE_0
        return fluid_loops_b.get("pump_power_per_flow_rate")

    class CondensingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule30.CondensingFluidLoopRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.BASELINE_0
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
