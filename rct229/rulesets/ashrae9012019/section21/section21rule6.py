from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_1A,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_12A,
]
FLUID_LOOP = schema_enums["FluidLoopOptions"]


class Section21Rule6(RuleDefinitionListIndexedBase):
    """Rule 6 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(Section21Rule6, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section21Rule6.HeatingFluidLoopRule(),
            index_rmr="baseline",
            id="21-6",
            description="When baseline building includes two boilers each shall stage as required by load.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="fluid_loops[*]",
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        boilers = find_all("$.boilers[*]", rmi_b)
        loop_boiler_dict = {}
        for boiler_b in boilers:
            loop_id = getattr_(boiler_b, "boiler", "loop")
            if not loop_id in loop_boiler_dict.keys():
                loop_boiler_dict[loop_id] = []
            loop_boiler_dict[loop_id].append(boiler_b)
        return {"loop_boiler_dict": loop_boiler_dict}

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list containing all HVAC systems that are modeled in the rmi_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict.keys()
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_type_list
            ]
        )

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.baseline
        return (
            getattr_(fluid_loop_b, "FluidLoop", "type") == FLUID_LOOP.HEATING
        )

    class HeatingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section21Rule6.HeatingFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def is_applicable(self, context, data=None):
            fluid_loop_b = context.baseline
            loop_boiler_dict = data["loop_boiler_dict"]
            return len(loop_boiler_dict[fluid_loop_b["id"]]) == 2

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.baseline
            boiler_list = data["loop_boiler_dict"][fluid_loop_b["id"]]
            # Guarantee two boilers in this list.
            boiler_1 = boiler_list[0]
            boiler_2 = boiler_list[1]

            return {
                "boiler_1_operation_lower_limit": CalcQ(
                    "capacity", getattr_(boiler_1, "boiler", "operation_lower_limit")
                ),
                "boiler_1_operation_upper_limit": CalcQ(
                    "capacity", getattr_(boiler_1, "boiler", "operation_upper_limit")
                ),
                "boiler_1_rated_capacity": CalcQ(
                    "capacity", getattr_(boiler_1, "boiler", "rated_capacity")
                ),
                "boiler_2_operation_lower_limit": CalcQ(
                    "capacity", getattr_(boiler_2, "boiler", "operation_lower_limit")
                ),
                "boiler_2_operation_upper_limit": CalcQ(
                    "capacity", getattr_(boiler_2, "boiler", "operation_upper_limit")
                ),
                "boiler_2_rated_capacity": CalcQ(
                    "capacity", getattr_(boiler_2, "boiler", "rated_capacity")
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            boiler_1_operation_lower_limit = calc_vals["boiler_1_operation_lower_limit"]
            boiler_1_operation_upper_limit = calc_vals["boiler_1_operation_upper_limit"]
            boiler_1_rated_capacity = calc_vals["boiler_1_rated_capacity"]
            boiler_2_operation_lower_limit = calc_vals["boiler_2_operation_lower_limit"]
            boiler_2_operation_upper_limit = calc_vals["boiler_2_operation_upper_limit"]
            boiler_2_rated_capacity = calc_vals["boiler_2_rated_capacity"]

            return (
                boiler_1_operation_lower_limit == ZERO.POWER
                and std_equal(boiler_1_operation_upper_limit, boiler_1_rated_capacity)
                and std_equal(boiler_2_operation_lower_limit, boiler_1_rated_capacity)
                and std_equal(
                    boiler_2_operation_upper_limit,
                    boiler_1_rated_capacity + boiler_2_rated_capacity,
                )
            ) or (
                boiler_2_operation_lower_limit == ZERO.POWER
                and std_equal(boiler_2_operation_upper_limit, boiler_2_rated_capacity)
                and std_equal(boiler_1_operation_lower_limit, boiler_2_rated_capacity)
                and std_equal(
                    boiler_1_operation_upper_limit,
                    boiler_2_rated_capacity + boiler_1_rated_capacity,
                )
            )
