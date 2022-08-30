from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_baseline_system_types import get_baseline_system_types
from rct229.utils.jsonpath_utils import find_all

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
HEATING = schema_enums["FluidLoopOptions"].HEATING


class Section21Rule16(RuleDefinitionListIndexedBase):
    """Rule 16 of ASHRAE 90.1-2019 Appendix G Section 23 (Hot water loop)"""

    def __init__(self):
        super(Section21Rule16, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section21Rule16.RuleSetModelInstanceRule(),
            index_rmr="baseline",
            id="21-16",
            description="Baseline shall have only one heating hot water plant.",
            rmr_context="ruleset_model_instances/0",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7B": ["hvac_sys_7_b"],
            "SYS-11C": ["hvac_sys_11_c"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    class RuleSetModelInstanceRule(RuleDefinitionBase):
        def __init__(self):
            super(Section21Rule16.RuleSetModelInstanceRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def get_calc_vals(self, context, data=None):
            heating_fluid_loop_b = context.baseline
            bool_hhw_loop_count = (
                len(
                    find_all(
                        "fluid_loops[?type == HEATING]",
                        heating_fluid_loop_b,
                    )
                )
                == 1
            )
            return {"bool_hhw_loop_count": bool_hhw_loop_count}

        def rule_check(self, context, calc_vals=None, data=None):
            bool_hhw_loop_count = calc_vals["bool_hhw_loop_count"]
            return bool_hhw_loop_count
