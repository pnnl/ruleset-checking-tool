from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
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
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.std_comparisons import std_equal

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
REQUIRED_MIN_FLOW_FRACTION = 0.25
MIN_CHW_PRIMARY_LOOP_COOLING_CAPACITY = 300.0 * ureg("ton")


class PRM9012019Rule78g49(RuleDefinitionListIndexedBase):
    """Rule 9 of ASHRAE 90.1-2019 Appendix G Section 22 (Chilled water loop)"""

    def __init__(self):
        super(PRM9012019Rule78g49, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule78g49.ChillerFluidLoopRule(),
            index_rmd=BASELINE_0,
            id="22-9",
            description="Baseline chilled water systems with a cooling capacity of 300 tons or more shall have the secondary loop modeled with a minimum flow of 25% of the design flow rate.",
            ruleset_section_title="HVAC - Chiller",
            standard_section="Section G3.1.3.10 Chilled-water pumps (System 7, 8, 11, 12 and 13)",
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

        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmd_b)

        return (
            any(
                [
                    available_type in APPLICABLE_SYS_TYPES
                    for available_type in available_type_list
                ]
            )
            and len(primary_secondary_loop_dict) > 0
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0

        chw_loop_capacity_dict = {}
        for chiller in find_all("$.chillers[*]", rmd_b):
            if chiller["cooling_loop"] not in chw_loop_capacity_dict:
                chw_loop_capacity_dict[chiller["cooling_loop"]] = ZERO.POWER
            chw_loop_capacity_dict[chiller["cooling_loop"]] += getattr_(
                chiller, "chiller", "rated_capacity"
            )

        primary_secondary_loop_dict = get_primary_secondary_loops_dict(rmd_b)

        return {
            "chw_loop_capacity_dict": chw_loop_capacity_dict,
            "primary_secondary_loop_dict": primary_secondary_loop_dict,
        }

    def list_filter(self, context_item, data):
        fluid_loop_b = context_item.BASELINE_0
        primary_secondary_loop_dict = data["primary_secondary_loop_dict"]
        chw_loop_capacity_dict = data["chw_loop_capacity_dict"]

        return (
            fluid_loop_b["id"] in primary_secondary_loop_dict
            and chw_loop_capacity_dict[fluid_loop_b["id"]]
            >= MIN_CHW_PRIMARY_LOOP_COOLING_CAPACITY
        )

    class ChillerFluidLoopRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule78g49.ChillerFluidLoopRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012019Rule78g49.ChillerFluidLoopRule.SecondaryChildLoopRule(),
                index_rmd=BASELINE_0,
                list_path="$.child_loops[*]",
            )

        class SecondaryChildLoopRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule78g49.ChillerFluidLoopRule.SecondaryChildLoopRule,
                    self,
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    required_fields={
                        "$": ["cooling_or_condensing_design_and_control"],
                        "cooling_or_condensing_design_and_control": [
                            "minimum_flow_fraction"
                        ],
                    },
                    precision={
                        "min_flow_fraction": {
                            "precision": 0.1,
                        },
                    },
                )

            def get_calc_vals(self, context, data=None):
                child_loop_b = context.BASELINE_0
                min_flow_fraction = child_loop_b[
                    "cooling_or_condensing_design_and_control"
                ]["minimum_flow_fraction"]

                return {"min_flow_fraction": min_flow_fraction}

            def rule_check(self, context, calc_vals=None, data=None):
                min_flow_fraction = calc_vals["min_flow_fraction"]

                return self.precision_comparison["min_flow_fraction"](
                    min_flow_fraction,
                    REQUIRED_MIN_FLOW_FRACTION,
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                min_flow_fraction = calc_vals["min_flow_fraction"]

                return std_equal(REQUIRED_MIN_FLOW_FRACTION, min_flow_fraction)
