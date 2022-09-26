from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    "SYS-11.1",
    "SYS-11.2",
    "SYS-11.1A",
    "SYS-11.2A",
    "SYS-11B",
    "SYS-11C",
]
REQUIRED_LOOP_SUPPLY_TEMP_AT_LOW_LOAD = ureg("54 degF")


class Section22Rule6(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule6, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule6.ChillerFluidLoopRule(),
            index_rmr="baseline",
            id="22-6",
            description="For Baseline chilled water loop that is not purchased chilled water and serves computer room HVAC systems (System Type-11), The maximum reset chilled-water supply temperature shall be 54F.",
            rmr_context="ruleset_model_instances/0",
            list_path="fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-11.1": ["hvac_sys_11_1"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        chiller_loop_ids_list = find_all("chillers[*].cooling_loop", rmi_b)
        return {"chiller_loop_ids_list": chiller_loop_ids_list}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.baseline
        loop_chiller_list = data["chiller_loop_ids_list"]
        return fluid_loop_b["id"] in loop_chiller_list

    class ChillerFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule6.ChillerFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["cooling_or_condensing_design_and_control"],
                    "cooling_or_condensing_design_and_control": [
                        "loop_supply_temperature_at_low_load",
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.baseline
            loop_supply_temperature_at_low_load = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["loop_supply_temperature_at_low_load"]

            return {
                "loop_supply_temperature_at_low_load": CalcQ(
                    "temperature", loop_supply_temperature_at_low_load
                )
            }

        def rule_check(self, context, calc_vals=None, data=None):
            loop_supply_temperature_at_low_load = calc_vals[
                "loop_supply_temperature_at_low_load"
            ]

            return std_equal(
                loop_supply_temperature_at_low_load.to(ureg.kelvin),
                REQUIRED_LOOP_SUPPLY_TEMP_AT_LOW_LOAD.to(ureg.kelvin),
            )
