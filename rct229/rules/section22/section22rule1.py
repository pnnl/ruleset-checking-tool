from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = ["SYS-7", "SYS-8", "SYS-11.1", "SYS-11.2", "SYS-12", "SYS-13", "SYS-1A", "SYS-3A", "SYS-7A", "SYS-8A", "SYS-11.1A", "SYS-11.2A", "SYS-12A", "SYS-13A", "SYS-7B", "SYS-8B", "SYS-11B", "SYS-12B", "SYS-13B", "SYS-1C", "SYS-3C", "SYS-7C", "SYS-11C", "SYS-12C", "SYS-13C"]
DESIGN_SUPPLY_TEMP = 44 * ureg("degF")


class Section22Rule1(RuleDefinitionListIndexedBase):
    """Rule 1 of ASHRAE 90.1-2019 Appendix G Section 22 (Hot water loop)"""

    def __init__(self):
        super(Section22Rule1, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule1.ChillerFluidLoopRule(),
            index_rmr="baseline",
            id="22-1",
            description="Baseline chilled water design supply temperature shall be modeled at 44F.",
            rmr_context="ruleset_model_instances/0",
            list_path="fluid_loops[*]",
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        chillers = find_all("$.chillers[*]", rmi_b)
        loop_chiller_dict = {}
        for chiller_b in chillers:
            loop_id = getattr_(chiller_b, "chiller", "loop")
            if not loop_id in loop_chiller_dict.keys():
                loop_chiller_dict[loop_id] = []
            loop_chiller_dict[loop_id].append(chiller_b)
        return {"loop_chiller_dict": loop_chiller_dict}

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        # FIXME: replace with baseline_system_types = get_baseline_system_types(rmi_b) when get_baseline_system_types
        #  is ready.
        baseline_system_types = {
            "SYS-7": ["hvac_sys_7"],
            "SYS-11-a": ["hvac_sys_11_a"],
        }
        # if any system type found in the APPLICABLE_SYS_TYPES then return applicable.
        return any(
            [key in APPLICABLE_SYS_TYPES for key in baseline_system_types.keys()]
        )

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.baseline
        loop_chiller_dict = data["loop_chiller_dict"]
        return fluid_loop_b["id"] in loop_chiller_dict.keys()

    class ChillerFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule1.ChillerFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.baseline
            design_supply_temperature = fluid_loop_b["heating_design_and_control"][
                "design_supply_temperature"
            ]

            return {"design_supply_temperature": design_supply_temperature}


        def rule_check(self, context, calc_vals=None, data=None):
            design_supply_temperature = calc_vals["design_supply_temperature"]
            return design_supply_temperature == DESIGN_SUPPLY_TEMP
