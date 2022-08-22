from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_baseline_system_types import mock_get_baseline_system_types
from rct229.utils.assertions import getattr_

APPLICABLE_SYS_TYPES = ["SYS-1", "SYS-5", "SYS-7", "SYS-11.2", "SYS-12", "SYS-1A", "SYS-7A", "SYS-11.2A", "SYS-12A"]
FLUID_LOOP = schema_enums["FluidLoopOptions"]


class Section21Rule3(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 23 (Hot water loop)"""
    def __init__(self):
        super(Section21Rule3, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section21Rule3.HeatingFluidLoopRule(),
            index_rmr="baseline",
            id="21-3",
            description="Heating hot water plant capacity shall be based on coincident loads.",
            list_path="ruleset_model_instances[0].fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmd_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {"SYS-7A": ["hvac_sys_7_a"], "SYS-11A": ["hvac_sys_11_a"]}
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any([key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()])

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.baseline
        return getattr_(fluid_loop_b, "FluidLoop", "type") == FLUID_LOOP.HEATING

    class HeatingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section21Rule3.HeatingFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["heating_design_and_control"],
                    "$.heating_design_and_control": ["is_sized_using_coincident_load"]
                }
            )

        def get_calc_vals(self, context, data=None):
            heating_fluid_loop_b = context.baseline
            is_sized_using_coincident_load = heating_fluid_loop_b["heating_design_and_control"]["is_sized_using_coincident_load"]
            return {
                "is_sized_using_coincident_load": is_sized_using_coincident_load
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return calc_vals["is_sized_using_coincident_load"]
