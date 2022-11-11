from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.ruleset_functions.get_primary_secondary_loops_dict import (
    get_primary_secondary_loops_dict,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_12B,
]
PUMP_SPPED_CONTROL = schema_enums["PumpSpeedControlOptions"]
MAX_FIXED_SPEED_CHW_LOOP_COOLING_CAPACITY = 300.0 * ureg("ton")


class Section22Rule10(RuleDefinitionListIndexedBase):
    """Rule 10 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule10, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule10.ChillerFluidLoopRule(),
            index_rmr="baseline",
            id="22-10",
            description="For Baseline chilled water system with cooling capacity less than 300ton, the secondary pump shall be modeled as riding the pump curve. For Baseline chilled water system with cooling capacity of 300 tons or more, the secondary pump shall be modeled with variable-speed drives.",
            list_path="ruleset_model_instances[0].fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmr_baseline = context.baseline
        rmi_b = rmr_baseline["ruleset_model_instances"][0]
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list contains all HVAC systems that are modeled in the rmi_b
        available_type_lists = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]

        primary_secondary_loop_dictionary = get_primary_secondary_loops_dict(rmi_b)

        return (
            any(
                [
                    available_type in APPLICABLE_SYS_TYPES
                    for available_type in available_type_lists
                ]
            )
            and primary_secondary_loop_dictionary
        )

    def create_data(self, context, data):
        rmr_baseline = context.baseline
        rmi_b = rmr_baseline["ruleset_model_instances"][0]

        loop_pump_dictionary = {
            pump["loop_or_piping"]: pump for pump in find_all("pumps[*]", rmi_b)
        }

        chw_loop_capacity_dict = {}
        for chiller in find_all("chillers[*]", rmi_b):
            if chiller["cooling_loop"] not in chw_loop_capacity_dict.keys():
                chw_loop_capacity_dict[chiller["cooling_loop"]] = ZERO.POWER
            chw_loop_capacity_dict[chiller["cooling_loop"]] += getattr_(
                chiller, "chiller", "rated_capacity"
            )

        primary_secondary_loop_dictionary = get_primary_secondary_loops_dict(rmi_b)

        return {
            "loop_pump_dictionary": loop_pump_dictionary,
            "chw_loop_capacity_dict": chw_loop_capacity_dict,
            "primary_secondary_loop_dictionary": primary_secondary_loop_dictionary,
        }

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.baseline
        chw_loop_capacity_dict = data["chw_loop_capacity_dict"]

        return fluid_loop_b["id"] in chw_loop_capacity_dict.keys()

    class ChillerFluidLoopRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section22Rule10.ChillerFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                each_rule=Section22Rule10.ChillerFluidLoopRule.SecondaryChildLoopRule(),
                index_rmr="baseline",
                list_path="$..child_loops[*]",
            )

        def create_data(self, context, data):
            fluid_loop_b = context.baseline
            chw_loop_capacity_dict = data["chw_loop_capacity_dict"]

            if (
                chw_loop_capacity_dict[fluid_loop_b["id"]]
                < MAX_FIXED_SPEED_CHW_LOOP_COOLING_CAPACITY
            ):
                target_secondary_pump_type = PUMP_SPPED_CONTROL.FIXED_SPEED
            else:
                target_secondary_pump_type = PUMP_SPPED_CONTROL.VARIABLE_SPEED

            return {**data, "target_secondary_pump_type": target_secondary_pump_type}

        def list_filter(self, context_item, data):
            child_loop_b = context_item.baseline
            loop_pump_dictionary = data["loop_pump_dictionary"]

            return child_loop_b["id"] in loop_pump_dictionary.keys()

        class SecondaryChildLoopRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    Section22Rule10.ChillerFluidLoopRule.SecondaryChildLoopRule, self
                ).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, False),
                )

            def get_calc_vals(self, context, data=None):
                child_loop_b = context.baseline
                loop_pump_dictionary = data["loop_pump_dictionary"]
                secondary_pump_speed_control = loop_pump_dictionary[child_loop_b["id"]][
                    "speed_control"
                ]

                return {"secondary_pump_speed_control": secondary_pump_speed_control}

            def rule_check(self, context, calc_vals=None, data=None):
                secondary_pump_speed_control = calc_vals["secondary_pump_speed_control"]
                target_secondary_pump_type = data["target_secondary_pump_type"]

                return secondary_pump_speed_control == target_secondary_pump_type
