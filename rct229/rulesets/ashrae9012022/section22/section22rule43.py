from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_primary_secondary_loops_dict import (
    get_primary_secondary_loops_dict,
)
from rct229.rulesets.ashrae9012022 import PROPOSED

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

REQ_MIN_LOAD_RATIO = 0.25
REQ_MIN_UNLOAD_RATIO = 0.25


class PRM9012022Rule93e20(RuleDefinitionListIndexedBase):
    """Rule 43 of ASHRAE 90.1-2022 Appendix G Section 22 (Chilled Water Loop)"""

    def __init__(self):
        super(PRM9012022Rule93e20, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012022Rule93e20.ChillerRule(),
            index_rmd=PROPOSED,
            id="22-43",
            description="hen using performance curves from Normative Appendix J, chiller minimum part-load ratio (ratio of load to available capacity at a given simulation time step) "
            "and minimum compressor unloading ratio (part-load ratio below which the chiller capacity cannot be reduced by unloading and chiller is false loaded) shall be equal to 0.25.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.2.2.1 Equipment Efficiencies",
            is_primary_rule=True,
            list_path="$.buildings[*].building_segments[*].chillers[*]",
            rmd_context="ruleset_model_descriptions/0",
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

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        primary_secondary_loop_dict_b = get_primary_secondary_loops_dict(rmd_b)

        return {"primary_secondary_loop_dict_b": primary_secondary_loop_dict_b}

    class ChillerRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012022Rule93e20.ChillerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["cooling_loop"],
                },
            )

        def is_applicable(self, context, data=None):
            chiller_b = context.PROPOSED
            primary_secondary_loop_dict_b = data["primary_secondary_loop_dict_b"]

            return (
                chiller_b["cooling_loop"] in primary_secondary_loop_dict_b
            )  # add is_chiller_performance_app_j

        def get_calc_vals(self, context, data=None):
            chiller_b = context.PROPOSED

            minimum_load_ratio_b = chiller_b.get("minimum_load_ratio")
            minimum_unload_ratio_b = chiller_b.get("minimum_unload_ratio")

            return {
                "minimum_load_ratio_b": minimum_load_ratio_b,
                "minimum_unload_ratio_b": minimum_unload_ratio_b,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            minimum_load_ratio_b = calc_vals["minimum_load_ratio_b"]
            minimum_unload_ratio_b = calc_vals["minimum_unload_ratio_b"]

            return minimum_load_ratio_b is None or minimum_unload_ratio_b is None

        def rule_check(self, context, calc_vals=None, data=None):
            minimum_load_ratio_b = calc_vals["minimum_load_ratio_b"]
            minimum_unload_ratio_b = calc_vals["minimum_unload_ratio_b"]

            return (
                minimum_load_ratio_b == REQ_MIN_LOAD_RATIO
                and minimum_unload_ratio_b == REQ_MIN_UNLOAD_RATIO
            )
