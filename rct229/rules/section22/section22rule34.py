from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
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
    HVAC_SYS.SYS_13B,
]


class Section22Rule34(RuleDefinitionListIndexedBase):
    """Rule 34 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule34, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule34.ChillerFluidLoopRule(),
            index_rmr="baseline",
            id="22-34",
            description="For baseline cooling chilled water plant that is served by chiller(s), the capacity shall be based on coincident loads.",
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
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_lists
            ]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        chiller_loop_ids = find_all("chillers[*].cooling_loop", rmi_b)
        return {"loop_chiller_dict": chiller_loop_ids}

    class ChillerFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule34.ChillerFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["cooling_or_condensing_design_and_control"],
                    "cooling_or_condensing_design_and_control": [
                        "is_sized_using_coincident_load"
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.baseline
            is_sized_using_coincident_load_bool = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["is_sized_using_coincident_load"]
            return {
                "is_sized_using_coincident_load": is_sized_using_coincident_load_bool
            }

        def rule_check(self, context, calc_vals=None, data=None):
            is_sized_using_coincident_load_bool = calc_vals[
                "is_sized_using_coincident_load_bool"
            ]
            return is_sized_using_coincident_load_bool
