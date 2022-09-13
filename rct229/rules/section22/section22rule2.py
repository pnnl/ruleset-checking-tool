from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    "SYS-7",
    "SYS-8",
    "SYS-11.1",
    "SYS-11.2",
    "SYS-12",
    "SYS-13",
    "SYS-1A",
    "SYS-3A",
    "SYS-7A",
    "SYS-8A",
    "SYS-11.1A",
    "SYS-11.2A",
    "SYS-12A",
    "SYS-13A",
    "SYS-7B",
    "SYS-8B",
    "SYS-11B",
    "SYS-12B",
    "SYS-13B",
    "SYS-1C",
    "SYS-3C",
    "SYS-7C",
    "SYS-11C",
    "SYS-12C",
    "SYS-13C",
]
DESIGN_RETURN_TEMP = 56 * ureg("degF")


class Section22Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 22 (Hot water loop)"""

    def __init__(self):
        super(Section22Rule2, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule2.ChillerFluidLoopRule(),
            index_rmr="baseline",
            id="22-2",
            description="Baseline chilled water design return temperature shall be modeled at 56F.",
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
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
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
            super(Section22Rule2.ChillerFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["cooling_or_condensing_design_and_control"],
                    "cooling_or_condensing_design_and_control": [
                        "design_return_temperature"
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.baseline
            design_return_temperature = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["design_return_temperature"]

            return {
                "design_return_temperature": CalcQ(
                    "temperature", design_return_temperature
                )
            }

        def rule_check(self, context, calc_vals=None, data=None):
            design_return_temperature = calc_vals["design_return_temperature"]
            return std_equal(
                design_return_temperature.to(ureg.kelvin),
                DESIGN_RETURN_TEMP.to(ureg.kelvin),
            )
