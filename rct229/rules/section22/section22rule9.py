from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.ruleset_functions.get_primary_secondary_loops_dict import (
    get_primary_secondary_loops_dict,
)
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_11B,
    HVAC_SYS.SYS_12B,
]
MIN_FLOW_FRACTION = 0.25
MIN_CHW_PRIMARY_LOOP_COOLING_CAPACITY = 300.0 * ureg("ton")


class Section22Rule9(RuleDefinitionListIndexedBase):
    """Rule 9 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule9, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule9.ChillerFluidLoopRule(),
            index_rmr="baseline",
            id="22-9",
            description="For Baseline chilled water system with cooling capacity of 300 tons or more, the secondary loop shall be modeled with a minimum flow of 25% of the design flow rate.",
            rmr_context="ruleset_model_instances/0",
            list_path="fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
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
        rmi_b = context.baseline
        chw_loop_capacity_dict = {}
        for chiller in find_all("chillers[*]", rmi_b):
            if chiller["cooling_loop"] not in chw_loop_capacity_dict.keys():
                chw_loop_capacity_dict[chiller["cooling_loop"]] = 0.0 * ureg("W")
                chw_loop_capacity_dict[chiller["cooling_loop"]] += chiller[
                    "rated_capacity"
                ]

        primary_secondary_loop_dictionary = get_primary_secondary_loops_dict(rmi_b)

        return {
            "chw_loop_capacity_dict": chw_loop_capacity_dict,
            "primary_secondary_loop_dictionary": primary_secondary_loop_dictionary,
        }

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.baseline
        primary_secondary_loop_dictionary = data["primary_secondary_loop_dictionary"]
        chw_loop_capacity_dict = data["chw_loop_capacity_dict"]

        return (
            fluid_loop_b["id"] in primary_secondary_loop_dictionary.keys()
            and chw_loop_capacity_dict[fluid_loop_b["id"]]
            >= MIN_CHW_PRIMARY_LOOP_COOLING_CAPACITY
        )

    class ChillerFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule9.ChillerFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.baseline

            for secondary_loop_id_b in fluid_loop_b["child_loops"]:
                secondary_loop_min_flow_rate = secondary_loop_id_b[
                    "cooling_or_condensing_design_and_control"
                ]["minimum_flow_fraction"]

            return {"secondary_loop_min_flow_rate": secondary_loop_min_flow_rate}

        def rule_check(self, context, calc_vals=None, data=None):
            secondary_loop_min_flow_rate = calc_vals["secondary_loop_min_flow_rate"]

            return secondary_loop_min_flow_rate == MIN_FLOW_FRACTION
