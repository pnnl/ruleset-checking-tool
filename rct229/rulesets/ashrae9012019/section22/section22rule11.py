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


class Section22Rule11(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule11, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section22Rule11.ChillerFluidLoopRule(),
            index_rmr=BASELINE_0,
            id="22-11",
            description="For Baseline chilled-water system that does not use purchased chilled water, variable-flow secondary pump shall be modeled as 13W/gpm at design conditions.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.10 Chilled-water pumps (System 7, 8, 11, 12 and 13)",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.BASELINE_0

        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list contains all HVAC systems that are modeled in the rmi_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]

        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmi_b)

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
        rmi_b = context.BASELINE_0

        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmi_b)

        return {"primary_secondary_loop_dict": primary_secondary_loop_dict}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.BASELINE_0
        primary_secondary_loop_dict = data["primary_secondary_loop_dict"]

        return fluid_loop_b["id"] in primary_secondary_loop_dict

    class ChillerFluidLoopRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section22Rule11.ChillerFluidLoopRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=Section22Rule11.ChillerFluidLoopRule.SecondaryChildLoopRule(),
                index_rmr=BASELINE_0,
                list_path="$.child_loops[*]",
            )

        class SecondaryChildLoopRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    Section22Rule11.ChillerFluidLoopRule.SecondaryChildLoopRule, self
                ).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    required_fields={
                        "$": ["pump_power_per_flow_rate"],
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
                        "power_per_volumetric_flow_rate",
                        secondary_loop_pump_power_per_flow_rate,
                    ),
                    "req_pump_flow_rate": CalcQ(
                        "power_per_volumetric_flow_rate", req_pump_flow_rate
                    ),
                }

            def rule_check(self, context, calc_vals=None, data=None):
                secondary_loop_pump_power_per_flow_rate = calc_vals[
                    "secondary_loop_pump_power_per_flow_rate"
                ]
                req_pump_flow_rate = calc_vals["req_pump_flow_rate"]

                return std_equal(
                    secondary_loop_pump_power_per_flow_rate, req_pump_flow_rate
                )
