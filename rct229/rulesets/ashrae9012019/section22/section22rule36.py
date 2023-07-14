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
from rct229.rulesets.ashrae9012019.ruleset_functions.get_primary_secondary_loops_dict import (
    get_primary_secondary_loops_dict,
)
from rct229.utils.assertions import getattr_

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
    HVAC_SYS.SYS_7B,
    HVAC_SYS.SYS_8B,
    HVAC_SYS.SYS_11_1B,
    HVAC_SYS.SYS_12B,
]

FluidLoopFlowControl = schema_enums["FluidLoopFlowControlOptions"]


class Section22Rule36(RuleDefinitionListIndexedBase):
    """Rule 36 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule36, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section22Rule36.PrimaryFluidlLoop(),
            index_rmr="baseline",
            id="22-36",
            description="Baseline chilled water system that does not use purchased chilled water shall be modeled with constant flow primary loop and variable flow secondary loop.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.10 Chilled-Water Pumps (Systems 7, 8, 11, 12, and 13)",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="fluid_loops[*]",
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

        # primary secondary loop
        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmi_b)

        return (
            any(
                [
                    available_type in APPLICABLE_SYS_TYPES
                    for available_type in available_type_list
                ]
            )
            and primary_secondary_loop_dict
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        # create primary secondary loop
        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmi_b)
        return {"primary_secondary_loop_dict": primary_secondary_loop_dict}

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.baseline
        primary_loop_ids = data["primary_secondary_loop_dict"]
        return fluid_loop_b["id"] in primary_loop_ids

    class PrimaryFluidlLoop(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule36.PrimaryFluidlLoop, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$": ["cooling_or_condensing_design_and_control"],
                    "$.cooling_or_condensing_design_and_control": ["flow_control"],
                },
            )

        def get_calc_vals(self, context, data=None):
            primary_loop_b = context.baseline
            primary_loop_flow_control = primary_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["flow_control"]

            # The logic in list_filter ensures this primary loop has child loops
            secondary_loops = primary_loop_b["child_loops"]
            # For reporting purpose
            secondary_loop_ids = [
                secondary_loop["id"] for secondary_loop in secondary_loops
            ]
            secondary_loops_flow_control = [
                getattr_(
                    secondary_loop,
                    "child loops",
                    "cooling_or_condensing_design_and_control",
                    "flow_control",
                )
                for secondary_loop in secondary_loops
            ]

            return {
                "primary_loop_flow_control": primary_loop_flow_control,
                "secondary_loop_ids": secondary_loop_ids,
                "secondary_loops_flow_control": secondary_loops_flow_control,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            primary_loop_flow_control = calc_vals["primary_loop_flow_control"]
            secondary_loops_flow_control = calc_vals["secondary_loops_flow_control"]
            return primary_loop_flow_control == FluidLoopFlowControl.FIXED_FLOW and all(
                secondary_loop_flow_control == FluidLoopFlowControl.VARIABLE_FLOW
                for secondary_loop_flow_control in secondary_loops_flow_control
            )
