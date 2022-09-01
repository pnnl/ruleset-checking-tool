from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.utils.assertions import getattr_

APPLICABLE_SYS_TYPES = [
    "SYS-1",
    "SYS-5",
    "SYS-7",
    "SYS-11.2",
    "SYS-12",
    "SYS-1A",
    "SYS-7A",
    "SYS-11.2A",
    "SYS-12A",
    "SYS-1B",
    "SYS-3B",
    "SYS-5B",
    "SYS-6B",
    "SYS-7B",
    "SYS-8B",
    "SYS-9B",
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
FLUID_LOOP = schema_enums["FluidLoopOptions"]


class Section21Rule11(RuleDefinitionListIndexedBase):
    """Rule 11 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(Section21Rule11, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section21Rule11.HeatingFluidLoopRule(),
            index_rmr="baseline",
            id="21-11",
            description="The baseline building design uses boilers or purchased hot water, the hot water pumping system shall be modeled as primary-only.",
            list_path="ruleset_model_instances[0].fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmd_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11B": ["hvac_sys_11_b"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.baseline
        return getattr_(fluid_loop_b, "FluidLoop", "type") == FLUID_LOOP.HEATING

    class HeatingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section21Rule11.HeatingFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def get_calc_vals(self, context, data=None):
            heating_fluid_loop_b = context.baseline
            return {"has_child_loops": bool(heating_fluid_loop_b.get("child_loops"))}

        def rule_check(self, context, calc_vals=None, data=None):
            has_child_loops = calc_vals["has_child_loops"]
            return not has_child_loops
