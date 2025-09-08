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
from rct229.rulesets.ashrae9012019.ruleset_functions.get_primary_secondary_loops_dict import (
    get_primary_secondary_loops_dict,
)
from rct229.schema.config import ureg
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
REQUIRED_PUMP_FLOW_RATE = 13 * ureg("W/gpm")


class PRM9012019Rule57w94(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule57w94, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule57w94.ChillerFluidLoopRule(),
            index_rmd=BASELINE_0,
            id="22-11",
            description="Baseline chilled water systems that do not use purchased chilled water shall have a variable-flow secondary pump power of 13 W/gpm at design conditions.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.10 Chilled-water pumps (System 7, 8, 11, 12 and 13)",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0

        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list contains all HVAC systems that are modeled in the rmd_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]

        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmd_b)

        return (
            any(
                [
                    available_type in APPLICABLE_SYS_TYPES
                    for available_type in available_type_list
                ]
            )
            and primary_secondary_loop_dict
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0

        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmd_b)

        return {"primary_secondary_loop_dict": primary_secondary_loop_dict}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.BASELINE_0
        primary_secondary_loop_dict = data["primary_secondary_loop_dict"]

        return fluid_loop_b["id"] in primary_secondary_loop_dict

    class ChillerFluidLoopRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule57w94.ChillerFluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012019Rule57w94.ChillerFluidLoopRule.SecondaryChildLoopRule(),
                index_rmd=BASELINE_0,
                list_path="$.child_loops[*]",
            )

        class SecondaryChildLoopRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule57w94.ChillerFluidLoopRule.SecondaryChildLoopRule,
                    self,
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    required_fields={
                        "$": ["pump_power_per_flow_rate"],
                    },
                    precision={
                        "secondary_loop_pump_power_per_flow_rate": {
                            "precision": 1,
                            "unit": "W/gpm",
                        },
                    },
                )

            def get_calc_vals(self, context, data=None):
                child_loop_b = context.BASELINE_0
                secondary_loop_pump_power_per_flow_rate = child_loop_b[
                    "pump_power_per_flow_rate"
                ]
                req_pump_flow_rate = REQUIRED_PUMP_FLOW_RATE

                return {
                    "secondary_loop_pump_power_per_flow_rate": CalcQ(
                        "power_per_liquid_flow_rate",
                        secondary_loop_pump_power_per_flow_rate,
                    ),
                    "req_pump_flow_rate": CalcQ(
                        "power_per_liquid_flow_rate", req_pump_flow_rate
                    ),
                }

            def rule_check(self, context, calc_vals=None, data=None):
                secondary_loop_pump_power_per_flow_rate = calc_vals[
                    "secondary_loop_pump_power_per_flow_rate"
                ]
                req_pump_flow_rate = calc_vals["req_pump_flow_rate"]

                return self.precision_comparison[
                    "secondary_loop_pump_power_per_flow_rate"
                ](
                    secondary_loop_pump_power_per_flow_rate,
                    req_pump_flow_rate,
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                secondary_loop_pump_power_per_flow_rate = calc_vals[
                    "secondary_loop_pump_power_per_flow_rate"
                ]
                req_pump_flow_rate = calc_vals["req_pump_flow_rate"]

                return std_equal(
                    secondary_loop_pump_power_per_flow_rate, req_pump_flow_rate
                )
