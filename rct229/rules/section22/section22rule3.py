from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all

APPLICABLE_SYS_TYPES = [
    "SYS-7",
    "SYS-8",
    "SYS-12",
    "SYS-13",
    "SYS-7B",
    "SYS-8B",
    "SYS-12B",
    "SYS-13B",
]
NOT_APPLICABLE_SYS_TYPES = [
    "SYS-11.1",
    "SYS-11.2",
    "SYS-11.1A",
    "SYS-11.2A",
    "SYS-11B",
    "SYS-11C",
]
TEMP_RETURN_TYPE = schema_enums["TemperatureResetOptions"]


class Section22Rule3(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 22 (Hot water loop)"""

    def __init__(self):
        super(Section22Rule3, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule3.ChillerFluidLoopRule(),
            index_rmr="baseline",
            id="22-3",
            description="For Baseline chilled water loop that is not purchased cooling, chilled-water supply temperature shall be reset based on outdoor dry-bulb temperature if loop does not serve any Baseline System Type-11.",
            rmr_context="ruleset_model_instances/0",
            list_path="fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11": ["hvac_sys_11"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES and not found in NOT_APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        ) and not any(
            [key in NOT_APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        chiller_loop_ids = find_all("chillers[*].cooling_loop", rmi_b)
        return {"loop_chiller_dict": chiller_loop_ids}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.baseline
        loop_chiller_dict = data["loop_chiller_dict"]
        return fluid_loop_b["id"] in loop_chiller_dict

    class ChillerFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule3.ChillerFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["cooling_or_condensing_design_and_control"],
                    "cooling_or_condensing_design_and_control": [
                        "temperature_reset_type"
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.baseline
            temperature_reset_type = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["temperature_reset_type"]
            return {"temperature_reset_type": temperature_reset_type}

        def rule_check(self, context, calc_vals=None, data=None):
            temperature_reset_type = calc_vals["temperature_reset_type"]
            return temperature_reset_type == TEMP_RETURN_TYPE.OUTSIDE_AIR_RESET
