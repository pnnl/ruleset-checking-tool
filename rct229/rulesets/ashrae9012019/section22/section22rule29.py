from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal
from rct229.utils.utility_functions import find_exactly_one_fluid_loop

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
FluidLoopOptions = SchemaEnums.schema_enums["FluidLoopOptions"]


class PRM9012019Rule60w01(RuleDefinitionListIndexedBase):
    """Rule 29 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule60w01, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule60w01.CondensingFluidLoopRule(),
            index_rmd=BASELINE_0,
            id="22-29",
            description="Baseline chilled water loops that do not use purchased chilled water and do not serve computer rooms (i.e., do not serve baseline system type 11) shall have a condenser water pump power of 19 W/gpm at design conditions.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.11 Heat Rejection (Systems 7, 8, 11, 12, and 13)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list containing all HVAC systems that are modeled in the rmd_b
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
        rmd_b = context.BASELINE_0
        condenser_loop_pump_power_dict = {
            chiller["condensing_loop"]: find_exactly_one_fluid_loop(
                rmd_b, getattr_(chiller, "Chiller", "condensing_loop")
            ).get("pump_power_per_flow_rate")
            for chiller in find_all("$.chillers[*]", rmd_b)
        }
        return {"condenser_loop_pump_power_dict": condenser_loop_pump_power_dict}

    def list_filter(self, context_item, data):
        fluid_loops_b = context_item.BASELINE_0
        return fluid_loops_b.get("type") == FluidLoopOptions.CONDENSER

    class CondensingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule60w01.CondensingFluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["pump_power_per_flow_rate"],
                },
                precision={
                    "pump_power_per_flow_rate": {
                        "precision": 1,
                        "unit": "W/gpm",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.BASELINE_0
            pump_power_per_flow_rate = fluid_loop_b["pump_power_per_flow_rate"]
            required_pump_power = REQUIRED_PUMP_POWER

            return {
                "pump_power_per_flow_rate": CalcQ(
                    "power_per_liquid_flow_rate", pump_power_per_flow_rate
                ),
                "required_pump_power": CalcQ(
                    "power_per_liquid_flow_rate", required_pump_power
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            pump_power_per_flow_rate = calc_vals["pump_power_per_flow_rate"]
            required_pump_power = calc_vals["required_pump_power"]

            return self.precision_comparison["pump_power_per_flow_rate"](
                pump_power_per_flow_rate,
                required_pump_power,
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            pump_power_per_flow_rate = calc_vals["pump_power_per_flow_rate"]
            required_pump_power = calc_vals["required_pump_power"]

            return std_equal(pump_power_per_flow_rate, required_pump_power)
