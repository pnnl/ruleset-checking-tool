from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012022 import BASELINE_0
from rct229.rulesets.ashrae9012022.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012022.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_

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

FLUID_LOOP = SchemaEnums.schema_enums["FluidLoopOptions"]
FLUID_LOOP_OPERATION = SchemaEnums.schema_enums["FluidLoopOperationOptions"]


class PRM9012022Rule93e12(RuleDefinitionListIndexedBase):
    """Rule 19 of ASHRAE 90.1-2022 Appendix G Section 21 (Hot water loop)"""

    def __init__(self):
        super(PRM9012022Rule93e12, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012022Rule93e12.HeatingFluidLoopRule(),
            index_rmd=BASELINE_0,
            id="21-19",
            description="Hot-water pumps shall only be enabled when a load exists on the associated hot-water loop.",
            ruleset_section_title="HVAC - Water Side",
            standard_section="Section G3.2.3.5",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list containing all HVAC systems that are modeled in the rmd_b
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
        fluid_loop_b = context_item.BASELINE_0

        return getattr_(fluid_loop_b, "FluidLoop", "type") == FLUID_LOOP.HEATING

    class HeatingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012022Rule93e12.HeatingFluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def get_calc_vals(self, context, data=None):
            hw_looop_b = context.BASELINE_0
            hw_design_control_operation_b = getattr_(
                hw_looop_b, "fluid_loops", "heating_design_and_control", "operation"
            )

            return {"hw_design_control_operation_b": hw_design_control_operation_b}

        def rule_check(self, context, calc_vals=None, data=None):
            hw_design_control_operation_b = calc_vals["hw_design_control_operation_b"]

            return hw_design_control_operation_b == FLUID_LOOP_OPERATION.INTERMITTENT
