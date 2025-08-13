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
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_1A,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_12A,
]
REQUIRED_PUMP_POWER_PER_FLOW_RATE = 19.0 * ureg("W/gpm")


class PRM9012019Rule39a29(RuleDefinitionListIndexedBase):
    """Rule 9 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(PRM9012019Rule39a29, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule39a29.HeatingFluidLoopRule(),
            index_rmd=BASELINE_0,
            id="21-9",
            description="When baseline building includes boilers, Hot Water Pump Power = 19W/gpm.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model",
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
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        boiler_loop_ids = find_all("boilers[*].loop", rmd_b)
        return {"loop_boiler_dict": boiler_loop_ids}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.BASELINE_0
        loop_boiler_dict = data["loop_boiler_dict"]
        return fluid_loop_b["id"] in loop_boiler_dict

    class HeatingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule39a29.HeatingFluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["pump_power_per_flow_rate"],
                },
                precision={
                    "pump_power_per_flow_rate": {
                        "precision": 0.1,
                        "unit": "W/gpm",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.BASELINE_0
            pump_power_per_flow_rate = fluid_loop_b["pump_power_per_flow_rate"]
            return {
                "pump_power_per_flow_rate": CalcQ(
                    "power_per_liquid_flow_rate", pump_power_per_flow_rate
                ),
                "required_pump_power_per_flow_rate": CalcQ(
                    "power_per_liquid_flow_rate", REQUIRED_PUMP_POWER_PER_FLOW_RATE
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            pump_power_per_flow_rate = calc_vals["pump_power_per_flow_rate"]
            required_pump_power_per_flow_rate = calc_vals[
                "required_pump_power_per_flow_rate"
            ]
            return self.precision_comparison["pump_power_per_flow_rate"](
                pump_power_per_flow_rate, required_pump_power_per_flow_rate
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            pump_power_per_flow_rate = calc_vals["pump_power_per_flow_rate"]
            required_pump_power_per_flow_rate = calc_vals[
                "required_pump_power_per_flow_rate"
            ]
            return std_equal(
                required_pump_power_per_flow_rate, pump_power_per_flow_rate
            )
