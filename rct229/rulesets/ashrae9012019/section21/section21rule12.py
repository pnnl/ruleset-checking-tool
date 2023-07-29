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

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_1A,
    HVAC_SYS.SYS_7A,
    HVAC_SYS.SYS_11_2A,
    HVAC_SYS.SYS_12A,
    HVAC_SYS.SYS_1B,
    HVAC_SYS.SYS_3B,
    HVAC_SYS.SYS_5B,
    HVAC_SYS.SYS_6B,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_9B,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_12B,
    HVAC_SYS.SYS_1C,
    HVAC_SYS.SYS_3C,
    HVAC_SYS.SYS_7C,
    HVAC_SYS.SYS_11_1C,
]
FLUID_LOOP = schema_enums["FluidLoopOptions"]
FLUID_LOOP_FLOW_CONTROL = schema_enums["FluidLoopFlowControlOptions"]
FLUID_LOOP_FLOW_OPERATION = schema_enums["FluidLoopOperationOptions"]


class Section21Rule12(RuleDefinitionListIndexedBase):
    """Rule 12 of ASHRAE 90.1-2019 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(Section21Rule12, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section21Rule12.HeatingFluidLoopRule(),
            index_rmr="baseline",
            id="21-12",
            description="The baseline building design uses boilers or purchased hot water, the hot water pumping system shall be modeled with continuous variable flow.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        # create a list containing all HVAC systems that are modeled in the rmi_b
        available_type_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
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
        return getattr_(fluid_loop_b, "FluidLoop", "type") == FLUID_LOOP.HEATING

    class HeatingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section21Rule12.HeatingFluidLoopRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["heating_design_and_control"],
                    "heating_design_and_control": ["flow_control", "operation"],
                },
            )

        def get_calc_vals(self, context, data=None):
            heating_fluid_loop_b = context.baseline
            flow_control = heating_fluid_loop_b["heating_design_and_control"][
                "flow_control"
            ]
            operation = heating_fluid_loop_b["heating_design_and_control"]["operation"]
            return {"flow_control": flow_control, "operation": operation}

        def rule_check(self, context, calc_vals=None, data=None):
            flow_control = calc_vals["flow_control"]
            operation = calc_vals["operation"]

            return (
                flow_control == FLUID_LOOP_FLOW_CONTROL.VARIABLE_FLOW
                and operation == FLUID_LOOP_FLOW_OPERATION.CONTINUOUS
            )
