from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_primary_secondary_loops_dict import (
    get_primary_secondary_loops_dict,
)

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


class Section22Rule34(RuleDefinitionListIndexedBase):
    """Rule 34 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(Section22Rule34, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=Section22Rule34.CoolingFluidLoopRule(),
            index_rmr=BASELINE_0,
            id="22-34",
            description="For baseline cooling chilled water plant that is served by chiller(s), the capacity shall be based on coincident loads.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.2.2 Building System-Specific Modeling Requirements for the Baseline model",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.fluid_loops[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.BASELINE_0
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

    def create_data(self, context, data):
        rmi_b = context.BASELINE_0
        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmi_b)

        return {"primary_secondary_loop_dict": primary_secondary_loop_dict}

    def list_filter(self, context_item, data):
        fluid_loops_b = context_item.BASELINE_0
        primary_secondary_loop_dict = data["primary_secondary_loop_dict"]

        return fluid_loops_b["id"] in primary_secondary_loop_dict

    class CoolingFluidLoopRule(RuleDefinitionBase):
        def __init__(self):
            super(Section22Rule34.CoolingFluidLoopRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["cooling_or_condensing_design_and_control"],
                    "cooling_or_condensing_design_and_control": [
                        "is_sized_using_coincident_load"
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            fluid_loop_b = context.BASELINE_0
            is_sized_using_coincident_load = fluid_loop_b[
                "cooling_or_condensing_design_and_control"
            ]["is_sized_using_coincident_load"]

            return {"is_sized_using_coincident_load": is_sized_using_coincident_load}

        def rule_check(self, context, calc_vals=None, data=None):
            is_sized_using_coincident_load = calc_vals["is_sized_using_coincident_load"]

            return is_sized_using_coincident_load
