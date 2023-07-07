from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
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
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_11_1B,
]

REQUIRED_PUMP_POWER_PER_FLOW_RATE = 12 * ureg("W/gpm")


class Section22Rule26(RuleDefinitionListIndexedBase):
    """Rule 26 of ASHRAE 90.1-2019 Appendix G Section 22 (Hot water loop)"""

    def __init__(self):
        super(Section22Rule26, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule26.PrimaryCoolingFluidLoop(),
            index_rmr="baseline",
            id="22-26",
            description="For chilled-water systems served by chiller(s) and serves baseline System-11, the baseline building constant-volume primary pump power shall be modeled as 12 W/gpm.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.10 Chilled-water pumps (Systems 7, 8, 11, 12, and 13)",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list contains all HVAC systems that are modeled in the rmi_b
        available_sys_types = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmi_b)

        return (
            any(
                [
                    available_type in APPLICABLE_SYS_TYPES
                    for available_type in available_sys_types
                ]
            )
            and len(primary_secondary_loop_dict) > 0
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        primary_secondary_loops_dict = get_primary_secondary_loops_dict(rmi_b)
        return {"primary_secondary_loops_dict": primary_secondary_loops_dict}

    def list_filter(self, context_item, data):
        fluid_loop = context_item.baseline
        primary_loop_ids = data["primary_secondary_loops_dict"].keys()
        return fluid_loop["id"] in primary_loop_ids

    class PrimaryCoolingFluidLoop(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule26.PrimaryCoolingFluidLoop, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["pump_power_per_flow_rate"],
                },
            )

        def get_calc_vals(self, context, data=None):
            primary_pump_b = context.baseline
            primary_pump_power_per_flow_rate = primary_pump_b[
                "pump_power_per_flow_rate"
            ]
            return {
                "primary_pump_power_per_flow_rate": CalcQ(
                    "power_per_flow_rate", primary_pump_power_per_flow_rate
                ),
                "required_pump_power_per_flow_rate": CalcQ(
                    "power_per_flow_rate", REQUIRED_PUMP_POWER_PER_FLOW_RATE
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            primary_pump_power_per_flow_rate = calc_vals[
                "primary_pump_power_per_flow_rate"
            ]
            required_pump_power_per_flow_rate = calc_vals[
                "required_pump_power_per_flow_rate"
            ]
            return std_equal(
                required_pump_power_per_flow_rate, primary_pump_power_per_flow_rate
            )
